#!/usr/bin/env python3
import ctypes
from typing import Optional

from .animation import Animation
from .base import AnimationPointer, PaintPointer, Result, SaverPointer
from .engine import Engine
from .paint import Paint


class Saver:
    """
    Saver API

    A module for exporting a paint object into a specified file.

    The module enables to save the composed scene and/or image from a paint object.
    Once it's successfully exported to a file, it can be recreated using the Picture module.
    """

    def __init__(self, engine: Engine, saver: Optional[SaverPointer] = None):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if saver is None:
            self._saver = self._new()
        else:
            self._saver = saver

    def _new(self) -> SaverPointer:
        """Creates a new SaverPointer object.

        :return: A new SaverPointer object.
        :rtype: SaverPointer

        .. note:: You need not call this method as it is auto called when initializing ``Saver()``.
        """
        self.thorvg_lib.tvg_saver_new.restype = SaverPointer
        return self.thorvg_lib.tvg_saver_new()

    def save_paint(
        self,
        paint: Paint,
        path: str,
        quality: int,
    ) -> Result:
        """Exports the given ``paint`` data to the given ``path``

        If the saver module supports any compression mechanism, it will optimize the data size.
        This might affect the encoding/decoding time in some cases. You can turn off the compression
        if you wish to optimize for speed.

        :param thorvg_python.paint.Paint paint: The paint to be saved with all its associated properties.
        :param str path: A path to the file, in which the paint data is to be saved.
        :param bool quality: If ``true`` then compress data if possible.

        :return:
            - Result.INVALID_ARGUMENT A ``None`` passed as the argument.
            - Result.INSUFFICIENT_CONDITION Currently saving other resources.
            - Result.NOT_SUPPORTED Trying to save a file with an unknown extension or in an unsupported format.
            - Result.UNKNOWN An empty paint is to be saved.
        :rtype: thorvg_python.base.Result

        .. note::
            Saving can be asynchronous if the assigned thread number is greater than zero. To guarantee the saving is done, call Saver.sync() afterwards.
        .. seealso:: Saver.sync()
        """
        path_bytes = path.encode() + b"\x00"
        path_arr_type = ctypes.c_char * len(path)
        path_arr = path_arr_type.from_buffer_copy(path_bytes)
        self.thorvg_lib.tvg_saver_save_paint.argtypes = [
            SaverPointer,
            PaintPointer,
            ctypes.POINTER(path_arr_type),
            ctypes.c_uint32,
        ]
        self.thorvg_lib.tvg_saver_save_paint.restype = Result
        return self.thorvg_lib.tvg_saver_save_paint(
            self._saver,
            paint._paint,  # type: ignore
            ctypes.pointer(path_arr),
            ctypes.c_uint32(quality),
        )

    def save_animation(
        self,
        animation: Animation,
        path: str,
        quality: int,
        fps: int,
    ) -> Result:
        """Exports the given ``animation`` data to the given ``path``

        If the saver module supports any compression mechanism, it will optimize the data size.
        This might affect the encoding/decoding time in some cases. You can turn off the compression
        if you wish to optimize for speed.

        :param thorvg_python.animation.Animation animation: The animation to be saved with all its associated properties.
        :param str path: A path to the file, in which the animation data is to be saved.
        :param int quality: The encoded quality level. ``0`` is the minimum, ``100`` is the maximum value(recommended).
        :param int fps: The frames per second for the animation. If ``0``, the default fps is used.

        :return:
            - Result.INVALID_ARGUMENT A ``None`` passed as the argument.
            - Result.INSUFFICIENT_CONDITION Currently saving other resources or animation has no frames.
            - Result.NOT_SUPPORTED Trying to save a file with an unknown extension or in an unsupported format.
            - Result.UNKNOWN Unknown if attempting to save an empty paint.
        :rtype: thorvg_python.base.Result

        .. note::
            A higher frames per second (FPS) would result in a larger file size. It is recommended to use the default value.
        .. note::
            Saving can be asynchronous if the assigned thread number is greater than zero. To guarantee the saving is done, call Saver.sync() afterwards.

        .. seealso:: Saver.sync()

        .. versionadded:: 1.0
        """
        path_bytes = path.encode() + b"\x00"
        path_arr_type = ctypes.c_char * len(path)
        path_arr = path_arr_type.from_buffer_copy(path_bytes)
        self.thorvg_lib.tvg_saver_save_paint.argtypes = [
            SaverPointer,
            AnimationPointer,
            ctypes.POINTER(path_arr_type),
            ctypes.c_uint32,
            ctypes.c_uint32,
        ]
        self.thorvg_lib.tvg_saver_save_paint.restype = Result
        return self.thorvg_lib.tvg_saver_save_paint(
            self._saver,
            animation._animation,  # type: ignore
            ctypes.pointer(path_arr),
            ctypes.c_uint32(quality),
            ctypes.c_uint32(fps),
        )

    def sync(self) -> Result:
        """Guarantees that the saving task is finished.

        The behavior of the Saver module works on a sync/async basis, depending on the threading setting of the Initializer.
        Thus, if you wish to have a benefit of it, you must call Saver.sync() after the Saver.save() in the proper delayed time.
        Otherwise, you can call Saver.sync() immediately.

        :return:
            - Result.INVALID_ARGUMENT A ``None`` passed as the argument.
            - Result.INSUFFICIENT_CONDITION No saving task is running.
        :rtype: thorvg_python.base.Result

        .. note::
            The asynchronous tasking is dependent on the Saver module implementation.
        .. seealso:: Saver.save()
        """
        self.thorvg_lib.tvg_saver_sync.argtypes = [
            SaverPointer,
        ]
        self.thorvg_lib.tvg_saver_sync.restype = Result
        return self.thorvg_lib.tvg_saver_sync(
            self._saver,
        )

    def _del(self) -> Result:
        """Deletes the given SaverPointer object.

        :return: Result.INVALID_ARGUMENT An invalid SaverPointer.
        :rtype: thorvg_python.base.Result
        """
        self.thorvg_lib.tvg_saver_del.argtypes = [
            SaverPointer,
        ]
        self.thorvg_lib.tvg_saver_del.restype = Result
        return self.thorvg_lib.tvg_saver_del(
            self._saver,
        )
