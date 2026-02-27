#!/usr/bin/env python3
import ctypes
from typing import Optional, Sequence, Tuple, Union

from ..base import (
    FillRule,
    GradientPointer,
    PaintPointer,
    PathCommand,
    PointStruct,
    Result,
    StrokeCap,
    StrokeJoin,
    TvgType,
)
from ..engine import Engine
from ..gradient import Gradient
from ..gradient.linear import LinearGradient
from ..gradient.radial import RadialGradient
from . import Paint


class Shape(Paint):
    """
    Shape API

    A module for managing two-dimensional figures and their properties.

    A shape has three major properties: shape outline, stroking, filling. The outline in the shape is retained as the path.
    Path can be composed by accumulating primitive commands such as Shape.move_to(), Shape.line_to(), Shape.cubic_to() or complete shape interfaces such as Shape.append_rect(), Shape.append_circle(), etc.
    Path can consists of sub-paths. One sub-path is determined by a close command.

    The stroke of a shape is an optional property in case the shape needs to be represented with/without the outline borders.
    It's efficient since the shape path and the stroking path can be shared with each other. It's also convenient when controlling both in one context.
    """

    def __init__(self, engine: Engine, paint: Optional[PaintPointer] = None):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if paint is None:
            self._paint = self._new()
        else:
            self._paint = paint

    def _new(self) -> PaintPointer:
        """Creates a new shape object.

        Note that you need not call this method as it is auto called when initializing ``Shape()``.

        :return: A new shape object.
        :rtype: thorvg_python.base.PaintPointer
        """
        self.thorvg_lib.tvg_shape_new.restype = PaintPointer
        return self.thorvg_lib.tvg_shape_new()

    def reset(self) -> Result:
        """Resets the shape path properties.

        The color, the fill and the stroke properties are retained.

        :return: Result.INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: thorvg_python.base.Result

        .. note::
            The memory, where the path data is stored, is not deallocated at this stage for caching effect.
        """
        self.thorvg_lib.tvg_shape_reset.argtypes = [PaintPointer]
        self.thorvg_lib.tvg_shape_reset.restype = Result
        return self.thorvg_lib.tvg_shape_reset(self._paint)

    def move_to(self, x: float, y: float) -> Result:
        """Sets the initial point of the sub-path.

        The value of the current point is set to the given point.

        :param float x: The horizontal coordinate of the initial point of the sub-path.
        :param float y: The vertical coordinate of the initial point of the sub-path.

        :return: Result.INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: thorvg_python.base.Result
        """
        self.thorvg_lib.tvg_shape_move_to.argtypes = [
            PaintPointer,
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_shape_move_to.restype = Result
        return self.thorvg_lib.tvg_shape_move_to(
            self._paint,
            ctypes.c_float(x),
            ctypes.c_float(y),
        )

    def line_to(self, x: float, y: float) -> Result:
        """Adds a new point to the sub-path, which results in drawing a line from
        the current point to the given end-point.

        The value of the current point is set to the given end-point.

        :param float x: The horizontal coordinate of the end-point of the line.
        :param float y: The vertical coordinate of the end-point of the line.

        :return: Result.INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: thorvg_python.base.Result

        .. note::
            In case this is the first command in the path, it corresponds to the Shape.move_to() call.
        """
        self.thorvg_lib.tvg_shape_line_to.argtypes = [
            PaintPointer,
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_shape_line_to.restype = Result
        return self.thorvg_lib.tvg_shape_line_to(
            self._paint,
            ctypes.c_float(x),
            ctypes.c_float(y),
        )

    def cubic_to(
        self,
        cx1: float,
        cy1: float,
        cx2: float,
        cy2: float,
        x: float,
        y: float,
    ) -> Result:
        """Adds new points to the sub-path, which results in drawing a cubic Bezier curve.

        The Bezier curve starts at the current point and ends at the given end-point (``x``, ``y``).
        Two control points (``cx1``, ``cy1``) and (``cx2``, ``cy2``) are used to determine the shape of the curve.
        The value of the current point is set to the given end-point.

        :param float cx1: The horizontal coordinate of the 1st control point.
        :param float cy1: The vertical coordinate of the 1st control point.
        :param float cx2: The horizontal coordinate of the 2nd control point.
        :param float cy2: The vertical coordinate of the 2nd control point.
        :param float x: The horizontal coordinate of the endpoint of the curve.
        :param float y: The vertical coordinate of the endpoint of the curve.

        :return: Result.INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: thorvg_python.base.Result

        .. note::
            In case this is the first command in the path, no data from the path are rendered.
        """
        self.thorvg_lib.tvg_shape_cubic_to.argtypes = [
            PaintPointer,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_shape_cubic_to.restype = Result
        return self.thorvg_lib.tvg_shape_cubic_to(
            self._paint,
            ctypes.c_float(cx1),
            ctypes.c_float(cy1),
            ctypes.c_float(cx2),
            ctypes.c_float(cy2),
            ctypes.c_float(x),
            ctypes.c_float(y),
        )

    def close(
        self,
    ) -> Result:
        """Closes the current sub-path by drawing a line from the current point to the initial point of the sub-path.

        The value of the current point is set to the initial point of the closed sub-path.

        :return: Result.INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: thorvg_python.base.Result

        .. note::
            In case the sub-path does not contain any points, this function has no effect.
        """
        self.thorvg_lib.tvg_shape_close.argtypes = [
            PaintPointer,
        ]
        self.thorvg_lib.tvg_shape_close.restype = Result
        return self.thorvg_lib.tvg_shape_close(
            self._paint,
        )

    def append_rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        rx: float,
        ry: float,
        cw: bool,
    ) -> Result:
        """Appends a rectangle to the path.

        The rectangle with rounded corners can be achieved by setting non-zero values to ``rx`` and ``ry`` arguments.
        The ``rx`` and ``ry`` values specify the radii of the ellipse defining the rounding of the corners.

        The position of the rectangle is specified by the coordinates of its upper-left corner -  ``x`` and ``y`` arguments.

        The rectangle is treated as a new sub-path - it is not connected with the previous sub-path.

        The value of the current point is set to (``x`` + ``rx``, ``y``) - in case ``rx`` is greater
        than ``w/2`` the current point is set to (``x`` +  ``w/2``, ``y``)

        :param float x: The horizontal coordinate of the upper-left corner of the rectangle.
        :param float y: The vertical coordinate of the upper-left corner of the rectangle.
        :param float w: The width of the rectangle.
        :param float h: The height of the rectangle.
        :param float rx: The x-axis radius of the ellipse defining the rounded corners of the rectangle.
        :param float ry: The y-axis radius of the ellipse defining the rounded corners of the rectangle.
        :param bool cw: Specifies the path direction: ``true`` for clockwise, ``false`` for counterclockwise.

        :return: Result.INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: thorvg_python.base.Result

        .. note::
            For ``rx`` and ``ry`` greater than or equal to the half of ``w`` and the half of ``h``,
            respectively, the shape become an ellipse.
        """
        self.thorvg_lib.tvg_shape_append_rect.argtypes = [
            PaintPointer,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_bool,
        ]
        self.thorvg_lib.tvg_shape_append_rect.restype = Result
        return self.thorvg_lib.tvg_shape_append_rect(
            self._paint,
            ctypes.c_float(x),
            ctypes.c_float(y),
            ctypes.c_float(w),
            ctypes.c_float(h),
            ctypes.c_float(rx),
            ctypes.c_float(ry),
            ctypes.c_bool(cw),
        )

    def append_circle(
        self,
        cx: float,
        cy: float,
        rx: float,
        ry: float,
        cw: bool,
    ) -> Result:
        """Appends an ellipse to the path.

        The position of the ellipse is specified by the coordinates of its center - ``cx`` and ``cy`` arguments.

        The ellipse is treated as a new sub-path - it is not connected with the previous sub-path.

        The value of the current point is set to (``cx``, ``cy`` - ``ry``).

        :param float cx: The horizontal coordinate of the center of the ellipse.
        :param float cy: The vertical coordinate of the center of the ellipse.
        :param float rx: The x-axis radius of the ellipse.
        :param float ry: The y-axis radius of the ellipse.
        :param bool cw: Specifies the path direction: ``true`` for clockwise, ``false`` for counterclockwise.

        :return: Result.INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: thorvg_python.base.Result
        """
        self.thorvg_lib.tvg_shape_append_circle.argtypes = [
            PaintPointer,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_bool,
        ]
        self.thorvg_lib.tvg_shape_append_circle.restype = Result
        return self.thorvg_lib.tvg_shape_append_circle(
            self._paint,
            ctypes.c_float(cx),
            ctypes.c_float(cy),
            ctypes.c_float(rx),
            ctypes.c_float(ry),
            ctypes.c_bool(cw),
        )

    def append_path(
        self,
        cmds: Sequence[PathCommand],
        pts: Sequence[PointStruct],
    ) -> Result:
        """Appends a given sub-path to the path.

        The current point value is set to the last point from the sub-path.
        For each command from the ``cmds`` array, an appropriate number of points in ``pts`` array should be specified.
        If the number of points in the ``pts`` array is different than the number required by the ``cmds`` array, the shape with this sub-path will not be displayed on the screen.

        :param Sequence[thorvg_python.base.PathCommand] cmds: The array of the commands in the sub-path.
        :param Sequence[thorvg_python.base.PointStruct] pts: The array of the two-dimensional points.

        :return: Result.INVALID_ARGUMENT A ``None`` passed as the argument or ``cmdCnt`` or ``ptsCnt`` equal to zero.
        :rtype: thorvg_python.base.Result
        """
        cmds_arr_type = ctypes.c_uint8 * len(cmds)
        pts_arr_type = PointStruct * len(pts)
        cmds_arr = cmds_arr_type(*cmds)
        pts_arr = pts_arr_type(*pts)
        self.thorvg_lib.tvg_shape_append_path.argtypes = [
            PaintPointer,
            ctypes.POINTER(cmds_arr_type),
            ctypes.c_uint32,
            ctypes.POINTER(pts_arr_type),
            ctypes.c_uint32,
        ]
        self.thorvg_lib.tvg_shape_append_path.restype = Result
        return self.thorvg_lib.tvg_shape_append_path(
            self._paint,
            ctypes.pointer(cmds_arr),
            ctypes.c_uint32(len(cmds)),
            ctypes.pointer(pts_arr),
            ctypes.c_uint32(len(pts)),
        )

    def get_path(self) -> Tuple[Result, Sequence[PathCommand], Sequence[PointStruct]]:
        """Gets the points values of the path.

        The function does not allocate any data, it operates on internal memory. There is no need to free the ``pts`` sequence.

        :return: Result.INVALID_ARGUMENT A ``None`` passed as the argument.
        :rtype: thorvg_python.base.Result
        :return: A sequence of the commands from the path.
        :rtype: Sequence[thorvg_python.base.PathCommand]
        :return: A sequence of the two-dimensional points from the path.
        :rtype: Sequence[thorvg_python.base.PointStruct]
        """
        cmds_ptr = ctypes.POINTER(ctypes.c_uint8)()
        cmds_cnt = ctypes.c_uint32()

        pts_ptr = ctypes.POINTER(PointStruct)()
        pts_cnt = ctypes.c_uint32()

        self.thorvg_lib.tvg_shape_get_path.argtypes = [
            PaintPointer,
            ctypes.POINTER(ctypes.POINTER(ctypes.c_uint8)),
            ctypes.POINTER(ctypes.c_uint32),
            ctypes.POINTER(ctypes.POINTER(PointStruct)),
            ctypes.POINTER(ctypes.c_uint32),
        ]
        self.thorvg_lib.tvg_shape_get_path.restype = Result
        result = self.thorvg_lib.tvg_shape_get_path(
            self._paint,
            ctypes.pointer(cmds_ptr),
            ctypes.pointer(cmds_cnt),
            ctypes.pointer(pts_ptr),
            ctypes.pointer(pts_cnt),
        )

        cmds_arr_type = ctypes.c_uint8 * cmds_cnt.value
        cmds_arr = cmds_arr_type.from_address(ctypes.addressof(cmds_ptr.contents))

        pts_arr_type = PointStruct * pts_cnt.value
        pts_arr = pts_arr_type.from_address(ctypes.addressof(pts_ptr.contents))

        return (
            result,
            [PathCommand(cmds_arr[i]) for i in range(cmds_cnt.value)],
            [pts_arr[i] for i in range(pts_cnt.value)],
        )

    def set_stroke_width(self, width: float) -> Result:
        """Sets the stroke width for the path.

        This function defines the thickness of the stroke applied to all figures
        in the path object. A stroke is the outline drawn along the edges of the
        path's geometry.

        :param width: The width of the stroke in pixels. Must be positive value. (The default is 0)

        :return: TVG_RESULT_INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: thorvg_python.base.Result

        .. note::
            A value of ``width`` 0 disables the stroke.

        .. seealso:: Shape.set_stroke_color()
        """
        self.thorvg_lib.tvg_shape_set_stroke_width.argtypes = [
            PaintPointer,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_shape_set_stroke_width.restype = Result
        return self.thorvg_lib.tvg_shape_set_stroke_width(
            self._paint,
            ctypes.c_float(width),
        )

    def get_stroke_width(self) -> Tuple[Result, float]:
        """Gets the shape's stroke width.

        :return: Result.INVALID_ARGUMENT An invalid pointer passed as an argument.
        :rtype: thorvg_python.base.Result
        :return: The stroke width.
        :rtype: float
        """
        width = ctypes.c_float()
        self.thorvg_lib.tvg_shape_get_stroke_width.argtypes = [
            PaintPointer,
            ctypes.POINTER(ctypes.c_float),
        ]
        self.thorvg_lib.tvg_shape_get_stroke_width.restype = Result
        result = self.thorvg_lib.tvg_shape_get_stroke_width(
            self._paint,
            ctypes.pointer(width),
        )
        return result, width.value

    def set_stroke_color(
        self,
        r: int,
        g: int,
        b: int,
        a: int,
    ) -> Result:
        """Sets the shape's stroke color.

        :param int r: The red color channel value in the range [0 ~ 255]. The default value is 0.
        :param int g: The green color channel value in the range [0 ~ 255]. The default value is 0.
        :param int b: The blue color channel value in the range [0 ~ 255]. The default value is 0.
        :param int a: The alpha channel value in the range [0 ~ 255], where 0 is completely transparent and 255 is opaque.

        :return: Result.INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: thorvg_python.base.Result

        .. note::
            If the stroke width is 0 (default), the stroke will not be visible regardless of the color.
        .. note::
            Either a solid color or a gradient fill is applied, depending on what was set as last.

        .. seealso:: Shape.set_stroke_width()
        .. seealso:: Shape.set_stroke_gradient()
        """
        self.thorvg_lib.tvg_shape_set_stroke_color.argtypes = [
            PaintPointer,
            ctypes.c_uint8,
            ctypes.c_uint8,
            ctypes.c_uint8,
            ctypes.c_uint8,
        ]
        self.thorvg_lib.tvg_shape_set_stroke_color.restype = Result
        return self.thorvg_lib.tvg_shape_set_stroke_color(
            self._paint,
            ctypes.c_uint8(r),
            ctypes.c_uint8(g),
            ctypes.c_uint8(b),
            ctypes.c_uint8(a),
        )

    def get_stroke_color(self) -> Tuple[Result, int, int, int, int]:
        """Gets the shape's stroke color.

        :return:
            - Result.INVALID_ARGUMENT An invalid PaintPointer.
            - Result.INSUFFICIENT_CONDITION No stroke was set.
        :rtype: thorvg_python.base.Result
        :return: The red color channel value in the range [0 ~ 255]. The default value is 0.
        :rtype: int
        :return: The green color channel value in the range [0 ~ 255]. The default value is 0.
        :rtype: int
        :return: The blue color channel value in the range [0 ~ 255]. The default value is 0.
        :rtype: int
        :return: The alpha channel value in the range [0 ~ 255], where 0 is completely transparent and 255 is opaque.
        :rtype: int
        """
        r = ctypes.c_uint8()
        g = ctypes.c_uint8()
        b = ctypes.c_uint8()
        a = ctypes.c_uint8()

        self.thorvg_lib.tvg_shape_get_stroke_color.argtypes = [
            PaintPointer,
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.POINTER(ctypes.c_uint8),
        ]
        self.thorvg_lib.tvg_shape_get_stroke_color.restype = Result
        result = self.thorvg_lib.tvg_shape_get_stroke_color(
            self._paint,
            ctypes.pointer(r),
            ctypes.pointer(g),
            ctypes.pointer(b),
            ctypes.pointer(a),
        )
        return result, r.value, g.value, b.value, a.value

    def set_stroke_gradient(self, grad: "Gradient") -> Result:
        """Sets the gradient fill of the stroke for all of the figures from the path.

        :param thorvg_python.gradient.Gradient grad: The gradient fill.

        :return:
            - Result.INVALID_ARGUMENT An invalid PaintPointer.
            - Result.MEMORY_CORRUPTION An invalid GradientPointer or an error with accessing it.
        :rtype: thorvg_python.base.Result

        .. note::
            Either a solid color or a gradient fill is applied, depending on what was set as last.

        .. seealso:: Shape.set_stroke_color()
        """
        self.thorvg_lib.tvg_shape_set_stroke_gradient.argtypes = [
            PaintPointer,
            GradientPointer,
        ]
        self.thorvg_lib.tvg_shape_set_stroke_gradient.restype = Result
        return self.thorvg_lib.tvg_shape_set_stroke_gradient(
            self._paint,
            grad._grad,  # type: ignore
        )

    def get_stroke_gradient(self) -> Tuple[Result, Optional[Gradient]]:
        """Gets the gradient fill of the shape's stroke.

        The function does not allocate any memory.

        :return: Result.INVALID_ARGUMENT An invalid pointer passed as an argument.
        :rtype: thorvg_python.base.Result
        :return: The gradient fill.
        :rtype: Optional[thorvg_python.Gradient]
        """
        grad = GradientPointer()
        self.thorvg_lib.tvg_shape_get_stroke_gradient.argtypes = [
            PaintPointer,
            ctypes.POINTER(GradientPointer),
        ]
        self.thorvg_lib.tvg_shape_get_stroke_gradient.restype = Result
        result = self.thorvg_lib.tvg_shape_get_stroke_gradient(
            self._paint,
            ctypes.pointer(grad),
        )
        _, grad_type = Gradient(self.engine, grad).get_type()
        if grad_type == TvgType.LINEAR_GRAD:
            return result, LinearGradient(self.engine, grad)
        elif grad_type == TvgType.RADIAL_GRAD:
            return result, RadialGradient(self.engine, grad)
        elif result != Result.SUCCESS:
            return result, None
        else:
            raise RuntimeError(f"Invalid gradient type {grad_type}")

    def set_stroke_dash(
        self, dash_pattern: Optional[Sequence[float]], offset: float
    ) -> Result:
        """Sets the shape's stroke dash pattern.

        :param Optional[Sequence[float]] dash_pattern: An array of alternating dash and gap lengths.
        :param float offset: The shift of the starting point within the repeating dash pattern, from which the pattern begins to be applied.

        :return: Result.INVALID_ARGUMENT In case ``dash_pattern`` is ``None`` and ``cnt`` > 0 or ``dash_pattern`` is not ``None`` and ``cnt`` is zero.
        :rtype: thorvg_python.base.Result

        .. note::
            To reset the stroke dash pattern, pass ``None`` to ``dash_pattern`` and zero to ``cnt``.
        .. note::
            Values of ``dash_pattern`` less than zero are treated as zero.
        .. note::
            If all values in the ``dash_pattern`` are equal to or less than 0, the dash is ignored.
        .. note::
            If the ``dash_pattern`` contains an odd number of elements, the sequence is repeated in the same
            order to form an even-length pattern, preserving the alternation of dashes and gaps.
        .. versionadded:: 1.0
        """
        if dash_pattern is not None:
            cnt = len(dash_pattern)
            dash_pattern_type = ctypes.c_float * cnt
            dash_pattern_type_ptr = ctypes.POINTER(dash_pattern_type)
            dash_pattern_ptr = ctypes.pointer(dash_pattern_type(*dash_pattern))
        else:
            cnt = 0
            dash_pattern_type_ptr = ctypes.c_void_p  # type: ignore
            dash_pattern_ptr = ctypes.c_void_p()  # type: ignore

        self.thorvg_lib.tvg_shape_set_stroke_dash.argtypes = [
            PaintPointer,
            dash_pattern_type_ptr,
            ctypes.c_uint32,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_shape_set_stroke_dash.restype = Result
        return self.thorvg_lib.tvg_shape_set_stroke_dash(
            self._paint, dash_pattern_ptr, ctypes.c_uint32(cnt), ctypes.c_float(offset)
        )

    def get_stroke_dash(self) -> Tuple[Result, Sequence[float], float]:
        """Gets the dash pattern of the stroke.

        The function does not allocate any memory.

        :return: Result.INVALID_ARGUMENT An invalid pointer passed as an argument.
        :rtype: thorvg_python.base.Result
        :return: The array of consecutive pair values of the dash length and the gap length.
        :rtype: Sequence[float]
        :return: The shift of the starting point within the repeating dash pattern.
        :rtype: float

        .. versionadded:: 1.0
        """
        dash_pattern_ptr = ctypes.POINTER(ctypes.c_float)()
        cnt = ctypes.c_uint32()
        offset = ctypes.c_float()
        self.thorvg_lib.tvg_shape_get_stroke_dash.argtypes = [
            PaintPointer,
            ctypes.POINTER(ctypes.POINTER(ctypes.c_float)),
            ctypes.POINTER(ctypes.c_uint32),
            ctypes.POINTER(ctypes.c_float),
        ]
        self.thorvg_lib.tvg_shape_get_stroke_dash.restype = Result
        result = self.thorvg_lib.tvg_shape_get_stroke_dash(
            self._paint,
            ctypes.pointer(dash_pattern_ptr),
            ctypes.pointer(cnt),
            ctypes.pointer(offset),
        )
        dash_pattern_arr_type = ctypes.c_float * cnt.value
        dash_pattern_arr = dash_pattern_arr_type.from_address(
            ctypes.addressof(dash_pattern_ptr.contents)
        )
        return result, [dash_pattern_arr[i] for i in range(cnt.value)], offset.value

    def set_stroke_cap(
        self,
        cap: StrokeCap,
    ) -> Result:
        """Sets the cap style used for stroking the path.

        The cap style specifies the shape to be used at the end of the open stroked sub-paths.

        :param thorvg_python.base.StrokeCap cap: The cap style value. The default value is ``StrokeCap.SQUARE``.

        :return: Result.INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: thorvg_python.base.Result
        """
        self.thorvg_lib.tvg_shape_set_stroke_cap.argtypes = [
            PaintPointer,
            ctypes.c_uint8,
        ]
        self.thorvg_lib.tvg_shape_set_stroke_cap.restype = Result
        return self.thorvg_lib.tvg_shape_set_stroke_cap(
            self._paint,
            cap,
        )

    def get_stroke_cap(self) -> Tuple[Result, StrokeCap]:
        """Gets the stroke cap style used for stroking the path.

        :return: Result.INVALID_ARGUMENT An invalid pointer passed as an argument.
        :rtype: thorvg_python.base.Result
        :return: The cap style value.
        :rtype: thorvg_python.base.StrokeCap
        """
        cap = ctypes.c_uint8()
        self.thorvg_lib.tvg_shape_get_stroke_cap.argtypes = [
            PaintPointer,
            ctypes.POINTER(ctypes.c_uint8),
        ]
        self.thorvg_lib.tvg_shape_get_stroke_cap.restype = Result
        result = self.thorvg_lib.tvg_shape_get_stroke_cap(
            self._paint,
            ctypes.pointer(cap),
        )
        return result, StrokeCap(cap.value)

    def set_stroke_join(self, join: StrokeJoin) -> Result:
        """Sets the join style for stroked path segments.

        :param thorvg_python.base.StrokeJoin join: The join style value. The default value is ``StrokeJoin.BEVEL``.

        :return: Result.INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: thorvg_python.base.Result
        """
        self.thorvg_lib.tvg_shape_set_stroke_join.argtypes = [
            PaintPointer,
            ctypes.c_uint8,
        ]
        self.thorvg_lib.tvg_shape_set_stroke_join.restype = Result
        return self.thorvg_lib.tvg_shape_set_stroke_join(
            self._paint,
            join,
        )

    def get_stroke_join(self) -> Tuple[Result, StrokeJoin]:
        """The function gets the stroke join method

        :return: Result.INVALID_ARGUMENT An invalid pointer passed as an argument.
        :rtype: thorvg_python.base.Result
        :return: The join style value.
        :rtype: thorvg_python.base.StrokeJoin
        """
        join = ctypes.c_uint8()
        self.thorvg_lib.tvg_shape_get_stroke_join.argtypes = [
            PaintPointer,
            ctypes.POINTER(ctypes.c_uint8),
        ]
        self.thorvg_lib.tvg_shape_get_stroke_join.restype = Result
        result = self.thorvg_lib.tvg_shape_get_stroke_join(
            self._paint,
            ctypes.pointer(join),
        )
        return result, StrokeJoin(join.value)

    def set_stroke_miterlimit(self, miterlimit: float) -> Result:
        """Sets the stroke miterlimit.

        :param float miterlimit: The miterlimit imposes a limit on the extent of the stroke join when the ``MITER`` join style is set. The default value is 4.

        :return: Result enumeration
            INVALID_ARGUMENT An invalid PaintPointer or Unsupported ``miterlimit`` values (less than zero).
        :rtype: thorvg_python.base.Result

        .. versionadded:: 0.11
        """
        self.thorvg_lib.tvg_shape_set_stroke_miterlimit.argtypes = [
            PaintPointer,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_shape_set_stroke_miterlimit.restype = Result
        return self.thorvg_lib.tvg_shape_set_stroke_miterlimit(
            self._paint,
            miterlimit,
        )

    def get_stroke_miterlimit(self) -> Tuple[Result, float]:
        """The function gets the stroke miterlimit.

        :return: Result.INVALID_ARGUMENT An invalid pointer passed as an argument.
        :rtype: thorvg_python.base.Result
        :return: The stroke miterlimit.
        :rtype: float

        .. versionadded:: 0.11
        """
        miterlimit = ctypes.c_float()
        self.thorvg_lib.tvg_shape_get_stroke_miterlimit.argtypes = [
            PaintPointer,
            ctypes.POINTER(ctypes.c_float),
        ]
        self.thorvg_lib.tvg_shape_get_stroke_miterlimit.restype = Result
        result = self.thorvg_lib.tvg_shape_get_stroke_miterlimit(
            self._paint,
            ctypes.pointer(miterlimit),
        )
        return result, miterlimit.value

    def set_trimpath(
        self,
        begin: float,
        end: float,
        simultaneous: bool,
    ) -> Result:
        """Sets the trim of the shape along the defined path segment, allowing control over which part of the shape is visible.

        If the values of the arguments ``begin`` and ``end`` exceed the 0-1 range, they are wrapped around in a manner similar to angle wrapping, effectively treating the range as circular.

        :param float begin: Specifies the start of the segment to display along the path.
        :param float end: Specifies the end of the segment to display along the path.
        :param bool simultaneous: Determines how to trim multiple paths within a single shape. If set to ``true`` (default), trimming is applied simultaneously to all paths;
            Otherwise, all paths are treated as a single entity with a combined length equal to the sum of their individual lengths and are trimmed as such.

        :return: TVG_RESULT_INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: thorvg_python.base.Result

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_shape_set_trimpath.argtypes = [
            PaintPointer,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_bool,
        ]
        self.thorvg_lib.tvg_shape_set_trimpath.restype = Result
        return self.thorvg_lib.tvg_shape_set_trimpath(
            self._paint,
            ctypes.c_float(begin),
            ctypes.c_float(end),
            ctypes.c_bool(simultaneous),
        )

    def set_fill_color(
        self,
        r: int,
        g: int,
        b: int,
        a: int,
    ) -> Result:
        """Sets the shape's solid color.

        The parts of the shape defined as inner are colored.

        :param int r The red color channel value in the range [0 ~ 255]. The default value is 0.
        :param int g: The green color channel value in the range [0 ~ 255]. The default value is 0.
        :param int b: The blue color channel value in the range [0 ~ 255]. The default value is 0.
        :param int a The alpha channel value in the range [0 ~ 255], where 0 is completely transparent and 255 is opaque. The default value is 0.

        :return: Result.INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: thorvg_python.base.Result

        .. note::
            Either a solid color or a gradient fill is applied, depending on what was set as last.
        .. seealso:: Shape.set_fill_rule()
        """
        self.thorvg_lib.tvg_shape_set_fill_color.argtypes = [
            PaintPointer,
            ctypes.c_uint8,
            ctypes.c_uint8,
            ctypes.c_uint8,
            ctypes.c_uint8,
        ]
        self.thorvg_lib.tvg_shape_set_fill_color.restype = Result
        return self.thorvg_lib.tvg_shape_set_fill_color(
            self._paint,
            ctypes.c_uint8(r),
            ctypes.c_uint8(g),
            ctypes.c_uint8(b),
            ctypes.c_uint8(a),
        )

    def get_fill_color(self) -> Tuple[Result, int, int, int, int]:
        """Gets the shape's solid color.

        :return: The red color channel value in the range [0 ~ 255]. The default value is 0.
        :rtype: int
        :return: The green color channel value in the range [0 ~ 255]. The default value is 0.
        :rtype: int
        :return: The blue color channel value in the range [0 ~ 255]. The default value is 0.
        :rtype: int
        :return: The alpha channel value in the range [0 ~ 255], where 0 is completely transparent and 255 is opaque. The default value is 0.
        :rtype: int
        :return: Result.INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: thorvg_python.base.Result
        """
        r = ctypes.c_uint8()
        g = ctypes.c_uint8()
        b = ctypes.c_uint8()
        a = ctypes.c_uint8()
        self.thorvg_lib.tvg_shape_get_fill_color.argtypes = [
            PaintPointer,
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.POINTER(ctypes.c_uint8),
        ]
        self.thorvg_lib.tvg_shape_get_fill_color.restype = Result
        result = self.thorvg_lib.tvg_shape_get_fill_color(
            self._paint,
            ctypes.pointer(r),
            ctypes.pointer(g),
            ctypes.pointer(b),
            ctypes.pointer(a),
        )

        return result, r.value, g.value, b.value, a.value

    def set_fill_rule(self, rule: FillRule) -> Result:
        """Sets the fill rule for the shape.

        Specifies how the interior of the shape is determined when its path intersects itself.
        The default fill rule is ``FillRule.NON_ZERO``.

        :param thorvg_python.base.FillRule rule: The fill rule to apply to the shape.

        :return: TVG_RESULT_INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: thorvg_python.base.Result
        """
        self.thorvg_lib.tvg_shape_set_fill_rule.argtypes = [
            PaintPointer,
            ctypes.c_uint8,
        ]
        self.thorvg_lib.tvg_shape_set_fill_rule.restype = Result
        return self.thorvg_lib.tvg_shape_set_fill_rule(
            self._paint,
            ctypes.c_uint8(rule),
        )

    def get_fill_rule(self) -> Tuple[Result, FillRule]:
        """Retrieves the current fill rule used by the shape.

        This function returns the fill rule, which determines how the interior
        regions of the shape are calculated when it overlaps itself.

        :return: The current FillRule value of the shape.
        :rtype: thorvg_python.base.FillRule
        :return: TVG_RESULT_INVALID_ARGUMENT An invalid pointer passed as an argument.
        :rtype: thorvg_python.base.Result
        """
        rule = ctypes.c_uint8()
        self.thorvg_lib.tvg_shape_get_fill_rule.argtypes = [
            PaintPointer,
            ctypes.POINTER(ctypes.c_uint8),
        ]
        self.thorvg_lib.tvg_shape_get_fill_rule.restype = Result
        result = self.thorvg_lib.tvg_shape_get_fill_rule(
            self._paint,
            ctypes.pointer(rule),
        )

        return result, FillRule(rule.value)

    def set_paint_order(self, stroke_first: bool) -> Result:
        """Sets the rendering order of the stroke and the fill.

        :param bool stroke_first: If ``true`` the stroke is rendered before the fill, otherwise the stroke is rendered as the second one (the default option).

        :return: Result.INVALID_ARGUMENT An invalid PaintPointer.
        :rtype: thorvg_python.base.Result

        .. versionadded:: 0.10
        """
        self.thorvg_lib.tvg_shape_set_paint_order.argtypes = [
            PaintPointer,
            ctypes.c_bool,
        ]
        self.thorvg_lib.tvg_shape_set_paint_order.restype = Result
        return self.thorvg_lib.tvg_shape_set_paint_order(
            self._paint,
            ctypes.c_bool(stroke_first),
        )

    def set_gradient(self, grad: "Gradient") -> Result:
        """Sets the gradient fill for all of the figures from the path.

        The parts of the shape defined as inner are filled.

        :param thorvg_python.gradient.Gradient grad: The gradient fill.

        :return:
            - TVG_RESULT_INVALID_ARGUMENT An invalid PaintPointer.
            - TVG_RESULT_MEMORY_CORRUPTION An invalid GradientPointer.
        :rtype: thorvg_python.base.Result

        .. note::
            Either a solid color or a gradient fill is applied, depending on what was set as last.
        .. seealso:: Shape.set_fill_rule()
        """
        self.thorvg_lib.tvg_shape_set_gradient.argtypes = [
            PaintPointer,
            GradientPointer,
        ]
        self.thorvg_lib.tvg_shape_set_gradient.restype = Result
        return self.thorvg_lib.tvg_shape_set_gradient(
            self._paint,
            grad._grad,  # type: ignore
        )

    def get_gradient(self) -> Tuple[Result, Union["LinearGradient", "RadialGradient"]]:
        """Gets the gradient fill of the shape.

        The function does not allocate any data.

        :return: Result.INVALID_ARGUMENT An invalid pointer passed as an argument.
        :rtype: thorvg_python.base.Result
        :return: The gradient fill.
        :rtype: thorvg_python.base.GradientPointer
        """
        grad = GradientPointer()
        self.thorvg_lib.tvg_shape_get_gradient.argtypes = [
            PaintPointer,
            ctypes.POINTER(GradientPointer),
        ]
        self.thorvg_lib.tvg_shape_get_gradient.restype = Result
        result = self.thorvg_lib.tvg_shape_get_gradient(
            self._paint,
            ctypes.pointer(grad),
        )
        _, tvg_type = Gradient(self.engine, grad).get_type()
        if tvg_type == TvgType.LINEAR_GRAD:
            return result, LinearGradient(self.engine, grad)
        elif tvg_type == TvgType.RADIAL_GRAD:
            return result, RadialGradient(self.engine, grad)
        else:
            raise RuntimeError(f"Invalid gradient TvgType: {tvg_type}")
