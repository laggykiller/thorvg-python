#!/usr/bin/env python3
import ctypes
from typing import TYPE_CHECKING, Optional, Tuple

from ..base import CanvasPointer, Colorspace, EngineOption, Result
from ..engine import Engine
from . import Canvas

if TYPE_CHECKING:
    from PIL import Image


class SwCanvas(Canvas):
    """
    SwCanvas API

    A module for rendering the graphical elements using the software engine.
    """

    def __init__(
        self,
        engine: Engine,
        op: EngineOption = EngineOption.DEFAULT,
        canvas: Optional[CanvasPointer] = None
    ):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        self.buffer_arr: Optional[ctypes.Array[ctypes.c_uint32]] = None
        self.w: Optional[int] = None
        self.h: Optional[int] = None
        self.stride: Optional[int] = None
        self.cs: Optional[Colorspace] = None
        if canvas is None:
            self._canvas = self._create(op)
        else:
            self._canvas = canvas

    def _create(self, op: EngineOption = EngineOption.DEFAULT) -> CanvasPointer:
        """Creates a new Software Canvas object with optional rendering engine settings.

        This method generates a software canvas instance that can be used for drawing vector graphics.
        It accepts an optional parameter ``op`` to choose between different rendering engine behaviors.

        :param EngineOption op: The rendering engine option.

        :return: A new CanvasPointer object.
        :rtype: CanvasPointer

        .. note::
            You need not call this method as it is auto called when initializing ``SwCanvas()``.

        .. seealso:: EngineOption
        """
        self.thorvg_lib.tvg_swcanvas_create.argtypes = [ctypes.c_int]
        self.thorvg_lib.tvg_swcanvas_create.restype = CanvasPointer
        return self.thorvg_lib.tvg_swcanvas_create(op)

    def set_target(
        self,
        w: int,
        h: int,
        stride: Optional[int] = None,
        cs: Colorspace = Colorspace.ABGR8888,
    ) -> Tuple[Result, ctypes.Array[ctypes.c_uint32]]:
        """Sets the buffer used in the rasterization process and defines the used colorspace.

        For optimisation reasons TVG does not allocate memory for the output buffer on its own.
        The buffer of a desirable size should be allocated and owned by the caller.

        w, h, stride, cs and buffer_arr will be stored in instance when calling this method.

        :param int w: The width of the raster image.
        :param int h: The height of the raster image.
        :param Optional[int] stride: The stride of the raster image - default is same value as ``w``.
        :param Colorspace cs: The colorspace value defining the way the 32-bits colors should be read/written.

        :return:
            - Result.INVALID_ARGUMENTS An invalid canvas or buffer pointer passed or one of the ``stride``, ``w`` or ``h`` being zero.
            - Result.INSUFFICIENT_CONDITION if the canvas is performing rendering. Please ensure the canvas is synced.
            - Result.NOT_SUPPORTED The software engine is not supported.
        :rtype: Result
        :return: A pointer to the allocated memory block of the size ``stride`` x ``h``.
        :rtype: ctypes.Array[ctypes.c_uint32]

        .. warning::
            Do not access ``buffer`` during Canvas_draw() - Canvas_sync(). It should not be accessed while the engine is writing on it.

        .. seealso:: Colorspace
        """
        if stride is None:
            stride = w
        buffer_arr_type = ctypes.c_uint32 * (stride * h)
        buffer_arr = buffer_arr_type()
        self.thorvg_lib.tvg_swcanvas_set_target.argtypes = [
            CanvasPointer,
            ctypes.POINTER(buffer_arr_type),
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_int,
        ]
        self.thorvg_lib.tvg_swcanvas_set_target.restype = Result
        result = self.thorvg_lib.tvg_swcanvas_set_target(
            self._canvas,
            ctypes.pointer(buffer_arr),
            ctypes.c_uint32(stride),
            ctypes.c_uint32(w),
            ctypes.c_uint32(h),
            cs,
        )
        self.buffer_arr = buffer_arr
        self.w = w
        self.h = h
        self.stride = stride
        self.cs = cs
        return result

    def get_pillow(self, pil_mode: str = "RGBA") -> "Image.Image":
        """Gets Pillow Image from buffer of canvas

        :param str pil_mode: Color mode of Pillow Image. Defaults to RGBA

        :return: Pillow image
        :rtype: PIL.Image.Image
        """
        from PIL import Image

        if self.w is None:
            raise RuntimeError("w cannot be None")
        if self.h is None:
            raise RuntimeError("h cannot be None")
        if self.buffer_arr is None:
            raise RuntimeError("buffer_arr cannot be None")

        return Image.frombuffer(  # type: ignore
            "RGBA", (self.w, self.h), bytes(self.buffer_arr), "raw"
        ).convert(pil_mode)
