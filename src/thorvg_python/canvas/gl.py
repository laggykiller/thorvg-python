#!/usr/bin/env python3
import ctypes
from typing import Any, Optional, Tuple

from ..base import CanvasPointer, Colorspace, EngineOption, Result
from ..engine import Engine
from . import Canvas


class GlCanvas(Canvas):
    """
    GlCanvas API

    A module for rendering the graphical elements using the opengl engine.

    .. warning::
        The thorvg library bundled with precompiled wheel was not compiled with Gl support
        You will have to load your own thorvg library compiled with Gl support
        with Engine(thorvg_lib_path="...")
    """

    def __init__(
        self, engine: Engine, op: EngineOption, canvas: Optional[CanvasPointer] = None
    ):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if canvas is None:
            self._canvas = self._create(op)
        else:
            self._canvas = canvas

    def _create(self, op: EngineOption) -> CanvasPointer:
        """Creates a new OpenGL/ES Canvas object with optional rendering engine settings.

        This method generates a OpenGL/ES canvas instance that can be used for drawing vector graphics.
        It accepts an optional parameter ``op`` to choose between different rendering engine behaviors.

        :param thorvg_python.engine.EngineOption op: The rendering engine option.

        :return: A new CanvasPointer object.
        :rtype: thorvg_python.base.CanvasPointer

        .. note::
            Currently, it does not support ``EngineOption.SMART_RENDER``. The request will be ignored.

        .. note::
            You need not call this method as it is auto called when initializing ``GlCanvas()``.

        .. seealso:: EngineOption

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_glcanvas_create.argtypes = [ctypes.c_int]
        self.thorvg_lib.tvg_glcanvas_create.restype = CanvasPointer
        return self.thorvg_lib.tvg_glcanvas_create(op)

    def set_target(
        self,
        display: Any,
        surface: Any,
        context: Any,
        _id: int,
        w: int,
        h: int,
        cs: Colorspace = Colorspace.ABGR8888,
    ) -> Tuple[Result]:
        """Sets the drawing target for rasterization.

        This function specifies the drawing target where the rasterization will occur. It can target
        a specific framebuffer object (FBO) or the main surface.

        :param Any display: The platform-specific display handle (EGLDisplay for EGL). Set ``None`` for other systems.
        :param Any surface: The platform-specific surface handle (EGLSurface for EGL, HDC for WGL). Set ``None`` for other systems.
        :param Any context: The OpenGL context to be used for rendering on this canvas.
        :param int _id: The GL target ID, usually indicating the FBO ID. A value of ``0`` specifies the main surface.
        :param int w: The width (in pixels) of the raster image.
        :param int h: The height (in pixels) of the raster image.
        :param ColorSpace cs: Specifies how the pixel values should be interpreted. Currently, it only allows ``Colorspace.ABGR8888S`` as ``GL_RGBA8``.

        :return:
            - Result.INSUFFICIENT_CONDITION If the canvas is currently rendering.
              Ensure that ``Canvas.sync()`` has been called before setting a new target.
            - Result.NOT_SUPPORTED In case the gl engine is not supported.
        :rtype: thorvg_python.base.Result

        .. note::
            If ``display`` and ``surface`` are not provided, the ThorVG GL engine assumes that
            the appropriate OpenGL context is already current and will not attempt to bind a new one.

        .. seealso:: Canvas.sync()

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_glcanvas_set_target.argtypes = [
            CanvasPointer,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_int,
        ]
        self.thorvg_lib.tvg_glcanvas_set_target.restype = Result
        result = self.thorvg_lib.tvg_glcanvas_set_target(
            self._canvas,
            display,
            surface,
            context,
            ctypes.c_uint32(_id),
            ctypes.c_uint32(w),
            ctypes.c_uint32(h),
            cs,
        )
        return result
