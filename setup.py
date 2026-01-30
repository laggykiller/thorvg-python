import json
import os
import platform
import shutil
import subprocess
import sys
from typing import Any, Dict, List

from setuptools import find_packages, setup  # type: ignore

CONAN_ARCHS = {
    "x86_64": ["amd64", "x86_64", "x64"],
    "x86": ["i386", "i686", "x86"],
    "armv8": ["arm64", "aarch64", "aarch64_be", "armv8b", "armv8l"],
    "ppc64le": ["ppc64le", "powerpc"],
    "s390x": ["s390", "s390x"],
}


def get_arch() -> str:
    """Get the Conan compilation target architecture.

    If not explicitly set using the `TVGPY_COMPILE_TARGET` environment variable, this will be
    determined using the host machine"s platform information.
    """
    env_arch = os.getenv("TVGPY_COMPILE_TARGET", "")
    if env_arch:
        return env_arch

    if platform.architecture()[0] == "32bit" and platform.machine().lower() in (
        CONAN_ARCHS["x86"] + CONAN_ARCHS["x86_64"]
    ):
        return "x86"

    for k, v in CONAN_ARCHS.items():
        if platform.machine().lower() in v:
            return k

    raise RuntimeError("Unable to determine the compilation target architecture")


def install_thorvg(arch: str) -> Dict[Any, Any]:
    """Install thorvg using Conan."""
    settings: List[str] = []
    options: List[str] = []
    build: List[str] = []

    if platform.system() == "Windows":
        settings.append("os=Windows")
        if sys.platform.startswith(("cygwin", "msys")):
            # Need python headers and libraries, but msvc not able to find them
            # If inside cygwin or msys.
            settings.append("compiler=gcc")
            settings.append("compiler.version=10")
            settings.append("compiler.libcxx=libstdc++")
        else:
            settings.append("compiler.runtime=static")
    elif platform.system() == "Darwin":
        settings.append("os=Macos")
        if arch == "x86_64":
            settings.append("os.version=10.9")
        else:
            settings.append("os.version=11.0")
        settings.append("compiler=apple-clang")
        settings.append("compiler.libcxx=libc++")
    elif platform.system() == "Linux":
        settings.append("os=Linux")

    settings.append(f"arch={arch}")

    build.append("missing")

    if platform.system() != "Darwin":
        options.append("libwebp/*:with_simd=False")
    options.append("thorvg/*:shared=True")
    options.append("thorvg/*:with_savers=all")
    options.append("thorvg/*:with_loaders=all")
    options.append("thorvg/*:with_bindings=capi")

    print("conan cli settings:")
    print("settings: " + str(settings))
    print("build: " + str(build))
    print("options: " + str(options))

    profiles = subprocess.run(
        ["conan", "profile", "list"],
        stdout=subprocess.PIPE,
    ).stdout.decode()
    if "thorvg_python" not in profiles:
        subprocess.run(["conan", "profile", "detect", "-f", "--name", "thorvg_python"])

        if platform.architecture()[0] == "32bit" or platform.machine().lower() not in (
            CONAN_ARCHS["armv8"] + CONAN_ARCHS["x86_64"]
        ):
            profile_path = (
                subprocess.run(
                    ["conan", "profile", "path", "thorvg_python"],
                    stdout=subprocess.PIPE,
                )
                .stdout.decode()
                .strip()
            )

            with open(profile_path, "a+") as f:
                # https://github.com/conan-io/conan/issues/19179#issuecomment-3472691734
                f.write("\n")
                f.write("[platform_tool_requires]\n")
                f.write("cmake/*\n")
                f.write("[replace_tool_requires]\n")
                f.write("cmake/*: cmake/[*]")

    conan_output = os.path.join("conan_output", arch)

    result = subprocess.run(
        [
            "conan",
            "install",
            *[x for s in settings for x in ("-s", s)],
            *[x for b in build for x in ("-b", b)],
            *[x for o in options for x in ("-o", o)],
            "-of",
            conan_output,
            "--deployer=direct_deploy",
            "--format=json",
            ".",
            "--profile:all=thorvg_python",
        ],
        stdout=subprocess.PIPE,
    ).stdout.decode()
    conan_info = json.loads(result)

    return conan_info


def fetch_thorvg(conan_info: Dict[Any, Any]) -> List[str]:
    lib_paths: List[str] = []
    for dep in conan_info["graph"]["nodes"].values():
        if dep.get("package_folder") is not None and "thorvg" not in dep.get(
            "package_folder"
        ):
            continue

        for cpp_info in dep["cpp_info"].values():
            libs = cpp_info.get("libs")
            if libs is None:
                continue
            for lib_name in libs:
                if platform.system() == "Windows":
                    # https://github.com/conan-io/conan-center-index/blob/a83f000910e17ec8612c59fb881930a603d49ff2/recipes/thorvg/all/conanfile.py#L164-L166
                    lib_filename = "{}-0.dll".format(lib_name)
                elif platform.system() == "Darwin":
                    lib_filename = "lib{}.dylib".format(lib_name)
                else:
                    lib_filename = "lib{}.so".format(lib_name)

                if platform.system() == "Windows":
                    libdirs = cpp_info.get("libdirs", []) + cpp_info.get("bindirs", [])
                else:
                    libdirs = cpp_info.get("libdirs", [])
                for lib_dir in libdirs:
                    lib_path = os.path.join(lib_dir, lib_filename)
                    lib_path = lib_path.replace(os.path.dirname(__file__), ".")
                    if os.path.isfile(lib_path):
                        lib_paths.append(lib_path)

    return lib_paths


def compile():
    arch = get_arch()
    print(f"Detected system architecture as {arch}")

    if arch == "universal2":
        conan_info = install_thorvg("x86_64")
        lib_paths = fetch_thorvg(conan_info)
        conan_info = install_thorvg("armv8")
        lib_paths.extend(fetch_thorvg(conan_info))
        print(f"{lib_paths=}")
        subprocess.run(
            [
                "python3",
                "-m",
                "lipomerge",
                lib_paths[0],
                lib_paths[1],
                "src/thorvg_python/",
            ]
        )
    else:
        conan_info = install_thorvg(arch)
        lib_paths = fetch_thorvg(conan_info)
        print(f"{lib_paths=}")
        for lib_path in lib_paths:
            shutil.copy(lib_path, "src/thorvg_python/")

    setup(
        zip_safe=False,
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        include_package_data=True,
        package_data={
            "thorvg_python": ["*.dll", "*.dylib", "*.so"],
        },
    )


if __name__ == "__main__":
    compile()
