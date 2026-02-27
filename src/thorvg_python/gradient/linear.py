#!/usr/bin/env python3
import ctypes
from typing import Optional, Tuple

from ..base import GradientPointer, Result
from ..engine import Engine
from . import Gradient


class LinearGradient(Gradient):
    """
    Linear Gradient API
    """

    def __init__(self, engine: Engine, grad: Optional[GradientPointer] = None):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if grad is None:
            self._grad = self._new()
        else:
            self._grad = grad

    def _new(self) -> GradientPointer:
        """Creates a new linear gradient object.

        :return: A new linear gradient object.
        :rtype: GradientPointer

        .. note::
            You need not call this method as it is auto called when initializing ``LinearGradient()``.
        """
        self.thorvg_lib.tvg_linear_gradient_new.restype = GradientPointer
        return self.thorvg_lib.tvg_linear_gradient_new()

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

        :return: Result.INVALID_ARGUMENT An invalid GradientPointer.
        :rtype: Result

        .. note::
            In case the first and the second points are equal, an object is filled with a single color using the last color specified in the Gradient.set_color_stops().
        .. seealso:: Gradient.set_color_stops()
        """
        self.thorvg_lib.tvg_linear_gradient_set.argtypes = [
            GradientPointer,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_linear_gradient_set.restype = Result
        return self.thorvg_lib.tvg_linear_gradient_set(
            self._grad,
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

        :return: Result.INVALID_ARGUMENT An invalid GradientPointer.
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
            GradientPointer,
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
        ]
        self.thorvg_lib.tvg_linear_gradient_get.restype = Result
        result = self.thorvg_lib.tvg_linear_gradient_get(
            self._grad,
            ctypes.pointer(x1),
            ctypes.pointer(y1),
            ctypes.pointer(x2),
            ctypes.pointer(y2),
        )
        return result, x1.value, y1.value, x2.value, y2.value
