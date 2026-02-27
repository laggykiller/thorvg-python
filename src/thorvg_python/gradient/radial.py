#!/usr/bin/env python3
import ctypes
from typing import Optional, Tuple

from ..base import GradientPointer, Result
from ..engine import Engine
from . import Gradient


class RadialGradient(Gradient):
    """
    Radial Gradient API
    """

    def __init__(self, engine: Engine, grad: Optional[GradientPointer] = None):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if grad is None:
            self._grad = self._new()
        else:
            self._grad = grad

    def _new(self) -> GradientPointer:
        """Creates a new radial gradient object.

        :return: A new radial gradient object.
        :rtype: thorvg_python.base.GradientPointer

        .. note::
            You need not call this method as it is auto called when initializing ``LinearGradient()``.
        """
        self.thorvg_lib.tvg_radial_gradient_new.restype = GradientPointer
        return self.thorvg_lib.tvg_radial_gradient_new()

    def set(
        self,
        cx: float,
        cy: float,
        r: float,
        fx: float,
        fy: float,
        fr: float,
    ) -> Result:
        """Sets the radial gradient attributes.

        The radial gradient is defined by the end circle with a center (``cx``, ``cy``) and a radius ``r`` and
        the start circle with a center/focal point (``fx``, ``fy``) and a radius ``fr``.
        The gradient will be rendered such that the gradient stop at an offset of 100% aligns with the edge of the end circle
        and the stop at an offset of 0% aligns with the edge of the start circle.

        :param float cx: The horizontal coordinate of the center of the end circle.
        :param float cy: The vertical coordinate of the center of the end circle.
        :param float r: The radius of the end circle.
        :param float fx: The horizontal coordinate of the center of the start circle.
        :param float fy: The vertical coordinate of the center of the start circle.
        :param float fr: The radius of the start circle.

            TVG_RESULT_INVALID_ARGUMENT An invalid GradientPointer or the radius ``r`` or ``fr`` value is negative.

        .. note::
            In case the radius ``r`` is zero, an object is filled with a single color using the last color specified in the specified in the Gradient.set_color_stops().
        .. note::
            In case the focal point (``fx` and ``fy``) lies outside the end circle, it is projected onto the edge of the end circle.
        .. note::
            If the start circle doesn't fully fit inside the end circle (after possible repositioning), the ``fr`` is reduced accordingly.
        .. note::
            By manipulating the position and size of the focal point, a wide range of visual effects can be achieved, such as directing
            the gradient focus towards a specific edge or enhancing the depth and complexity of shading patterns.
            If a focal effect is not desired, simply align the focal point (``fx`` and ``fy``) with the center of the end circle (``cx`` and ``cy``)
            and set the radius (``fr``) to zero. This will result in a uniform gradient without any focal variations.

        .. seealso:: Gradient.set_color_stops()
        """
        self.thorvg_lib.tvg_radial_gradient_set.argtypes = [
            GradientPointer,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_radial_gradient_set.restype = Result
        return self.thorvg_lib.tvg_radial_gradient_set(
            self._grad,
            ctypes.c_float(cx),
            ctypes.c_float(cy),
            ctypes.c_float(r),
            ctypes.c_float(fx),
            ctypes.c_float(fy),
            ctypes.c_float(fr),
        )

    def get(self) -> Tuple[Result, float, float, float, float, float, float]:
        """The function gets radial gradient attributes.

        :return: Result.INVALID_ARGUMENT An invalid GradientPointer.
        :rtype: thorvg_python.base.Result
        :return: The horizontal coordinate of the center of the bounding circle.
        :rtype: float
        :return: The vertical coordinate of the center of the bounding circle.
        :rtype: float
        :return: The radius of the bounding circle.
        :rtype: float
        :return: The horizontal coordinate of the center of the start circle.
        :rtype: float
        :return: The vertical coordinate of the center of the start circle.
        :rtype: float
        :return: The radius of the start circle.
        :rtype: float
        """
        cx = ctypes.c_float()
        cy = ctypes.c_float()
        r = ctypes.c_float()
        fx = ctypes.c_float()
        fy = ctypes.c_float()
        fr = ctypes.c_float()
        self.thorvg_lib.tvg_radial_gradient_get.argtypes = [
            GradientPointer,
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
        ]
        self.thorvg_lib.tvg_radial_gradient_get.restype = Result
        result = self.thorvg_lib.tvg_radial_gradient_get(
            self._grad,
            ctypes.pointer(cx),
            ctypes.pointer(cy),
            ctypes.pointer(r),
            ctypes.pointer(fx),
            ctypes.pointer(fy),
            ctypes.pointer(fr),
        )
        return result, cx.value, cy.value, r.value, fx.value, fy.value, fr.value
