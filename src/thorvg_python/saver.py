#!/usr/bin/env python3
import ctypes
from typing import Optional

from .base import PaintStruct, Result, SaverStruct
from .engine import Engine
from .paint import Paint


class Saver:
    """
    Saver API

    A module for exporting a paint object into a specified file.

    The module enables to save the composed scene and/or image from a paint object.
    Once it's successfully exported to a file, it can be recreated using the Picture module.
    """

    def __init__(self, engine: Engine, saver: Optional[SaverStruct] = None):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if saver is None:
            self._saver = self._new()
        else:
            self._saver = saver

    def _new(self) -> SaverStruct:
        """Creates a new SaverStruct object.

        Note that you need not call this method as it is auto called when initializing ``Saver()``.

        :return: A new SaverStruct object.
        """
        self.thorvg_lib.tvg_saver_new.restype = ctypes.POINTER(SaverStruct)
        return self.thorvg_lib.tvg_saver_new().contents

    def save(
        self,
        paint: Paint,
        path: str,
        compress: bool,
    ) -> Result:
        """Exports the given ``paint`` data to the given ``path``

        If the saver module supports any compression mechanism, it will optimize the data size.
        This might affect the encoding/decoding time in some cases. You can turn off the compression
        if you wish to optimize for speed.

        :param Paint paint: The paint to be saved with all its associated properties.
        :param str path: A path to the file, in which the paint data is to be saved.
        :param bool compress: If ``true`` then compress data if possible.

        :return:
            - INVALID_ARGUMENT A ``nullptr`` passed as the argument.
            - INSUFFICIENT_CONDITION Currently saving other resources.
            - NOT_SUPPORTED Trying to save a file with an unknown extension or in an unsupported format.
            - UNKNOWN An empty paint is to be saved.
        :rtype: Result

        .. note::
            Saving can be asynchronous if the assigned thread number is greater than zero. To guarantee the saving is done, call Saver.sync() afterwards.
        .. seealso:: Saver.sync()
        """
        path_arr_type = ctypes.c_char * len(path)
        path_arr = path_arr_type.from_buffer_copy(path.encode())
        self.thorvg_lib.tvg_saver_save.argtypes = [
            ctypes.POINTER(SaverStruct),
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(path_arr_type),
            ctypes.c_bool,
        ]
        self.thorvg_lib.tvg_saver_save.restype = Result
        return self.thorvg_lib.tvg_saver_save(
            ctypes.pointer(self._saver),
            ctypes.pointer(paint._paint),  # type: ignore
            ctypes.pointer(path_arr),
            ctypes.c_bool(compress),
        )

    def sync(self) -> Result:
        """Guarantees that the saving task is finished.

        The behavior of the Saver module works on a sync/async basis, depending on the threading setting of the Initializer.
        Thus, if you wish to have a benefit of it, you must call Saver.sync() after the Saver.save() in the proper delayed time.
        Otherwise, you can call Saver.sync() immediately.

        :return:
            - INVALID_ARGUMENT A ``nullptr`` passed as the argument.
            - INSUFFICIENT_CONDITION No saving task is running.
        :rtype: Result

        .. note::
            The asynchronous tasking is dependent on the Saver module implementation.
        .. seealso:: Saver.save()
        """
        self.thorvg_lib.tvg_saver_sync.argtypes = [
            ctypes.POINTER(SaverStruct),
        ]
        self.thorvg_lib.tvg_saver_sync.restype = Result
        return self.thorvg_lib.tvg_saver_sync(
            ctypes.pointer(self._saver),
        )

    def _del(self) -> Result:
        """Deletes the given SaverStruct object.

        :return: INVALID_ARGUMENT An invalid SaverStruct pointer.
        :rtype: Result
        """
        self.thorvg_lib.tvg_saver_del.argtypes = [
            ctypes.POINTER(SaverStruct),
        ]
        self.thorvg_lib.tvg_saver_del.restype = Result
        return self.thorvg_lib.tvg_saver_del(
            ctypes.pointer(self._saver),
        )
