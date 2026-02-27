#!/usr/bin/env python3
import ctypes
from typing import Optional

from ..base import PaintPointer, Result
from ..engine import Engine
from . import Paint


class Scene(Paint):
    """
    Scene API

    A module managing the multiple paints as one group paint.

    As a group, scene can be transformed, translucent, maskd with other target paints,
    its children will be affected by the scene world.
    """

    def __init__(self, engine: Engine, scene: Optional[PaintPointer] = None):
        self.engine = engine
        self.thorvg_lib = engine.thorvg_lib
        if scene is None:
            self._paint = self._new()
        else:
            self._paint = scene

    def _new(self) -> PaintPointer:
        """Creates a new Scene object.

        This function allocates and returns a new Scene instance.
        To properly destroy the Scene object, use ``Paint.rel()``.

        :return: A pointer to the newly created Scene object.
        :rtype: PaintPointer

        .. seealso:: Paint.rel()
        """
        self.thorvg_lib.tvg_scene_new.restype = PaintPointer
        return self.thorvg_lib.tvg_scene_new()

    def add(
        self,
        paint: Paint,
    ) -> Result:
        """Adds a paint object to the scene.

        Appends the specified paint object to the given scene. Only paint objects
        added to the scene are considered rendering targets.

        :param Paint paint: A handle to the paint object to be added to the scene.
        This parameter must not be ``None``.

        :rtype: Result

        .. note::
            Ownership of the ``paint`` object is transferred to the canvas upon
            successful addition. To retain ownership, call ``Paint.ref()``
            before adding it to the scene.
        .. note::
            The rendering order of paint objects follows their order in the root
            scene. If layering is required, ensure the paints are added in the
            desired order.

        .. seealso:: Scene.insert()
        .. seealso:: Scene.remove()

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_scene_add.argtypes = [
            PaintPointer,
            PaintPointer,
        ]
        self.thorvg_lib.tvg_scene_add.restype = Result
        return self.thorvg_lib.tvg_scene_add(
            self._paint,
            paint._paint,
        )

    def insert(self, at: Paint) -> Result:
        """Inserts a paint object into the scene.

        Inserts the specified paint object into the scene immediately before the
        given paint object ``at``. The ``at`` parameter must reference an existing
        paint object already added to the scene.

        :param Paint at: A handle to an existing paint object in the scene before
        which ``target`` will be inserted.
        This parameter must not be ``None``.

        :rtype: Result

        .. note::
            Ownership of the ``target`` object is transferred to the scene upon
            successful addition. To retain ownership, call ``Paint.ref()``
            before adding it to the scene.
        .. note::
            The rendering order of paint objects follows their order in the root
            scene. If layering is required, ensure the paints are added in the
            desired order.

        .. seealso:: Scene.add()
        .. seealso:: Scene.remove()

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_scene_insert.argtypes = [
            PaintPointer,
            PaintPointer,
        ]
        self.thorvg_lib.tvg_scene_insert.restype = Result
        return self.thorvg_lib.tvg_scene_insert(
            self._paint,
            at._paint,
        )

    def remove(
        self,
        paint: Optional[Paint],
    ) -> Result:
        """Removes a paint object from the scene.

        This function removes a specified paint object from the scene. If no paint
        object is specified (i.e., the default ``None`` is used), the function
        performs to clear all paints from the scene.

        :param paint: A pointer to the Paint object to be removed from the scene.
        If ``None``, remove all the paints from the scene.

        :rtype: Result

        .. seealso:: Scene.add()
        .. versionadded:: 1.0
        """
        if paint is None:
            paint_type = ctypes.c_void_p
            paint_ptr = ctypes.c_void_p()
        else:
            paint_type = PaintPointer
            paint_ptr = paint._paint  # type: ignore
        self.thorvg_lib.tvg_scene_remove.argtypes = [
            PaintPointer,
            paint_type,
        ]
        self.thorvg_lib.tvg_scene_remove.restype = Result
        return self.thorvg_lib.tvg_scene_remove(
            self._paint,
            paint_ptr,
        )

    def clear_effects(self) -> Result:
        """Clears all previously applied scene effects.

        This function clears all effects that have been applied to the scene,
        restoring it to its original state without any post-processing.

        :rtype: Result

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_scene_clear_effects.argtypes = [
            PaintPointer,
        ]
        self.thorvg_lib.tvg_scene_clear_effects.restype = Result
        return self.thorvg_lib.tvg_scene_clear_effects(
            self._paint,
        )

    def add_effect_gaussian_blur(
        self,
        sigma: float,
        direction: int,
        border: int,
        quality: int,
    ) -> Result:
        """Adds a Gaussian blur effect to the scene.

        This function adds a Gaussian blur filter to the scene as a post-processing effect.
        The blur can be applied in different directions with configurable border handling and quality settings.

        :param float sigma: The blur radius (sigma) value. Must be greater than 0.
        :param int direction: Blur direction: 0 = both directions, 1 = horizontal only, 2 = vertical only.
        :param int border: Border handling method: 0 = duplicate, 1 = wrap.
        :param int quality: Blur quality level [0 - 100].

        :rtype: Result

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_scene_add_effect_gaussian_blur.argtypes = [
            PaintPointer,
            ctypes.c_double,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
        ]
        self.thorvg_lib.tvg_scene_add_effect_gaussian_blur.restype = Result
        return self.thorvg_lib.tvg_scene_add_effect_gaussian_blur(
            self._paint,
            ctypes.c_double(sigma),
            ctypes.c_int(direction),
            ctypes.c_int(border),
            ctypes.c_int(quality),
        )

    def add_effect_drop_shadow(
        self,
        r: int,
        g: int,
        b: int,
        a: int,
        angle: float,
        distance: float,
        sigma: float,
        quality: int,
    ) -> Result:
        """Adds a drop shadow effect to the scene.

        This function adds a drop shadow with a Gaussian blur to the scene. The shadow
        can be customized using color, opacity, angle, distance, blur radius (sigma),
        and quality parameters.

        :param int r Red channel value of the shadow color [0 - 255].
        :param int g: Green channel value of the shadow color [0 - 255].
        :param int b: Blue channel value of the shadow color [0 - 255].
        :param int a Alpha (opacity) channel value of the shadow [0 - 255].
        :param float angle: Shadow direction in degrees [0 - 360].
        :param float distance: Distance of the shadow from the original object.
        :param float sigma: Gaussian blur sigma value for the shadow. Must be > 0.
        :param int quality: Blur quality level [0 - 100].

        :rtype: Result

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_scene_add_effect_drop_shadow.argtypes = [
            PaintPointer,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_int,
        ]
        self.thorvg_lib.tvg_scene_add_effect_drop_shadow.restype = Result
        return self.thorvg_lib.tvg_scene_add_effect_drop_shadow(
            self._paint,
            ctypes.c_int(r),
            ctypes.c_int(g),
            ctypes.c_int(b),
            ctypes.c_int(a),
            ctypes.c_double(angle),
            ctypes.c_double(distance),
            ctypes.c_double(sigma),
            ctypes.c_int(quality),
        )

    def add_effect_fill(
        self,
        r: int,
        g: int,
        b: int,
        a: int,
    ) -> Result:
        """Adds a fill color effect to the scene.

        This function overrides the scene's content colors with the specified fill color.

        :param int r Red color channel value [0 - 255].
        :param int g: Green color channel value [0 - 255].
        :param int b: Blue color channel value [0 - 255].
        :param int a Alpha (opacity) channel value [0 - 255].

        :rtype: Result

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_scene_add_effect_fill.argtypes = [
            PaintPointer,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
        ]
        self.thorvg_lib.tvg_scene_add_effect_fill.restype = Result
        return self.thorvg_lib.tvg_scene_add_effect_fill(
            self._paint,
            ctypes.c_int(r),
            ctypes.c_int(g),
            ctypes.c_int(b),
            ctypes.c_int(a),
        )

    def add_effect_tint(
        self,
        black_r: int,
        black_g: int,
        black_b: int,
        white_r: int,
        white_g: int,
        white_b: int,
        intensity: float,
    ) -> Result:
        """Adds a tint effect to the scene.

        This function tints the current scene using specified black and white color values,
        modulated by a given intensity.

        :param int black_r: Red component of the black color [0 - 255].
        :param int black_g: Green component of the black color [0 - 255].
        :param int black_b: Blue component of the black color [0 - 255].
        :param int white_r: Red component of the white color [0 - 255].
        :param int white_g: Green component of the white color [0 - 255].
        :param int white_b: Blue component of the white color [0 - 255].
        :param float intensity: Tint intensity value [0 - 100].

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_scene_add_effect_tint.argtypes = [
            PaintPointer,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_double,
        ]
        self.thorvg_lib.tvg_scene_add_effect_tint.restype = Result
        return self.thorvg_lib.tvg_scene_add_effect_tint(
            self._paint,
            ctypes.c_int(black_r),
            ctypes.c_int(black_g),
            ctypes.c_int(black_b),
            ctypes.c_int(white_r),
            ctypes.c_int(white_g),
            ctypes.c_int(white_b),
            ctypes.c_double(intensity),
        )

    def add_effect_effect_tritone(
        self,
        shadow_r: int,
        shadow_g: int,
        shadow_b: int,
        midtone_r: int,
        midtone_g: int,
        midtone_b: int,
        highlight_r: int,
        highlight_g: int,
        highlight_b: int,
        blend: int,
    ) -> Result:
        """Adds a tritone color effect to the scene.

        This function adds a tritone color effect to the given scene using three sets of RGB values
        representing shadow, midtone, and highlight colors.

        :param int shadow_r: Red component of the shadow color [0 - 255].
        :param int shadow_g: Green component of the shadow color [0 - 255].
        :param int shadow_b: Blue component of the shadow color [0 - 255].
        :param int midtone_r: Red component of the midtone color [0 - 255].
        :param int midtone_g: Green component of the midtone color [0 - 255].
        :param int midtone_b: Blue component of the midtone color [0 - 255].
        :param int highlight_r: Red component of the highlight color [0 - 255].
        :param int highlight_g: Green component of the highlight color [0 - 255].
        :param int highlight_b: Blue component of the highlight color [0 - 255].
        :param int blend: A blending factor that determines the mix between the original color and the tritone colors [0 - 255].

        .. versionadded:: 1.0
        """
        self.thorvg_lib.tvg_scene_add_effect_tritone.argtypes = [
            PaintPointer,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
        ]
        self.thorvg_lib.tvg_scene_add_effect_tritone.restype = Result
        return self.thorvg_lib.tvg_scene_add_effect_tritone(
            self._paint,
            ctypes.c_int(shadow_r),
            ctypes.c_int(shadow_g),
            ctypes.c_int(shadow_b),
            ctypes.c_int(midtone_r),
            ctypes.c_int(midtone_g),
            ctypes.c_int(midtone_b),
            ctypes.c_int(highlight_r),
            ctypes.c_int(highlight_g),
            ctypes.c_int(highlight_b),
            ctypes.c_int(blend),
        )
