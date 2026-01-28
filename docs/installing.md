# Installing

Note that thorvg is included in the wheel package, you need not install libthorvg.
Version bundled is the version available on [Conan](https://conan.io/center/recipes/thorvg)
(Currently 0.15.16)

To install, run the following:
```bash
pip3 install thorvg-python
```

`Pillow` is optional dependency. It is required for `SwCanvas.get_pillow()`. To also install Pillow, run:
```bash
pip3 install thorvg-python[full]
```