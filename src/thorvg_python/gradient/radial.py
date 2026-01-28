#!/usr/bin/env python3
import ctypes
from typing import Optional, Tuple

from ..base import GradientStruct, Result
from ..engine import Engine
from . import Gradient


class RadialGradient(Gradient):
    """
    Radial Gradient API
    """

    def __init__(self, engine: Engine, grad: Optional[GradientStruct] = None):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if grad is None:
            self._grad = self._new()
        else:
            self._grad = grad

    def _new(self) -> GradientStruct:
        """Creates a new radial gradient object.

        Note that you need not call this method as it is auto called when initializing ``RadialGradient()``.

        .. code-block:: python

            from thorvg_python import Engine, Shape, RadialGradient, Tvg_ColorStop

            engine = Engine()
            shape = Shape(engine)
            shape.append_rect(700, 700, 100, 100, 20, 20)
            grad = RadialGradient(engine)
            grad.set(550, 550, 50)
            color_stops =
            [
                ColorStop(0.0, 0, 0,   0, 255),
                ColorStop(1.0, 0, 255, 0, 255),
            ]
            grad.set_color_stops(color_stops, 2)
            shape.set_radial_gradient(grad)

        :return: A new radial gradient object.
        :rtype: GradientStruct
        """
        self.thorvg_lib.tvg_radial_gradient_new.restype = ctypes.POINTER(GradientStruct)
        return self.thorvg_lib.tvg_radial_gradient_new().contents

    def set(
        self,
        cx: float,
        cy: float,
        radius: float,
    ) -> Result:
        """Sets the radial gradient bounds.

        The radial gradient bounds are defined as a circle centered in a given point (``cx``, ``cy``) of a given radius.

        :param float cx: The horizontal coordinate of the center of the bounding circle.
        :param float cy: The vertical coordinate of the center of the bounding circle.
        :param float radius: The radius of the bounding circle.

        :return: INVALID_ARGUMENT An invalid GradientStruct pointer or the ``radius`` value less than zero.
        :rtype: Result

        .. note::
            In case the ``radius`` is zero, an object is filled with a single color using the last color specified in the specified in the tvg_gradient_set_color_stops().
        .. seealso:: Gradient.set_color_stops()
        """
        self.thorvg_lib.tvg_radial_gradient_set.argtypes = [
            ctypes.POINTER(GradientStruct),
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_radial_gradient_set.restype = Result
        return self.thorvg_lib.tvg_radial_gradient_set(
            ctypes.pointer(self._grad),
            ctypes.c_float(cx),
            ctypes.c_float(cy),
            ctypes.c_float(radius),
        )

    def get(self) -> Tuple[Result, float, float, float]:
        """The function gets radial gradient center point ant radius

        :return: INVALID_ARGUMENT An invalid GradientStruct pointer.
        :rtype: Result
        :return: The horizontal coordinate of the center of the bounding circle.
        :rtype: float
        :return: The vertical coordinate of the center of the bounding circle.
        :rtype: float
        :return: The radius of the bounding circle.
        :rtype: float
        """
        cx = ctypes.c_float()
        cy = ctypes.c_float()
        radius = ctypes.c_float()
        self.thorvg_lib.tvg_radial_gradient_get.argtypes = [
            ctypes.POINTER(GradientStruct),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
        ]
        self.thorvg_lib.tvg_radial_gradient_get.restype = Result
        result = self.thorvg_lib.tvg_radial_gradient_get(
            ctypes.pointer(self._grad),
            ctypes.pointer(cx),
            ctypes.pointer(cy),
            ctypes.pointer(radius),
        )
        return result, cx.value, cy.value, radius.value
