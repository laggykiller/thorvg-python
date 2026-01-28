# thorvg-python

A ctypes API for thorvg, with additional functions for getting Pillow Image.

The functions mostly follow [thorvg/src/bindings/capi/thorvg_capi.h](https://github.com/thorvg/thorvg/blob/v0.15.16/src/bindings/capi/thorvg_capi.h)

Documentations: https://thorvg-python.readthedocs.io/en/latest/

## Table of contents
- [Installing](#installing)
- [Building from source](#building-from-source)
- [Examples](#examples)
- [Credits](#credits)

## Installing

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

## Examples
Drawing and getting pillow image
```python
import thorvg_python as tvg

engine = tvg.Engine(threads=4)
canvas = tvg.SwCanvas(engine)
canvas.set_target(512, 256)  # w, h

rect = tvg.Shape(engine)
rect.append_rect(10, 10, 64, 64, 10, 10)  # x, y, w, h, rx, ry
rect.set_fill_color(32, 64, 128, 100)  # r, g, b, a
canvas.push(rect)

canvas.update()
canvas.draw()
canvas.sync()

im = canvas.get_pillow()
canvas.destroy()
engine.term()
```

Rendering lottie animation
```python
import thorvg_python as tvg
from PIL import Image

engine = tvg.Engine(threads=4)
canvas = tvg.SwCanvas(engine)
canvas.set_target(512, 512)  # w, h

animation = tvg.LottieAnimation(engine)
picture = animation.get_picture()
picture.load("tests/test.json")
picture.set_size(512, 512)

canvas.push(picture)

ims: list[Image.Image] = []
result, total_frame = animation.get_total_frame()
result, duration = animation.get_duration()
frame_duration = duration / total_frame
# fps = total_frame / duration
for i in range(int(total_frame)):
    animation.set_frame(i)
    canvas.update()
    canvas.draw()
    canvas.sync()
    im = canvas.get_pillow()
    ims.append(im)

ims[0].save("test.apng", save_all=True, append_images=ims[1:], duration=frame_duration * 1000)
```

## Building from source

To build wheel, run the following:
```bash
git clone --recursive https://github.com/laggykiller/thorvg-python.git
cd thorvg-python

# To build wheel
python3 -m build .

# To install directly
pip3 install .
```

## Development
To run tests:
```bash
pip install pytest
pytest
```

To lint:
```bash
pip install ruff mypy isort
mypy
isort .
ruff check
ruff format
```

## Credits
- thorvg library: https://github.com/thorvg/thorvg