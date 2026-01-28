#!/usr/bin/env python3
import ctypes
from enum import IntEnum


class CanvasStruct(ctypes.Structure):
    """A structure responsible for managing and drawing graphical elements.

    It sets up the target buffer, which can be drawn on the screen. It stores the PaintStruct objects (Shape, Scene, Picture).

    .. note::
        You should use ``Canvas`` class instead.
    """


class PaintStruct(ctypes.Structure):
    """A structure representing a graphical element.

    .. warning::
        The PaintStruct objects cannot be shared between Canvases.

    .. note::
        You should use ``Paint`` class instead.
    """


class GradientStruct(ctypes.Structure):
    """A structure representing a gradient fill of a PaintStruct object.

    .. note::
        You should use ``LinearGradient`` or ``RadialGradient`` class instead.
    """


class SaverStruct(ctypes.Structure):
    """A structure representing an object that enables to save a PaintStruct object into a file.

    .. note::
        You should use `Saver` class instead.
    """


class AnimationStruct(ctypes.Structure):
    """A structure representing an animation controller object.

    .. note::
        You should use ``Animation`` class instead.
    """


class EngineBackend(IntEnum):
    """Enumeration specifying the engine type used for the graphics backend. For multiple backends bitwise operation is allowed."""

    SW = 2  #: CPU rasterizer.
    GL = 4  #: OpenGL rasterizer.

    @classmethod
    def from_param(cls, obj: int) -> int:
        return int(obj)


class Result(IntEnum):
    """Enumeration specifying the result from the APIs.

    All ThorVG APIs could potentially return one of the values in the list.
    Please note that some APIs may additionally specify the reasons that trigger their return values.
    """

    #: The value returned in case of a correct request execution.
    SUCCESS = 0

    #: The value returned in the event of a problem with the arguments given to the API
    #: - e.g. empty paths or null pointers.
    INVALID_ARGUMENT = 1

    #: The value returned in case the request cannot be processed
    #: - e.g. asking for properties of an object, which does not exist.
    INSUFFICIENT_CONDITION = 2

    #: The value returned in case of unsuccessful memory allocation.
    FAILED_ALLOCATION = 3

    #: The value returned in the event of bad memory handling
    #: - e.g. failing in pointer releasing or casting
    MEMORY_CORRUPTION = 4

    #: The value returned in case of choosing unsupported engine features(options).
    NOT_SUPPORTED = 5

    #: The value returned in all other cases.
    UNKNOWN = 6

    @classmethod
    def from_param(cls, obj: int) -> int:
        return int(obj)


class CompositeMethod(IntEnum):
    """Enumeration indicating the method used in the composition of two objects - the target and the source.

    .. deprecated:: 0.15
        CLIP_PATH deprecated. Use Paint::clip() instead.

    .. versionchanged:: 0.9
        Added LUMA_MASK

    .. versionchanged:: 0.14
        Added INVERSE_LUMA_MAS
    """

    #: No composition is applied.
    NONE = 0

    #: The intersection of the source and the target is determined and only the resulting pixels
    #: from the source are rendered. Note that ClipPath only supports the Shape type.
    CLIP_PATH = 1

    #: The pixels of the source and the target are alpha blended.
    #: As a result, only the part of the source, which intersects with the target is visible.
    ALPHA_MASK = 2

    #: The pixels of the source and the complement to the target's pixels are alpha blended.
    #: As a result, only the part of the source which is not covered by the target is visible.
    INVERSE_ALPHA_MASK = 3

    #: The source pixels are converted to grayscale (luma value) and alpha blended with the target.
    #: As a result, only the part of the source which intersects with the target is visible.
    LUMA_MASK = 4

    #: The source pixels are converted to grayscale (luma value) and complement to the target's pixels
    #: are alpha blended. As a result, only the part of the source which is not covered by the target is visible.
    INVERSE_LUMA_MASK = 5

    @classmethod
    def from_param(cls, obj: int) -> int:
        return int(obj)


class BlendMethod(IntEnum):
    """Enumeration indicates the method used for blending paint.
    Please refer to the respective formulas for each method.
    """

    #: Perform the alpha blending (default). S if (Sa == 255),
    #: otherwise (Sa * S) + (255 - Sa) * D
    NORMAL = 0

    #: Takes the RGB channel values from 0 to 255 of each pixel in the top layer and
    #: multiplies them with the values for the corresponding pixel from the bottom layer.
    #: (S * D)
    MULTIPLY = 1

    #: The values of the pixels in the two layers are inverted, multiplied, and then inverted again.
    #: (S + D) - (S * D)
    SCREEN = 2

    #: Combines Multiply and Screen blend modes. (2 * S * D) if (2 * D < Da),
    #: otherwise (Sa * Da) - 2 * (Da - S) * (Sa - D)
    OVERLAY = 3

    #: Creates a pixel that retains the smallest components of the top and bottom layer pixels.
    #: min(S, D)
    DARKEN = 4

    #: Opposite action of Darken. max(S, D)
    LIGHTEN = 5

    #: Divides the bottom layer by the inverted top layer. D / (255 - S)
    COLORDODGE = 6

    #: Divides the inverted bottom layer by the top layer, then inverts the result.
    #: 255 - (255 - D) / S
    COLORBURN = 7

    #: Same as Overlay but with color roles reversed. (2 * S * D) if (S < Sa),
    #: otherwise (Sa * Da) - 2 * (Da - S) * (Sa - D)
    HARDLIGHT = 8

    #: Same as Overlay but applying pure black or white does not result in pure black or white.
    #: (1 - 2 * S) * (D ^ 2) + (2 * S * D)
    SOFTLIGHT = 9

    #: Subtracts the bottom layer from the top layer or vice versa, always non-negative.
    #: (S - D) if (S > D), otherwise (D - S)
    DIFFERENCE = 10

    #: Result is twice the product of the top and bottom layers, subtracted from their sum.
    #: S + D - (2 * S * D)
    EXCLUSION = 11

    #: Reserved. Not supported.
    HUE = 12

    #: Reserved. Not supported.
    SATURATION = 13

    #: Reserved. Not supported.
    COLOR = 14

    #: Reserved. Not supported.
    LUMINOSITY = 15

    #: Simply adds pixel values of one layer with the other. (S + D)
    ADD = 16

    #: Reserved. Not supported.
    HARDMIX = 17

    @classmethod
    def from_param(cls, obj: int) -> int:
        return int(obj)


class Identifier(IntEnum):
    """see TvgType

    .. deprecated:: 0.15
    """

    UNDEF = 0  #: Undefined type.
    SHAPE = 1  #: A shape type paint.
    SCENE = 2  #: A scene type paint.
    PICTURE = 3  #: A picture type paint.
    LINEAR_GRAD = 4  #: A linear gradient type.
    RADIAL_GRAD = 5  #: A radial gradient type.
    TEXT = 6  #: A text type paint.

    @classmethod
    def from_param(cls, obj: int) -> int:
        return int(obj)


class TvgType(IntEnum):
    """Enumeration indicating the ThorVG object type value.

    ThorVG's drawing objects can return object type values, allowing you to identify the specific type of each object.
    """

    UNDEF = 0  #: Undefined type.
    SHAPE = 1  #: A shape type paint.
    SCENE = 2  #: A scene type paint.
    PICTURE = 3  #: A picture type paint.
    TEXT = 4  #: A text type paint.
    LINEAR_GRAD = 10  #: A linear gradient type.
    RADIAL_GRAD = 11  #: A radial gradient type.

    @classmethod
    def from_param(cls, obj: int) -> int:
        return int(obj)


class PathCommand(IntEnum):
    """Enumeration specifying the values of the path commands accepted by ThorVG."""

    #: Ends the current sub-path and connects it with its initial point.
    #: Corresponds to Z command in the SVG path commands.
    CLOSE = 0

    #: Sets a new initial point of the sub-path and a new current point.
    #: Corresponds to M command in the SVG path commands.
    MOVE_TO = 1

    #: Draws a line from the current point to the given point and sets a new value of the current point.
    #: Corresponds to L command in the SVG path commands.
    LINE_TO = 2

    #: Draws a cubic Bezier curve from the current point to the given point using
    #: two given control points and sets a new value of the current point.
    #: Corresponds to C command in the SVG path commands.
    CUBIC_TO = 3

    @classmethod
    def from_param(cls, obj: int) -> int:
        return int(obj)


class StrokeCap(IntEnum):
    """Enumeration determining the ending type of a stroke in the open sub-paths."""

    #: The stroke is extended in both endpoints of a sub-path by a rectangle,
    #: with the width equal to the stroke width and the length equal to half of the stroke width.
    #: For zero length sub-paths the square is rendered with the size of the stroke width.
    SQUARE = 0

    #: The stroke is extended in both endpoints of a sub-path by a half circle,
    #: with a radius equal to half of the stroke width. For zero length sub-paths a full circle is rendered.
    ROUND = 1

    #: The stroke ends exactly at each of the two endpoints of a sub-path.
    #: For zero length sub-paths no stroke is rendered.
    BUTT = 2

    @classmethod
    def from_param(cls, obj: int) -> int:
        return int(obj)


class StrokeJoin(IntEnum):
    """Enumeration specifying how to fill the area outside the gradient bounds."""

    #: The outer corner of the joined path segments is bevelled at the join point.
    #: The triangular region of the corner is enclosed by a straight line between the outer corners of each stroke.
    BEVEL = 0

    #: The outer corner of the joined path segments is rounded.
    #: The circular region is centered at the join point.
    ROUND = 1

    #: The outer corner of the joined path segments is spiked.
    #: The spike is created by extension beyond the join point of the outer edges of the stroke until they intersect.
    #: If the extension goes beyond the limit, the join style is converted to the Bevel styl
    MITER = 2

    @classmethod
    def from_param(cls, obj: int) -> int:
        return int(obj)


class StrokeFill(IntEnum):
    """Enumeration specifying how to fill the area outside the gradient bounds."""

    #: The remaining area is filled with the closest stop color.
    PAD = 0

    #: The gradient pattern is reflected outside the gradient area
    #: until the expected region is filled.
    REFLECT = 1

    #: The gradient pattern is repeated continuously beyond the gradient area
    #: until the expected region is filled.
    REPEAT = 2

    @classmethod
    def from_param(cls, obj: int) -> int:
        return int(obj)


class FillRule(IntEnum):
    """Enumeration specifying the algorithm used to establish which parts of the shape
    are treated as the inside of the shape.
    """

    #: A line from the point to a location outside the shape is drawn.
    #: The intersections of the line with the path segment of the shape are counted.
    #: Starting from zero, if the path segment of the shape crosses the line clockwise,
    #: one is added, otherwise one is subtracted. If the resulting sum is non zero,
    #: the point is inside the shape.
    WINDING = 0

    #: A line from the point to a location outside the shape is drawn
    #: and its intersections with the path segments of the shape are counted.
    #: If the number of intersections is an odd number, the point is inside the shape.
    EVEN_ODD = 1

    @classmethod
    def from_param(cls, obj: int) -> int:
        return int(obj)


class ColorStop(ctypes.Structure):
    """A data structure storing the information about the color and its relative position inside the gradient bounds."""

    _fields_ = [
        ("offset", ctypes.c_float),
        ("r", ctypes.c_uint8),
        ("g", ctypes.c_uint8),
        ("b", ctypes.c_uint8),
        ("a", ctypes.c_uint8),
    ]

    offset: float  #: The relative position of the color.
    r: int  #: The red color channel value in the range [0 ~ 255].
    g: int  #: The green color channel value in the range [0 ~ 255].
    b: int  #: The blue color channel value in the range [0 ~ 255].
    a: int  #: The alpha channel value in the range [0 ~ 255], where 0 is completely transparent and 255 is opaque.


class PointStruct(ctypes.Structure):
    """A data structure representing a point in two-dimensional space."""

    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
    ]


class Matrix(ctypes.Structure):
    """A data structure representing a three-dimensional matrix.

    The elements e11, e12, e21 and e22 represent the rotation matrix, including the scaling factor.

    The elements e13 and e23 determine the translation of the object along the x and y-axis, respectively.

    The elements e31 and e32 are set to 0, e33 is set to 1.
    """

    _fields_ = [
        ("e11", ctypes.c_float),
        ("e12", ctypes.c_float),
        ("e13", ctypes.c_float),
        ("e21", ctypes.c_float),
        ("e22", ctypes.c_float),
        ("e23", ctypes.c_float),
        ("e31", ctypes.c_float),
        ("e32", ctypes.c_float),
        ("e33", ctypes.c_float),
    ]


class MempoolPolicy(IntEnum):
    """Enumeration specifying the methods of Memory Pool behavior policy."""

    DEFAULT = 0  #: Default behavior that ThorVG is designed to.
    SHAREABLE = 1  #: Memory Pool is shared among canvases.
    INDIVIDUAL = 2  #: Allocate designated memory pool that is used only by the current canvas instance.

    @classmethod
    def from_param(cls, obj: int) -> int:
        return int(obj)


class Colorspace(IntEnum):
    """Enumeration specifying the methods of combining the 8-bit color channels into 32-bit color.

    .. versionchanged:: 0.13
        Added ``ABGR8888S`` and ``ARGB8888S``
    """

    #: The channels are joined in the order: alpha, blue, green, red.
    #: Colors are alpha-premultiplied. (a << 24 | b << 16 | g << 8 | r)
    ABGR8888 = 0

    #: The channels are joined in the order: alpha, red, green, blue.
    #: Colors are alpha-premultiplied. (a << 24 | r << 16 | g << 8 | b)
    ARGB8888 = 1

    #: The channels are joined in the order: alpha, blue, green, red.
    #: Colors are un-alpha-premultiplied.
    ABGR8888S = 2

    #: The channels are joined in the order: alpha, red, green, blue.
    #: Colors are un-alpha-premultiplied.
    ARGB8888S = 3

    @classmethod
    def from_param(cls, obj: int) -> int:
        return int(obj)
