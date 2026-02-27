#!/usr/bin/env python3
import ctypes
from typing import Callable, Optional, Tuple

from ..base import Colorspace, PaintPointer, PictureAssetResolverType, Result
from ..engine import Engine
from . import Paint


class Picture(Paint):
    """
    Picture API

    A module enabling to create and to load an image in one of the supported formats: svg, png, jpg, lottie and raw.
    """

    def __init__(self, engine: Engine, paint: Optional[PaintPointer] = None):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if paint is None:
            self._paint = self._new()
        else:
            self._paint = paint

    def _new(self) -> PaintPointer:
        """Creates a new picture object.

        Note that you need not call this method as it is auto called when initializing ``Picture()``.

        :return: A new picture object.
        :rtype: PaintPointer
        """
        self.thorvg_lib.tvg_picture_new.restype = PaintPointer
        return self.thorvg_lib.tvg_picture_new()

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
            - Result.INVALID_ARGUMENT An invalid PaintPointer or an empty ``path``.
            - Result.NOT_SUPPORTED A file with an unknown extension.
        :rtype: Result
        """
        path_bytes = path.encode() + b"\x00"
        path_char = ctypes.create_string_buffer(path_bytes)
        self.thorvg_lib.tvg_picture_load.argtypes = [
            PaintPointer,
            ctypes.c_char * ctypes.sizeof(path_char),
        ]
        self.thorvg_lib.tvg_picture_load.restype = Result
        return self.thorvg_lib.tvg_picture_load(
            self._paint,
            path_char,
        )

    def load_raw(
        self,
        data: bytes,
        w: int,
        h: int,
        cs: Colorspace,
        copy: bool,
    ) -> Result:
        """Loads a picture data from a memory block of a given size.

        ThorVG efficiently caches the loaded data using the specified ``data`` address as a key
        when the ``copy`` has ``false``. This means that loading the same data again will not result in duplicate operations
        for the sharable ``data``. Instead, ThorVG will reuse the previously loaded picture data.

        :param bytes data: A pointer to a memory location where the content of the picture raw data is stored.
        :param int w: The width of the image ``data`` in pixels.
        :param int h: The height of the image ``data`` in pixels.
        :param Colorspace cs: Specifies how the 32-bit color values should be interpreted (read/write).
        :param bool copy: If ``true`` the data are copied into the engine local buffer, otherwise they are not.

        :return: Result.INVALID_ARGUMENT An invalid PaintPointer or no data are provided or the ``w`` or ``h`` value is zero or less.
        :rtype: Result

        .. versionadded:: 0.9
        """
        data_arr_type = ctypes.c_uint32 * int(len(data) / 4)
        data_arr = data_arr_type.from_buffer_copy(data)
        self.thorvg_lib.tvg_picture_load_raw.argtypes = [
            PaintPointer,
            ctypes.POINTER(data_arr_type),
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_int,
            ctypes.c_bool,
        ]
        self.thorvg_lib.tvg_picture_load_raw.restype = Result
        return self.thorvg_lib.tvg_picture_load_raw(
            self._paint,
            ctypes.pointer(data_arr),
            ctypes.c_uint32(w),
            ctypes.c_uint32(h),
            cs,
            ctypes.c_bool(copy),
        )

    def load_data(
        self,
        data: bytes,
        mimetype: str,
        rpath: Optional[str],
        copy: bool,
    ) -> Result:
        """Loads a picture data from a memory block of a given size.

        ThorVG efficiently caches the loaded data using the specified ``data`` address as a key
        when the ``copy`` has ``false``. This means that loading the same data again will not result in duplicate operations
        for the sharable ``data``. Instead, ThorVG will reuse the previously loaded picture data.

        :param bytes data: A pointer to a memory location where the content of the picture file is stored. A null-terminated string is expected for non-binary data if ``copy`` is ``false``
        :param str mimetype: Mimetype or extension of data such as "jpg", "jpeg", "svg", "svg+xml", "lottie", "png", etc. In case an empty string or an unknown type is provided, the loaders will be tried one by one.
        :param Optional[str] rpath: A resource directory path, if the ``data`` needs to access any external resources.
        :param bool copy: If ``true`` the data are copied into the engine local buffer, otherwise they are not.

        :return:
            - Result.INVALID_ARGUMENT In case a ``None`` is passed as the argument or the ``size`` is zero or less.
            - Result.NOT_SUPPORTED A file with an unknown extension.
        :rtype: Result

        .. warning::
            : It's the user responsibility to release the ``data`` memory if the ``copy`` is ``true``.
        """
        data_arr_type = ctypes.c_char * len(data)
        data_arr = data_arr_type.from_buffer_copy(data)

        mimetype_bytes = mimetype.encode() + b"\x00"
        mimetype_char_type = ctypes.c_char * len(mimetype_bytes)
        mimetype_char = mimetype_char_type.from_buffer_copy(mimetype_bytes)

        if rpath is None:
            rpath_char_type = ctypes.c_void_p
            rpath_char_p = ctypes.c_void_p()
        else:
            rpath_bytes = rpath.encode() + b"\x00"
            rpath_char_type = ctypes.c_char * len(rpath_bytes)  # type: ignore
            rpath_char = mimetype_char_type.from_buffer_copy(rpath_bytes)
            rpath_char_p = ctypes.pointer(rpath_char)  # type: ignore

        self.thorvg_lib.tvg_picture_load_data.argtypes = [
            PaintPointer,
            ctypes.POINTER(data_arr_type),
            ctypes.c_uint32,
            ctypes.POINTER(mimetype_char_type),
            ctypes.POINTER(rpath_char_type),
            ctypes.c_bool,
        ]
        self.thorvg_lib.tvg_picture_load_data.restype = Result
        return self.thorvg_lib.tvg_picture_load_data(
            self._paint,
            ctypes.pointer(data_arr),
            ctypes.c_uint32(ctypes.sizeof(data_arr)),
            ctypes.pointer(mimetype_char),
            rpath_char_p,
            ctypes.c_bool(copy),
        )

    def set_asset_resolver(
        self,
        resolver: Callable[[PaintPointer, ctypes.c_char_p, ctypes.c_void_p], bool],
        data: bytes,
    ) -> Result:
        """Sets the asset resolver callback for handling external resources (e.g., images and fonts).

        This callback is invoked when an external asset reference (such as an image source or file path)
        is encountered in a Picture object. It allows the user to provide a custom mechanism for loading
        or substituting assets, such as loading from an external source or a virtual filesystem.

        :param Callable[[PaintPointer, ctypes.c_char_p, ctypes.c_void_p], bool] resolver:
            A user-defined function that handles the resolution of asset paths.
            The function should return ``true`` if the asset was successfully resolved by the user, or ``false`` if it was not.
        :param bytes data:
            A pointer to user-defined data that will be passed to the callback each time it is invoked.
            This can be used to maintain context or access external resources.

        :return:
            - Result.INVALID_ARGUMENT A ``None`` passed as the ``picture`` argument.
            - Result.INSUFFICIENT_CONDITION If the ``picture`` is already loaded.
        :rtype: Result

        .. note::
            This function must be called before ``Picture.load()``
        Setting the resolver after loading will have no effect on asset resolution for that asset.
        .. note::
            If ``false`` is returned by ``resolver``, ThorVG will attempt to resolve the resource using its internal resolution mechanism as a fallback.
        .. note::
            To unset the resolver, pass ``None`` as the ``resolver`` parameter.
        .. note::
            Experimental API

        .. seealso:: PictureAssetResolverType
        """
        data_arr_type = ctypes.c_char * len(data)
        data_arr = data_arr_type.from_buffer_copy(data)

        self.thorvg_lib.tvg_picture_set_asset_resolver.argtypes = [
            PaintPointer,
            PictureAssetResolverType,
            data_arr_type,
        ]
        self.thorvg_lib.tvg_picture_set_asset_resolver.restype = Result
        return self.thorvg_lib.tvg_picture_set_asset_resolver(
            self._paint,
            PictureAssetResolverType(resolver),
            data_arr,
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

        :return: Result.INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: Result
        """
        self.thorvg_lib.tvg_picture_set_size.argtypes = [
            PaintPointer,
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_picture_set_size.restype = Result
        return self.thorvg_lib.tvg_picture_set_size(
            self._paint,
            ctypes.c_float(w),
            ctypes.c_float(h),
        )

    def get_size(self) -> Tuple[Result, float, float]:
        """Gets the size of the loaded picture.

        :return: Result.INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: Result
        :return: A width of the image in pixels.
        :rtype: float
        :return: A height of the image in pixels.
        :rtype: float
        """
        w = ctypes.c_float()
        h = ctypes.c_float()
        self.thorvg_lib.tvg_picture_get_size.argtypes = [
            PaintPointer,
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
        ]
        self.thorvg_lib.tvg_picture_get_size.restype = Result
        result = self.thorvg_lib.tvg_picture_get_size(
            self._paint,
            ctypes.pointer(w),
            ctypes.pointer(h),
        )
        return result, w.value, h.value

    def set_origin(self, x: float, y: float) -> Result:
        """Sets the normalized origin point of the Picture object.

        This method defines the origin point of the Picture using normalized coordinates.
        Unlike a typical pivot point used only for transformations, this origin affects both
        the transformation behavior and the actual rendering position of the Picture.

        The specified origin becomes the reference point for positioning the Picture on the canvas.
        For example, setting the origin to (0.5f, 0.5f) moves the visual center of the picture
        to the position specified by Paint.translate().

        The coordinates are given in a normalized range relative to the picture's bounds:
        - (0.0f, 0.0f): top-left corner
        - (0.5f, 0.5f): center
        - (1.0f, 1.0f): bottom-right corner

        :param picture: A PaintPointer to the picture object.
        :param x: The normalized x-coordinate of the origin point (range: 0.0f to 1.0f).
        :param y: The normalized y-coordinate of the origin point (range: 0.0f to 1.0f).

        :return: Result.INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: Result

        .. note::
            This origin directly affects how the Picture is placed on the canvas when using
        transformations such as translate(), rotate(), or scale().

        .. seealso:: Paint.translate()
        .. seealso:: Paint.rotate()
        .. seealso:: Paint.scale()
        .. seealso:: Paint.set_transform()
        .. seealso:: Picture.get_origin()

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_picture_set_origin.argtypes = [
            PaintPointer,
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_picture_set_origin.restype = Result
        return self.thorvg_lib.tvg_picture_set_origin(
            self._paint,
            ctypes.c_float(x),
            ctypes.c_float(y),
        )

    def get_origin(self) -> Tuple[Result, float, float]:
        """Gets the normalized origin point of the Picture object.

        This method retrieves the current origin point of the Picture, expressed
        in normalized coordinates relative to the picture’s bounds.

        :param picture: A PaintPointer to the picture object.
        :param x: The normalized x-coordinate of the origin (range: 0.0f to 1.0f).
        :param y: The normalized y-coordinate of the origin (range: 0.0f to 1.0f).

        :return: Result.INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: Result

        .. seealso:: Picture.set_origin()
        .. versionadded:: 1.0
        """
        x = ctypes.c_float()
        y = ctypes.c_float()
        self.thorvg_lib.tvg_picture_get_size.argtypes = [
            PaintPointer,
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
        ]
        self.thorvg_lib.tvg_picture_get_size.restype = Result
        result = self.thorvg_lib.tvg_picture_get_size(
            self._paint,
            ctypes.pointer(x),
            ctypes.pointer(y),
        )
        return result, x.value, y.value

    def get_paint(self, _id: int) -> Optional[Paint]:
        """Retrieve a paint object from the Picture scene by its Unique ID.

        This function searches for a paint object within the Picture scene that matches the provided ``id``.

        :param int _id: The Unique ID of the paint object.
        :return: A pointer to the paint object that matches the given identifier, or ``None`` if no matching paint object is found.
        :rtype: PaintPointer

        .. seealso:: Engine.accessor_generate_id()
        .. versionadded: 1.0
        """
        self.thorvg_lib.tvg_picture_get_size.argtypes = [
            PaintPointer,
            ctypes.c_uint32,
        ]
        self.thorvg_lib.tvg_picture_get_size.restype = PaintPointer
        paint_struct = self.thorvg_lib.tvg_picture_get_size(
            self._paint,
            ctypes.c_uint32(_id),
        )
        if paint_struct is not None:
            return Paint(self.engine, paint_struct)
        else:
            return None
