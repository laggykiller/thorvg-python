#!/usr/bin/env python3
import ctypes
from typing import TYPE_CHECKING, Optional, Tuple

from ..base import CanvasStruct, Colorspace, MempoolPolicy, Result
from ..engine import Engine
from . import Canvas

if TYPE_CHECKING:
    from PIL import Image


class SwCanvas(Canvas):
    """
    SwCanvas API

    A module for rendering the graphical elements using the software engine.
    """

    def __init__(self, engine: Engine, canvas: Optional[CanvasStruct] = None):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        self.buffer_arr: Optional[ctypes.Array[ctypes.c_uint32]] = None
        self.w: Optional[int] = None
        self.h: Optional[int] = None
        self.stride: Optional[int] = None
        self.cs: Optional[Colorspace] = None
        if canvas is None:
            self._canvas = self._create()
        else:
            self._canvas = canvas

    def _create(self) -> CanvasStruct:
        """Creates a Canvas object.

        Note that you need not call this method as it is auto called when initializing ``SwCanvas()``.

        .. code-block:: python
            from thorvg_python import Engine, SwCanvas

            engine = Engine()
            canvas = SwCanvas(engine)
            result, buffer = canvas.set_target(100, 100, 100, Colorspace.ARGB8888)

            //set up paints and add them into the canvas before drawing it

            canvas.destroy()
            engine.term()

        :return: new CanvasStruct object.
        :rtype: CanvasStruct
        """
        self.thorvg_lib.tvg_swcanvas_create.restype = ctypes.POINTER(CanvasStruct)
        return self.thorvg_lib.tvg_swcanvas_create().contents

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
            - ABGR8888 (Default)
            - ARGB8888

        :return:
            - INVALID_ARGUMENTS An invalid canvas or buffer pointer passed or one of the ``stride``, ``w`` or ``h`` being zero.
            - INSUFFICIENT_CONDITION if the canvas is performing rendering. Please ensure the canvas is synced.
            - NOT_SUPPORTED The software engine is not supported.
        :rtype: Result
        :return: A pointer to the allocated memory block of the size ``stride`` x ``h``.
        :rtype: ctypes.Array[ctypes.c_uint32]

        .. warning::
            Do not access ``buffer`` during tvg_canvas_draw() - tvg_canvas_sync(). It should not be accessed while the engine is writing on it.

        .. seealso:: Colorspace
        """
        if stride is None:
            stride = w
        buffer_arr_type = ctypes.c_uint32 * (stride * h)
        buffer_arr = buffer_arr_type()
        self.thorvg_lib.tvg_swcanvas_set_target.argtypes = [
            ctypes.POINTER(CanvasStruct),
            ctypes.POINTER(buffer_arr_type),
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_int,
        ]
        self.thorvg_lib.tvg_swcanvas_set_target.restype = Result
        result = self.thorvg_lib.tvg_swcanvas_set_target(
            ctypes.pointer(self._canvas),
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

        .. code-block:: python

            from thorvg_python import Engine, SwCanvas, Shape

            engine = tvg.Engine()
            canvas = tvg.SwCanvas(engine)
            canvas.set_target(1920, 1080)

            // Draw on canvas
            rect = Shape(engine)
            rect.append_rect(50, 50, 200, 200, 20, 20)
            rect.set_fill_color(100, 100, 100, 100)
            canvas.push(rect)

            canvas.draw()
            canvas.sync()

            im = canvas.get_pillow()

            canvas.destroy()
            engine.term()

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

    def set_mempool(
        self,
        policy: MempoolPolicy,
    ) -> Result:
        """Sets the software engine memory pool behavior policy.

        ThorVG draws a lot of shapes, it allocates/deallocates a few chunk of memory
        while processing rendering. It internally uses one shared memory pool
        which can be reused among the canvases in order to avoid memory overhead.

        Thus ThorVG suggests using a memory pool policy to satisfy user demands,
        if it needs to guarantee the thread-safety of the internal data access.

        :param MempoolPolicy policy: The method specifying the Memory Pool behavior. The default value is ``DEFAULT``.

        :return:
            - INVALID_ARGUMENTS An invalid canvas pointer passed.
            - INSUFFICIENT_CONDITION The canvas contains some paints already.
            - NOT_SUPPORTED The software engine is not supported.
        :rtype: Result

        .. note::
            When ``policy`` is set as ``INDIVIDUAL``, the current instance of canvas uses its own individual
        memory data, which is not shared with others. This is necessary when the canvas is accessed on a worker-thread.

        .. warning::
            It's not allowed after pushing any paints.
        """
        self.thorvg_lib.tvg_swcanvas_set_mempool.argtypes = [
            ctypes.POINTER(CanvasStruct),
            ctypes.c_int,
        ]
        self.thorvg_lib.tvg_swcanvas_set_mempool.restype = Result
        return self.thorvg_lib.tvg_swcanvas_set_mempool(
            ctypes.pointer(self._canvas), policy
        )
