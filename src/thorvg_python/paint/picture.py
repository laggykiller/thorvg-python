#!/usr/bin/env python3
import ctypes
from typing import Optional, Tuple

from ..base import PaintStruct, Result
from ..engine import Engine
from . import Paint


class Picture(Paint):
    """
    Picture API

    A module enabling to create and to load an image in one of the supported formats: svg, png, jpg, lottie and raw.
    """

    def __init__(self, engine: Engine, paint: Optional[PaintStruct] = None):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if paint is None:
            self._paint = self._new()
        else:
            self._paint = paint

    def _new(self) -> PaintStruct:
        """Creates a new picture object.

        Note that you need not call this method as it is auto called when initializing ``Picture()``.

        :return: A new picture object.
        :rtype: PaintStruct
        """
        self.thorvg_lib.tvg_picture_new.restype = ctypes.POINTER(PaintStruct)
        return self.thorvg_lib.tvg_picture_new().contents

    def load(
        self,
        path: str,
    ) -> Result:
        """Loads a picture data directly from a file.

        ThorVG efficiently caches the loaded data using the specified ``path`` as a key.
        This means that loading the same file again will not result in duplicate operations;
        instead, ThorVG will reuse the previously loaded picture data.

        :param str path: The absolute path to the image file.

        :return:
            - INVALID_ARGUMENT An invalid PaintStruct pointer or an empty ``path``.
            - NOT_SUPPORTED A file with an unknown extension.
        :rtype: Result
        """
        path_char = ctypes.create_string_buffer(path.encode())
        self.thorvg_lib.tvg_picture_load.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_char * ctypes.sizeof(path_char),
        ]
        return self.thorvg_lib.tvg_picture_load(
            ctypes.pointer(self._paint),
            path_char,
        )

    def load_raw(
        self,
        data: bytes,
        w: int,
        h: int,
        copy: bool,
    ) -> Result:
        """Loads a picture data from a memory block of a given size.

        ThorVG efficiently caches the loaded data using the specified ``data`` address as a key
        when the ``copy`` has ``false``. This means that loading the same data again will not result in duplicate operations
        for the sharable ``data``. Instead, ThorVG will reuse the previously loaded picture data.

        :param bytes data: A pointer to a memory location where the content of the picture raw data is stored.
        :param int w: The width of the image ``data`` in pixels.
        :param int h: The height of the image ``data`` in pixels.
        :param bool copy: If ``true`` the data are copied into the engine local buffer, otherwise they are not.

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer or no data are provided or the ``width`` or ``height`` value is zero or less.
            FAILED_ALLOCATION A problem with memory allocation occurs.
        :rtype: Result

        .. versionadded:: 0.9
        """
        data_arr_type = ctypes.c_uint32 * int(len(data) / 4)
        data_arr = data_arr_type.from_buffer_copy(data)
        self.thorvg_lib.tvg_picture_load_raw.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(data_arr_type),
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_bool,
        ]
        return self.thorvg_lib.tvg_picture_load_raw(
            ctypes.pointer(self._paint),
            ctypes.pointer(data_arr),
            ctypes.c_uint32(w),
            ctypes.c_uint32(h),
            ctypes.c_bool(copy),
        )

    def load_data(
        self,
        data: bytes,
        mimetype: str,
        copy: bool,
    ) -> Result:
        """Loads a picture data from a memory block of a given size.

        ThorVG efficiently caches the loaded data using the specified ``data`` address as a key
        when the ``copy`` has ``false``. This means that loading the same data again will not result in duplicate operations
        for the sharable ``data``. Instead, ThorVG will reuse the previously loaded picture data.

        :param bytes data: A pointer to a memory location where the content of the picture file is stored. A null-terminated string is expected for non-binary data if ``copy`` is ``false``
        :param str mimetype: Mimetype or extension of data such as "jpg", "jpeg", "svg", "svg+xml", "lottie", "png", etc. In case an empty string or an unknown type is provided, the loaders will be tried one by one.
        :param bool copy: If ``true`` the data are copied into the engine local buffer, otherwise they are not.

        :return: INVALID_ARGUMENT In case a ``nullptr`` is passed as the argument or the ``size`` is zero or less.
            NOT_SUPPORTED A file with an unknown extension.
        :rtype: Result

        .. warning::
            : It's the user responsibility to release the ``data`` memory if the ``copy`` is ``true``.
        """
        data_arr_type = ctypes.c_char * len(data)
        data_arr = data_arr_type.from_buffer_copy(data)
        mimetype_char_type = ctypes.c_char * len(mimetype.encode())
        mimetype_char = mimetype_char_type.from_buffer_copy(mimetype.encode())
        self.thorvg_lib.tvg_picture_load_data.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(data_arr_type),
            ctypes.c_uint32,
            ctypes.POINTER(mimetype_char_type),
            ctypes.c_bool,
        ]
        return self.thorvg_lib.tvg_picture_load_data(
            ctypes.pointer(self._paint),
            ctypes.pointer(data_arr),
            ctypes.c_uint32(ctypes.sizeof(data_arr)),
            ctypes.pointer(mimetype_char),
            ctypes.c_bool(copy),
        )

    def set_size(
        self,
        w: float,
        h: float,
    ) -> Result:
        """Resizes the picture content to the given width and height.

        The picture content is resized while keeping the default size aspect ratio.
        The scaling factor is established for each of dimensions and the smaller value is applied to both of them.

        :param float w: A new width of the image in pixels.
        :param float h: A new height of the image in pixels.

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result
        """
        self.thorvg_lib.tvg_picture_set_size.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_picture_set_size.restype = Result
        return self.thorvg_lib.tvg_picture_set_size(
            ctypes.pointer(self._paint),
            ctypes.c_float(w),
            ctypes.c_float(h),
        )

    def get_size(self) -> Tuple[Result, float, float]:
        """Gets the size of the loaded picture.

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result
        :return: A width of the image in pixels.
        :rtype: float
        :return: A height of the image in pixels.
        :rtype: float
        """
        w = ctypes.c_float()
        h = ctypes.c_float()
        self.thorvg_lib.tvg_picture_get_size.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
        ]
        self.thorvg_lib.tvg_picture_get_size.restype = Result
        result = self.thorvg_lib.tvg_picture_get_size(
            ctypes.pointer(self._paint),
            ctypes.pointer(w),
            ctypes.pointer(h),
        )
        return result, w.value, h.value

    def get_paint(self, _id: int) -> Optional[Paint]:
        """Retrieve a paint object from the Picture scene by its Unique ID.

        This function searches for a paint object within the Picture scene that matches the provided ``id``.

        :param int _id: The Unique ID of the paint object.
        :return: A pointer to the paint object that matches the given identifier, or ``nullptr`` if no matching paint object is found.
        :rtype: PaintStruct

        .. seealso:: Engine.accessor_generate_id()
        .. note::
            experimental API
        """
        self.thorvg_lib.tvg_picture_get_size.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.c_uint32),
        ]
        self.thorvg_lib.tvg_picture_get_size.restype = ctypes.POINTER(PaintStruct)
        paint_struct = self.thorvg_lib.tvg_picture_get_size(
            ctypes.pointer(self._paint),
            ctypes.c_uint32(_id),
        ).contents
        if paint_struct is not None:
            return Paint(self.engine, paint_struct)
        else:
            return None
