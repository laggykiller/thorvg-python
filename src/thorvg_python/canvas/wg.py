#!/usr/bin/env python3
import ctypes
from typing import Any, Optional, Tuple

from ..base import CanvasPointer, Colorspace, EngineOption, Result
from ..engine import Engine
from . import Canvas


class WgCanvas(Canvas):
    """
    WgCanvas API

    A module for rendering the graphical elements using the webgpu engine.

    .. warning::
        The thorvg library bundled with precompiled wheel was not compiled with Wg support
        You will have to load your own thorvg library compiled with Wg support
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
        """Creates a new WebGPU Canvas object with optional rendering engine settings.

        This method generates a WebGPU canvas instance that can be used for drawing vector graphics.
        It accepts an optional parameter ``op`` to choose between different rendering engine behaviors.

        :param thorvg_python.engine.EngineOption op: The rendering engine option.

        :return: A new CanvasPointer object.
        :rtype: thorvg_python.base.CanvasPointer

        .. note::
            Currently, it does not support ``EngineOption.SMART_RENDER``. The request will be ignored.

        .. seealso:: EngineOption

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_wgcanvas_create.argtypes = [ctypes.c_int]
        self.thorvg_lib.tvg_wgcanvas_create.restype = CanvasPointer
        return self.thorvg_lib.tvg_wgcanvas_create(op)

    def set_target(
        self,
        device: Any,
        instance: Any,
        target: Any,
        _type: int,
        w: int,
        h: int,
        cs: Colorspace = Colorspace.ABGR8888,
    ) -> Tuple[Result]:
        """Sets the drawing target for the rasterization.

        :param Any device: WGPUDevice, a desired handle for the wgpu device. If it is ``None``, ThorVG will assign an appropriate device internally.
        :param Any instance: WGPUInstance, context for all other wgpu objects.
        :param Any target: Either WGPUSurface or WGPUTexture, serving as handles to a presentable surface or texture.
        :param int w: The width of the target.
        :param int h: The height of the target.
        :param int cs: Specifies how the pixel values should be interpreted. Currently, it only allows ``Colorspace.ABGR8888S`` as ``WGPUTextureFormat_RGBA8Unorm``.
        :param int _type: ``0``: surface,  ``1``: texture are used as pesentable target.

            TVG_RESULT_INSUFFICIENT_CONDITION if the canvas is performing rendering. Please ensure the canvas is synced.
            TVG_RESULT_NOT_SUPPORTED In case the wg engine is not supported.

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_wgcanvas_set_target.argtypes = [
            CanvasPointer,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_int,
            ctypes.c_int,
        ]
        self.thorvg_lib.tvg_wgcanvas_set_target.restype = Result
        result = self.thorvg_lib.tvg_wgcanvas_set_target(
            self._canvas,
            device,
            instance,
            target,
            ctypes.c_uint32(w),
            ctypes.c_uint32(h),
            cs,
            ctypes.c_uint(_type),
        )
        return result
