#!/usr/bin/env python3
# type: ignore
import shutil
from conan import ConanFile


class ThorvgRecipe(ConanFile):
    def requirements(self):
        self.requires("thorvg/0.15.16")

    def build(self):
        build_type = "Release"  # noqa: F841

    def build_requirements(self):
        if not shutil.which("cmake"):
            self.tool_requires("cmake/[>=3.27]")