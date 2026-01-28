#!/usr/bin/env python3
import ctypes
from typing import Optional

from ..base import GradientStruct, PaintStruct, Result
from ..engine import Engine
from ..gradient import Gradient
from . import Paint


class Text(Paint):
    """
    Text API

    A class to represent text objects in a graphical context, allowing for rendering and manipulation of unicode text.
    """

    def __init__(self, engine: Engine, paint: Optional[PaintStruct] = None):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if paint is None:
            self._paint = self._new()
        else:
            self._paint = paint

    def _new(self) -> PaintStruct:
        """Creates a new text object.

        Note that you need not call this method as it is auto called when initializing ``Text()``.

        :return: A new text object.

        .. versionadded:: 0.15
        """
        self.thorvg_lib.tvg_text_new.restype = ctypes.POINTER(PaintStruct)
        return self.thorvg_lib.tvg_text_new().contents

    def set_font(
        self,
        name: Optional[str] = None,
        size: float = 12,
        style: Optional[str] = None,
    ) -> Result:
        """Sets the font properties for the text.

        This function allows you to define the font characteristics used for text rendering.
        It sets the font name, size and optionally the style.

        :param str name: The name of the font. This should correspond to a font available in the canvas.
        If set to ``None``, ThorVG will attempt to select a fallback font available on the system.
        :param float size: The size of the font in points.
        :param str style: The style of the font. If empty, the default style is used. Currently only 'italic' style is supported.

        :return: INVALID_ARGUMENT A ``nullptr`` passed as the ``paint`` argument.
            INSUFFICIENT_CONDITION  The specified ``name`` cannot be found.
        :rtype: Result

        .. note::
            If the ``name`` is not specified, ThorVG will select any available font candidate.
        .. versionadded:: 1.0

        .. code-block:: python

            from thorvg_python import Engine, Text

            engine = Engine()
            text = Text(engine)
            // Fallback example: Try a specific font, then fallback to any available one.
            if (text.set_font("Arial", 24, None) != Result.SUCCESS):
                text.set_font(None, 24, None)
        """
        if name is not None and name != "":
            name_arr_type = ctypes.c_char * len(name.encode())
            name_arr_type_ptr = ctypes.POINTER(name_arr_type)
            name_arr = name_arr_type.from_buffer_copy(name.encode())
            name_arr_ptr = ctypes.pointer(name_arr)
        else:
            name_arr_type_ptr = ctypes.c_void_p  # type: ignore
            name_arr_ptr = ctypes.c_void_p()  # type: ignore

        if style is not None and style != "":
            style_arr_type = ctypes.c_char * len(style.encode())
            style_arr_type_ptr = ctypes.POINTER(style_arr_type)
            style_arr = style_arr_type.from_buffer_copy(style.encode())
            style_arr_ptr = ctypes.pointer(style_arr)
        else:
            style_arr_type_ptr = ctypes.c_void_p  # type: ignore
            style_arr_ptr = ctypes.c_void_p()  # type: ignore

        self.thorvg_lib.tvg_text_set_font.argtypes = [
            ctypes.POINTER(PaintStruct),
            name_arr_type_ptr,
            ctypes.c_float,
            style_arr_type_ptr,
        ]
        self.thorvg_lib.tvg_text_set_font.restype = Result
        return self.thorvg_lib.tvg_text_set_font(
            ctypes.pointer(self._paint),
            name_arr_ptr,
            ctypes.c_float(size),
            style_arr_ptr,
        )

    def set_text(
        self,
        text: str,
    ) -> Result:
        """Assigns the given unicode text to be rendered.

        This function sets the unicode text that will be displayed by the rendering system.
        The text is set according to the specified UTF encoding method, which defaults to UTF-8.

        :param str text: The multi-byte text encoded with utf8 string to be rendered.

        :return: INVALID_ARGUMENT A ``nullptr`` passed as the ``paint`` argument.
        :rtyle: Result

        .. note::
            Experimental API
        """
        text_arr_type = ctypes.c_char * len(text.encode())
        text_arr = text_arr_type.from_buffer_copy(text.encode())
        self.thorvg_lib.tvg_text_set_text.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(text_arr_type),
        ]
        self.thorvg_lib.tvg_text_set_text.restype = Result
        return self.thorvg_lib.tvg_text_set_text(
            ctypes.pointer(self._paint),
            ctypes.pointer(text_arr),
        )

    def set_fill_color(
        self,
        r: int,
        g: int,
        b: int,
    ) -> Result:
        """Sets the text solid color.

        :param int r The red color channel value in the range [0 ~ 255]. The default value is 0.
        :param int g: The green color channel value in the range [0 ~ 255]. The default value is 0.
        :param int b: The blue color channel value in the range [0 ~ 255]. The default value is 0.

        :return: INVALID_ARGUMENT A ``nullptr`` passed as the ``paint`` argument.
        :rtype: Result

        .. note::
            Either a solid color or a gradient fill is applied, depending on what was set as last.
        .. seealso:: Text.set_font()

        .. versionadded:: 0.15
        """
        self.thorvg_lib.tvg_text_set_fill_color.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_uint8,
            ctypes.c_uint8,
            ctypes.c_uint8,
        ]
        self.thorvg_lib.tvg_text_set_fill_color.restype = Result
        return self.thorvg_lib.tvg_text_set_fill_color(
            ctypes.pointer(self._paint),
            ctypes.c_uint8(r),
            ctypes.c_uint8(g),
            ctypes.c_uint8(b),
        )

    def set_gradient(
        self,
        gradient: Gradient,
    ) -> Result:
        """Sets the gradient fill for the text.

        :param GradientStruct grad: The linear or radial gradient fill

        :return:
            - INVALID_ARGUMENT A ``nullptr`` passed as the ``paint`` argument.
            - MEMORY_CORRUPTION An invalid GradientStruct pointer.
        :rtype: Result

        .. note::
            Either a solid color or a gradient fill is applied, depending on what was set as last.
        .. seealso:: Text.set_font()

        .. versionadded:: 0.15
        """
        self.thorvg_lib.tvg_text_set_gradient.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(GradientStruct),
        ]
        self.thorvg_lib.tvg_text_set_gradient.restype = Result
        return self.thorvg_lib.tvg_text_set_gradient(
            ctypes.pointer(self._paint),
            ctypes.pointer(gradient._grad),  # type: ignore
        )
