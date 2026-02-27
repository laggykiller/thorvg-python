#!/usr/bin/env python3
import ctypes
from typing import Optional, Tuple

from ..base import AnimationPointer, PaintPointer, Result
from ..engine import Engine
from ..paint.picture import Picture


class Animation:
    """
    Animation API

    A module for manipulation of animatable images.

    The module supports the display and control of animation frames.
    """

    def __init__(self, engine: Engine, animation: Optional[AnimationPointer] = None):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if animation is None:
            self._animation = self._new()
        else:
            self._animation = animation

    def _new(self) -> AnimationPointer:
        """Creates a new Animation object.

        :return: AnimationPointer A new AnimationPointer object.
        :rtype: AnimationPointer

        .. note::
            You need not call this method as it is auto called when initializing ``Animation()``.

        .. versionadded:: 0.13
        """
        self.thorvg_lib.tvg_animation_new.restype = AnimationPointer
        return self.thorvg_lib.tvg_animation_new()

    def set_frame(
        self,
        no: float,
    ) -> Result:
        """Specifies the current frame in the animation.

        :param float no: The index of the animation frame to be displayed. The index should be less than the Animation.get_total_frame().

        :return:
            - Result.INVALID_ARGUMENT An invalid AnimationPointer.
            - Result.INSUFFICIENT_CONDITION if the given ``no`` is the same as the current frame value.
            - Result.NOT_SUPPORTED The picture data does not support animations.
        :rtype: Result

        .. note::
            For efficiency, ThorVG ignores updates to the new frame value if the difference from the current frame value
            is less than 0.001. In such cases, it returns ``Result.InsufficientCondition``.
            Values less than 0.001 may be disregarded and may not be accurately retained by the Animation.

        .. seealso:: Animation.get_total_frame()

        .. versionadded:: 0.13
        """
        self.thorvg_lib.tvg_animation_set_frame.argtypes = [
            AnimationPointer,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_animation_set_frame.restype = Result
        return self.thorvg_lib.tvg_animation_set_frame(
            self._animation,
            ctypes.c_float(no),
        )

    def get_picture(self) -> Picture:
        """Retrieves a picture instance associated with this animation instance.

        This function provides access to the picture instance that can be used to load animation formats, such as Lottie(json).
        After setting up the picture, it can be pushed to the designated canvas, enabling control over animation frames
        with this Animation instance.

        :return: A picture instance that is tied to this animation.
        :rtype: Picture

        .. warning::
            The picture instance is owned by Animation. It should not be deleted manually.

        .. versionadded:: 0.13
        """
        self.thorvg_lib.tvg_animation_get_picture.argtypes = [
            AnimationPointer,
        ]
        self.thorvg_lib.tvg_animation_get_picture.restype = PaintPointer
        return Picture(
            self.engine,
            self.thorvg_lib.tvg_animation_get_picture(
                self._animation,
            ),
        )

    def get_frame(self) -> Tuple[Result, float]:
        """Retrieves the current frame number of the animation.

        :return: Result.INVALID_ARGUMENT An invalid AnimationPointer or ``no``
        :rtype: Result
        :return: The current frame number of the animation, between 0 and totalFrame() - 1.
        :rtype: float

        .. seealso:: Animation.get_total_frame()
        .. seealso:: Animation.set_frame()

        .. versionadded:: 0.13
        """
        no = ctypes.c_float()
        self.thorvg_lib.tvg_animation_get_frame.argtypes = [
            AnimationPointer,
            ctypes.POINTER(ctypes.c_float),
        ]
        self.thorvg_lib.tvg_animation_get_frame.restype = Result
        result = self.thorvg_lib.tvg_animation_get_frame(
            self._animation,
            ctypes.pointer(no),
        )
        return result, no.value

    def get_total_frame(self) -> Tuple[Result, float]:
        """Retrieves the total number of frames in the animation.

        :return: Result.INVALID_ARGUMENT An invalid AnimationPointer or ``cnt``.
        :rtype: Result
        :return: The total number of frames in the animation.
        :rtype: float

        .. note::
            Frame numbering starts from 0.
        .. note::
            If the Picture is not properly configured, this function will return 0.

        .. versionadded:: 0.13
        """
        cnt = ctypes.c_float()
        self.thorvg_lib.tvg_animation_get_total_frame.argtypes = [
            AnimationPointer,
            ctypes.POINTER(ctypes.c_float),
        ]
        self.thorvg_lib.tvg_animation_get_total_frame.restype = Result
        result = self.thorvg_lib.tvg_animation_get_total_frame(
            self._animation,
            ctypes.pointer(cnt),
        )
        return result, cnt.value

    def get_duration(self) -> Tuple[Result, float]:
        """Retrieves the duration of the animation in seconds.

        :return: Result.INVALID_ARGUMENT An invalid AnimationPointer or ``duration``.
        :rtype: Result
        :return: The duration of the animation in seconds.
        :rtype: float

        .. note::
            If the Picture is not properly configured, this function will return 0.

        .. versionadded:: 0.13
        """
        duration = ctypes.c_float()
        self.thorvg_lib.tvg_animation_get_duration.argtypes = [
            AnimationPointer,
            ctypes.POINTER(ctypes.c_float),
        ]
        self.thorvg_lib.tvg_animation_get_duration.restype = Result
        result = self.thorvg_lib.tvg_animation_get_duration(
            self._animation,
            ctypes.pointer(duration),
        )
        return result, duration.value

    def set_segment(
        self,
        begin: float,
        end: float,
    ) -> Result:
        """Specifies the playback segment of the animation.

        The set segment is designated as the play area of the animation.
        This is useful for playing a specific segment within the entire animation.
        After setting, the number of animation frames and the playback time are calculated
        by mapping the playback segment as the entire range.

        :param begin: segment begin frame.
        :param end: segment end frame.

        :return:
            - Result.INSUFFICIENT_CONDITION In case the animation is not loaded.
            - Result.INVALID_ARGUMENT If the ``begin`` is higher than ``end``.

        .. note::
            Animation allows a range from 0.0 to the total frame. ``end`` should not be higher than ``begin``.
        .. note::
            If a marker has been specified, its range will be disregarded.

        .. seealso:: Animation.set_marker()
        .. seealso:: Animation.get_total_frame()

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_animation_set_segment.argtypes = [
            AnimationPointer,
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.thorvg_lib.tvg_animation_set_segment.restype = Result
        result = self.thorvg_lib.tvg_animation_set_segment(
            self._animation,
            ctypes.c_float(begin),
            ctypes.c_float(end),
        )
        return result

    def get_segment(self) -> Tuple[Result, float, float]:
        """Gets the current segment.

        :return:
            - Result.INSUFFICIENT_CONDITION In case the animation is not loaded.
            - Result.INVALID_ARGUMENT An invalid AnimationPointer.
        :rtype: Result
        :return: segment begin frame.
        :rtype: float
        :return: segment end frame.
        :rtype: float

        .. versionadded:: 1.0
        """
        begin = ctypes.c_float()
        end = ctypes.c_float()
        self.thorvg_lib.tvg_animation_get_segment.argtypes = [
            AnimationPointer,
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
        ]
        self.thorvg_lib.tvg_animation_get_segment.restype = Result
        result = self.thorvg_lib.tvg_animation_get_segment(
            self._animation,
            ctypes.pointer(begin),
            ctypes.pointer(end),
        )
        return result, begin.value, end.value

    def _del(self) -> Result:
        """Deletes the given AnimationPointer object.

        :return: Result.INVALID_ARGUMENT An invalid AnimationPointer.
        :rtype: Result

        .. versionadded:: 0.13
        """
        self.thorvg_lib.tvg_animation_del.argtypes = [
            AnimationPointer,
        ]
        self.thorvg_lib.tvg_animation_del.restype = Result
        return self.thorvg_lib.tvg_animation_del(
            self._animation,
        )
