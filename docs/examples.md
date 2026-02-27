# Examples

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
canvas.draw(True)
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
    canvas.draw(True)
    canvas.sync()
    im = canvas.get_pillow()
    ims.append(im)

ims[0].save("test.apng", save_all=True, append_images=ims[1:], duration=frame_duration * 1000)
```