#!/usr/bin/env python3
import ctypes
from enum import IntEnum


class CanvasPointer(ctypes.c_void_p):
    """A structure responsible for managing and drawing graphical elements.

    It sets up the target buffer, which can be drawn on the screen. It stores the PaintPointer objects (Shape, Scene, Picture).

    .. note::
        You should use ``Canvas`` class instead.
    """


class PaintPointer(ctypes.c_void_p):
    """A structure representing a graphical element.

    .. warning::
        The PaintPointer objects cannot be shared between Canvases.

    .. note::
        You should use ``Paint`` class instead.
    """


class GradientPointer(ctypes.c_void_p):
    """A structure representing a gradient fill of a PaintPointer object.

    .. note::
        You should use ``LinearGradient`` or ``RadialGradient`` class instead.
    """


class SaverPointer(ctypes.c_void_p):
    """A structure representing an object that enables to save a PaintPointer object into a file.

    .. note::
        You should use `Saver` class instead.
    """


class AnimationPointer(ctypes.c_void_p):
    """A structure representing an animation controller object.

    .. note::
        You should use ``Animation`` class instead.
    """


class AccessorPointer(ctypes.c_void_p):
    """A structure representing an object that enables iterating through a scene's descendents.

    .. note::
        You should use ``Accessor`` class instead
    """


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
    UNKNOWN = 255

    @classmethod
    def from_param(cls, obj: int) -> int:
        return int(obj)


class Colorspace(IntEnum):
    """Enumeration specifying the methods of combining the 8-bit color channels into 32-bit color.

    .. versionchanged:: 0.13
        Added ``ABGR8888S`` and ``ARGB8888S``

    .. versionchanged:: 1.0
        Added ``UNKNOWN``
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

    #: Unknown channel data. This is reserved for an initial ColorSpace value.
    UNKNOWN = 255

    @classmethod
    def from_param(cls, obj: int) -> int:
        return int(obj)


class EngineOption(IntEnum):
    """Enumeration to specify rendering engine behavior.

    .. note::
        The availability or behavior of ``EngineMethod.SMART_RENDER`` may vary depending on platform or backend support.
        It attempts to optimize rendering performance by updating only the regions  of the canvas that have
        changed between frames (partial redraw). This can be highly effective in scenarios  where most of the
        canvas remains static and only small portions are updated—such as simple animations or GUI interactions.
        However, in complex scenes where a large portion of the canvas changes frequently (e.g., full-screen animations
        or heavy object movements), the overhead of tracking changes and managing update regions may outweigh the benefits,
        resulting in decreased performance compared to the default rendering mode. Thus, it is recommended to benchmark
        both modes in your specific use case to determine the optimal setting.

    .. versionadded:: 1.0
    """

    #: No engine options are enabled.
    #: This may be used to explicitly disable all optional behaviors.
    NONE = 0

    #: Uses the default rendering mode
    DEFAULT = 1

    #: Enables automatic partial (smart) rendering optimizations.
    SMART_RENDER = 2


class MaskMethod(IntEnum):
    """Enumeration indicating the method used in the masking of two objects - the target and the source."""

    #: No composition is applied.
    NONE = 0

    #: Alpha Masking using the masking target's pixels as an alpha value.
    ALPHA = 1

    #: Alpha Masking using the complement to the masking target's pixels as an alpha value.
    INVERSE_ALPHA = 2

    #: Alpha Masking using the grayscale (0.2126R + 0.7152G + 0.0722*B) of the masking target's pixels.
    LUMA = 3

    #: Alpha Masking using the grayscale (0.2126R + 0.7152G + 0.0722*B) of the complement to the masking target's pixels.
    INVERSE_LUMA = 4

    #: Combines the target and source objects pixels using target alpha. (T * TA) + (S * (255 - TA))
    ADD = 5

    #: Subtracts the source color from the target color while considering their respective target alpha. (T * TA) - (S * (255 - TA))
    SUBTRACT = 6

    #: Computes the result by taking the minimum value between the target alpha and the source alpha and multiplies it with the target color. (T * min(TA, SA))
    INTERSECT = 7

    #: Calculates the absolute difference between the target color and the source color multiplied by the complement of the target alpha. abs(T - S * (255 - TA))
    DIFFERENCE = 8

    #: Where multiple masks intersect, the highest transparency value is used.
    LIGHTEN = 9

    #: Where multiple masks intersect, the lowest transparency value is used.
    DARKEN = 10

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

    #: Combine with HSL(Sh + Ds + Dl) then convert it to RGB.
    HUE = 12

    #: Combine with HSL(Dh + Ss + Dl) then convert it to RGB.
    SATURATION = 13

    #: Combine with HSL(Sh + Ss + Dl) then convert it to RGB.
    COLOR = 14

    #: Combine with HSL(Dh + Ds + Sl) then convert it to RGB.
    LUMINOSITY = 15

    #: Simply adds pixel values of one layer with the other. (S + D)
    ADD = 16

    #: Used for intermediate composition.
    COMPOSITION = 255

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

    #: The stroke ends exactly at each of the two endpoints of a sub-path.
    #: For zero length sub-paths no stroke is rendered.
    BUTT = 0

    #: The stroke is extended in both endpoints of a sub-path by a half circle,
    #: with a radius equal to half of the stroke width. For zero length sub-paths a full circle is rendered.
    ROUND = 1

    #: The stroke is extended in both endpoints of a sub-path by a rectangle,
    #: with the width equal to the stroke width and the length equal to half of the stroke width.
    #: For zero length sub-paths the square is rendered with the size of the stroke width.
    SQUARE = 2

    @classmethod
    def from_param(cls, obj: int) -> int:
        return int(obj)


class StrokeJoin(IntEnum):
    """Enumeration specifying how to fill the area outside the gradient bounds."""

    #: The outer corner of the joined path segments is spiked.
    #: The spike is created by extension beyond the join point of the outer edges of the stroke until they intersect.
    #: If the extension goes beyond the limit, the join style is converted to the Bevel styl
    MITER = 0

    #: The outer corner of the joined path segments is rounded.
    #: The circular region is centered at the join point.
    ROUND = 1

    #: The outer corner of the joined path segments is bevelled at the join point.
    #: The triangular region of the corner is enclosed by a straight line between the outer corners of each stroke.
    BEVEL = 2

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
    NON_ZERO = 0

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

    # offset: float  #: The relative position of the color.
    # r: int  #: The red color channel value in the range [0 ~ 255].
    # g: int  #: The green color channel value in the range [0 ~ 255].
    # b: int  #: The blue color channel value in the range [0 ~ 255].
    # a: int  #: The alpha channel value in the range [0 ~ 255], where 0 is completely transparent and 255 is opaque.


class TextWrap(ctypes.Structure):
    """A data structure storing the information about the color and its relative position inside the gradient bounds."""

    #: Do not wrap text. Text is rendered on a single line and may overflow the bounding area.
    TVG_TEXT_WRAP_NONE = 0

    #: Wrap at the character level. If a word cannot fit, it is broken into individual characters to fit the line.
    TVG_TEXT_WRAP_CHARACTER = 1

    #: Wrap at the word level. Words that do not fit are moved to the next line.
    TVG_TEXT_WRAP_WORD = 2

    #: Smart choose wrapping method: word wrap first, falling back to character wrap if a word does not fit.
    TVG_TEXT_WRAP_SMART = 3

    #: Truncate overflowing text and append an ellipsis ("...") at the end. Typically used for single-line labels.
    TVG_TEXT_WRAP_ELLIPSIS = 4

    #: Reserved. No Support.
    TVG_TEXT_WRAP_HYPHENATION = 5


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


class TextMetrics(ctypes.Structure):
    """Describes the font metrics of a text object.

    Provides the basic vertical layout metrics used for text rendering,
    such as ascent, descent, and line spacing (linegap).

    .. seealso:: Text.get_metrics()
    .. note::
        Experimental API
    """
    _fields_ = [
        ("ascent", ctypes.c_float),
        ("descent", ctypes.c_float),
        ("linegap", ctypes.c_float),
        ("advance", ctypes.c_float),
    ]
    ascent: float #: Distance from the baseline to the top of the highest glyph (usually positive).
    descent: float #: Distance from the baseline to the bottom of the lowest glyph (usually negative, as in TTF).
    linegap: float #: Additional spacing recommended between lines (leading).
    advance: float #: The total vertical advance between lines of text: ascent - descent + linegap (i.e., ascent + |descent| + linegap when descent is negative).

"""Callback function type for resolving external assets.

This callback is invoked when a Picture requires an external asset
(such as an image or font resource). Implementations should load the asset
into the given ``paint`` object.

:param PaintPointer paint: The target paint object where the resolved asset will be loaded.
:param str src: The source path, identifier, or URI of the asset to be resolved.
:param bytes data: User-provided custom data passed to the callback for context.

:return: true if the asset was successfully resolved and loaded into paint, otherwise false.
:rtype: bool

.. seealso:: Picture.set_asset_resolver()
.. note::
    Experimental API
"""
PictureAssetResolverType = ctypes.CFUNCTYPE(
    ctypes.c_bool, PaintPointer, ctypes.c_char_p, ctypes.c_void_p
)
