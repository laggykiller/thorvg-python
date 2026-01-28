#!/usr/bin/env python3
import ctypes
from typing import Optional, Tuple

from ..base import GradientStruct, Result
from ..engine import Engine
from . import Gradient


class LinearGradient(Gradient):
    """
    Linear Gradient API
    """

    def __init__(self, engine: Engine, grad: Optional[GradientStruct] = None):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if grad is None:
            self._grad = self._new()
        else:
            self._grad = grad

    def _new(self) -> GradientStruct:
        """Creates a new linear gradient object.

        Note that you need not call this method as it is auto called when initializing ``LinearGradient()``.

        .. code-block:: python

            from thorvg_python import Engine, Shape, LinearGradient, ColorStop

            engine = Engine()
            shape = Shape(engine)
            shape.append_rect(700, 700, 100, 100, 20, 20)
            grad = LinearGradient(engine)
            grad.set(700, 700, 800, 800)
            color_stops = [
                ColorStop(0.0, 0, 0,   0, 255),
                ColorStop(1.0, 0, 255, 0, 255),
            ]
            grad.set_color_stops(color_stops, 2)
            shape.set_linear_gradient(grad)

        :return: A new linear gradient object.
        :rtype: GradientStruct
        """
        self.thorvg_lib.tvg_linear_gradient_new.restype = ctypes.POINTER(GradientStruct)
        return self.thorvg_lib.tvg_linear_gradient_new().contents

    def set(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
    ) -> Result:
        """Sets the linear gradient bounds.

        The bounds of the linear gradient are defined as a surface constrained by two parallel lines crossing
        the given points (``x1``, ``y1``) and (``x2``, ``y2``), respectively. Both lines are perpendicular to the line linking
        (``x1``, ``y1``) and (``x2``, ``y2``).

        :param float x1: The horizontal coordinate of the first point used to determine the gradient bounds.
        :param float y1: The vertical coordinate of the first point used to determine the gradient bounds.
        :param float x2: The horizontal coordinate of the second point used to determine the gradient bounds.
        :param float y2: The vertical coordinate of the second point used to determine the gradient bounds.

        :return: INVALID_ARGUMENT An invalid GradientStruct pointer.
        :rtype: Result

        .. note::
            In case the first and the second points are equal, an object is filled with a single color using the last color specified in the tvg_gradient_set_color_stops().
        .. seealso:: Gradient.set_color_stops()
        """
        self.thorvg_lib.tvg_linear_gradient_set.argtypes = [
            ctypes.POINTER(GradientStruct),
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_linear_gradient_set.restype = Result
        return self.thorvg_lib.tvg_linear_gradient_set(
            ctypes.pointer(self._grad),
            ctypes.c_float(x1),
            ctypes.c_float(y1),
            ctypes.c_float(x2),
            ctypes.c_float(y2),
        )

    def get(
        self,
    ) -> Tuple[Result, float, float, float, float]:
        """Gets the linear gradient bounds.

        The bounds of the linear gradient are defined as a surface constrained by two parallel lines crossing
        the given points (``x1``, ``y1``) and (``x2``, ``y2``), respectively. Both lines are perpendicular to the line linking
        (``x1``, ``y1``) and (``x2``, ``y2``).

        :return: INVALID_ARGUMENT An invalid GradientStruct pointer.
        :rtype: Result
        :return: The horizontal coordinate of the first point used to determine the gradient bounds.
        :rtype: float
        :return: The vertical coordinate of the first point used to determine the gradient bounds.
        :rtype: float
        :return: The horizontal coordinate of the second point used to determine the gradient bounds.
        :rtype: float
        :return: The vertical coordinate of the second point used to determine the gradient bounds.
        :rtype: float
        """
        x1 = ctypes.c_float()
        y1 = ctypes.c_float()
        x2 = ctypes.c_float()
        y2 = ctypes.c_float()
        self.thorvg_lib.tvg_linear_gradient_get.argtypes = [
            ctypes.POINTER(GradientStruct),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
        ]
        self.thorvg_lib.tvg_linear_gradient_get.restype = Result
        result = self.thorvg_lib.tvg_linear_gradient_get(
            ctypes.pointer(self._grad),
            ctypes.pointer(x1),
            ctypes.pointer(y1),
            ctypes.pointer(x2),
            ctypes.pointer(y2),
        )
        return result, x1.value, y1.value, x2.value, y2.value
