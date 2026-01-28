#!/usr/bin/env python3
import ctypes
from typing import Optional, Sequence, Tuple, Union

from ..base import (
    FillRule,
    GradientStruct,
    PaintStruct,
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
    Path can be composed by accumulating primitive commands such as tvg_shape_move_to(), tvg_shape_line_to(), tvg_shape_cubic_to() or complete shape interfaces such as tvg_shape_append_rect(), tvg_shape_append_circle(), etc.
    Path can consists of sub-paths. One sub-path is determined by a close command.

    The stroke of a shape is an optional property in case the shape needs to be represented with/without the outline borders.
    It's efficient since the shape path and the stroking path can be shared with each other. It's also convenient when controlling both in one context.
    """

    def __init__(self, engine: Engine, paint: Optional[PaintStruct] = None):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if paint is None:
            self._paint = self._new()
        else:
            self._paint = paint

    def _new(self) -> PaintStruct:
        """Creates a new shape object.

        Note that you need not call this method as it is auto called when initializing ``Shape()``.

        :return: A new shape object.
        :rtype: PaintStruct
        """
        self.thorvg_lib.tvg_shape_new.restype = ctypes.POINTER(PaintStruct)
        return self.thorvg_lib.tvg_shape_new().contents

    def reset(self) -> Result:
        """Resets the shape path properties.

        The color, the fill and the stroke properties are retained.

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result

        .. note::
            The memory, where the path data is stored, is not deallocated at this stage for caching effect.
        """
        self.thorvg_lib.tvg_shape_reset.argtypes = [ctypes.POINTER(PaintStruct)]
        self.thorvg_lib.tvg_shape_reset.restype = Result
        return self.thorvg_lib.tvg_shape_reset(self._paint)

    def move_to(self, x: float, y: float) -> Result:
        """Sets the initial point of the sub-path.

        The value of the current point is set to the given point.

        :param float x: The horizontal coordinate of the initial point of the sub-path.
        :param float y: The vertical coordinate of the initial point of the sub-path.

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result
        """
        self.thorvg_lib.tvg_shape_move_to.argtypes = [
            ctypes.POINTER(PaintStruct),
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

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result

        .. note::
            In case this is the first command in the path, it corresponds to the tvg_shape_move_to() call.
        """
        self.thorvg_lib.tvg_shape_line_to.argtypes = [
            ctypes.POINTER(PaintStruct),
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

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result

        .. note::
            In case this is the first command in the path, no data from the path are rendered.
        """
        self.thorvg_lib.tvg_shape_cubic_to.argtypes = [
            ctypes.POINTER(PaintStruct),
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

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result

        .. note::
            In case the sub-path does not contain any points, this function has no effect.
        """
        self.thorvg_lib.tvg_shape_close.argtypes = [
            ctypes.POINTER(PaintStruct),
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

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result
        """
        self.thorvg_lib.tvg_shape_append_rect.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
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
        )

    def append_circle(
        self,
        cx: float,
        cy: float,
        rx: float,
        ry: float,
    ) -> Result:
        """Appends an ellipse to the path.

        The position of the ellipse is specified by the coordinates of its center - ``cx`` and ``cy`` arguments.

        The ellipse is treated as a new sub-path - it is not connected with the previous sub-path.

        The value of the current point is set to (``cx``, ``cy`` - ``ry``).

        :param float cx: The horizontal coordinate of the center of the ellipse.
        :param float cy: The vertical coordinate of the center of the ellipse.
        :param float rx: The x-axis radius of the ellipse.
        :param float ry: The y-axis radius of the ellipse.

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result
        """
        self.thorvg_lib.tvg_shape_append_circle.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_shape_append_circle.restype = Result
        return self.thorvg_lib.tvg_shape_append_circle(
            self._paint,
            ctypes.c_float(cx),
            ctypes.c_float(cy),
            ctypes.c_float(rx),
            ctypes.c_float(ry),
        )

    def append_arc(
        self,
        cx: float,
        cy: float,
        radius: float,
        startAngle: float,
        sweep: float,
        pie: bool,
    ) -> Result:
        """Appends a circular arc to the path.

        The arc is treated as a new sub-path - it is not connected with the previous sub-path.
        The current point value is set to the end-point of the arc in case ``pie`` is ``false``, and to the center of the arc otherwise.

        :param float cx: The horizontal coordinate of the center of the arc.
        :param float cy: The vertical coordinate of the center of the arc.
        :param float radius: The radius of the arc.
        :param float startAngle: The start angle of the arc given in degrees, measured counter-clockwise from the horizontal line.
        :param float sweep: The central angle of the arc given in degrees, measured counter-clockwise from ``startAngle``.
        :param bool pie: Specifies whether to draw radii from the arc's center to both of its end-point - drawn if ``1``.

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result

        .. note::
            Setting ``sweep`` value greater than 360 degrees, is equivalent to calling tvg_shape_append_circle(paint, cx, cy, radius, radius).
        .. deprecated:: 0.15
        """
        self.thorvg_lib.tvg_shape_append_arc.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_bool,
        ]
        self.thorvg_lib.tvg_shape_append_arc.restype = Result
        return self.thorvg_lib.tvg_shape_append_arc(
            self._paint,
            ctypes.c_float(cx),
            ctypes.c_float(cy),
            ctypes.c_float(radius),
            ctypes.c_float(startAngle),
            ctypes.c_float(sweep),
            ctypes.c_bool(pie),
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

        :param Sequence[PathCommand] cmds: The array of the commands in the sub-path.
        :param Sequence[PointStruct] pts: The array of the two-dimensional points.

        :return: INVALID_ARGUMENT A ``nullptr`` passed as the argument or ``cmdCnt`` or ``ptsCnt`` equal to zero.
        :rtype: Result
        """
        cmds_arr_type = ctypes.c_int * len(cmds)
        pts_arr_type = PointStruct * len(pts)
        cmds_arr = cmds_arr_type(*cmds)
        pts_arr = pts_arr_type(*pts)
        self.thorvg_lib.tvg_shape_append_path.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(cmds_arr_type),
            ctypes.c_int,
            ctypes.POINTER(pts_arr_type),
            ctypes.c_int,
        ]
        self.thorvg_lib.tvg_shape_append_path.restype = Result
        return self.thorvg_lib.tvg_shape_append_path(
            self._paint,
            ctypes.pointer(cmds_arr),
            ctypes.c_int(len(cmds)),
            ctypes.pointer(pts_arr),
            ctypes.c_int(len(pts)),
        )

    def get_path_coords(self) -> Tuple[Result, Sequence[PointStruct]]:
        """Gets the points values of the path.

        The function does not allocate any data, it operates on internal memory. There is no need to free the ``pts`` sequence.

        .. code-block:: python

            from thorvg_python import Engine, Shape

            engine = Engine()
            shape = Shape(engine)

            shape.append_circle(10, 10, 50, 50)
            coords = shape.get_path_coords(shape)
            //TVG approximates a circle by four Bezier curves. In the example above the coords sequence stores their coordinates.

        :return: INVALID_ARGUMENT A ``nullptr`` passed as the argument.
        :rtype: Result
        :return: A sequence of the two-dimensional points from the path.
        :rtype: Sequence[PointStruct]
        """
        pts_ptr = ctypes.POINTER(PointStruct)()
        cnt = ctypes.c_uint32()
        self.thorvg_lib.tvg_shape_get_path_coords.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.POINTER(PointStruct)),
            ctypes.POINTER(ctypes.c_uint32),
        ]
        self.thorvg_lib.tvg_shape_get_path_coords.restype = Result
        result = self.thorvg_lib.tvg_shape_get_path_coords(
            ctypes.pointer(self._paint), ctypes.pointer(pts_ptr), ctypes.pointer(cnt)
        )
        pts_arr_type = PointStruct * cnt.value
        pts_arr = pts_arr_type.from_address(ctypes.addressof(pts_ptr.contents))
        return result, [pts_arr[i] for i in range(cnt.value)]

    def get_path_commands(self) -> Tuple[Result, Sequence[PathCommand]]:
        """Gets the commands data of the path.

        The function does not allocate any data. There is no need to free the ``cmds`` seqeunce.

        .. code-block:: python

            from thorvg_python import Engine, Shape

            engine = Engine()
            shape = Shape(engine)

            shape.append_circle(10, 10, 50, 50)
            cmds = shape.get_path_commands()
            //TVG approximates a circle by four Bezier curves. In the example above the cmds seqeunce stores the commands of the path data.

        :return: INVALID_ARGUMENT A ``nullptr`` passed as the argument.
        :rtype: Result
        :return: A sequence of the commands from the path.
        :rtype: Sequence[PathCommand]
        """
        cmds_ptr = ctypes.POINTER(ctypes.c_int)()
        cnt = ctypes.c_uint32()
        self.thorvg_lib.tvg_shape_get_path_commands.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.POINTER(ctypes.c_int)),
            ctypes.POINTER(ctypes.c_uint32),
        ]
        self.thorvg_lib.tvg_shape_get_path_commands.restype = Result
        result = self.thorvg_lib.tvg_shape_get_path_commands(
            ctypes.pointer(self._paint), ctypes.pointer(cmds_ptr), ctypes.pointer(cnt)
        )
        cmds_arr_type = ctypes.c_int * cnt.value
        cmds_arr = cmds_arr_type.from_address(ctypes.addressof(cmds_ptr.contents))
        return result, [PathCommand(cmds_arr[i]) for i in range(cnt.value)]

    def set_stroke_width(self, width: float) -> Result:
        """Sets the stroke width for all of the figures from the ``paint``.

        :param float width: The width of the stroke. The default value is 0.

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result
        """
        self.thorvg_lib.tvg_shape_set_stroke_width.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_shape_set_stroke_width.restype = Result
        return self.thorvg_lib.tvg_shape_set_stroke_width(
            ctypes.pointer(self._paint),
            ctypes.c_float(width),
        )

    def get_stroke_width(self) -> Tuple[Result, float]:
        """Gets the shape's stroke width.

        :return: INVALID_ARGUMENT An invalid pointer passed as an argument.
        :rtype: Result
        :return: The stroke width.
        :rtype: float
        """
        width = ctypes.c_float()
        self.thorvg_lib.tvg_shape_get_stroke_width.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.c_float),
        ]
        self.thorvg_lib.tvg_shape_get_stroke_width.restype = Result
        result = self.thorvg_lib.tvg_shape_get_stroke_width(
            ctypes.pointer(self._paint),
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

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result

        .. note::
            Either a solid color or a gradient fill is applied, depending on what was set as last.
        """
        self.thorvg_lib.tvg_shape_set_stroke_color.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_uint8,
            ctypes.c_uint8,
            ctypes.c_uint8,
            ctypes.c_uint8,
        ]
        self.thorvg_lib.tvg_shape_set_stroke_color.restype = Result
        return self.thorvg_lib.tvg_shape_set_stroke_color(
            ctypes.pointer(self._paint),
            ctypes.c_uint8(r),
            ctypes.c_uint8(g),
            ctypes.c_uint8(b),
            ctypes.c_uint8(a),
        )

    def get_stroke_color(self) -> Tuple[Result, int, int, int, int]:
        """Gets the shape's stroke color.

        :return:
            - INVALID_ARGUMENT An invalid PaintStruct pointer.
            - INSUFFICIENT_CONDITION No stroke was set.
        :rtype: Result
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
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.POINTER(ctypes.c_uint8),
        ]
        self.thorvg_lib.tvg_shape_get_stroke_color.restype = Result
        result = self.thorvg_lib.tvg_shape_get_stroke_color(
            ctypes.pointer(self._paint),
            ctypes.pointer(r),
            ctypes.pointer(g),
            ctypes.pointer(b),
            ctypes.pointer(a),
        )
        return result, r.value, g.value, b.value, a.value

    def set_stroke_linear_gradient(self, grad: "Gradient") -> Result:
        """Sets the linear gradient fill of the stroke for all of the figures from the path.

        :param GradientStruct grad: The linear gradient fill.

        :return:
            - INVALID_ARGUMENT An invalid PaintStruct pointer.
            - MEMORY_CORRUPTION An invalid GradientStruct pointer or an error with accessing it.
        :rtype: Result

        .. note::
            Either a solid color or a gradient fill is applied, depending on what was set as last.
        """
        self.thorvg_lib.tvg_shape_set_stroke_linear_gradient.argtypes = [
            ctypes.POINTER(PaintStruct),
            GradientStruct,
        ]
        self.thorvg_lib.tvg_shape_set_stroke_linear_gradient.restype = Result
        return self.thorvg_lib.tvg_shape_set_stroke_linear_gradient(
            ctypes.pointer(self._paint),
            grad._grad,  # type: ignore
        )

    def set_stroke_radial_gradient(self, grad: "Gradient") -> Result:
        """Sets the radial gradient fill of the stroke for all of the figures from the path.

        :param GradientStruct grad: The radial gradient fill.

        :return:
            - INVALID_ARGUMENT An invalid PaintStruct pointer.
            - MEMORY_CORRUPTION An invalid GradientStruct pointer or an error with accessing it.
        :rtype: Result

        .. note::
            Either a solid color or a gradient fill is applied, depending on what was set as last.
        """
        self.thorvg_lib.tvg_shape_set_stroke_radial_gradient.argtypes = [
            ctypes.POINTER(PaintStruct),
            GradientStruct,
        ]
        self.thorvg_lib.tvg_shape_set_stroke_radial_gradient.restype = Result
        return self.thorvg_lib.tvg_shape_set_stroke_radial_gradient(
            ctypes.pointer(self._paint),
            grad._grad,  # type: ignore
        )

    def get_stroke_gradient(self) -> Tuple[Result, GradientStruct]:
        """Gets the gradient fill of the shape's stroke.

        The function does not allocate any memory.

        :return: INVALID_ARGUMENT An invalid pointer passed as an argument.
        :rtype: Result
        :return: The gradient fill.
        :rtype: GradientStruct
        """
        grad_ptr = ctypes.POINTER(GradientStruct)()
        self.thorvg_lib.tvg_shape_get_stroke_gradient.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.POINTER(GradientStruct)),
        ]
        self.thorvg_lib.tvg_shape_get_stroke_gradient.restype = Result
        result = self.thorvg_lib.tvg_shape_get_stroke_gradient(
            ctypes.pointer(self._paint),
            ctypes.pointer(grad_ptr),
        )
        return result, grad_ptr.contents

    def set_stroke_dash(self, dash_pattern: Optional[Sequence[float]]) -> Result:
        """Sets the shape's stroke dash pattern.

        :param Optional[Sequence[float]] dashPattern: The array of consecutive pair values of the dash length and the gap length.

        :return: INVALID_ARGUMENT An invalid pointer passed as an argument and ``cnt`` > 0, the given length of the array is less than two or any of the ``dashPattern`` values is zero or less.
        :rtype: Result

        .. note::
            To reset the stroke dash pattern, pass ``None`` to ``dashPattern``
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
            ctypes.POINTER(PaintStruct),
            dash_pattern_type_ptr,
            ctypes.c_uint32,
        ]
        self.thorvg_lib.tvg_shape_set_stroke_dash.restype = Result
        return self.thorvg_lib.tvg_shape_set_stroke_dash(
            ctypes.pointer(self._paint),
            dash_pattern_ptr,
            ctypes.c_uint32(cnt),
        )

    def get_stroke_dash(self) -> Tuple[Result, Sequence[float]]:
        """Gets the dash pattern of the stroke.

        The function does not allocate any memory.

        :return: INVALID_ARGUMENT An invalid pointer passed as an argument.
        :rtype: Result
        :return: The array of consecutive pair values of the dash length and the gap length.
        :rtype: Sequence[float]
        """
        dash_pattern_ptr = ctypes.POINTER(ctypes.c_float)()
        cnt = ctypes.c_uint32()
        self.thorvg_lib.tvg_shape_get_stroke_dash.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.POINTER(ctypes.c_float)),
            ctypes.POINTER(ctypes.c_uint32),
        ]
        self.thorvg_lib.tvg_shape_get_stroke_dash.restype = Result
        result = self.thorvg_lib.tvg_shape_get_stroke_dash(
            ctypes.pointer(self._paint),
            ctypes.pointer(dash_pattern_ptr),
            ctypes.pointer(cnt),
        )
        dash_pattern_arr_type = ctypes.c_float * cnt.value
        dash_pattern_arr = dash_pattern_arr_type.from_address(
            ctypes.addressof(dash_pattern_ptr.contents)
        )
        return result, [dash_pattern_arr[i] for i in range(cnt.value)]

    def set_stroke_cap(
        self,
        cap: StrokeCap,
    ) -> Result:
        """Sets the cap style used for stroking the path.

        The cap style specifies the shape to be used at the end of the open stroked sub-paths.

        :param StrokeCap cap: The cap style value. The default value is ``SQUARE``.

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result
        """
        self.thorvg_lib.tvg_shape_set_stroke_cap.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_int,
        ]
        self.thorvg_lib.tvg_shape_set_stroke_cap.restype = Result
        return self.thorvg_lib.tvg_shape_set_stroke_cap(
            ctypes.pointer(self._paint),
            cap,
        )

    def get_stroke_cap(self) -> Tuple[Result, StrokeCap]:
        """Gets the stroke cap style used for stroking the path.

        :return: INVALID_ARGUMENT An invalid pointer passed as an argument.
        :rtype: Result
        :return: The cap style value.
        :rtype: StrokeCap
        """
        cap = ctypes.c_int()
        self.thorvg_lib.tvg_shape_get_stroke_cap.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.c_int),
        ]
        self.thorvg_lib.tvg_shape_get_stroke_cap.restype = Result
        result = self.thorvg_lib.tvg_shape_get_stroke_cap(
            ctypes.pointer(self._paint),
            ctypes.pointer(cap),
        )
        return result, StrokeCap(cap.value)

    def set_stroke_join(self, join: StrokeJoin) -> Result:
        """Sets the join style for stroked path segments.

        :param StrokeJoin join: The join style value. The default value is ``BEVEL``.

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result
        """
        self.thorvg_lib.tvg_shape_set_stroke_join.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_int,
        ]
        self.thorvg_lib.tvg_shape_set_stroke_join.restype = Result
        return self.thorvg_lib.tvg_shape_set_stroke_join(
            ctypes.pointer(self._paint),
            join,
        )

    def get_stroke_join(self) -> Tuple[Result, StrokeJoin]:
        """The function gets the stroke join method

        :return: INVALID_ARGUMENT An invalid pointer passed as an argument.
        :rtype: Result
        :return: The join style value.
        :rtype: StrokeJoin
        """
        join = ctypes.c_int()
        self.thorvg_lib.tvg_shape_get_stroke_join.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.c_int),
        ]
        self.thorvg_lib.tvg_shape_get_stroke_join.restype = Result
        result = self.thorvg_lib.tvg_shape_get_stroke_join(
            ctypes.pointer(self._paint),
            ctypes.pointer(join),
        )
        return result, StrokeJoin(join.value)

    def set_stroke_miterlimit(self, miterlimit: float) -> Result:
        """Sets the stroke miterlimit.

        :param float miterlimit: The miterlimit imposes a limit on the extent of the stroke join when the ``MITER`` join style is set. The default value is 4.

        :return: Result enumeration
            INVALID_ARGUMENT An invalid PaintStruct pointer or Unsupported ``miterlimit`` values (less than zero).
        :rtype: Result

        .. versionadded:: 0.11
        """
        self.thorvg_lib.tvg_shape_set_stroke_miterlimit.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_shape_set_stroke_miterlimit.restype = Result
        return self.thorvg_lib.tvg_shape_set_stroke_miterlimit(
            ctypes.pointer(self._paint),
            miterlimit,
        )

    def get_stroke_miterlimit(self) -> Tuple[Result, float]:
        """The function gets the stroke miterlimit.

        :return: INVALID_ARGUMENT An invalid pointer passed as an argument.
        :rtype: Result
        :return: The stroke miterlimit.
        :rtype: float

        .. versionadded:: 0.11
        """
        miterlimit = ctypes.c_float()
        self.thorvg_lib.tvg_shape_get_stroke_miterlimit.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.c_float),
        ]
        self.thorvg_lib.tvg_shape_get_stroke_miterlimit.restype = Result
        result = self.thorvg_lib.tvg_shape_get_stroke_miterlimit(
            ctypes.pointer(self._paint),
            ctypes.pointer(miterlimit),
        )
        return result, miterlimit.value

    def set_stroke_trim(
        self,
        begin: float,
        end: float,
        simultaneous: bool,
    ) -> Result:
        """Sets the trim of the stroke along the defined path segment, allowing control over which part of the stroke is visible.

        If the values of the arguments ``begin`` and ``end`` exceed the 0-1 range, they are wrapped around in a manner similar to angle wrapping, effectively treating the range as circular.

        :param float begin: Specifies the start of the segment to display along the path.
        :param float end: Specifies the end of the segment to display along the path.
        :param bool simultaneous: Determines how to trim multiple paths within a single shape. If set to ``true`` (default), trimming is applied simultaneously to all paths;
            Otherwise, all paths are treated as a single entity with a combined length equal to the sum of their individual lengths and are trimmed as such.

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result

        .. note::
            Experimental API
        """
        self.thorvg_lib.tvg_shape_set_stroke_trim.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_bool,
        ]
        self.thorvg_lib.tvg_shape_set_stroke_trim.restype = Result
        return self.thorvg_lib.tvg_shape_set_stroke_trim(
            ctypes.pointer(self._paint),
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

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result

        .. note::
            Either a solid color or a gradient fill is applied, depending on what was set as last.
        .. seealso:: Shape.set_fill_rule()
        """
        self.thorvg_lib.tvg_shape_set_fill_color.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_uint8,
            ctypes.c_uint8,
            ctypes.c_uint8,
            ctypes.c_uint8,
        ]
        self.thorvg_lib.tvg_shape_set_fill_color.restype = Result
        return self.thorvg_lib.tvg_shape_set_fill_color(
            ctypes.pointer(self._paint),
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
        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result
        """
        r = ctypes.c_uint8()
        g = ctypes.c_uint8()
        b = ctypes.c_uint8()
        a = ctypes.c_uint8()
        self.thorvg_lib.tvg_shape_get_fill_color.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.POINTER(ctypes.c_uint8),
        ]
        self.thorvg_lib.tvg_shape_get_fill_color.restype = Result
        result = self.thorvg_lib.tvg_shape_get_fill_color(
            ctypes.pointer(self._paint),
            ctypes.pointer(r),
            ctypes.pointer(g),
            ctypes.pointer(b),
            ctypes.pointer(a),
        )

        return result, r.value, g.value, b.value, a.value

    def set_fill_rule(self, rule: FillRule) -> Result:
        """Sets the shape's fill rule.

        :param FillRule rule: The fill rule value. The default value is ``WINDING``.

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result
        """
        self.thorvg_lib.tvg_shape_set_fill_rule.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_uint8,
        ]
        self.thorvg_lib.tvg_shape_set_fill_rule.restype = Result
        return self.thorvg_lib.tvg_shape_set_fill_rule(
            ctypes.pointer(self._paint),
            ctypes.c_uint8(rule),
        )

    def get_fill_rule(self) -> Tuple[Result, FillRule]:
        """Gets the shape's fill rule.

        :return: INVALID_ARGUMENT An invalid pointer passed as an argument.
        :rtype: Result
        :return: shape's fill rule
        :rtype: FillRule
        """
        rule = ctypes.c_int()
        self.thorvg_lib.tvg_shape_get_fill_rule.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.c_int),
        ]
        self.thorvg_lib.tvg_shape_get_fill_rule.restype = Result
        result = self.thorvg_lib.tvg_shape_get_fill_rule(
            ctypes.pointer(self._paint),
            ctypes.pointer(rule),
        )

        return result, FillRule(rule.value)

    def set_paint_order(self, stroke_first: bool) -> Result:
        """Sets the rendering order of the stroke and the fill.

        :param bool strokeFirst: If ``true`` the stroke is rendered before the fill, otherwise the stroke is rendered as the second one (the default option).

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result

        .. versionadded:: 0.10
        """
        self.thorvg_lib.tvg_shape_set_paint_order.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_bool,
        ]
        self.thorvg_lib.tvg_shape_set_paint_order.restype = Result
        return self.thorvg_lib.tvg_shape_set_paint_order(
            ctypes.pointer(self._paint),
            ctypes.c_bool(stroke_first),
        )

    def set_linear_gradient(self, grad: "Gradient") -> Result:
        """Sets the linear gradient fill for all of the figures from the path.

        The parts of the shape defined as inner are filled.

        .. code-block:: python

            from thorvg_python import Engine, Shape, LinearGradient, ColorStop

            engine = Engine()
            shape = Shape(engine)
            grad = LinearGradient(engine)
            grad.set(700, 700, 800, 800)
            color_stops = [
                ColorStop(0.0 , 0,   0,   0,   255),
                ColorStop(0.25, 255, 0,   0,   255),
                ColorStop(0.5 , 0,   255, 0,   255),
                ColorStop(1.0 , 0,   0,   255, 255)
            ]
            grad.set_color_stops(color_stops, 4)
            shape.set_linear_gradient(grad)

        :param GradientStruct grad: The linear gradient fill.

        :return:
            - INVALID_ARGUMENT An invalid PaintStruct pointer.
            - MEMORY_CORRUPTION An invalid GradientStruct pointer.
        :rtype: Result

        .. note::
            Either a solid color or a gradient fill is applied, depending on what was set as last.
        .. seealso:: Shape.set_fill_rule()
        """
        self.thorvg_lib.tvg_shape_set_linear_gradient.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(GradientStruct),
        ]
        self.thorvg_lib.tvg_shape_set_linear_gradient.restype = Result
        return self.thorvg_lib.tvg_shape_set_linear_gradient(
            ctypes.pointer(self._paint),
            ctypes.pointer(grad._grad),  # type: ignore
        )

    def set_radial_gradient(self, grad: "Gradient") -> Result:
        """Sets the radial gradient fill for all of the figures from the path.

        The parts of the shape defined as inner are filled.

        .. code-block:: python

            from thorvg_python import Engine, Shape, RadialGradient, ColorStop

            engine = Engine()
            shape = Shape(engine)
            grad = RadialGradient(engine)
            grad.set(550, 550, 50)
            color_stops = [
                ColorStop(0.0 , 0,   0,   0,   255),
                ColorStop(0.25, 255, 0,   0,   255),
                ColorStop(0.5 , 0,   255, 0,   255),
                ColorStop(1.0 , 0,   0,   255, 255)
            ]
            grad.set_color_stops(color_stops, 4)
            shape.set_radial_gradient(grad)

        :param GradientStruct grad: The radial gradient fill.

        :return: INVALID_ARGUMENT An invalid PaintStruct pointer.
            MEMORY_CORRUPTION An invalid GradientStruct pointer.
        :rtype: Result

        .. note::
            Either a solid color or a gradient fill is applied, depending on what was set as last.
        .. seealso:: Shape.set_fill_rule()
        """
        self.thorvg_lib.tvg_shape_set_radial_gradient.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(GradientStruct),
        ]
        self.thorvg_lib.tvg_shape_set_radial_gradient.restype = Result
        return self.thorvg_lib.tvg_shape_set_radial_gradient(
            ctypes.pointer(self._paint),
            ctypes.pointer(grad._grad),  # type: ignore
        )

    def get_gradient(self) -> Tuple[Result, Union["LinearGradient", "RadialGradient"]]:
        """Gets the gradient fill of the shape.

        The function does not allocate any data.

        :return: INVALID_ARGUMENT An invalid pointer passed as an argument.
        :rtype: Result
        :return: The gradient fill.
        :rtype: GradientStruct
        """
        grad_ptr = ctypes.POINTER(GradientStruct)()
        self.thorvg_lib.tvg_shape_get_gradient.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(ctypes.POINTER(GradientStruct)),
        ]
        self.thorvg_lib.tvg_shape_get_gradient.restype = Result
        result = self.thorvg_lib.tvg_shape_get_gradient(
            ctypes.pointer(self._paint),
            ctypes.pointer(grad_ptr),
        )
        _, tvg_type = Gradient(self.engine, grad_ptr.contents).get_type()
        if tvg_type == TvgType.LINEAR_GRAD:
            return result, LinearGradient(self.engine, grad_ptr.contents)
        elif tvg_type == TvgType.RADIAL_GRAD:
            return result, RadialGradient(self.engine, grad_ptr.contents)
        else:
            raise RuntimeError(f"Invalid gradient TvgType: {tvg_type}")
