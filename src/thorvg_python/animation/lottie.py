#!/usr/bin/env python3
import ctypes
from typing import Optional, Tuple

from ..base import AnimationPointer, Result
from ..engine import Engine
from . import Animation


class LottieAnimation(Animation):
    """
    LottieAnimation Extension API

    A module for manipulation of the scene tree

    This module helps to control the scene tree.
    """

    def __init__(self, engine: Engine, animation: Optional[AnimationPointer] = None):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if animation is None:
            self._animation = self._new()
        else:
            self._animation = animation

    def new(self) -> AnimationPointer:
        """Creates a new LottieAnimation object.

        :return: AnimationPointer A new Lottie AnimationPointer object.
        :rtype: thorvg_python.base.AnimationPointer

        .. versionadded:: 0.15
        """
        self.thorvg_lib.tvg_lottie_animation_new.restype = AnimationPointer
        return self.thorvg_lib.tvg_lottie_animation_new()

    def gen_slot(
        self,
        slot: str,
    ) -> int:
        """Generates a new slot from the given slot data.

        :param str slot: The Lottie slot data in JSON format.

        :return: The generated slot ID when successful, 0 otherwise.
        :rtype: int

        .. versionadded:: 1.0
        """
        slot_bytes = slot.encode() + b"\x00"
        slot_arr_type = ctypes.c_char * len(slot_bytes)

        self.thorvg_lib.tvg_lottie_animation_gen_slot.argtypes = [
            AnimationPointer,
            ctypes.POINTER(slot_arr_type),
        ]
        self.thorvg_lib.tvg_lottie_animation_gen_slot.restype = ctypes.c_uint32
        return self.thorvg_lib.tvg_lottie_animation_gen_slot(
            self._animation,
            ctypes.pointer(slot_arr_type.from_buffer_copy(slot_bytes)),
        )

    def apply_slot(
        self,
        _id: int,
    ) -> Result:
        """Applies a previously generated slot to the animation.

        :param int _id: The ID of the slot to apply, or 0 to reset all slots.

        :return:
            - Result.INSUFFICIENT_CONDITION In case the animation is not loaded.
            - Result.INVALID_ARGUMENT When the given ``_id`` is invalid
            - Result.NOT_SUPPORTED The Lottie Animation is not supported.
        :rtype: thorvg_python.base.Result

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_lottie_animation_apply_slot.argtypes = [
            AnimationPointer,
            ctypes.c_uint32,
        ]
        self.thorvg_lib.tvg_lottie_animation_apply_slot.restype = Result
        return self.thorvg_lib.tvg_lottie_animation_apply_slot(
            self._animation,
            ctypes.c_uint32(_id),
        )

    def del_slot(
        self,
        _id: int,
    ) -> Result:
        """Deletes a previously generated slot.

        :param _id: The ID of the slot to delete.

        :return:
            - Result.INSUFFICIENT_CONDITION In case the animation is not loaded or the slot ID is invalid.
            - Result.NOT_SUPPORTED The Lottie Animation is not supported.
        :rtype: thorvg_python.base.Result

        .. note::
            This function should be paired with gen.
        .. seealso:: LottieAnimation.gen_slot()
        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_lottie_animation_del_slot.argtypes = [
            AnimationPointer,
            ctypes.c_uint32,
        ]
        self.thorvg_lib.tvg_lottie_animation_del_slot.restype = Result
        return self.thorvg_lib.tvg_lottie_animation_del_slot(
            self._animation,
            ctypes.c_uint32(_id),
        )

    def set_marker(
        self,
        marker: str,
    ) -> Result:
        """Specifies a segment by marker.

        :param str marker: The name of the segment marker.

        :return:
            - Result.INSUFFICIENT_CONDITION In case the animation is not loaded.
            - Result.INVALID_ARGUMENT When the given ``marker`` is invalid.
            - Result.NOT_SUPPORTED The Lottie Animation is not supported.
        :rtype: thorvg_python.base.Result

        .. note::
            Experimental API
        """
        marker_bytes = marker.encode() + b"\x00"
        marker_arr_type = ctypes.c_char * len(marker_bytes)
        marker_arr = marker_arr_type.from_buffer_copy(marker_bytes)
        self.thorvg_lib.tvg_lottie_animation_set_marker.argtypes = [
            AnimationPointer,
            ctypes.POINTER(marker_arr_type),
        ]
        self.thorvg_lib.tvg_lottie_animation_set_marker.restype = Result
        return self.thorvg_lib.tvg_lottie_animation_set_marker(
            self._animation,
            ctypes.pointer(marker_arr),
        )

    def get_markers_cnt(
        self,
    ) -> Tuple[Result, int]:
        """Gets the marker count of the animation.

        :return: Result.INVALID_ARGUMENT In case a ``None`` is passed as the argument.
        :rtype: thorvg_python.base.Result
        :return: The count value of the markers.
        :rtype: int

        .. note::
            Experimental API
        """
        cnt = ctypes.c_uint32()
        self.thorvg_lib.tvg_lottie_animation_get_markers_cnt.argtypes = [
            AnimationPointer,
            ctypes.POINTER(ctypes.c_uint32),
        ]
        self.thorvg_lib.tvg_lottie_animation_get_markers_cnt.restype = Result
        result = self.thorvg_lib.tvg_lottie_animation_get_markers_cnt(
            self._animation,
            ctypes.pointer(cnt),
        )
        return result, cnt.value

    def get_marker(
        self,
        idx: int,
    ) -> Tuple[Result, Optional[str]]:
        """Gets the marker name by a given index.

        :param int idx: The index of the animation marker, starts from 0.

        :return: Result.INVALID_ARGUMENT In case ``None`` is passed as the argument or ``idx`` is out of range.
        :rtyle: Result
        :return: The name of marker when succeed.
        :rtype: Optional[str]

        .. note::
            Experimental API
        """
        name = ctypes.c_char_p()
        self.thorvg_lib.tvg_lottie_animation_get_marker.argtypes = [
            AnimationPointer,
            ctypes.POINTER(ctypes.c_uint32),
            ctypes.POINTER(ctypes.c_char_p),
        ]
        self.thorvg_lib.tvg_lottie_animation_get_marker.restype = Result
        result = self.thorvg_lib.tvg_lottie_animation_get_marker(
            self._animation,
            ctypes.c_uint32(idx),
            ctypes.pointer(name),
        )
        if name.value is not None:
            _name = name.value.decode("utf-8")
        else:
            _name = None
        return result, _name

    def tween(self, _from: float, to: float, progress: float) -> Result:
        """Interpolates between two frames over a specified duration.

        This method performs tweening, a process of generating intermediate frame
        between ``_from`` and ``to`` based on the given ``progress``.

        :param _from: The start frame number of the interpolation.
        :param to: The end frame number of the interpolation.
        :param progress: The current progress of the interpolation (range: 0.0 to 1.0).

        :return: TVG_RESULT_INSUFFICIENT_CONDITION In case the animation is not loaded.
        :rtype: thorvg_python.base.Result

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_lottie_animation_tween.argtypes = [
            AnimationPointer,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_lottie_animation_tween.restype = Result
        return self.thorvg_lib.tvg_lottie_animation_tween(
            self._animation,
            ctypes.c_float(_from),
            ctypes.c_float(to),
            ctypes.c_float(progress),
        )

    def assign(self, layer: str, ix: int, var: str, val: float) -> Result:
        """Updates the value of an expression variable for a specific layer.

        :param str layer: The name of the layer containing the variable to be updated.
        :param int ix: The property index of the variable within the layer.
        :param str var: The name of the variable to be updated.
        :param float val: The new value to assign to the variable.

        :return:
            - Result.INSUFFICIENT_CONDITION If the animation is not loaded.
            - Result.INVALID_ARGUMENT When the given parameter is invalid.
            - Result.NOT_SUPPORTED When neither the layer nor the property is found in the current animation.
        :rtype: thorvg_python.base.Result

        .. note::
            Experimental API
        """
        layer_bytes = layer.encode() + b"\x00"
        layer_arr_type = ctypes.c_char * len(layer_bytes)
        layer_arr = layer_arr_type.from_buffer_copy(layer_bytes)

        var_bytes = layer.encode() + b"\x00"
        var_arr_type = ctypes.c_char * len(var_bytes)
        var_arr = var_arr_type.from_buffer_copy(var_bytes)

        self.thorvg_lib.tvg_lottie_animation_assign.argtypes = [
            AnimationPointer,
            ctypes.POINTER(layer_arr_type),
            ctypes.c_uint32,
            ctypes.POINTER(var_arr_type),
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_lottie_animation_assign.restype = Result
        return self.thorvg_lib.tvg_lottie_animation_assign(
            self._animation,
            ctypes.pointer(layer_arr),
            ctypes.c_uint32(ix),
            ctypes.pointer(var_arr),
            ctypes.c_float(val),
        )

    def set_quality(self, value: int) -> Result:
        """Sets the quality level for Lottie effects.

        This function controls the rendering quality of effects like blur, shadows, etc.
        Lower values prioritize performance while higher values prioritize quality.

        :param int value: The quality level (0-100). 0 represents lowest quality/best performance,
            100 represents highest quality/lowest performance, default is 50.

        :return:
            - Result.INSUFFICIENT_CONDITION If the animation is not loaded.
            - Result.INVALID_ARGUMENT An invalid AnimationPointer.
        :rtype: thorvg_python.base.Result

        .. note::
            This option is used as a hint; its behavior heavily depends on the render backend.

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_lottie_animation_set_quality.argtypes = [
            AnimationPointer,
            ctypes.c_uint8,
        ]
        self.thorvg_lib.tvg_lottie_animation_set_quality.restype = Result
        return self.thorvg_lib.tvg_lottie_animation_set_quality(
            self._animation,
            ctypes.c_uint8(value),
        )
