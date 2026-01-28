#!/usr/bin/env python3
import ctypes
from typing import Optional

from ..base import PaintStruct, Result
from ..engine import Engine
from . import Paint


class Scene(Paint):
    """
    Scene API

    A module managing the multiple paints as one group paint.

    As a group, scene can be transformed, translucent, composited with other target paints,
    its children will be affected by the scene world.
    """

    def __init__(self, engine: Engine, scene: Optional[PaintStruct] = None):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if scene is None:
            self._paint = self._new()
        else:
            self._paint = scene

    def _new(self) -> PaintStruct:
        """Creates a new scene object.

        Note that you need not call this method as it is auto called when initializing ``Scene()``.

        A scene object is used to group many paints into one object, which can be manipulated using TVG APIs.

        :return: A new scene object.
        :rtype: PaintStruct
        """
        self.thorvg_lib.tvg_scene_new.restype = ctypes.POINTER(PaintStruct)
        return self.thorvg_lib.tvg_scene_new().contents

    def reserve(
        self,
        size: int,
    ) -> Result:
        """Sets the size of the container, where all the paints pushed into the scene are stored.

        If the number of objects pushed into the scene is known in advance, calling the function
        prevents multiple memory reallocation, thus improving the performance.

        :param int size: The number of objects for which the memory is to be reserved.

        :return:
            - FAILED_ALLOCATION An internal error with a memory allocation.
            - INVALID_ARGUMENT An invalid PaintStruct pointer.
        :rtype: Result

        .. deprecated:: 0.15
        .. note:: Malfunctional
        """
        self.thorvg_lib.tvg_scene_reserve.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_uint32,
        ]
        self.thorvg_lib.tvg_scene_reserve.restype = Result
        return self.thorvg_lib.tvg_scene_reserve(
            ctypes.pointer(self._paint),
            ctypes.c_uint32(size),
        )

    def push(
        self,
        paint: Paint,
    ) -> Result:
        """Passes drawing elements to the scene using PaintStruct objects.

        Only the paints pushed into the scene will be the drawn targets.
        The paints are retained by the scene until the tvg_scene_clear() is called.
        If you know the number of pushed objects in advance, please call tvg_scene_reserve().

        :param PaintStruct paint: A graphical object to be drawn.

        :return: INVALID_ARGUMENT A ``nullptr`` passed as the argument.
        :rtype: Result

        .. note::
            The rendering order of the paints is the same as the order as they were pushed. Consider sorting the paints before pushing them if you intend to use layering.
        """
        self.thorvg_lib.tvg_scene_push.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.POINTER(PaintStruct),
        ]
        self.thorvg_lib.tvg_scene_push.restype = Result
        return self.thorvg_lib.tvg_scene_push(
            ctypes.pointer(self._paint),
            ctypes.pointer(paint._paint),
        )

    def clear(
        self,
        free: bool,
    ) -> Result:
        """Clears a scene objects from pushed paints.

        PaintStruct objects stored in the scene are released if ``free`` is set to ``true``, otherwise the memory is not deallocated and
        all paints should be released manually in order to avoid memory leaks.

        :param bool free: If ``true`` the memory occupied by paints is deallocated, otherwise it is not.

        :return: INVALID_ARGUMENT An invalid CanvasStruct pointer.
        :rtype: Result

        .. warning::
            Please use the ``free`` argument only when you know how it works, otherwise it's not recommended.
        """
        self.thorvg_lib.tvg_scene_clear.argtypes = [
            ctypes.POINTER(PaintStruct),
            ctypes.c_bool,
        ]
        self.thorvg_lib.tvg_scene_clear.restype = Result
        return self.thorvg_lib.tvg_scene_clear(
            ctypes.pointer(self._paint),
            ctypes.c_bool(free),
        )
