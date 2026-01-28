#!/usr/bin/env python3
import ctypes
from typing import Optional, Tuple

from ..base import (
    BlendMethod,
    CompositeMethod,
    Identifier,
    Matrix,
    PaintStruct,
    Result,
    TvgType,
)
from ..engine import Engine


class Paint:
    """
    Paint API

    A module for managing graphical elements. It enables duplication, transformation and composition.

    This is base Paint class. Please instantiate with Shape, Picture, Scene or Text instead.
    """

    def __init__(self, engine: Engine, paint: PaintStruct):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        self._paint = paint

    def _del(self) -> Result:
        """Releases the given PaintStruct object.

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.

        .. warning::
            If this function is used, tvg_canvas_clear() with the ``free`` argument value set to ``false`` should be used in order to avoid unexpected behaviours.

        .. seealso:: Canvas.clear(), Canvas.destroy()
        """
        self.thorvg_lib.tvg_paint_del.argtypes = [
            ctypes.POINTER(PaintStruct),
        ]
        self.thorvg_lib.tvg_paint_del.restype = Result
        return self.thorvg_lib.tvg_paint_del(
            ctypes.pointer(self._paint),
        )

    def scale(self, factor: float) -> Result:
        """Scales the given PaintStruct object by the given factor.

        :param float factor: The value of the scaling factor. The default value is 1.

        :return:
            - INVALID_ARGUMENT An invalid PaintStruct pointer.
            - INSUFFICIENT_CONDITION in case a custom transform is applied.
        :rtype: Result

        .. seealso:: Paint.set_transform()
        """
        self.thorvg_lib.tvg_paint_scale.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_paint_scale.restype = Result
        return self.thorvg_lib.tvg_paint_scale(
            ctypes.pointer(self._paint),
            ctypes.c_float(factor),
        )

    def rotate(
        self,
        degree: float,
    ) -> Result:
        """Rotates the given PaintStruct by the given angle.

        The angle in measured clockwise from the horizontal axis.
        The rotational axis passes through the point on the object with zero coordinates.

        :param float degree: The value of the rotation angle in degrees.

        :return:
            - INVALID_ARGUMENT An invalid PaintStruct pointer.
            - INSUFFICIENT_CONDITION in case a custom transform is applied.
        :rtype: Result

        .. seealso:: Paint.set_transform()
        """
        self.thorvg_lib.tvg_paint_rotate.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_paint_rotate.restype = Result
        return self.thorvg_lib.tvg_paint_rotate(
            ctypes.pointer(self._paint),
            ctypes.c_float(degree),
        )

    def translate(
        self,
        x: float,
        y: float,
    ) -> Result:
        """Moves the given PaintStruct in a two-dimensional space.

        The origin of the coordinate system is in the upper-left corner of the canvas.
        The horizontal and vertical axes point to the right and down, respectively.

        :param float x: The value of the horizontal shift.
        :param float y: The value of the vertical shift.

        :return:
            - INVALID_ARGUMENT An invalid PaintStruct pointer.
            - INSUFFICIENT_CONDITION in case a custom transform is applied.
        :rtype: Result

        .. seealso:: Paint.set_transform()
        """
        self.thorvg_lib.tvg_paint_translate.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_paint_translate.restype = Result
        return self.thorvg_lib.tvg_paint_translate(
            ctypes.pointer(self._paint),
            ctypes.c_float(x),
            ctypes.c_float(y),
        )

    def set_transform(
        self,
        m: Matrix,
    ) -> Result:
        """Transforms the given PaintStruct using the augmented transformation matrix.

        The augmented matrix of the transformation is expected to be given.

        :param Matrix m: The 3x3 augmented matrix.

        :return: INVALID_ARGUMENT A ``nullptr`` is passed as the argument.
        :rtype: Result
        """
        self.thorvg_lib.tvg_paint_set_transform.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(Matrix),
        ]
        self.thorvg_lib.tvg_paint_set_transform.restype = Result
        return self.thorvg_lib.tvg_paint_set_transform(
            ctypes.pointer(self._paint),
            ctypes.pointer(m),
        )

    def get_transform(
        self,
    ) -> Tuple[Result, Matrix]:
        """Gets the matrix of the affine transformation of the given PaintStruct object.

        In case no transformation was applied, the identity matrix is returned.

        :return: INVALID_ARGUMENT A ``nullptr`` is passed as the argument.
        :rtype: Result
        :return: The 3x3 augmented matrix.
        :rtype: Matrix
        """
        m = Matrix()
        self.thorvg_lib.tvg_paint_get_transform.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(Matrix),
        ]
        self.thorvg_lib.tvg_paint_get_transform.restype = Result
        result = self.thorvg_lib.tvg_paint_get_transform(
            ctypes.pointer(self._paint),
            ctypes.pointer(m),
        )
        return result, m

    def set_opacity(
        self,
        opacity: int,
    ) -> Result:
        """Sets the opacity of the given PaintStruct.

        :param int opacity: The opacity value in the range [0 ~ 255], where 0 is completely transparent and 255 is opaque.

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result

        .. note::
            Setting the opacity with this API may require multiple renderings using a composition.
            It is recommended to avoid changing the opacity if possible.
        """
        self.thorvg_lib.tvg_paint_set_opacity.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_uint8,
        ]
        self.thorvg_lib.tvg_paint_set_opacity.restype = Result
        return self.thorvg_lib.tvg_paint_set_opacity(
            ctypes.pointer(self._paint),
            ctypes.c_uint8(opacity),
        )

    def get_opacity(
        self,
    ) -> Tuple[Result, int]:
        """Gets the opacity of the given PaintStruct.

        :return: INVALID_ARGUMENT In case a ``nullptr`` is passed as the argument.
        :rtype: Result
        :return: The opacity value in the range [0 ~ 255], where 0 is completely transparent and 255 is opaque.
        :rtype: int
        """
        opacity = ctypes.c_uint8()
        self.thorvg_lib.tvg_paint_get_opacity.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.c_uint8),
        ]
        self.thorvg_lib.tvg_paint_get_opacity.restype = Result
        result = self.thorvg_lib.tvg_paint_get_opacity(
            ctypes.pointer(self._paint),
            ctypes.pointer(opacity),
        )
        return result, opacity.value

    def duplicate(
        self,
    ) -> Optional[PaintStruct]:
        """Duplicates the given PaintStruct object.

        Creates a new object and sets its all properties as in the original object.

        :return: A copied PaintStruct object if succeed, ``nullptr`` otherwise.
        :rtype: Optional[PaintStruct]
        """
        self.thorvg_lib.tvg_paint_duplicate.argtypes = [
            ctypes.POINTER(PaintStruct),
        ]
        self.thorvg_lib.tvg_paint_duplicate.restype = ctypes.POINTER(PaintStruct)
        return self.thorvg_lib.tvg_paint_duplicate(
            ctypes.pointer(self._paint),
        ).contents

    def get_bounds(
        self,
        transformed: bool = False,
    ) -> Tuple[Result, float, float, float, float]:
        """Gets the axis-aligned bounding box of the PaintStruct object.

        :param bool transformed: If ``true``, the paint's transformations are taken into account in the scene it belongs to. Otherwise they aren't.

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result
        :return: The x-coordinate of the upper-left corner of the object.
        :rtype: float
        :return: The y-coordinate of the upper-left corner of the object.
        :rtype: float
        :return: The width of the object.
        :rtype: float
        :return: The height of the object.
        :rtype: float

        .. note::
            This is useful when you need to figure out the bounding box of the paint in the canvas space.
        .. note::
            The bounding box doesn't indicate the actual drawing region. It's the smallest rectangle that encloses the object.
        .. note::
            If ``transformed`` is ``true``, the paint needs to be pushed into a canvas and updated before this api is called.
        .. seealso:: Canvas.update_paint()
        """
        x = ctypes.c_float(0.0)
        y = ctypes.c_float(0.0)
        w = ctypes.c_float(0.0)
        h = ctypes.c_float(0.0)
        self.thorvg_lib.tvg_paint_get_bounds.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.c_bool,
        ]
        self.thorvg_lib.tvg_paint_get_bounds.restype = Result
        result = self.thorvg_lib.tvg_paint_get_bounds(
            ctypes.pointer(self._paint),
            ctypes.pointer(x),
            ctypes.pointer(y),
            ctypes.pointer(w),
            ctypes.pointer(h),
            ctypes.c_bool(transformed),
        )
        return result, x.value, y.value, w.value, h.value

    def set_composite_method(
        self,
        target: "Paint",
        method: CompositeMethod,
    ) -> Result:
        """Sets the composition target object and the composition method.

        :param Paint target: The target object of the composition.
        :param CompositeMethod method: The method used to composite the source object with the target.

        :return: INVALID_ARGUMENT An invalid ``paint`` or ``target`` object or the ``method`` equal to NONE.
        :rtype: Result
        """
        self.thorvg_lib.tvg_paint_set_composite_method.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(PaintStruct),
            ctypes.c_int,
        ]
        self.thorvg_lib.tvg_paint_set_composite_method.restype = Result
        return self.thorvg_lib.tvg_paint_set_composite_method(
            ctypes.pointer(self._paint), ctypes.pointer(target._paint), method
        )

    def get_composite_method(
        self,
    ) -> Tuple[Result, PaintStruct, CompositeMethod]:
        """Gets the composition target object and the composition method.

        :return: INVALID_ARGUMENT A ``nullptr`` is passed as the argument.
        :rtype: Result
        :return: The target object of the composition.
        :rtype: PaintStruct
        :return: The method used to composite the source object with the target.
        :rtype: CompositeMethod
        """
        target = PaintStruct()
        method = ctypes.c_int()
        self.thorvg_lib.tvg_paint_get_composite_method.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.POINTER(PaintStruct)),
            ctypes.POINTER(ctypes.c_int),
        ]
        self.thorvg_lib.tvg_paint_get_composite_method.restype = Result
        result = self.thorvg_lib.tvg_paint_get_composite_method(
            ctypes.pointer(self._paint),
            ctypes.pointer(ctypes.pointer(target)),
            ctypes.pointer(method),
        )
        return result, target, CompositeMethod(method.value)

    def set_clip(self, clipper: "Paint") -> Result:
        """Clip the drawing region of the paint object.

        This function restricts the drawing area of the paint object to the specified shape's paths.

        :param Paint clipper: The shape object as the clipper.

        :return:
            - INVALID_ARGUMENT In case a ``nullptr`` is passed as the argument.
            - NOT_SUPPORTED If the ``clipper`` type is not Shape.
        :rtype: Result

        .. note::
            Experimental API
        """
        self.thorvg_lib.tvg_paint_set_clip.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(PaintStruct),
        ]
        self.thorvg_lib.tvg_paint_set_clip.restype = Result
        return self.thorvg_lib.tvg_paint_set_clip(
            ctypes.pointer(self._paint),
            ctypes.pointer(clipper._paint),
        )

    def get_type(self) -> Tuple[Result, TvgType]:
        """
        Gets the unique value of the paint instance indicating the instance type.

        :return: INVALID_ARGUMENT In case a ``nullptr`` is passed as the argument.
        :rtype: Result
        :return: The unique type of the paint instance type.
        :rtype: TvgType

        .. note::
            Experimental API
        """
        _type = ctypes.c_int()
        self.thorvg_lib.tvg_paint_get_type.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.c_int),
        ]
        self.thorvg_lib.tvg_paint_get_type.restype = Result
        result = self.thorvg_lib.tvg_paint_get_type(
            ctypes.pointer(self._paint),
            ctypes.pointer(_type),
        )
        return result, TvgType(_type.value)

    def get_identifier(self) -> Tuple[Result, Identifier]:
        """
        .. deprecated:: 0.15

        .. seealso:: Paint.get_type()
        """
        identifier = ctypes.c_int()
        self.thorvg_lib.tvg_paint_get_identifier.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.c_int),
        ]
        self.thorvg_lib.tvg_paint_get_identifier.restype = Result
        result = self.thorvg_lib.tvg_paint_get_identifier(
            ctypes.pointer(self._paint),
            ctypes.pointer(identifier),
        )
        return result, Identifier(identifier.value)

    def set_blend_method(self, method: BlendMethod) -> Result:
        """Sets the blending method for the paint object.

        The blending feature allows you to combine colors to create visually appealing effects, including transparency, lighting, shading, and color mixing, among others.
        its process involves the combination of colors or images from the source paint object with the destination (the lower layer image) using blending operations.
        The blending operation is determined by the chosen ``BlendMethod``, which specifies how the colors or images are combined.

        :param BlendMethod method: The blending method to be set.

        :return: INVALID_ARGUMENT In case a ``nullptr`` is passed as the argument.
        :rtype: Result

        .. versionadded:: 0.15
        """
        self.thorvg_lib.tvg_paint_set_blend_method.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_int,
        ]
        self.thorvg_lib.tvg_paint_set_blend_method.restype = Result
        return self.thorvg_lib.tvg_paint_set_blend_method(
            ctypes.pointer(self._paint),
            method,
        )
