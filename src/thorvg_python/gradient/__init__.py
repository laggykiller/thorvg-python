#!/usr/bin/env python3
import ctypes
from typing import Optional, Sequence, Tuple, cast

from ..base import ColorStop, GradientPointer, Matrix, Result, StrokeFill, TvgType
from ..engine import Engine


class Gradient:
    """
    Common Gradient API

    A module managing the gradient fill of objects.

    The module enables to set and to get the gradient colors and their arrangement inside the gradient bounds,
    to specify the gradient bounds and the gradient behavior in case the area defined by the gradient bounds
    is smaller than the area to be filled.

    This is base Gradient class. Please use LinearGradient or RadialGradient for creating
    """

    def __init__(self, engine: Engine, grad: GradientPointer):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        self._grad = grad

    def set_color_stops(
        self,
        color_stop: Sequence[ColorStop],
    ) -> Result:
        """Sets the parameters of the colors of the gradient and their position.

        :param Sequence[thorvg_python.base.ColorStop] color_stop: An array of ColorStop data structure.

        :return: Result.INVALID_ARGUMENT An invalid GradientPointer.
        :rtype: thorvg_python.base.Result
        """
        color_stop_arr_type = ColorStop * len(color_stop)
        self.thorvg_lib.tvg_gradient_set_color_stops.argtypes = [
            GradientPointer,
            ctypes.POINTER(color_stop_arr_type),
            ctypes.c_uint32,
        ]
        self.thorvg_lib.tvg_gradient_set_color_stops.restype = Result
        return self.thorvg_lib.tvg_gradient_set_color_stops(
            self._grad,
            ctypes.pointer(color_stop_arr_type(*color_stop)),
            ctypes.c_uint32(len(color_stop)),
        )

    def get_color_stops(
        self,
    ) -> Tuple[Result, Sequence[ColorStop]]:
        """Gets the parameters of the colors of the gradient, their position and number

        The function does not allocate any memory.

        :return: Result.INVALID_ARGUMENT A ``None`` passed as the argument.
        :rtype: thorvg_python.base.Result
        :return: An array of ColorStop data structure.
        :rtype: Sequence[ColorStop]
        """
        color_stop_ptr = ctypes.POINTER(ColorStop)()
        cnt = ctypes.c_uint32()
        self.thorvg_lib.tvg_gradient_get_color_stops.argtypes = [
            GradientPointer,
            ctypes.POINTER(ctypes.POINTER(ColorStop)),
            ctypes.POINTER(ctypes.c_uint32),
        ]
        self.thorvg_lib.tvg_gradient_get_color_stops.restype = Result
        result = self.thorvg_lib.tvg_gradient_get_color_stops(
            self._grad,
            ctypes.pointer(color_stop_ptr),
            ctypes.pointer(cnt),
        )
        color_stop_type = ColorStop * cnt.value
        color_stop_arr = color_stop_type.from_address(
            ctypes.addressof(color_stop_ptr.contents)
        )
        return result, [color_stop_arr[i] for i in range(cnt.value)]

    def set_spread(
        self,
        spread: StrokeFill,
    ) -> Result:
        """Sets the StrokeFill value, which specifies how to fill the area outside the gradient bounds.

        :param StrokeFill spread: The FillSpread value.

        :return: Result.INVALID_ARGUMENT An invalid GradientPointer.
        :rtype: thorvg_python.base.Result
        """
        self.thorvg_lib.tvg_gradient_set_spread.argtypes = [
            GradientPointer,
            ctypes.c_uint8,
        ]
        self.thorvg_lib.tvg_gradient_set_spread.restype = Result
        return self.thorvg_lib.tvg_gradient_set_spread(
            self._grad,
            spread,
        )

    def get_spread(self) -> Tuple[Result, StrokeFill]:
        """Gets the FillSpread value of the gradient object.

        :return: Result.INVALID_ARGUMENT A ``None`` passed as the argument.
        :rtype: thorvg_python.base.Result
        :return: The FillSpread value.
        :rtype: StrokeFill
        """
        spread = ctypes.c_uint8()
        self.thorvg_lib.tvg_gradient_get_spread.argtypes = [
            GradientPointer,
            ctypes.POINTER(ctypes.c_uint8),
        ]
        self.thorvg_lib.tvg_gradient_get_spread.restype = Result
        result = self.thorvg_lib.tvg_gradient_get_spread(
            self._grad,
            ctypes.pointer(spread),
        )
        return result, StrokeFill(spread.value)

    def set_transform(self, m: Matrix) -> Result:
        """Sets the matrix of the affine transformation for the gradient object.

        The augmented matrix of the transformation is expected to be given.

        :param Matrix m The 3x3 augmented matrix.

        :return: Result.INVALID_ARGUMENT A ``None`` is passed as the argument.
        :rtype: thorvg_python.base.Result
        """
        self.thorvg_lib.tvg_gradient_set_transform.argtypes = [
            GradientPointer,
            ctypes.POINTER(Matrix),
        ]
        self.thorvg_lib.tvg_gradient_set_transform.restype = Result
        return self.thorvg_lib.tvg_gradient_set_transform(
            self._grad,
            ctypes.pointer(m),
        )

    def get_transform(self) -> Tuple[Result, Matrix]:
        """Gets the matrix of the affine transformation of the gradient object.

        In case no transformation was applied, the identity matrix is set.

        :return: Result.INVALID_ARGUMENT A ``None`` is passed as the argument.
        :rtype: thorvg_python.base.Result
        :return: The 3x3 augmented matrix.
        :rtype: thorvg_python.base.Matrix
        """
        m = Matrix()
        self.thorvg_lib.tvg_gradient_get_transform.argtypes = [
            GradientPointer,
            ctypes.POINTER(Matrix),
        ]
        self.thorvg_lib.tvg_gradient_get_transform.restype = Result
        result = self.thorvg_lib.tvg_gradient_get_transform(
            self._grad,
            ctypes.pointer(m),
        )
        return result, m

    def get_type(self) -> Tuple[Result, TvgType]:
        """Gets the unique value of the gradient instance indicating the instance type.

        :return: Result.INVALID_ARGUMENT In case a ``None`` is passed as the argument.
        :rtype: thorvg_python.base.Result
        :return: The unique type of the gradient instance type.
        :rtype: thorvg_python.base.TvgType

        .. note::
            Experimental API
        """
        _type = ctypes.c_uint8()
        self.thorvg_lib.tvg_gradient_get_type.argtypes = [
            GradientPointer,
            ctypes.POINTER(ctypes.c_uint8),
        ]
        self.thorvg_lib.tvg_gradient_get_type.restype = Result
        result = self.thorvg_lib.tvg_gradient_get_type(
            self._grad,
            ctypes.pointer(_type),
        )
        return result, TvgType(_type.value)

    def duplicate(self) -> Optional["Gradient"]:
        """Duplicates the given GradientPointer object.

        Creates a new object and sets its all properties as in the original object.

        :return: A copied GradientPointer object if succeed, ``None`` otherwise.
        :rtype: thorvg_python.base.GradientPointer
        """
        self.thorvg_lib.tvg_gradient_duplicate.argtypes = [GradientPointer]
        self.thorvg_lib.tvg_gradient_duplicate.restype = GradientPointer
        tvg_gradient = cast(
            GradientPointer,
            self.thorvg_lib.tvg_gradient_duplicate(self._grad),
        )
        if type(self).__name__ == "LinearGradient":
            from .linear import LinearGradient

            return LinearGradient(self.engine, tvg_gradient)
        elif type(self).__name__ == "RadialGradient":
            from .radial import RadialGradient

            return RadialGradient(self.engine, tvg_gradient)
        else:
            raise TypeError(f"Unknown Gradient class {type(self).__name__}")

    def _del(self) -> Result:
        """Deletes the given gradient object.

        :return: Result.INVALID_ARGUMENT An invalid GradientPointer.
        :rtype: thorvg_python.base.Result
        """
        self.thorvg_lib.tvg_gradient_del.argtypes = [GradientPointer]
        self.thorvg_lib.tvg_gradient_del.restype = Result
        return self.thorvg_lib.tvg_gradient_del(self._grad)
