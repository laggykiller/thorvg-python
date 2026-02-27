#!/usr/bin/env python3
import ctypes
from typing import Optional, Tuple

from ..base import (
    BlendMethod,
    MaskMethod,
    Matrix,
    PaintPointer,
    PointStruct,
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

    def __init__(self, engine: Engine, paint: PaintPointer):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        self._paint = paint

    def _rel(self) -> Result:
        """Safely releases a Tv_Paint object.

        This is the counterpart to the ``new()`` API, and releases the given Paint object safely,
        handling ``None`` and managing ownership properly.

        :param PaintPointer paint: A PaintPointer object to release.
        """
        self.thorvg_lib.tvg_paint_rel.argtypes = [
            PaintPointer,
        ]
        self.thorvg_lib.tvg_paint_rel.restype = Result
        return self.thorvg_lib.tvg_paint_rel(
            self._paint,
        )

    def ref(self) -> int:
        """Increment the reference count for the PaintPointer object.

        This method increases the reference count of PaintPointer object, allowing shared ownership and control over its lifetime.

        :return: The updated reference count after the increment by 1.
        :rtype: int

        .. warning::
            Please ensure that each call to Paint.ref() is paired with a corresponding call to Paint.unref() to prevent a dangling instance.

        .. seealso:: Paint.unref()
        .. seealso:: Paint.get_ref()

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_paint_ref.argtypes = [
            PaintPointer,
        ]
        self.thorvg_lib.tvg_paint_ref.restype = ctypes.c_uint16
        return self.thorvg_lib.tvg_paint_ref(
            self._paint,
        ).value

    def deref(self, free: bool) -> int:
        """Decrement the reference count for the PaintPointer object.

        This method decreases the reference count of the PaintPointer object by 1.
        If the reference count reaches zero and the ``free`` flag is set to true, the instance is automatically deleted.

        :param bool free: Flag indicating whether to delete the Paint instance when the reference count reaches zero.

        :return: The updated reference count after the decrement.
        :rtype: int

        .. seealso:: Paint.ref()
        .. seealso:: Paint.get_ref()

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_paint_deref.argtypes = [
            PaintPointer,
            ctypes.c_bool,
        ]
        self.thorvg_lib.tvg_paint_deref.restype = ctypes.c_uint16
        return self.thorvg_lib.tvg_paint_deref(self._paint, ctypes.c_bool(free)).value

    def get_ref(self) -> int:
        """Retrieve the current reference count of the PaintPointer object.

        This method provides the current reference count, allowing the user to check the shared ownership state of the PaintPointer object.

        :return: The current reference count of the PaintPointer object.
        :rtype: int

        .. seealso:: Paint.ref()
        .. seealso:: Paint.unref()

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_paint_get_ref.argtypes = [
            PaintPointer,
        ]
        self.thorvg_lib.tvg_paint_get_ref.restype = ctypes.c_uint16
        return self.thorvg_lib.tvg_paint_get_ref(
            self._paint,
        ).value

    def set_visible(self, visible: bool) -> Result:
        """Sets the visibility of the Paint object.

        This is useful for selectively excluding paint objects during rendering.

        :param bool visible: A boolean flag indicating visibility. The default is ``true``.
            - ``true``: the object will be rendered by the engine.
            - ``false``: the object will be excluded from the drawing process.

        .. note::
            An invisible object is not considered inactive—it may still participate
            in internal update processing if its properties are updated, but it will not
            be taken into account for the final drawing output. To completely deactivate
            a paint object, remove it from the canvas.

        .. seealso:: Paint.get_visible()
        .. seealso:: Canvas.remove()

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_paint_set_visible.argtypes = [
            PaintPointer,
            ctypes.c_bool,
        ]
        self.thorvg_lib.tvg_paint_set_visible.restype = Result
        return self.thorvg_lib.tvg_paint_set_visible(
            self._paint, ctypes.c_bool(visible)
        )

    def get_visible(self, visible: bool) -> Result:
        """Sets the visibility of the Paint object.

        This is useful for selectively excluding paint objects during rendering.

        :param bool visible: A boolean flag indicating visibility. The default is ``true``.
            - ``true``: the object will be rendered by the engine.
            - ``false``: the object will be excluded from the drawing process.

        .. note::
            An invisible object is not considered inactive—it may still participate
            in internal update processing if its properties are updated, but it will not
            be taken into account for the final drawing output. To completely deactivate
            a paint object, remove it from the canvas.

        .. seealso:: Paint.get_visible()
        .. seealso:: Canvas.remove()

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_paint_get_visible.argtypes = [
            PaintPointer,
        ]
        self.thorvg_lib.tvg_paint_get_visible.restype = ctypes.c_bool
        return self.thorvg_lib.tvg_paint_get_visible(
            self._paint,
        ).value

    def scale(self, factor: float) -> Result:
        """Scales the given PaintPointer object by the given factor.

        :param float factor: The value of the scaling factor. The default value is 1.

        :return:
            - Result.INVALID_ARGUMENT An invalid PaintPointer.
            - Result.INSUFFICIENT_CONDITION in case a custom transform is applied.
        :rtype: Result

        .. seealso:: Paint.set_transform()
        """
        self.thorvg_lib.tvg_paint_scale.argtypes = [
            PaintPointer,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_paint_scale.restype = Result
        return self.thorvg_lib.tvg_paint_scale(
            self._paint,
            ctypes.c_float(factor),
        )

    def rotate(
        self,
        degree: float,
    ) -> Result:
        """Rotates the given PaintPointer by the given angle.

        The angle in measured clockwise from the horizontal axis.
        The rotational axis passes through the point on the object with zero coordinates.

        :param float degree: The value of the rotation angle in degrees.

        :return:
            - Result.INVALID_ARGUMENT An invalid PaintPointer.
            - Result.INSUFFICIENT_CONDITION in case a custom transform is applied.
        :rtype: Result

        .. seealso:: Paint.set_transform()
        """
        self.thorvg_lib.tvg_paint_rotate.argtypes = [
            PaintPointer,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_paint_rotate.restype = Result
        return self.thorvg_lib.tvg_paint_rotate(
            self._paint,
            ctypes.c_float(degree),
        )

    def translate(
        self,
        x: float,
        y: float,
    ) -> Result:
        """Moves the given PaintPointer in a two-dimensional space.

        The origin of the coordinate system is in the upper-left corner of the canvas.
        The horizontal and vertical axes point to the right and down, respectively.

        :param float x: The value of the horizontal shift.
        :param float y: The value of the vertical shift.

        :return:
            - Result.INVALID_ARGUMENT An invalid PaintPointer.
            - Result.INSUFFICIENT_CONDITION in case a custom transform is applied.
        :rtype: Result

        .. seealso:: Paint.set_transform()
        """
        self.thorvg_lib.tvg_paint_translate.argtypes = [
            PaintPointer,
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_paint_translate.restype = Result
        return self.thorvg_lib.tvg_paint_translate(
            self._paint,
            ctypes.c_float(x),
            ctypes.c_float(y),
        )

    def set_transform(
        self,
        m: Matrix,
    ) -> Result:
        """Transforms the given PaintPointer using the augmented transformation matrix.

        The augmented matrix of the transformation is expected to be given.

        :param Matrix m: The 3x3 augmented matrix.

        :return: Result.INVALID_ARGUMENT A ``None`` is passed as the argument.
        :rtype: Result
        """
        self.thorvg_lib.tvg_paint_set_transform.argtypes = [
            PaintPointer,
            ctypes.POINTER(Matrix),
        ]
        self.thorvg_lib.tvg_paint_set_transform.restype = Result
        return self.thorvg_lib.tvg_paint_set_transform(
            self._paint,
            ctypes.pointer(m),
        )

    def get_transform(
        self,
    ) -> Tuple[Result, Matrix]:
        """Gets the matrix of the affine transformation of the given PaintPointer object.

        In case no transformation was applied, the identity matrix is returned.

        :return: Result.INVALID_ARGUMENT A ``None`` is passed as the argument.
        :rtype: Result
        :return: The 3x3 augmented matrix.
        :rtype: Matrix
        """
        m = Matrix()
        self.thorvg_lib.tvg_paint_get_transform.argtypes = [
            PaintPointer,
            ctypes.POINTER(Matrix),
        ]
        self.thorvg_lib.tvg_paint_get_transform.restype = Result
        result = self.thorvg_lib.tvg_paint_get_transform(
            self._paint,
            ctypes.pointer(m),
        )
        return result, m

    def set_opacity(
        self,
        opacity: int,
    ) -> Result:
        """Sets the opacity of the given PaintPointer.

        :param int opacity: The opacity value in the range [0 ~ 255], where 0 is completely transparent and 255 is opaque.

        :return: Result.INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: Result

        .. note::
            Setting the opacity with this API may require multiple renderings using a composition.
            It is recommended to avoid changing the opacity if possible.
        """
        self.thorvg_lib.tvg_paint_set_opacity.argtypes = [
            PaintPointer,
            ctypes.c_uint8,
        ]
        self.thorvg_lib.tvg_paint_set_opacity.restype = Result
        return self.thorvg_lib.tvg_paint_set_opacity(
            self._paint,
            ctypes.c_uint8(opacity),
        )

    def get_opacity(
        self,
    ) -> Tuple[Result, int]:
        """Gets the opacity of the given PaintPointer.

        :return: Result.INVALID_ARGUMENT In case a ``None`` is passed as the argument.
        :rtype: Result
        :return: The opacity value in the range [0 ~ 255], where 0 is completely transparent and 255 is opaque.
        :rtype: int
        """
        opacity = ctypes.c_uint8()
        self.thorvg_lib.tvg_paint_get_opacity.argtypes = [
            PaintPointer,
            ctypes.POINTER(ctypes.c_uint8),
        ]
        self.thorvg_lib.tvg_paint_get_opacity.restype = Result
        result = self.thorvg_lib.tvg_paint_get_opacity(
            self._paint,
            ctypes.pointer(opacity),
        )
        return result, opacity.value

    def duplicate(
        self,
    ) -> Optional[PaintPointer]:
        """Duplicates the given PaintPointer object.

        Creates a new object and sets its all properties as in the original object.

        :return: A copied PaintPointer object if succeed, ``None`` otherwise.
        :rtype: Optional[PaintPointer]
        """
        self.thorvg_lib.tvg_paint_duplicate.argtypes = [
            PaintPointer,
        ]
        self.thorvg_lib.tvg_paint_duplicate.restype = PaintPointer
        return self.thorvg_lib.tvg_paint_duplicate(
            self._paint,
        )

    def intersects(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
    ) -> bool:
        """Checks whether a given region intersects the filled area of the paint.

        This function determines whether the specified rectangular region—defined by (`x`, `y`, `w`, `h`)—
        intersects the geometric fill region of the paint object.

        This is useful for hit-testing purposes, such as detecting whether a user interaction (e.g., touch or click)
        occurs within a painted region.

        The paint must be updated in a Canvas beforehand—typically after the Canvas has been
        drawn and synchronized.

        :param int x: The x-coordinate of the top-left corner of the test region.
        :param int y: The y-coordinate of the top-left corner of the test region.
        :param int w: The width of the region to test. Must be greater than 0; defaults to 1.
        :param int h: The height of the region to test. Must be greater than 0; defaults to 1.

        :return: ``true`` if any part of the region intersects the filled area; otherwise, ``false``.

        .. note::
            To test a single point, set the region size to w = 1, h = 1.
        .. note::
            For efficiency, an AABB (axis-aligned bounding box) test is performed internally before precise hit detection.
        .. note::
            This test does not take into account the results of blending or masking.
        .. note::
            This test does take into account the the hidden paints as well. See ``Paint.set_visible()``.
        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_paint_intersects.argtypes = [
            PaintPointer,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
        ]
        self.thorvg_lib.tvg_paint_intersects.restype = PaintPointer
        return self.thorvg_lib.tvg_paint_intersects(
            self._paint,
            ctypes.c_int32(x),
            ctypes.c_int32(y),
            ctypes.c_int32(w),
            ctypes.c_int32(h),
        )

    def get_aabb(self) -> Tuple[Result, float, float, float, float]:
        """Retrieves the axis-aligned bounding box (AABB) of the paint object in canvas space.

        Returns the bounding box of the paint as an axis-aligned bounding box (AABB), with all relevant transformations applied.
        The returned values ``x``, ``y``, ``w``, ``h``, may have invalid if the operation fails. Thus, please check the retval.

        This bounding box can be used to determine the actual rendered area of the object on the canvas,
        for purposes such as hit-testing, culling, or layout calculations.

        :return:
            - Result.INVALID_ARGUMENT An invalid ``paint``.
            - Result.INSUFFICIENT_CONDITION If it failed to compute the bounding box (mostly due to invalid path information).
        :rtype: Result
        :return: The x-coordinate of the upper-left corner of the bounding box.
        :rtype: float
        :return: The y-coordinate of the upper-left corner of the bounding box.
        :rtype: float
        :return: The width of the bounding box.
        :rtype: float
        :return: The height of the bounding box.
        :rtype: float

        .. seealso:: Paint.get_obb()
        .. seealso:: Canvas.update()
        """
        x = ctypes.c_float()
        y = ctypes.c_float()
        w = ctypes.c_float()
        h = ctypes.c_float()
        self.thorvg_lib.tvg_paint_get_aabb.argtypes = [
            PaintPointer,
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
        ]
        self.thorvg_lib.tvg_paint_get_aabb.restype = PaintPointer
        result = self.thorvg_lib.tvg_paint_get_aabb(
            self._paint,
            ctypes.pointer(x),
            ctypes.pointer(y),
            ctypes.pointer(w),
            ctypes.pointer(h),
        )
        return result, x.value, y.value, w.value, h.value

    def get_obb(self) -> Tuple[Result, PointStruct]:
        """Retrieves the object-oriented bounding box (OBB) of the paint object in canvas space.

        This function returns the bounding box of the paint, as an oriented bounding box (OBB) after transformations are applied.
        The returned values ``pt4`` may have invalid if the operation fails. Thus, please check the retval.

        This bounding box can be used to obtain the transformed bounding region in canvas space
        by taking the geometry's axis-aligned bounding box (AABB) in the object's local coordinate space
        and applying the object's transformations.

        :return:
            - Result.INVALID_ARGUMENT ``paint`` or ``pt4`` is invalid.
            - Result.INSUFFICIENT_CONDITION If it failed to compute the bounding box (mostly due to invalid path information).
        :rtype: Result
        :return: An array of four points representing the bounding box. The array size must be 4.
        :rtype: PointStruct

        .. seealso:: Paint.get_aabb()
        .. seealso:: Canvas.update()

        .. versionadded:: 1.0
        """
        pt4 = PointStruct()
        self.thorvg_lib.tvg_paint_get_aabb.argtypes = [
            PaintPointer,
            ctypes.POINTER(PointStruct),
        ]
        self.thorvg_lib.tvg_paint_get_aabb.restype = PaintPointer
        result = self.thorvg_lib.tvg_paint_get_aabb(
            self._paint,
            ctypes.pointer(pt4),
        )
        return result, pt4

    def set_mask_method(
        self,
        target: "Paint",
        method: MaskMethod,
    ) -> Result:
        """Sets the masking target object and the masking method.

        :param Paint target: The target object of the masking.
        :param MaskMethod method: The method used to mask the source object with the target.

        :return: Result.INSUFFICIENT_CONDITION if the target has already belonged to another paint.
        :rtype: Result
        """
        self.thorvg_lib.tvg_paint_set_mask_method.argtypes = [
            PaintPointer,
            PaintPointer,
            ctypes.c_int,
        ]
        self.thorvg_lib.tvg_paint_set_mask_method.restype = Result
        return self.thorvg_lib.tvg_paint_set_mask_method(
            self._paint, target._paint, method
        )

    def get_mask_method(self, target: "Paint") -> Tuple[Result, MaskMethod]:
        """Gets the masking target object and the masking method.

        :return: Result.INVALID_ARGUMENT A ``None`` is passed as the argument.
        :rtype: Result
        :return: The method used to mask the source object with the target.
        :rtype: MaskMethod
        """
        method = ctypes.c_int()
        self.thorvg_lib.tvg_paint_get_mask_method.argtypes = [
            PaintPointer,
            PaintPointer,
            ctypes.POINTER(ctypes.c_int),
        ]
        self.thorvg_lib.tvg_paint_get_mask_method.restype = Result
        result = self.thorvg_lib.tvg_paint_get_mask_method(
            self._paint,
            target._paint,
            ctypes.pointer(method),
        )
        return result, MaskMethod(method.value)

    def set_clip(self, clipper: "Paint") -> Result:
        """Clip the drawing region of the paint object.

        This function restricts the drawing area of the paint object to the specified shape's paths.

        :param Paint clipper: The shape object as the clipper.

        :return:
            - Result.INVALID_ARGUMENT In case a ``None`` is passed as the argument.
            - Result.NOT_SUPPORTED If the ``clipper`` type is not Shape.
        :rtype: Result
        """
        self.thorvg_lib.tvg_paint_set_clip.argtypes = [
            PaintPointer,
            PaintPointer,
        ]
        self.thorvg_lib.tvg_paint_set_clip.restype = Result
        return self.thorvg_lib.tvg_paint_set_clip(
            self._paint,
            clipper._paint,
        )

    def get_clip(self) -> "Optional[Paint]":
        """Get the clipper shape of the paint object.

        This function returns the clipper that has been previously set to this paint object.

        :return: The shape object used as the clipper, or ``None`` if no clipper is set.
        :rtype: Optional[Paint]

        .. seealso:: Paint.set_clip()

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_paint_get_clip.argtypes = [
            PaintPointer,
        ]
        self.thorvg_lib.tvg_paint_get_clip.restype = PaintPointer
        clipper = self.thorvg_lib.tvg_paint_get_clip(self._paint)
        if clipper is not ctypes.c_void_p():
            return Paint(self.engine, clipper)
        else:
            return None

    def get_parent(self) -> "Optional[Paint]":
        """Retrieves the parent paint object.

        This function returns a pointer to the parent object if the current paint
        belongs to one. Otherwise, it returns ``None``.

        :return: The parent object if available, otherwise ``None``.
        :rtype: Optional[Paint]

        .. seealso:: Scene.add()
        .. seealso:: Canvas.add()

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_paint_get_parent.argtypes = [
            PaintPointer,
        ]
        self.thorvg_lib.tvg_paint_get_parent.restype = PaintPointer
        parent = self.thorvg_lib.tvg_paint_get_parent(self._paint)
        if isinstance(ctypes.c_void_p, parent):
            return None
        else:
            return Paint(self.engine, parent)

    def get_type(self) -> Tuple[Result, TvgType]:
        """
        Gets the unique value of the paint instance indicating the instance type.

        :return: Result.INVALID_ARGUMENT In case a ``None`` is passed as the argument.
        :rtype: Result
        :return: The unique type of the paint instance type.
        :rtype: TvgType
        """
        _type = ctypes.c_int()
        self.thorvg_lib.tvg_paint_get_type.argtypes = [
            PaintPointer,
            ctypes.POINTER(ctypes.c_int),
        ]
        self.thorvg_lib.tvg_paint_get_type.restype = Result
        result = self.thorvg_lib.tvg_paint_get_type(
            self._paint,
            ctypes.pointer(_type),
        )
        return result, TvgType(_type.value)

    def set_blend_method(self, method: BlendMethod) -> Result:
        """Sets the blending method for the paint object.

        The blending feature allows you to combine colors to create visually appealing effects, including transparency, lighting, shading, and color mixing, among others.
        its process involves the combination of colors or images from the source paint object with the destination (the lower layer image) using blending operations.
        The blending operation is determined by the chosen ``BlendMethod``, which specifies how the colors or images are combined.

        :param BlendMethod method: The blending method to be set.

        :return: Result.INVALID_ARGUMENT In case a ``None`` is passed as the argument.
        :rtype: Result

        .. versionadded:: 0.15
        """
        self.thorvg_lib.tvg_paint_set_blend_method.argtypes = [
            PaintPointer,
            ctypes.c_int,
        ]
        self.thorvg_lib.tvg_paint_set_blend_method.restype = Result
        return self.thorvg_lib.tvg_paint_set_blend_method(
            self._paint,
            method,
        )
