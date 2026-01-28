#!/usr/bin/env python3
import ctypes
from typing import Optional, Tuple

from ..base import AnimationStruct, Result
from ..engine import Engine
from . import Animation


class LottieAnimation(Animation):
    """
    LottieAnimation Extension API

    A module for manipulation of the scene tree

    This module helps to control the scene tree.
    """

    def __init__(self, engine: Engine, animation: Optional[AnimationStruct] = None):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if animation is None:
            self._animation = self._new()
        else:
            self._animation = animation

    def new(self) -> AnimationStruct:
        """Creates a new LottieAnimation object.

        :return: AnimationStruct A new Tvg_LottieAnimation object.
        :rtype: AnimationStruct

        .. versionadded:: 0.15
        """
        self.thorvg_lib.tvg_lottie_animation_new.restype = ctypes.POINTER(
            AnimationStruct
        )
        return self.thorvg_lib.tvg_lottie_animation_new().contents

    def override(
        self,
        slot: Optional[str],
    ) -> Result:
        """Override the lottie properties through the slot data.

        :param str slot: The Lottie slot data in json, or ``None`` to reset.

        :return:
            - INSUFFICIENT_CONDITION In case the animation is not loaded.
            - INVALID_ARGUMENT When the given ``slot`` is invalid
            - NOT_SUPPORTED The Lottie Animation is not supported.
        :rtype: Result

        .. note::
            Experimental API
        """
        if slot is not None and slot != "":
            slot_arr_type = ctypes.c_char * len(slot.encode())
            slot_arr_type_ptr = ctypes.POINTER(slot_arr_type)
            slot_arr_ptr = ctypes.pointer(slot_arr_type.from_buffer_copy(slot.encode()))
        else:
            slot_arr_type_ptr = ctypes.c_void_p  # type: ignore
            slot_arr_ptr = ctypes.c_void_p()  # type: ignore
        self.thorvg_lib.tvg_lottie_animation_override.argtypes = [
            ctypes.POINTER(AnimationStruct),
            slot_arr_type_ptr,
        ]
        self.thorvg_lib.tvg_lottie_animation_override.restype = Result
        return self.thorvg_lib.tvg_lottie_animation_override(
            ctypes.pointer(self._animation),
            slot_arr_ptr,
        )

    def set_marker(
        self,
        marker: str,
    ) -> Result:
        """Specifies a segment by marker.

        :param str marker: The name of the segment marker.

        :return:
            - INSUFFICIENT_CONDITION In case the animation is not loaded.
            - INVALID_ARGUMENT When the given ``marker`` is invalid.
            - NOT_SUPPORTED The Lottie Animation is not supported.
        :rtype: Result

        .. note::
            Experimental API
        """
        marker_arr_type = ctypes.c_char * len(marker.encode())
        marker_arr = marker_arr_type.from_buffer_copy(marker.encode())
        self.thorvg_lib.tvg_lottie_animation_set_marker.argtypes = [
            ctypes.POINTER(AnimationStruct),
            ctypes.POINTER(marker_arr_type),
        ]
        self.thorvg_lib.tvg_lottie_animation_set_marker.restype = Result
        return self.thorvg_lib.tvg_lottie_animation_set_marker(
            ctypes.pointer(self._animation),
            ctypes.pointer(marker_arr),
        )

    def get_markers_cnt(
        self,
    ) -> Tuple[Result, int]:
        """Gets the marker count of the animation.

        :return: INVALID_ARGUMENT In case a ``nullptr`` is passed as the argument.
        :rtype: Result
        :return: The count value of the markers.
        :rtype: int

        .. note::
            Experimental API
        """
        cnt = ctypes.c_uint32()
        self.thorvg_lib.tvg_lottie_animation_get_markers_cnt.argtypes = [
            ctypes.POINTER(AnimationStruct),
            ctypes.POINTER(ctypes.c_uint32),
        ]
        self.thorvg_lib.tvg_lottie_animation_get_markers_cnt.restype = Result
        result = self.thorvg_lib.tvg_lottie_animation_get_markers_cnt(
            ctypes.pointer(self._animation),
            ctypes.pointer(cnt),
        )
        return result, cnt.value

    def get_marker(
        self,
        idx: int,
    ) -> Tuple[Result, Optional[str]]:
        """Gets the marker name by a given index.

        :param int idx: The index of the animation marker, starts from 0.

        :return: INVALID_ARGUMENT In case ``nullptr`` is passed as the argument or ``idx`` is out of range.
        :rtyle: Result
        :return: The name of marker when succeed.
        :rtype: Optional[str]

        .. note::
            Experimental API
        """
        name = ctypes.c_char_p()
        self.thorvg_lib.tvg_lottie_animation_get_marker.argtypes = [
            ctypes.POINTER(AnimationStruct),
            ctypes.POINTER(ctypes.c_uint32),
            ctypes.POINTER(ctypes.c_char_p),
        ]
        self.thorvg_lib.tvg_lottie_animation_get_marker.restype = Result
        result = self.thorvg_lib.tvg_lottie_animation_get_marker(
            ctypes.pointer(self._animation),
            ctypes.c_uint32(idx),
            ctypes.pointer(name),
        )
        if name.value is not None:
            _name = name.value.decode("utf-8")
        else:
            _name = None
        return result, _name
