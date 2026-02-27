#!/usr/bin/env python3
import ctypes
import os
import sys
import sysconfig
from types import TracebackType
from typing import List, Optional, Tuple, Type

from .base import Result


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
        lib = _load_lib_with_prefix_suffix("", "-1.dll")
    elif sys.platform.startswith("darwin"):
        lib = _load_lib_with_prefix_suffix("lib", "-1.dylib")
    else:
        lib = _load_lib_with_prefix_suffix("lib", "-1.so")

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
        threads: int = 0,
    ) -> None:
        self.threads = threads
        self._load_lib(thorvg_lib_path)
        self.init_result = self.init(threads)

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
            self.term()

    def __enter__(self) -> "Engine":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self.thorvg_lib:
            self.term()

    def init(self, threads: int) -> Result:
        """Initializes TVG engines.

        ThorVG requires an active runtime environment to operate.
        Internally, it utilizes a task scheduler to efficiently parallelize rendering operations.
        You can specify the number of worker threads using the ``threads`` parameter.
        During initialization, ThorVG will spawn the specified number of threads.

        :param int threads: The number of additional threads used to perform rendering. Zero indicates only the main thread is to be used.

        :rtype: Result

        .. note::
            The initializer uses internal reference counting to track multiple calls.
            The number of threads is fixed on the first call to Engine.init()
            and cannot be changed in subsequent calls.
        .. seealso:: Engine.term()
        """
        self.thorvg_lib.tvg_engine_init.argtypes = [ctypes.c_int]
        self.thorvg_lib.tvg_engine_init.restype = Result
        return self.thorvg_lib.tvg_engine_init(ctypes.c_int(threads))

    def term(self) -> Result:
        """Terminates TVG engines.

        Cleans up resources and stops any internal threads initialized by Engine.init().

        :return: Result.INSUFFICIENT_CONDITION Returned if there is nothing to terminate (e.g., Engine.init() was not called).
        :rtype: Result

        .. seealso:: Engine.init()
        """
        self.thorvg_lib.tvg_engine_term.argtypes = []
        self.thorvg_lib.tvg_engine_term.restype = Result
        return self.thorvg_lib.tvg_engine_term()

    def version(self) -> Tuple[Result, int, int, int, Optional[str]]:
        """
        Retrieves the version of the TVG engine.

        :return: Result.SUCCESS
        :rtype: Result
        :return: A major version number.
        :rtype: int
        :return: A minor version number.
        :rtype: int
        :return: A micro version number.
        :rtype: int
        :return: The version of the engine in the format major.minor.micro, or a ``None`` in case of an internal error.
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
