#!/usr/bin/env python3
import ctypes
from typing import Optional

from ..base import CanvasPointer, PaintPointer, Result
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

    def __init__(self, engine: Engine, canvas: CanvasPointer):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        self._canvas = canvas

    def destroy(self) -> Result:
        """Clears the canvas internal data, releases all paints stored by the canvas and destroys the canvas object itself.

        :rtype: thorvg_python.base.Result
        """
        self.thorvg_lib.tvg_canvas_destroy.argtypes = [CanvasPointer]
        self.thorvg_lib.tvg_canvas_destroy.restype = Result
        return self.thorvg_lib.tvg_canvas_destroy(self._canvas)

    def add(
        self,
        paint: "Paint",
    ) -> Result:
        """Adds a paint object to the canvas for rendering.

        Adds the specified paint into the canvas root scene. Only paints added to
        the canvas are considered rendering targets. The canvas retains the paint
        object until it is explicitly removed via Canvas.remove().

        :param thorvg_python.paint.Paint paint: A handle to the paint object to be rendered.

        :return: TVG_RESULT_INSUFFICIENT_CONDITION If the canvas is not in a valid state to accept new paints.
        :rtype: thorvg_python.base.Result

        ..note:: Ownership of the ``paint`` object is transferred to the canvas upon
            successful addition. To retain ownership, call ``Paint.ref()``
            before adding it to the canvas.

        ..note:: The rendering order of paint objects follows the order in which they are
            added to the canvas. If layering is required, ensure paints are added in
            the desired order.

        .. seealso:: Canvas.insert()

        .. seealso:: Canvas.remove()
        """
        self.thorvg_lib.tvg_canvas_add.argtypes = [
            CanvasPointer,
            PaintPointer,
        ]
        self.thorvg_lib.tvg_canvas_add.restype = Result
        return self.thorvg_lib.tvg_canvas_add(
            self._canvas,
            paint._paint,  # type: ignore
        )

    def insert(
        self,
        target: Paint,
        at: Optional[Paint],
    ) -> Result:
        """Inserts a paint object into the canvas root scene.

        Inserts a paint object into the root scene of the specified canvas. If the
        ``at`` parameter is provided, the paint object is inserted immediately before
        the specified paint in the root scene. If ``at`` is ``None``, the paint object
        is appended to the end of the root scene.

        :param thorvg_python.paint.Paint target: A handle to the paint object to be inserted into the root scene.
            This parameter must not be ``None``.
        :param Optional[Paint] at: A handle to an existing paint object in the root scene before
            which ``target`` will be inserted. If ``None``, ``target`` is
            appended to the end of the root scene.

        :return: TVG_RESULT_INSUFFICIENT_CONDITION If the canvas is not in a valid state to accept new paints.
        :rtype: thorvg_python.base.Result

        ..note:: Ownership of the ``paint`` object is transferred to the canvas upon
            successful addition. To retain ownership, call ``Paint.ref()``
            before adding it to the canvas.

        ..note:: The rendering order of paint objects follows the order in which they are
            added to the canvas. If layering is required, ensure paints are added in
            the desired order.

        .. seealso:: Canvas.insert()

        .. seealso:: Canvas.remove()
        """
        if at is None:
            at_type = ctypes.c_void_p
            at_c = ctypes.c_void_p()
        else:
            at_type = PaintPointer
            at_c = at._paint  # type: ignore

        self.thorvg_lib.tvg_canvas_insert.argtypes = [
            CanvasPointer,
            PaintPointer,
            at_type,
        ]
        self.thorvg_lib.tvg_canvas_insert.restype = Result
        return self.thorvg_lib.tvg_canvas_insert(
            self._canvas,
            target._paint,  # type: ignore
            at_c,
        )

    def remove(
        self,
        paint: Optional[Paint] = None,
    ) -> Result:
        """Removes a paint object from the root scene.

        This function removes a specified paint object from the root scene. If no paint
        object is specified (i.e., the default ``None`` is used), the function
        performs to clear all paints from the scene.

        :param Optional[thorvg_python.paint.Paint] paint: Paint object to be removed from the root scene.
            If ``None``, remove all the paints from the root scene.

        :return: Result.INVALID_ARGUMENT An invalid CanvasPointer.
        :rtype: thorvg_python.base.Result

        .. seealso:: Canvas.add()

        .. seealso:: Canvas.insert()

        .. versionadded:: 1.0
        """
        if paint is None:
            paint_type = ctypes.c_void_p
            paint_ptr = ctypes.c_void_p()
        else:
            paint_type = PaintPointer
            paint_ptr = paint._paint  # type: ignore
        self.thorvg_lib.tvg_canvas_remove.argtypes = [
            CanvasPointer,
            paint_type,
        ]
        self.thorvg_lib.tvg_canvas_remove.restype = Result
        return self.thorvg_lib.tvg_canvas_remove(
            self._canvas,
            paint_ptr,
        )

    def update(self) -> Result:
        """Requests the canvas to update modified paint objects in preparation for rendering.

        This function triggers an internal update for all paint instances that have been modified
        since the last update. It ensures that the canvas state is ready for accurate rendering.

        :return:
            - TVG_RESULT_INVALID_ARGUMENT An invalid CanvasPointer.
            - TVG_RESULT_INSUFFICIENT_CONDITION The canvas is not properly prepared.
              This may occur if the canvas target has not been set or if the update is called during drawing.
              Call Canvas.sync() before trying.
        :rtype: thorvg_python.base.Result

        .. note::
            Only paint objects that have been changed will be processed.

        .. note::
            If the canvas is configured with multiple threads, the update may be performed asynchronously.

        .. seealso:: Canvas.sync()
        """
        self.thorvg_lib.tvg_canvas_update.argtypes = [
            CanvasPointer,
        ]
        self.thorvg_lib.tvg_canvas_update.restype = Result
        return self.thorvg_lib.tvg_canvas_update(
            self._canvas,
        )

    def draw(self, clear: bool) -> Result:
        """Requests the canvas to render the Paint objects.

        :param clear: If ``true``, clears the target buffer to zero before drawing.

        :return:
            - TVG_RESULT_INVALID_ARGUMENT An invalid CanvasPointer.
            - TVG_RESULT_INSUFFICIENT_CONDITION The canvas is not properly prepared.
              This may occur if the canvas target has not been set or if the update is called during drawing.
              without calling Canvas.sync() in between.
        :rtype: thorvg_python.base.Result

        .. note::
            Clearing the buffer is unnecessary if the canvas will be fully covered
            with opaque content. Skipping the clear can improve performance.
        .. note::
            Drawing may be performed asynchronously if the thread count is greater than zero.
            To ensure the drawing process is complete, call sync() afterwards.
        .. note::
            If the canvas has not been updated prior to Canvas.draw(), it may implicitly perform Canvas.update()

        .. seealso:: Canvas.sync()
        .. seealso:: Canvas.update()
        """
        self.thorvg_lib.tvg_canvas_draw.argtypes = [
            CanvasPointer,
            ctypes.c_bool,
        ]
        self.thorvg_lib.tvg_canvas_draw.restype = Result
        return self.thorvg_lib.tvg_canvas_draw(self._canvas, ctypes.c_bool(clear))

    def sync(self) -> Result:
        """Guarantees that drawing task is finished.

        The Canvas rendering can be performed asynchronously. To make sure that rendering is finished,
        the Canvas.sync() must be called after the Canvas.draw() regardless of threading.

        :return: TVG_RESULT_INVALID_ARGUMENT An invalid CanvasPointer.
        :rtype: thorvg_python.base.Result

        .. seealso:: Canvas.draw()
        """
        self.thorvg_lib.tvg_canvas_sync.argtypes = [
            CanvasPointer,
        ]
        self.thorvg_lib.tvg_canvas_sync.restype = Result
        return self.thorvg_lib.tvg_canvas_sync(
            self._canvas,
        )

    def set_viewport(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
    ) -> Result:
        """Sets the drawing region of the canvas.

        This function defines a rectangular area of the canvas to be used for drawing operations.
        The specified viewport clips rendering output to the boundaries of that rectangle.

        Please note that changing the viewport is only allowed at the beginning of the rendering sequence—that is, after calling Canvas.sync().

        :param x: The x-coordinate of the upper-left corner of the rectangle.
        :param y: The y-coordinate of the upper-left corner of the rectangle.
        :param w: The width of the rectangle.
        :param h: The height of the rectangle.

        :return:
            - Result.INVALID_ARGUMENT An invalid CanvasPointer.
            - Result.INSUFFICIENT_CONDITION If the canvas is not in a synced state.
        :rtype: thorvg_python.base.Result

        .. seealso:: Canvas.sync()
        .. seealso:: SwCanvas.set_target()
        .. seealso:: GlCanvas.set_target()
        .. seealso:: WgCanvas.set_target()

        .. warning::
            Changing the viewport is not allowed after calling Canvas.add(),
            Canvas.remove(), Canvas.update(), or Canvas.draw().

        .. note::
            When the target is reset, the viewport will also be reset to match the target size.

        .. versionadded:: 0.15
        """
        self.thorvg_lib.tvg_canvas_set_viewport.argtypes = [
            CanvasPointer,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
        ]
        self.thorvg_lib.tvg_canvas_set_viewport.restype = Result
        return self.thorvg_lib.tvg_canvas_set_viewport(
            self._canvas,
            ctypes.c_int32(x),
            ctypes.c_int32(y),
            ctypes.c_int32(w),
            ctypes.c_int32(h),
        )
