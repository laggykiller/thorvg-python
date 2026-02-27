#!/usr/bin/env python3
import ctypes
from typing import Callable, Optional

from .base import AccessorPointer, PaintPointer, Result
from .engine import Engine
from .paint import Paint


class Accessor:
    """
    Accessor API

    A module for manipulation of the scene tree

    This module helps to control the scene tree.
    """

    def __init__(self, engine: Engine, accessor: "Optional[AccessorPointer]"):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if accessor is None:
            self._accessor = self._new()
        else:
            self._accessor = accessor

    def _new(self) -> AccessorPointer:
        """Creates a new AccessorPointer object.

        :return: A new AccessorPointer object.
        :rtype: AccessorPointer

        .. note:: You need not call this method as it is auto called when initializing ``Accessor()``.

        ..versionadded: 1.0
        """
        self.thorvg_lib.tvg_accessor_new.restype = AccessorPointer
        return self.thorvg_lib.tvg_accessor_new()

    def _del(self) -> Result:
        """Deletes the given accessor object.

        :return: Result.INVALID_ARGUMENT An invalid AccessorPointer.
        :rtype: Result

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_accessor_del.argtypes = [AccessorPointer]
        self.thorvg_lib.tvg_accessor_del.restype = Result
        return self.thorvg_lib.tvg_accessor_del(self._accessor)

    def set(
        self,
        paint: Paint,
        func: Callable[[PaintPointer, bytes], bool],
        data: bytes,
    ) -> Result:
        """Sets the paint of the accessor then iterates through its descendents.

        Iterates through all descendents of the scene passed through the paint argument
        while calling func on each and passing the data pointer to this function. When
        func returns false iteration stops and the function returns.

        :param Paint paint: A PaintPointer to the scene object.
        :param Callable[[PaintPointer, bytes], bool] func: A function pointer to the function that will be execute for each child.
        :param bytes data: A void pointer to data that will be passed to the func.

        :result: INVALID_ARGUMENT An invalid AccessorPointer, PaintPointer, or function pointer.
        :rtype: Result

        .. versionadded:: 1.0
        """
        func_type = ctypes.CFUNCTYPE(ctypes.c_bool, PaintPointer, ctypes.c_void_p)

        data_arr_type = ctypes.c_ubyte * len(data)
        data_arr = data_arr_type.from_buffer_copy(data)

        self.thorvg_lib.tvg_accessor_set.argtypes = [
            AccessorPointer,
            PaintPointer,
            func_type,
            data_arr_type,
        ]
        self.thorvg_lib.tvg_accessor_set.restype = Result
        return self.thorvg_lib.tvg_accessor_set(
            self._accessor,
            paint._paint,  # type: ignore
            func_type(func),
            data_arr,
        )

    def accessor_generate_id(
        self,
        name: str,
    ) -> int:
        """Generate a unique ID (hash key) from a given name.

        This function computes a unique identifier value based on the provided string.
        You can use this to assign a unique ID to the Paint object.

        :param str name: The input string to generate the unique identifier from.

        :return: The generated unique identifier value.
        :rtype: int

        .. versionadded: 1.0
        """
        name_bytes = name.encode() + b"\x00"
        name_char_type = ctypes.c_char * len(name_bytes)
        name_char = name_char_type.from_buffer_copy(name_bytes)
        self.thorvg_lib.tvg_accessor_generate_id.argtypes = [
            ctypes.POINTER(name_char_type)
        ]
        self.thorvg_lib.tvg_accessor_generate_id.restype = ctypes.c_uint32
        return self.thorvg_lib.tvg_accessor_generate_id(ctypes.pointer(name_char)).value
