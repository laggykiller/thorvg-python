#!/usr/bin/env python3
import ctypes
import os
import sys
import sysconfig
from types import TracebackType
from typing import List, Optional, Tuple, Type

from .base import EngineBackend, Result


def _load_lib_with_prefix_suffix(
    lib_prefix: str, lib_suffix: str
) -> Optional[ctypes.CDLL]:
    package_dir = os.path.dirname(__file__)
    thorvg_lib_name = lib_prefix + "thorvg" + lib_suffix
    thorvg_lib_path_local = os.path.join(package_dir, thorvg_lib_name)

    if os.path.isfile(thorvg_lib_path_local):
        thorvg_lib_path = thorvg_lib_path_local
    elif os.path.isfile(thorvg_lib_name):
        thorvg_lib_path = os.path.abspath(thorvg_lib_name)
    else:
        thorvg_lib_path = thorvg_lib_name

    try:
        return ctypes.cdll.LoadLibrary(thorvg_lib_path)
    except OSError:
        return None


def _load_lib(thorvg_lib_path: Optional[str] = None) -> Optional[ctypes.CDLL]:
    if thorvg_lib_path:
        try:
            return ctypes.cdll.LoadLibrary(thorvg_lib_path)
        except OSError:
            return None

    if sys.platform.startswith(("win32", "cygwin", "msys", "os2")):
        lib = _load_lib_with_prefix_suffix("", "-0.dll")
    elif sys.platform.startswith("darwin"):
        lib = _load_lib_with_prefix_suffix("lib", ".dylib")
    else:
        lib = _load_lib_with_prefix_suffix("lib", ".so")

    if lib:
        return lib

    lib_suffixes: List[str] = []
    shlib_suffix = sysconfig.get_config_var("SHLIB_SUFFIX")
    if isinstance(shlib_suffix, str):
        lib_suffixes.append(shlib_suffix)
    if sys.platform.startswith(("win32", "cygwin", "msys", "os2")):
        lib_prefixes = ("", "lib")
    elif sys.platform.startswith("darwin"):
        lib_prefixes = ("lib", "")
    else:
        lib_prefixes = ("lib", "")
    lib_suffixes.extend([".so", "-0.dll", ".dll", ".dylib"])

    for lib_prefix in lib_prefixes:
        for lib_suffix in set(lib_suffixes):
            lib = _load_lib_with_prefix_suffix(lib_prefix, lib_suffix)
            if lib:
                return lib

    return None


THORVG_LIB = _load_lib()


class Engine:
    """
    Engine API

    A module enabling initialization and termination of the TVG engines.
    """

    def __init__(
        self,
        thorvg_lib_path: Optional[str] = None,
        engine_method: EngineBackend = EngineBackend.SW,
        threads: int = 0,
    ) -> None:
        self.engine_method = engine_method
        self.threads = threads
        self._load_lib(thorvg_lib_path)
        self.init_result = self.init(self.engine_method, threads)

    def _load_lib(self, thorvg_lib_path: Optional[str] = None) -> None:
        if thorvg_lib_path is None:
            if THORVG_LIB is None:
                raise OSError("Could not load thorvg library")
            else:
                self.thorvg_lib = THORVG_LIB
                return

        thorvg_lib = _load_lib(thorvg_lib_path)
        if thorvg_lib is None:
            raise OSError(f"Could not load thorvg library from {thorvg_lib_path}")
        else:
            self.thorvg_lib = thorvg_lib

    def __del__(self) -> None:
        if self.thorvg_lib:
            self.term(self.engine_method)

    def __enter__(self) -> "Engine":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self.thorvg_lib:
            self.term(self.engine_method)

    def init(self, engine_method: EngineBackend, threads: int) -> Result:
        """Initializes TVG engines.

        TVG requires the running-engine environment.
        TVG runs its own task-scheduler for parallelizing rendering tasks efficiently.
        You can indicate the number of threads, the count of which is designated ``threads``.
        In the initialization step, TVG will generate/spawn the threads as set by ``threads`` count.

        .. code-block:: python

            from thorvg_python import Engine
            engine = Engine.init(EngineBackend.SW, 0);  //Initialize software renderer and use the main thread only

        :param EngineBackend engine_method: The engine types to initialize. This is relative to the Canvas types, in which it will be used. For multiple backends bitwise operation is allowed.
            - SW: CPU rasterizer
            - GL: OpenGL rasterizer (not supported yet)
        :param int threads: The number of additional threads used to perform rendering. Zero indicates only the main thread is to be used.

        :return:
            - INVALID_ARGUMENT Unknown engine type.
            - NOT_SUPPORTED Unsupported engine type.
        :rtype: Result

        .. note::
            The Initializer keeps track of the number of times it was called. Threads count is fixed at the first init() call.
        .. seealso:: Engine.term()
        .. seealso:: EngineBackend
        """
        self.thorvg_lib.tvg_engine_init.argtypes = [ctypes.c_int, ctypes.c_int]
        self.thorvg_lib.tvg_engine_init.restype = Result
        return self.thorvg_lib.tvg_engine_init(engine_method, ctypes.c_int(threads))

    def term(self, engine_method: Optional[EngineBackend] = None) -> Result:
        """Terminates TVG engines.

        It should be called in case of termination of the TVG client with the same engine types as were passed when tvg_engine_init() was called.

        .. code-block:: python

            from thorvg_python import Engine
            engine = Engine()
            //define canvas and shapes, update shapes, general rendering calls
            engine.tvg_engine_term()

        :param Optional[EngineBackend] engine_method: The engine types to terminate.
            This is relative to the Canvas types, in which it will be used.
            For multiple backends bitwise operation is allowed.
            If ``None`` is passed, all engine types will be terminated
            - SW: CPU rasterizer
            - GL: OpenGL rasterizer (not supported yet)

        :return:
            - INSUFFICIENT_CONDITION Nothing to be terminated.
            - INVALID_ARGUMENT Unknown engine type.
            - NOT_SUPPORTED Unsupported engine type.
        :rtype: Result

        .. seealso:: Engine.init()
        .. seealso:: EngineBackend
        """
        if engine_method is None:
            engine_method = self.engine_method
        self.thorvg_lib.tvg_engine_term.argtypes = [ctypes.c_int]
        self.thorvg_lib.tvg_engine_term.restype = Result
        return self.thorvg_lib.tvg_engine_term(engine_method)

    def version(self) -> Tuple[Result, int, int, int, Optional[str]]:
        """
        Retrieves the version of the TVG engine.

        :return: SUCCESS
        :rtype: Result
        :return: A major version number.
        :rtype: int
        :return: A minor version number.
        :rtype: int
        :return: A micro version number.
        :rtype: int
        :return: The version of the engine in the format major.minor.micro, or a ``nullptr`` in case of an internal error.
        :rtype: Optional[str]

        .. versionadded:: 0.15
        """
        self.thorvg_lib.tvg_engine_version.argtypes = [
            ctypes.POINTER(ctypes.c_uint32),
            ctypes.POINTER(ctypes.c_uint32),
            ctypes.POINTER(ctypes.c_uint32),
            ctypes.POINTER(ctypes.c_char_p),
        ]
        self.thorvg_lib.tvg_engine_version.restype = Result
        major = ctypes.c_uint32()
        minor = ctypes.c_uint32()
        micro = ctypes.c_uint32()
        version = ctypes.c_char_p()
        result = self.thorvg_lib.tvg_engine_version(
            ctypes.pointer(major),
            ctypes.pointer(minor),
            ctypes.pointer(micro),
            ctypes.pointer(version),
        )
        if version.value is not None:
            v = version.value.decode("utf-8")
        else:
            v = None
        return result, major.value, minor.value, micro.value, v

    def font_load(
        self,
        path: str,
    ) -> Result:
        """Loads a scalable font data from a file.

        ThorVG efficiently caches the loaded data using the specified ``path`` as a key.
        This means that loading the same file again will not result in duplicate operations;
        instead, ThorVG will reuse the previously loaded font data.

        :param str path: The path to the font file.

        :return:
            - INVALID_ARGUMENT An invalid ``path`` passed as an argument.
            - NOT_SUPPORTED When trying to load a file with an unknown extension.
        :rtype: Result

        .. seealso:: Engine.font_unload()

        .. versionadded:: 0.15
        """
        path_arr_type = ctypes.c_char * len(path.encode())
        path_arr = path_arr_type.from_buffer_copy(path.encode())
        self.thorvg_lib.tvg_font_load.argtypes = [
            ctypes.POINTER(path_arr_type),
        ]
        self.thorvg_lib.tvg_font_load.restype = Result
        return self.thorvg_lib.tvg_font_load(ctypes.pointer(path_arr))

    def font_load_data(
        self,
        name: str,
        data: bytes,
        mimetype: Optional[str],
        copy: bool,
    ) -> Result:
        """Loads a scalable font data from a memory block of a given size.

        ThorVG efficiently caches the loaded font data using the specified ``name`` as a key.
        This means that loading the same fonts again will not result in duplicate operations.
        Instead, ThorVG will reuse the previously loaded font data.

        :param str name: The name under which the font will be stored and accessible (e.x. in a ``tvg_text_set_font`` API).
        :param bytes data: A pointer to a memory location where the content of the font data is stored.
        :param str mimetype: Mimetype or extension of font data. In case a ``None`` or an empty "" value is provided the loader will be determined automatically.
        :param bool copy: If ``true`` the data are copied into the engine local buffer, otherwise they are not (default).

        :return:
            - INVALID_ARGUMENT If no name is provided or if ``size`` is zero while ``data`` points to a valid memory location.
            - NOT_SUPPORTED When trying to load a file with an unknown extension.
            - INSUFFICIENT_CONDITION When trying to unload the font data that has not been previously loaded.
        :rtype: Result

        .. warning::
            : It's the user responsibility to release the ``data`` memory.

        .. note::
            To unload the font data loaded using this API, pass the proper ``name`` and ``nullptr`` as ``data``.

        .. versionadded:: 0.15
        """
        name_char_type = ctypes.c_char * len(name.encode())
        name_char = name_char_type.from_buffer_copy(name.encode())
        data_arr_type = ctypes.c_ubyte * len(data)
        data_arr = data_arr_type.from_buffer_copy(data)
        if mimetype is not None and mimetype != "":
            mimetype_char_type = ctypes.c_char * len(mimetype.encode())
            mimetype_char_ptr_type = ctypes.POINTER(mimetype_char_type)
            mimetype_char = mimetype_char_type.from_buffer_copy(mimetype.encode())
            mimetype_char_ptr = ctypes.pointer(mimetype_char)
        else:
            mimetype_char_ptr_type = ctypes.c_void_p  # type: ignore
            mimetype_char_ptr = ctypes.c_void_p()  # type: ignore
        self.thorvg_lib.tvg_picture_load_raw.argtypes = [
            ctypes.POINTER(name_char_type),
            ctypes.POINTER(data_arr_type),
            ctypes.c_uint32,
            mimetype_char_ptr_type,
            ctypes.c_bool,
        ]
        return self.thorvg_lib.tvg_picture_load_raw(
            ctypes.pointer(name_char),
            ctypes.pointer(data_arr),
            ctypes.c_uint32(ctypes.sizeof(data_arr)),
            mimetype_char_ptr,
            ctypes.c_bool(copy),
        )

    def font_unload(
        self,
        path: str,
    ) -> Result:
        """Unloads the specified scalable font data that was previously loaded.

        This function is used to release resources associated with a font file that has been loaded into memory.

        :param str path: The path to the loaded font file.

        :return: INSUFFICIENT_CONDITION The loader is not initialized.
        :rtype: Result

        .. note::
            If the font data is currently in use, it will not be immediately unloaded.
        .. seealso:: Engine.font_load()

        .. versionadded:: 0.15
        """
        path_arr_type = ctypes.c_char * len(path.encode())
        path_arr = path_arr_type.from_buffer_copy(path.encode())
        self.thorvg_lib.tvg_font_unload.argtypes = [
            ctypes.POINTER(path_arr_type),
        ]
        self.thorvg_lib.tvg_font_unload.restype = Result
        return self.thorvg_lib.tvg_font_unload(ctypes.pointer(path_arr))

    def accessor_generate_id(
        self,
        name: str,
    ) -> int:
        """Generate a unique ID (hash key) from a given name.

        This function computes a unique identifier value based on the provided string.
        You can use this to assign a unique ID to the Paint object.

        :param str name: The input string to generate the unique identifier from.

        :return: The generated unique identifier value.
        :rtype: int

        .. note::
            Experimental API
        """
        name_char_type = ctypes.c_char * len(name.encode())
        name_char = name_char_type.from_buffer_copy(name.encode())
        self.thorvg_lib.tvg_accessor_generate_id.argtypes = [
            ctypes.POINTER(name_char_type)
        ]
        self.thorvg_lib.tvg_accessor_generate_id.restype = ctypes.c_uint32
        return self.thorvg_lib.tvg_accessor_generate_id(ctypes.pointer(name_char)).value
