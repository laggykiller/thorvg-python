#!/usr/bin/env python3
import ctypes

from ..base import CanvasStruct, PaintStruct, Result
from ..engine import Engine
from ..paint import Paint


class Canvas:
    """
    Common Canvas API

    A module for managing and drawing graphical elements.

    A canvas is an entity responsible for drawing the target. It sets up the drawing engine and the buffer, which can be drawn on the screen. It also manages given Paint objects.

    .. note::
        A Canvas behavior depends on the raster engine though the final content of the buffer is expected to be identical.
    .. warning::
        The Paint objects belonging to one Canvas can't be shared among multiple Canvases.

    This is base Canvas class. Please instantiate `SwCanvas`, `GlCanvas` or `WgCanvas` instead
    """

    def __init__(self, engine: Engine, canvas: CanvasStruct):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        self._canvas = canvas

    def destroy(self) -> Result:
        """Clears the canvas internal data, releases all paints stored by the canvas and destroys the canvas object itself.

        :return: INVALID_ARGUMENT An invalid pointer to the CanvasStruct object is passed.
        :rtype: Result

        .. note::
            If the paints from the canvas should not be released, the tvg_canvas_clear() with a ``free`` argument value set to ``false`` should be called.
            Please be aware that in such a case TVG is not responsible for the paints release anymore and it has to be done manually in order to avoid memory leaks.

        .. seealso:: Paint.del(), Canvas.clear()
        """
        self.thorvg_lib.tvg_canvas_destroy.argtypes = [ctypes.POINTER(CanvasStruct)]
        self.thorvg_lib.tvg_canvas_destroy.restype = Result
        return self.thorvg_lib.tvg_canvas_destroy(ctypes.pointer(self._canvas))

    def push(
        self,
        paint: "Paint",
    ) -> Result:
        """Inserts a drawing element into the canvas using a PaintStruct object.

        :param Paint paint: The Paint object to be drawn.

        Only the paints pushed into the canvas will be drawing targets.
        They are retained by the canvas until you call tvg_canvas_clear().

        :return:
            - INVALID_ARGUMENT In case a ``nullptr`` is passed as the argument.
            - INSUFFICIENT_CONDITION An internal error.
        :rtype: Result

        .. note::
            The rendering order of the paints is the same as the order as they were pushed. Consider sorting the paints before pushing them if you intend to use layering.
        .. seealso:: Canvas.clear()
        """
        self.thorvg_lib.tvg_canvas_push.argtypes = [
            ctypes.POINTER(CanvasStruct),
            ctypes.POINTER(PaintStruct),
        ]
        self.thorvg_lib.tvg_canvas_push.restype = Result
        return self.thorvg_lib.tvg_canvas_push(
            ctypes.pointer(self._canvas),
            ctypes.pointer(paint._paint),  # type: ignore
        )

    def reserve(self, n: int) -> Result:
        """Reserves a memory block where the objects pushed into a canvas are stored.

        If the number of PaintStructs to be stored in a canvas is known in advance, calling this function reduces the multiple
        memory allocations thus improves the performance.

        :param int n: The number of objects for which the memory is to be reserved.

        :return: INVALID_ARGUMENT An invalid CanvasStruct pointer.
        :rtype: Result

        .. deprecated:: 0.10
        .. note:: Malfunctional
        """
        self.thorvg_lib.tvg_canvas_reserve.argtypes = [
            ctypes.POINTER(CanvasStruct),
            ctypes.c_uint32,
        ]
        self.thorvg_lib.tvg_canvas_reserve.restype = Result
        return self.thorvg_lib.tvg_canvas_reserve(
            ctypes.pointer(self._canvas), ctypes.c_uint32(n)
        )

    def clear(
        self,
        free: bool,
    ) -> Result:
        """Sets the total number of the paints pushed into the canvas to be zero.
        PaintStruct objects stored in the canvas are released if ``free`` is set to true, otherwise the memory is not deallocated and
        all paints should be released manually in order to avoid memory leaks.

        :param bool free: If ``true`` the memory occupied by paints is deallocated, otherwise it is not.

        :return: INVALID_ARGUMENT An invalid CanvasStruct pointer.
        :rtype: Result

        .. seealso:: Canvas.destroy()
        """
        self.thorvg_lib.tvg_canvas_clear.argtypes = [
            ctypes.POINTER(CanvasStruct),
            ctypes.c_bool,
        ]
        self.thorvg_lib.tvg_canvas_clear.restype = Result
        return self.thorvg_lib.tvg_canvas_clear(
            ctypes.pointer(self._canvas), ctypes.c_bool(free)
        )

    def update(self) -> Result:
        """Updates all paints in a canvas.

        Should be called before drawing in order to prepare paints for the rendering.

        :return: INVALID_ARGUMENT An invalid CanvasStruct pointer.
        :rtype: Result

        .. seealso:: Canvas.update_paint()
        """
        self.thorvg_lib.tvg_canvas_update.argtypes = [
            ctypes.POINTER(CanvasStruct),
        ]
        self.thorvg_lib.tvg_canvas_update.restype = Result
        return self.thorvg_lib.tvg_canvas_update(
            ctypes.pointer(self._canvas),
        )

    def update_paint(self, paint: "Paint") -> Result:
        """Updates the given PaintStruct object from the canvas before the rendering.

        If a client application using the TVG library does not update the entire canvas with Canvas.update() in the frame
        rendering process, PaintStruct objects previously added to the canvas should be updated manually with this function.

        :param PaintStruct paint: The PaintStruct object to be updated.

        :return: INVALID_ARGUMENT In case a ``nullptr`` is passed as the argument.
        :rtype: Result

        .. seealso:: Canvas.update()
        """
        self.thorvg_lib.tvg_canvas_update_paint.argtypes = [
            ctypes.POINTER(CanvasStruct),
            ctypes.POINTER(PaintStruct),
        ]
        self.thorvg_lib.tvg_canvas_update_paint.restype = Result
        return self.thorvg_lib.tvg_canvas_update_paint(
            ctypes.pointer(self._canvas),
            ctypes.pointer(paint._paint),  # type: ignore
        )

    def draw(self) -> Result:
        """Requests the canvas to draw the PaintStruct objects.

        All paints from the given canvas will be rasterized to the buffer.

        :return: INVALID_ARGUMENT An invalid CanvasStruct pointer.
        :rtype: Result

        .. note::
            Drawing can be asynchronous based on the assigned thread number. To guarantee the drawing is done, call Canvas.sync() afterwards.
        .. seealso:: Canvas.sync()
        """
        self.thorvg_lib.tvg_canvas_draw.argtypes = [
            ctypes.POINTER(CanvasStruct),
        ]
        self.thorvg_lib.tvg_canvas_draw.restype = Result
        return self.thorvg_lib.tvg_canvas_draw(
            ctypes.pointer(self._canvas),
        )

    def sync(self) -> Result:
        """Guarantees that the drawing process is finished.

        Since the canvas rendering can be performed asynchronously, it should be called after the Canvas.draw().

        :return:
            - INVALID_ARGUMENT An invalid CanvasStruct pointer.
            - INSUFFICIENT_CONDITION ``canvas`` is either already in sync condition or in a damaged condition (a draw is required before syncing).
        :rtype: Result

        .. seealso:: Canvas.draw()
        """
        self.thorvg_lib.tvg_canvas_sync.argtypes = [
            ctypes.POINTER(CanvasStruct),
        ]
        self.thorvg_lib.tvg_canvas_sync.restype = Result
        return self.thorvg_lib.tvg_canvas_sync(
            ctypes.pointer(self._canvas),
        )

    def set_viewport(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
    ) -> Result:
        """Sets the drawing region in the canvas.

        This function defines the rectangular area of the canvas that will be used for drawing operations.
        The specified viewport is used to clip the rendering output to the boundaries of the rectangle.

        :param int x: The x-coordinate of the upper-left corner of the rectangle.
        :param int y: The y-coordinate of the upper-left corner of the rectangle.
        :param int w: The width of the rectangle.
        :param int h: The height of the rectangle.

        :return: Result enumeration.
        :rtype: Result

        .. warning::
            It's not allowed to change the viewport during tvg_canvas_update() - tvg_canvas_sync() or tvg_canvas_push() - tvg_canvas_sync().

        .. note::
            When resetting the target, the viewport will also be reset to the target size.
        .. seealso:: SwCanvas.set_target()
        .. versionadded:: 0.15
        """
        self.thorvg_lib.tvg_canvas_set_viewport.argtypes = [
            ctypes.POINTER(CanvasStruct),
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
        ]
        self.thorvg_lib.tvg_canvas_set_viewport.restype = Result
        return self.thorvg_lib.tvg_canvas_set_viewport(
            ctypes.pointer(self._canvas),
            ctypes.c_int32(x),
            ctypes.c_int32(y),
            ctypes.c_int32(w),
            ctypes.c_int32(h),
        )
