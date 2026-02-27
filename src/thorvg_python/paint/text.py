#!/usr/bin/env python3
import ctypes
from typing import Optional, Tuple

from ..base import GradientPointer, PaintPointer, Result, TextMetrics, TextWrap
from ..engine import Engine
from ..gradient import Gradient
from . import Paint


class Text(Paint):
    """
    Text API

    A class to represent text objects in a graphical context, allowing for rendering and manipulation of unicode text.
    """

    def __init__(self, engine: Engine, paint: Optional[PaintPointer] = None):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if paint is None:
            self._paint = self._new()
        else:
            self._paint = paint

    def _new(self) -> PaintPointer:
        """Creates a new text object.

        This function allocates and returns a new Text instance.
        To properly destroy the Text object, use ``Paint.rel()``

        :return: A pointer to the newly created Text object.
        :rtype: thorvg_python.base.PaintPointer

        .. versionadded:: 0.15

        .. note:: You need not call this method as it is auto called when initializing ``Text()``.
        """
        self.thorvg_lib.tvg_text_new.restype = PaintPointer
        return self.thorvg_lib.tvg_text_new()

    def set_font(
        self,
        name: Optional[str] = None,
    ) -> Result:
        """Sets the font family for the text.

        This function specifies the name of the font to be used when rendering text.

        :param name: The name of the font. This should match a font available through the canvas backend.
            If set to ``None``, ThorVG will attempt to select a fallback font available on the engine.

        :return:
            - Result.INVALID_ARGUMENT A ``None`` passed as the ``paint`` argument.
            - Result.INSUFFICIENT_CONDITION  The specified ``name`` cannot be found.

        .. note::
            This function only sets the font family name. Use ``size()`` to define the font size.
        .. note::
            If the ``name`` is not specified, ThorVG will select an available fallback font.

        .. seealso:: Text.set_size()
        .. seealso:: Engine.font_load()

        .. versionadded:: 1.0
        """
        if name is not None and name != "":
            name_bytes = name.encode() + b"\x00"
            name_arr_type = ctypes.c_char * len(name_bytes)
            name_arr_type_ptr = ctypes.POINTER(name_arr_type)
            name_arr = name_arr_type.from_buffer_copy(name_bytes)
            name_arr_ptr = ctypes.pointer(name_arr)
        else:
            name_arr_type_ptr = ctypes.c_void_p  # type: ignore
            name_arr_ptr = ctypes.c_void_p()  # type: ignore

        self.thorvg_lib.tvg_text_set_font.argtypes = [
            PaintPointer,
            name_arr_type_ptr,
        ]
        self.thorvg_lib.tvg_text_set_font.restype = Result
        return self.thorvg_lib.tvg_text_set_font(
            self._paint,
            name_arr_ptr,
        )

    def set_size(self, size: float) -> Result:
        """Sets the font size for the text.

        This function sets the font size used during text rendering.
        The size is specified in point units, and supports floating-point precision
        for smooth scaling and animation effects.

        :param float size: The font size in points. Must be greater than 0.0.

        :return:
            - Result.INVALID_ARGUMENT A ``None`` passed as the ``paint`` argument.
            - Result.INVALID_ARGUMENT if the ``size`` is less than or equal to 0.
        :rtype: thorvg_python.base.Result

        .. note::
            Use this function in combination with ``font()`` to fully define text appearance.
        .. note::
            Fractional sizes (e.g., 12.5) are supported for sub-pixel rendering and animations.

        .. seealso:: Text.set_font()

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_text_set_size.argtypes = [
            PaintPointer,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_text_set_size.restype = Result
        return self.thorvg_lib.tvg_text_set_size(
            self._paint,
            ctypes.c_float(size),
        )

    def set_text(
        self,
        utf8: str,
    ) -> Result:
        """Assigns the given unicode text to be rendered.

        This function sets the unicode text that will be displayed by the rendering system.
        The text is set according to the specified UTF encoding method, which defaults to UTF-8.

        :param str utf8: The multi-byte text encoded with utf8 string to be rendered.

        :rtyle: Result

        .. versionadded: 1.0
        """
        utf8_bytes = utf8.encode() + b"\x00"
        text_arr_type = ctypes.c_char * len(utf8_bytes)
        text_arr = text_arr_type.from_buffer_copy(utf8_bytes)
        self.thorvg_lib.tvg_text_set_text.argtypes = [
            PaintPointer,
            ctypes.POINTER(text_arr_type),
        ]
        self.thorvg_lib.tvg_text_set_text.restype = Result
        return self.thorvg_lib.tvg_text_set_text(
            self._paint,
            ctypes.pointer(text_arr),
        )

    def align(self, x: float, y: float) -> Result:
        """Sets text alignment or anchor per axis.

        If layout width/height is set on an axis, align within the layout box.
        Otherwise, treat it as an anchor within the text bounds which point of
        the text box is pinned to the paint position.

        :param float x: Horizontal alignment/anchor in [0..1]: 0=left/start, 0.5=center, 1=right/end. (Default is 0)
        :param float y: Vertical alignment/anchor in [0..1]: 0=top, 0.5=middle, 1=bottom. (Default is 0)

        .. versionadded:: 1.0

        .. seealso:: Text.layout()
        """
        self.thorvg_lib.tvg_text_align.argtypes = [
            PaintPointer,
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_text_align.restype = Result
        return self.thorvg_lib.tvg_text_align(
            self._paint,
            ctypes.c_float(x),
            ctypes.c_float(y),
        )

    def layout(self, w: float, h: float) -> Result:
        """Sets the virtual layout box (constraints) for the text.

        If width/height is set on an axis, that axis is constrained by a virtual layout box and
        the text may wrap/align inside it. If width/height == 0, the axis is
        unconstrained and ``Text.align()`` acts as an anchor on that axis.

        :param float w: Layout width in user space. Use 0 for no horizontal constraint. (Default is 0)
        :param float h: Layout height in user space. Use 0 for no vertical constraint. (Default is 0)

        .. note::
            This defines constraints only; alignment/anchoring is controlled by ``align()``.
        .. versionadded:: 1.0

        .. seealso:: Text.align()
        .. seealso:: Text.spacing()
        """
        self.thorvg_lib.tvg_text_layout.argtypes = [
            PaintPointer,
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_text_layout.restype = Result
        return self.thorvg_lib.tvg_text_layout(
            self._paint,
            ctypes.c_float(w),
            ctypes.c_float(h),
        )

    def wrap_mode(self, mode: TextWrap) -> Result:
        """Sets the text wrapping mode for this text object.

        This method controls how the text is laid out when it exceeds the available space.
        The wrapping mode determines whether text is truncated, wrapped by character or word,
        or adjusted automatically. An ellipsis mode is also available for truncation with "...".

        :param thorvg_python.base.TextWrap mode: The wrapping strategy to apply. Default is ``NONE``.

        .. seealso:: TextWrap
        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_text_wrap_mode.argtypes = [
            PaintPointer,
            ctypes.c_uint8,
        ]
        self.thorvg_lib.tvg_text_wrap_mode.restype = Result
        return self.thorvg_lib.tvg_text_wrap_mode(
            self._paint,
            mode,
        )

    def spacing(self, letter: float, line: float) -> Result:
        """Set the spacing scale factors for text layout.

        This function adjusts the letter spacing (horizontal space between glyphs) and
        line spacing (vertical space between lines of text) using scale factors.

        Both values are relative to the font's default metrics:
        - The letter spacing is applied as a scale factor to the glyph's advance width.
        - The line spacing is applied as a scale factor to the glyph's advance height.

        :param float letter: The scale factor for letter spacing.
            Values > 1.0 increase spacing, values < 1.0 decrease it.
            Must be greater than or equal to 0.0. (default: 1.0)

        :param line: The scale factor for line spacing.
            Values > 1.0 increase line spacing, values < 1.0 decrease it.
            Must be greater than or equal to 0.0. (default: 1.0)

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_text_spacing.argtypes = [
            PaintPointer,
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_text_spacing.restype = Result
        return self.thorvg_lib.tvg_text_spacing(
            self._paint,
            ctypes.c_float(letter),
            ctypes.c_float(line),
        )

    def set_italic(self, shear: float) -> Result:
        """Apply an italic (slant) transformation to the text.

        This function applies a shear transformation to simulate an italic (oblique) style
        for the current text object. The shear factor determines the degree of slant
        applied along the X-axis.

        :param float shear: The shear factor to apply. A value of 0.0 applies no slant,
            while values around 0.5 result in a strong slant.
            Must be in the range [0.0, 0.5]. Recommended value is 0.18.

        :return: Result.INVALID_ARGUMENT A ``None`` passed as the ``paint`` argument.
        :rtype: thorvg_python.base.Result

        .. note::
            The ``shear`` factor will be clamped to the valid range if it exceeds the limits.
        .. note::
            This does not require the font itself to be italic.
            It visually simulates the effect by applying a transformation matrix.

        .. warning::
            Excessive slanting may cause visual distortion depending on the font and size.

        .. seealso:: Text.set_font()

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_text_set_italic.argtypes = [
            PaintPointer,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_text_set_italic.restype = Result
        return self.thorvg_lib.tvg_text_set_italic(
            self._paint,
            ctypes.c_float(shear),
        )

    def set_outline(self, width: float, r: int, g: int, b: int) -> Result:
        """Sets an outline (stroke) around the text object.

        This function adds an outline to the text with the specified width and RGB color.
        The outline enhances the visibility of the text by rendering a stroke around its glyphs.

        :param width width: The width of the outline. Must be positive value. (The default is 0)
        :param int r: Red component of the outline color (0–255).
        :param int g: Green component of the outline color (0–255).
        :param int b: Blue component of the outline color (0–255).

        .. note::
            To disable the outline, set ``width`` to 0.
        .. seealso:: Text.set_fill_color() to set the main text fill color.

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_text_set_outline.argtypes = [
            PaintPointer,
            ctypes.c_float,
            ctypes.c_int8,
            ctypes.c_int8,
            ctypes.c_int8,
        ]
        self.thorvg_lib.tvg_text_set_outline.restype = Result
        return self.thorvg_lib.tvg_text_set_outline(
            self._paint,
            ctypes.c_float(width),
            ctypes.c_int8(r),
            ctypes.c_int8(g),
            ctypes.c_int8(b),
        )

    def set_color(
        self,
        r: int,
        g: int,
        b: int,
    ) -> Result:
        """Sets the text solid color.

        :param int r The red color channel value in the range [0 ~ 255]. The default value is 0.
        :param int g: The green color channel value in the range [0 ~ 255]. The default value is 0.
        :param int b: The blue color channel value in the range [0 ~ 255]. The default value is 0.

        :return: Result.INVALID_ARGUMENT A ``None`` passed as the ``paint`` argument.
        :rtype: thorvg_python.base.Result

        .. note::
            Either a solid color or a gradient fill is applied, depending on what was set as last.
        .. seealso:: Text.set_font()
        .. seealso:: Text.set_outline()

        .. versionadded:: 0.15
        """
        self.thorvg_lib.tvg_text_set_color.argtypes = [
            PaintPointer,
            ctypes.c_uint8,
            ctypes.c_uint8,
            ctypes.c_uint8,
        ]
        self.thorvg_lib.tvg_text_set_color.restype = Result
        return self.thorvg_lib.tvg_text_set_color(
            self._paint,
            ctypes.c_uint8(r),
            ctypes.c_uint8(g),
            ctypes.c_uint8(b),
        )

    def set_gradient(
        self,
        gradient: Gradient,
    ) -> Result:
        """Sets the gradient fill for the text.

        :param thorvg.base.GradientPointer gradient: The linear or radial gradient fill

        :return:
            - Result.INVALID_ARGUMENT A ``None`` passed as the ``paint`` argument.
            - Result.MEMORY_CORRUPTION An invalid GradientPointer.
        :rtype: thorvg_python.base.Result

        .. note::
            Either a solid color or a gradient fill is applied, depending on what was set as last.
        .. seealso:: Text.set_font()

        .. versionadded:: 0.15
        """
        self.thorvg_lib.tvg_text_set_gradient.argtypes = [
            PaintPointer,
            GradientPointer,
        ]
        self.thorvg_lib.tvg_text_set_gradient.restype = Result
        return self.thorvg_lib.tvg_text_set_gradient(
            self._paint,
            gradient._grad,  # type: ignore
        )

    def get_metrics(self) -> Tuple[Result, TextMetrics]:
        """Retrieves the layout metrics of the text object.

        Fills the provided `TextMetrics` structure with the font layout values of this text object,
        such as ascent, descent, linegap, and line advance.

        The returned values reflect the font size applied to the text object,
        but do not include any transformations (e.g., scale, rotation, or translation).

        :return: A `TextMetrics` structure filled with the resulting values.
        :rtype: thorvg_python.base.TextMetrics
        :return: TVG_RESULT_INSUFFICIENT_CONDITION if no font or size has been set yet.
        :rtype: thorvg_python.base.Result

        .. seealso:: TextMetrics
        .. note::
            Experimental API
        """
        metrics = TextMetrics()
        self.thorvg_lib.tvg_text_get_metrics.argtypes = [
            PaintPointer,
            ctypes.POINTER(TextMetrics),
        ]
        self.thorvg_lib.tvg_text_get_metrics.restype = Result
        result = self.thorvg_lib.tvg_text_get_metrics(
            self._paint,
            ctypes.pointer(metrics),
        )
        return result, metrics

    def font_load(
        self,
        path: str,
    ) -> Result:
        """Loads a scalable font data from a file.

        ThorVG efficiently caches the loaded data using the specified ``path`` as a key.
        This means that loading the same file again will not result in duplicate operations;
        instead, ThorVG will reuse the previously loaded font data.

        :param str path: The path to the font file.

        :return:
            - Result.INVALID_ARGUMENT An invalid ``path`` passed as an argument.
            - Result.NOT_SUPPORTED When trying to load a file with an unknown extension.
        :rtype: thorvg_python.base.Result

        .. seealso:: Engine.font_unload()

        .. versionadded:: 0.15
        """
        path_bytes = path.encode() + b"\x00"
        path_arr_type = ctypes.c_char * len(path_bytes)
        path_arr = path_arr_type.from_buffer_copy(path_bytes)
        self.thorvg_lib.tvg_font_load.argtypes = [
            ctypes.POINTER(path_arr_type),
        ]
        self.thorvg_lib.tvg_font_load.restype = Result
        return self.thorvg_lib.tvg_font_load(ctypes.pointer(path_arr))

    def font_load_data(
        self,
        name: str,
        data: bytes,
        mimetype: Optional[str],
        copy: bool,
    ) -> Result:
        """Loads a scalable font data from a memory block of a given size.

        ThorVG efficiently caches the loaded font data using the specified ``name`` as a key.
        This means that loading the same fonts again will not result in duplicate operations.
        Instead, ThorVG will reuse the previously loaded font data.

        :param str name: The name under which the font will be stored and accessible (e.x. in a ``Text.set_font`` API).
        :param bytes data: A pointer to a memory location where the content of the font data is stored.
        :param str mimetype: Mimetype or extension of font data. In case a ``None`` or an empty "" value is provided the loader will be determined automatically.
        :param bool copy: If ``true`` the data are copied into the engine local buffer, otherwise they are not (default).

        :return:
            - Result.INVALID_ARGUMENT If no name is provided or if ``size`` is zero while ``data`` points to a valid memory location.
            - Result.NOT_SUPPORTED When trying to load a file with an unknown extension.
            - Result.INSUFFICIENT_CONDITION When trying to unload the font data that has not been previously loaded.
        :rtype: thorvg_python.base.Result

        .. warning::
            : It's the user responsibility to release the ``data`` memory.

        .. note::
            To unload the font data loaded using this API, pass the proper ``name`` and ``None`` as ``data``.

        .. versionadded:: 0.15
        """
        name_bytes = name.encode() + b"\x00"
        name_bytes += b"\x00"
        name_char_type = ctypes.c_char * len(name_bytes)
        name_char = name_char_type.from_buffer_copy(name_bytes)
        data_arr_type = ctypes.c_ubyte * len(data)
        data_arr = data_arr_type.from_buffer_copy(data)
        if mimetype is not None and mimetype != "":
            mimetype_bytes = name.encode() + b"\x00"
            mimetype_char_type = ctypes.c_char * len(mimetype_bytes)
            mimetype_char_ptr_type = ctypes.POINTER(mimetype_char_type)
            mimetype_char = mimetype_char_type.from_buffer_copy(mimetype_bytes)
            mimetype_char_ptr = ctypes.pointer(mimetype_char)
        else:
            mimetype_char_ptr_type = ctypes.c_void_p  # type: ignore
            mimetype_char_ptr = ctypes.c_void_p()  # type: ignore
        self.thorvg_lib.tvg_picture_load_raw.argtypes = [
            ctypes.POINTER(name_char_type),
            ctypes.POINTER(data_arr_type),
            ctypes.c_uint32,
            mimetype_char_ptr_type,
            ctypes.c_bool,
        ]
        return self.thorvg_lib.tvg_picture_load_raw(
            ctypes.pointer(name_char),
            ctypes.pointer(data_arr),
            ctypes.c_uint32(ctypes.sizeof(data_arr)),
            mimetype_char_ptr,
            ctypes.c_bool(copy),
        )

    def font_unload(
        self,
        path: str,
    ) -> Result:
        """Unloads the specified scalable font data that was previously loaded.

        This function is used to release resources associated with a font file that has been loaded into memory.

        :param str path: The path to the loaded font file.

        :return: Result.INSUFFICIENT_CONDITION The loader is not initialized.
        :rtype: thorvg_python.base.Result

        .. note::
            If the font data is currently in use, it will not be immediately unloaded.
        .. seealso:: Engine.font_load()

        .. versionadded:: 0.15
        """
        path_bytes = path.encode() + b"\x00"
        path_arr_type = ctypes.c_char * len(path_bytes)
        path_arr = path_arr_type.from_buffer_copy(path_bytes)
        self.thorvg_lib.tvg_font_unload.argtypes = [
            ctypes.POINTER(path_arr_type),
        ]
        self.thorvg_lib.tvg_font_unload.restype = Result
        return self.thorvg_lib.tvg_font_unload(ctypes.pointer(path_arr))
