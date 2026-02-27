#!/usr/bin/env python3
import os
import platform
from importlib.util import find_spec
from typing import TYPE_CHECKING, List, Tuple

import pytest

import thorvg_python as tvg

PILLOW_LOADED = True if find_spec("PIL") else False
file_dir = os.path.split(__file__)[0]
ref_dir = os.path.join(file_dir, "ref")

if TYPE_CHECKING:
    from PIL import Image


def check_im_same(im: "Image.Image", im_ref_name: str):
    from PIL import Image, ImageChops

    # im.save(os.path.join(ref_dir, im_ref_name))
    im_ref = Image.open(os.path.join(ref_dir, im_ref_name))
    return ImageChops.difference(im_ref, im).getbbox() is None


def test_engine():
    engine = tvg.Engine()
    assert engine.init_result == tvg.Result.SUCCESS
    _, _, _, _, version = engine.version()
    assert version is not None
    assert engine.term() == tvg.Result.SUCCESS


def _test_swcanvas(cs: tvg.Colorspace, op: tvg.EngineOption, with_stride: bool):
    engine = tvg.Engine()
    canvas = tvg.SwCanvas(engine, op)
    if with_stride:
        stride = 512
    else:
        stride = None
    canvas.set_target(512, 256, stride, cs)

    rect = tvg.Shape(engine)
    assert rect.append_rect(10, 10, 64, 64, 10, 10, True) == tvg.Result.SUCCESS
    assert rect.set_fill_color(32, 64, 128, 100) == tvg.Result.SUCCESS
    assert canvas.add(rect) == tvg.Result.SUCCESS

    assert canvas.update() == tvg.Result.SUCCESS
    assert canvas.draw(clear=True) == tvg.Result.SUCCESS
    assert canvas.sync() == tvg.Result.SUCCESS

    if PILLOW_LOADED:
        im = canvas.get_pillow()
        assert check_im_same(im, "test_canvas_ref.png") is True

    assert canvas.destroy() == tvg.Result.SUCCESS
    assert engine.term() == tvg.Result.SUCCESS


def test_swcanvas_abgr8888():
    _test_swcanvas(tvg.Colorspace.ABGR8888, tvg.EngineOption.DEFAULT, True)


def test_swcanvas_abgr8888s():
    _test_swcanvas(tvg.Colorspace.ABGR8888S, tvg.EngineOption.DEFAULT, True)


def test_swcanvas_argb8888():
    _test_swcanvas(tvg.Colorspace.ARGB8888, tvg.EngineOption.DEFAULT, True)


def test_swcanvas_argb8888s():
    _test_swcanvas(tvg.Colorspace.ARGB8888S, tvg.EngineOption.DEFAULT, True)


def test_swcanvas_op_none():
    _test_swcanvas(tvg.Colorspace.ABGR8888, tvg.EngineOption.NONE, True)


def test_swcanvas_op_smart_render():
    _test_swcanvas(tvg.Colorspace.ABGR8888, tvg.EngineOption.SMART_RENDER, True)


def test_swcanvas_no_stride():
    _test_swcanvas(tvg.Colorspace.ABGR8888, tvg.EngineOption.DEFAULT, False)


def test_canvas_viewport():
    engine = tvg.Engine()
    canvas = tvg.SwCanvas(engine)
    canvas.set_target(512, 256, 512)

    # Shapes at the right should not be rendered
    assert canvas.set_viewport(0, 0, 256, 256) == tvg.Result.SUCCESS

    # Shape at left
    rect1 = tvg.Shape(engine)
    assert rect1.append_rect(10, 10, 64, 64, 10, 10, True) == tvg.Result.SUCCESS
    assert rect1.set_fill_color(32, 64, 128, 100) == tvg.Result.SUCCESS
    assert canvas.add(rect1) == tvg.Result.SUCCESS

    # Shape at right
    rect2 = tvg.Shape(engine)
    assert rect2.append_rect(260, 10, 64, 64, 10, 10, True) == tvg.Result.SUCCESS
    assert rect2.set_fill_color(32, 64, 128, 100) == tvg.Result.SUCCESS
    assert canvas.add(rect2) == tvg.Result.SUCCESS

    assert canvas.update() == tvg.Result.SUCCESS
    assert canvas.draw(True) == tvg.Result.SUCCESS
    assert canvas.sync() == tvg.Result.SUCCESS

    if PILLOW_LOADED:
        im = canvas.get_pillow()
        assert check_im_same(im, "test_canvas_ref.png") is True

    assert canvas.destroy() == tvg.Result.SUCCESS
    assert engine.term() == tvg.Result.SUCCESS


def test_canvas_clear():
    engine = tvg.Engine()
    canvas = tvg.SwCanvas(engine)
    canvas.set_target(512, 256, 512)

    rect1 = tvg.Shape(engine)
    assert rect1.append_rect(0, 0, 64, 64, 10, 10, True) == tvg.Result.SUCCESS
    assert rect1.set_fill_color(128, 32, 64, 50) == tvg.Result.SUCCESS
    assert canvas.add(rect1) == tvg.Result.SUCCESS
    assert canvas.remove(None) == tvg.Result.SUCCESS

    rect2 = tvg.Shape(engine)
    assert rect2.append_rect(10, 10, 64, 64, 10, 10, True) == tvg.Result.SUCCESS
    assert rect2.set_fill_color(32, 64, 128, 100) == tvg.Result.SUCCESS
    assert canvas.add(rect2) == tvg.Result.SUCCESS

    assert canvas.update() == tvg.Result.SUCCESS
    assert canvas.draw(True) == tvg.Result.SUCCESS
    assert canvas.sync() == tvg.Result.SUCCESS

    if PILLOW_LOADED:
        im = canvas.get_pillow()
        assert check_im_same(im, "test_canvas_ref.png") is True

    assert canvas.destroy() == tvg.Result.SUCCESS
    assert engine.term() == tvg.Result.SUCCESS


def test_shape_path():
    engine = tvg.Engine()
    canvas = tvg.SwCanvas(engine)
    canvas.set_target(512, 512)

    shape = tvg.Shape(engine)

    assert shape.move_to(199, 34) == tvg.Result.SUCCESS
    assert shape.line_to(253, 143) == tvg.Result.SUCCESS
    assert shape.line_to(374, 160) == tvg.Result.SUCCESS
    assert shape.line_to(287, 244) == tvg.Result.SUCCESS
    assert shape.line_to(307, 365) == tvg.Result.SUCCESS
    assert shape.line_to(199, 309) == tvg.Result.SUCCESS
    assert shape.line_to(97, 365) == tvg.Result.SUCCESS
    assert shape.line_to(112, 245) == tvg.Result.SUCCESS
    assert shape.line_to(26, 161) == tvg.Result.SUCCESS
    assert shape.line_to(146, 143) == tvg.Result.SUCCESS
    assert shape.close() == tvg.Result.SUCCESS
    assert shape.set_fill_color(0, 0, 255, 255) == tvg.Result.SUCCESS
    assert canvas.add(shape) == tvg.Result.SUCCESS

    assert canvas.draw(True) == tvg.Result.SUCCESS
    assert canvas.sync() == tvg.Result.SUCCESS

    if PILLOW_LOADED:
        im = canvas.get_pillow()
        assert check_im_same(im, "test_shape_path_ref1.png") is True

    cx = 256
    cy = 256
    radius = 256
    halfRadius = radius * 0.552284

    assert canvas.set_target(512, 512) == tvg.Result.SUCCESS
    assert shape.reset() == tvg.Result.SUCCESS
    assert shape.move_to(cx, cy - radius) == tvg.Result.SUCCESS
    assert (
        shape.cubic_to(
            cx + halfRadius, cy - radius, cx + radius, cy - halfRadius, cx + radius, cy
        )
        == tvg.Result.SUCCESS
    )
    assert (
        shape.cubic_to(
            cx + radius, cy + halfRadius, cx + halfRadius, cy + radius, cx, cy + radius
        )
        == tvg.Result.SUCCESS
    )
    assert (
        shape.cubic_to(
            cx - halfRadius, cy + radius, cx - radius, cy + halfRadius, cx - radius, cy
        )
        == tvg.Result.SUCCESS
    )
    assert (
        shape.cubic_to(
            cx - radius, cy - halfRadius, cx - halfRadius, cy - radius, cx, cy - radius
        )
        == tvg.Result.SUCCESS
    )
    assert shape.close() == tvg.Result.SUCCESS
    assert shape.set_fill_color(255, 0, 0, 255) == tvg.Result.SUCCESS

    assert canvas.draw(True) == tvg.Result.SUCCESS
    assert canvas.sync() == tvg.Result.SUCCESS

    if PILLOW_LOADED:
        im = canvas.get_pillow()
        assert check_im_same(im, "test_shape_path_ref2.png") is True

    assert canvas.destroy() == tvg.Result.SUCCESS
    assert engine.term() == tvg.Result.SUCCESS


def test_shape_append_rect():
    engine = tvg.Engine()
    canvas = tvg.SwCanvas(engine)
    canvas.set_target(512, 256)

    shape = tvg.Shape(engine)
    assert shape.append_rect(10, 10, 64, 64, 10, 10, True) == tvg.Result.SUCCESS
    assert shape.set_fill_color(32, 64, 128, 100) == tvg.Result.SUCCESS
    assert canvas.add(shape) == tvg.Result.SUCCESS

    assert canvas.draw(True) == tvg.Result.SUCCESS
    assert canvas.sync() == tvg.Result.SUCCESS

    if PILLOW_LOADED:
        im = canvas.get_pillow()
        assert check_im_same(im, "test_canvas_ref.png") is True

    assert canvas.destroy() == tvg.Result.SUCCESS
    assert engine.term() == tvg.Result.SUCCESS


def test_shape_append_circle():
    engine = tvg.Engine()
    canvas = tvg.SwCanvas(engine)
    canvas.set_target(512, 256)

    shape = tvg.Shape(engine)
    assert shape.append_circle(256, 128, 64, 32, True) == tvg.Result.SUCCESS
    assert shape.set_fill_color(32, 64, 128, 100) == tvg.Result.SUCCESS
    assert canvas.add(shape) == tvg.Result.SUCCESS

    assert canvas.draw(True) == tvg.Result.SUCCESS
    assert canvas.sync() == tvg.Result.SUCCESS

    if PILLOW_LOADED:
        im = canvas.get_pillow()
        assert check_im_same(im, "test_shape_append_circle_ref.png") is True

    assert canvas.destroy() == tvg.Result.SUCCESS
    assert engine.term() == tvg.Result.SUCCESS


def test_shape_get_path_commands():
    engine = tvg.Engine()
    shape = tvg.Shape(engine)
    shape.append_rect(16, 32, 64, 128, 0, 0, True)

    result, cmds, pts = shape.get_path()
    assert result is tvg.Result.SUCCESS
    cmds_list: List[tvg.PathCommand] = []
    for cmd in cmds:
        cmds_list.append(cmd)
    pts_list: List[Tuple[float, float]] = []
    for pt in pts:
        pts_list.append((pt.x, pt.y))
    assert cmds_list == [
        tvg.PathCommand.MOVE_TO,
        tvg.PathCommand.LINE_TO,
        tvg.PathCommand.LINE_TO,
        tvg.PathCommand.LINE_TO,
        tvg.PathCommand.CLOSE,
    ]
    assert pts_list == [(80.0, 32.0), (80.0, 160.0), (16.0, 160.0), (16.0, 32.0)]
    assert engine.term() == tvg.Result.SUCCESS


def test_paint():
    engine = tvg.Engine()
    scene = tvg.Scene(engine)

    shape = tvg.Shape(engine)
    assert scene.add(shape) == tvg.Result.SUCCESS
    assert shape.append_rect(16, 32, 64, 128, 0, 0, True) == tvg.Result.SUCCESS
    assert shape.scale(2.0) == tvg.Result.SUCCESS
    assert shape.rotate(45) == tvg.Result.SUCCESS
    assert shape.translate(60, 80) == tvg.Result.SUCCESS

    assert shape.set_opacity(60) == tvg.Result.SUCCESS
    assert shape.get_opacity() == (tvg.Result.SUCCESS, 60)

    matrix_list = [1, 0, 0, 0, 1, 0, 0, 0, 1]
    matrix = tvg.Matrix(*matrix_list)
    shape.set_transform(matrix)
    transform_result, matrix_out = shape.get_transform()
    assert transform_result == tvg.Result.SUCCESS
    matrix_out_list = [
        matrix_out.e11,
        matrix_out.e12,
        matrix_out.e13,
        matrix_out.e21,
        matrix_out.e22,
        matrix_out.e23,
        matrix_out.e31,
        matrix_out.e32,
        matrix_out.e33,
    ]
    assert matrix_list == matrix_out_list

    shape2 = tvg.Shape(engine)
    assert shape.set_mask_method(shape2, tvg.MaskMethod.DARKEN) == tvg.Result.SUCCESS
    result, method = shape.get_mask_method(shape2)
    assert result == tvg.Result.SUCCESS
    assert method == tvg.MaskMethod.DARKEN

    shape3 = tvg.Shape(engine)
    assert shape.set_clip(shape3) == tvg.Result.SUCCESS
    assert shape.get_type() == (tvg.Result.SUCCESS, tvg.TvgType.SHAPE)
    assert shape.set_blend_method(tvg.BlendMethod.ADD) == tvg.Result.SUCCESS

    # assert isinstance(shape.duplicate(), tvg.base.PaintPointer)

    assert engine.term() == tvg.Result.SUCCESS


def test_stroke():
    engine = tvg.Engine()
    canvas = tvg.SwCanvas(engine)
    canvas.set_target(512, 256)

    line = tvg.Shape(engine)

    assert line.move_to(20, 40) == tvg.Result.SUCCESS
    assert line.line_to(256, 40) == tvg.Result.SUCCESS
    assert line.line_to(256, 128) == tvg.Result.SUCCESS
    assert line.line_to(20, 128) == tvg.Result.SUCCESS
    assert line.close() == tvg.Result.SUCCESS

    assert line.set_fill_color(150, 150, 255, 100) == tvg.Result.SUCCESS
    assert line.set_stroke_width(5) == tvg.Result.SUCCESS
    assert line.set_stroke_color(32, 64, 128, 100) == tvg.Result.SUCCESS
    assert line.set_stroke_cap(tvg.StrokeCap.SQUARE) == tvg.Result.SUCCESS
    assert line.set_stroke_join(tvg.StrokeJoin.BEVEL) == tvg.Result.SUCCESS
    assert line.set_stroke_miterlimit(3.0) == tvg.Result.SUCCESS
    pattern = [7.0, 10.0]
    assert line.set_stroke_dash(pattern, 0) == tvg.Result.SUCCESS
    assert canvas.add(line) == tvg.Result.SUCCESS

    assert canvas.draw(True) == tvg.Result.SUCCESS
    assert canvas.sync() == tvg.Result.SUCCESS

    if PILLOW_LOADED:
        im = canvas.get_pillow()
        assert check_im_same(im, "test_stroke_ref.png") is True

    assert line.get_stroke_width() == (tvg.Result.SUCCESS, 5.0)
    assert line.get_stroke_color() == (tvg.Result.SUCCESS, 32, 64, 128, 100)
    assert line.get_stroke_cap() == (tvg.Result.SUCCESS, tvg.StrokeCap.SQUARE)
    assert line.get_stroke_dash() == (tvg.Result.SUCCESS, pattern, 0.0)
    assert line.get_stroke_join() == (tvg.Result.SUCCESS, tvg.StrokeJoin.BEVEL)
    assert line.get_stroke_miterlimit() == (tvg.Result.SUCCESS, 3.0)

    assert canvas.destroy() == tvg.Result.SUCCESS
    assert engine.term() == tvg.Result.SUCCESS


def test_fill():
    engine = tvg.Engine()
    canvas = tvg.SwCanvas(engine)
    canvas.set_target(512, 256)

    shape = tvg.Shape(engine)
    assert shape.append_rect(10, 10, 64, 64, 10, 10, True) == tvg.Result.SUCCESS

    assert shape.set_fill_rule(tvg.FillRule.EVEN_ODD) == tvg.Result.SUCCESS
    assert shape.set_fill_color(32, 64, 128, 100) == tvg.Result.SUCCESS
    assert shape.set_paint_order(True) == tvg.Result.SUCCESS
    assert shape.set_stroke_color(128, 64, 32, 150) == tvg.Result.SUCCESS
    assert shape.set_stroke_width(3) == tvg.Result.SUCCESS

    assert canvas.add(shape) == tvg.Result.SUCCESS

    assert canvas.draw(True) == tvg.Result.SUCCESS
    assert canvas.sync() == tvg.Result.SUCCESS

    if PILLOW_LOADED:
        im = canvas.get_pillow()
        assert check_im_same(im, "test_fill_ref.png") is True

    assert shape.get_fill_color() == (tvg.Result.SUCCESS, 32, 64, 128, 100)
    assert shape.get_fill_rule() == (tvg.Result.SUCCESS, tvg.FillRule.EVEN_ODD)

    assert canvas.destroy() == tvg.Result.SUCCESS
    assert engine.term() == tvg.Result.SUCCESS


def _test_gradient(gradient_type: str):
    engine = tvg.Engine()
    canvas = tvg.SwCanvas(engine)
    canvas.set_target(512, 256)

    shape = tvg.Shape(engine)
    assert shape.append_rect(0, 0, 512, 256, 0, 0, True) == tvg.Result.SUCCESS

    fill: tvg.Gradient
    if gradient_type == "linear":
        fill = tvg.LinearGradient(engine)
    elif gradient_type == "radial":
        fill = tvg.RadialGradient(engine)
    else:
        raise RuntimeError(f"Invalid gradient_type {gradient_type}")

    color_stops_list = [(0, 0, 0, 0, 255), (1, 255, 255, 255, 255)]
    color_stops: List[tvg.ColorStop] = []
    for i in color_stops_list:
        color_stops.append(tvg.ColorStop(*i))
    matrix_list = [1, 0, 0, 0, 1, 0, 0, 0, 1]
    matrix = tvg.Matrix(*matrix_list)

    if isinstance(fill, tvg.LinearGradient):
        assert fill.set(0, 0, 100, 100) == tvg.Result.SUCCESS
    elif isinstance(fill, tvg.RadialGradient):  # type: ignore
        assert fill.set(100, 100, 50, 100, 100, 50) == tvg.Result.SUCCESS
    else:
        raise RuntimeError(f"Invalid fill type {type(fill)}")

    assert fill.set_color_stops(color_stops) == tvg.Result.SUCCESS
    assert fill.set_spread(tvg.StrokeFill.REPEAT) == tvg.Result.SUCCESS
    assert fill.set_transform(matrix) == tvg.Result.SUCCESS
    assert shape.set_gradient(fill) == tvg.Result.SUCCESS
    assert canvas.add(shape) == tvg.Result.SUCCESS

    assert canvas.draw(True) == tvg.Result.SUCCESS
    assert canvas.sync() == tvg.Result.SUCCESS

    if PILLOW_LOADED:
        im = canvas.get_pillow()
        assert check_im_same(im, f"test_{gradient_type}_gradient_ref.png") is True

    result_get, fill_out = shape.get_gradient()
    assert result_get == tvg.Result.SUCCESS

    if isinstance(fill_out, tvg.LinearGradient):
        assert fill_out.get() == (tvg.Result.SUCCESS, 0, 0, 100, 100)
        assert isinstance(fill_out.duplicate(), tvg.LinearGradient)
    elif isinstance(fill_out, tvg.RadialGradient):  # type: ignore
        assert fill_out.get() == (tvg.Result.SUCCESS, 100, 100, 50, 100, 100, 50)
        assert isinstance(fill_out.duplicate(), tvg.RadialGradient)
    else:
        raise RuntimeError(f"Invalid fill_out type {type(fill_out)}")

    color_stops_result, color_stops_out = fill_out.get_color_stops()
    assert color_stops_result == tvg.Result.SUCCESS
    color_stops_out_list: List[Tuple[float, float, float, float, float]] = []
    for j in color_stops_out:
        color_stops_out_list.append((j.offset, j.r, j.g, j.b, j.a))
    assert color_stops_list == color_stops_out_list

    assert fill_out.get_spread() == (tvg.Result.SUCCESS, tvg.StrokeFill.REPEAT)

    transform_result, matrix_out = fill_out.get_transform()
    assert transform_result == tvg.Result.SUCCESS
    matrix_out_list = [
        matrix_out.e11,
        matrix_out.e12,
        matrix_out.e13,
        matrix_out.e21,
        matrix_out.e22,
        matrix_out.e23,
        matrix_out.e31,
        matrix_out.e32,
        matrix_out.e33,
    ]
    assert matrix_list == matrix_out_list

    assert canvas.destroy() == tvg.Result.SUCCESS
    assert engine.term() == tvg.Result.SUCCESS


def test_gradient_linear():
    _test_gradient("linear")


def test_gradient_radial():
    _test_gradient("radial")


def _test_picture_load(test_file: str, ref: str):
    engine = tvg.Engine()
    canvas = tvg.SwCanvas(engine)
    canvas.set_target(256, 256)

    picture = tvg.Picture(engine)
    assert picture.load(os.path.join(file_dir, test_file)) == tvg.Result.SUCCESS
    assert picture.set_size(256, 256) == tvg.Result.SUCCESS
    assert picture.translate(0, 0) == tvg.Result.SUCCESS
    assert canvas.add(picture) == tvg.Result.SUCCESS

    assert canvas.draw(True) == tvg.Result.SUCCESS
    assert canvas.sync() == tvg.Result.SUCCESS

    if PILLOW_LOADED:
        im = canvas.get_pillow()
        assert check_im_same(im, ref) is True

    assert picture.get_size() == (tvg.Result.SUCCESS, 256, 256)

    assert canvas.destroy() == tvg.Result.SUCCESS
    assert engine.term() == tvg.Result.SUCCESS


def test_picture_load_svg():
    _test_picture_load("test.svg", "test_picture_svg_ref.png")


def test_picture_load_png():
    _test_picture_load("test.png", "test_picture_png_ref.png")


def test_picture_load_webp():
    _test_picture_load("test.webp", "test_picture_webp_ref.png")


def test_picture_load_jpg():
    _test_picture_load("test.jpg", "test_picture_jpg_ref.png")


def test_picture_load_lottie():
    _test_picture_load("test.json", "test_picture_lottie_ref.png")


def _test_picture_load_raw(test_file: str, ref: str, copy: bool):
    from PIL import Image

    engine = tvg.Engine()
    canvas = tvg.SwCanvas(engine)
    canvas.set_target(512, 256)

    with Image.open(os.path.join(file_dir, test_file)) as im:
        im_h = im.height
        im_w = im.width
        im_bytes = im.tobytes()  # type: ignore

    picture = tvg.Picture(engine)
    assert (
        picture.load_raw(im_bytes, im_w, im_h, tvg.Colorspace.ABGR8888, copy)
        == tvg.Result.SUCCESS
    )
    assert picture.set_size(256, 256) == tvg.Result.SUCCESS
    assert picture.translate(0, 0) == tvg.Result.SUCCESS
    assert canvas.add(picture) == tvg.Result.SUCCESS

    assert canvas.draw(True) == tvg.Result.SUCCESS
    assert canvas.sync() == tvg.Result.SUCCESS

    if PILLOW_LOADED:
        im = canvas.get_pillow()
        assert check_im_same(im, ref) is True

    assert picture.get_size() == (tvg.Result.SUCCESS, 256, 256)

    assert canvas.destroy() == tvg.Result.SUCCESS
    assert engine.term() == tvg.Result.SUCCESS


@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
def test_picture_load_raw_copy_true():
    _test_picture_load_raw("test.png", "test_picture_png_ref.png", True)


@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
@pytest.mark.skipif(
    platform.system() == "Windows", reason="Known failure if on Windows"
)
def test_picture_load_raw_copy_false():
    _test_picture_load_raw("test.png", "test_picture_png_ref.png", False)


def _test_picture_load_data(test_file: str, ref: str, mimetype: str, copy: bool):
    engine = tvg.Engine()
    canvas = tvg.SwCanvas(engine)
    canvas.set_target(512, 256)

    with open(os.path.join(file_dir, test_file), "rb") as f:
        data = f.read()

    picture = tvg.Picture(engine)
    assert picture.load_data(data, mimetype, None, copy) == tvg.Result.SUCCESS
    if copy is False:
        del data
    assert picture.set_size(256, 256) == tvg.Result.SUCCESS
    assert picture.translate(0, 0) == tvg.Result.SUCCESS
    assert canvas.add(picture) == tvg.Result.SUCCESS

    assert canvas.draw(True) == tvg.Result.SUCCESS
    assert canvas.sync() == tvg.Result.SUCCESS

    if PILLOW_LOADED:
        im = canvas.get_pillow()
        assert check_im_same(im, ref) is True

    assert picture.get_size() == (tvg.Result.SUCCESS, 256, 256)

    assert canvas.destroy() == tvg.Result.SUCCESS
    assert engine.term() == tvg.Result.SUCCESS


def test_picture_load_data_svg():
    _test_picture_load_data("test.svg", "test_picture_svg_ref.png", "svg", True)


def test_picture_load_data_png():
    _test_picture_load_data("test.png", "test_picture_png_ref.png", "png", True)


def test_picture_load_data_webp():
    _test_picture_load_data("test.webp", "test_picture_webp_ref.png", "webp", True)


def test_picture_load_data_jpg():
    _test_picture_load_data("test.jpg", "test_picture_jpg_ref.png", "jpg", True)


def test_picture_load_data_jpeg():
    _test_picture_load_data("test.jpg", "test_picture_jpg_ref.png", "jpeg", True)


def test_picture_load_data_svg_no_mimetype():
    _test_picture_load_data("test.svg", "test_picture_svg_ref.png", "", True)


def test_picture_load_data_png_no_mimetype():
    _test_picture_load_data("test.png", "test_picture_png_ref.png", "", True)


def test_picture_load_data_webp_no_mimetype():
    _test_picture_load_data("test.webp", "test_picture_webp_ref.png", "", True)


def test_picture_load_data_jpg_no_mimetype():
    _test_picture_load_data("test.jpg", "test_picture_jpg_ref.png", "", True)


def test_picture_load_data_svg_invalid_mimetype():
    _test_picture_load_data(
        "test.svg", "test_picture_svg_ref.png", "invalid_mimetype", True
    )


def test_picture_load_data_png_invalid_mimetype():
    _test_picture_load_data(
        "test.png", "test_picture_png_ref.png", "invalid_mimetype", True
    )


def test_picture_load_data_webp_invalid_mimetype():
    _test_picture_load_data(
        "test.webp", "test_picture_webp_ref.png", "invalid_mimetype", True
    )


def test_picture_load_data_jpg_invalid_mimetype():
    _test_picture_load_data(
        "test.jpg", "test_picture_jpg_ref.png", "invalid_mimetype", True
    )


def test_picture_load_data_copy_false():
    _test_picture_load_data("test.png", "test_picture_png_ref.png", "png", False)


def test_scene():
    engine = tvg.Engine()
    canvas = tvg.SwCanvas(engine)
    canvas.set_target(512, 256, 512)

    scene = tvg.Scene(engine)
    rect = tvg.Shape(engine)
    assert rect.append_rect(10, 10, 64, 64, 10, 10, True) == tvg.Result.SUCCESS
    assert rect.set_fill_color(32, 64, 128, 100) == tvg.Result.SUCCESS
    assert scene.add(rect) == tvg.Result.SUCCESS

    assert canvas.add(scene) == tvg.Result.SUCCESS
    assert canvas.update() == tvg.Result.SUCCESS
    assert canvas.draw(True) == tvg.Result.SUCCESS
    assert canvas.sync() == tvg.Result.SUCCESS

    if PILLOW_LOADED:
        im = canvas.get_pillow()
        assert check_im_same(im, "test_canvas_ref.png") is True

    assert canvas.destroy() == tvg.Result.SUCCESS
    assert engine.term() == tvg.Result.SUCCESS


def test_scene_clear():
    engine = tvg.Engine()
    canvas = tvg.SwCanvas(engine)
    canvas.set_target(512, 256, 512)
    scene = tvg.Scene(engine)
    assert canvas.add(scene) == tvg.Result.SUCCESS

    rect1 = tvg.Shape(engine)
    assert rect1.append_rect(0, 0, 64, 64, 10, 10, True) == tvg.Result.SUCCESS
    assert rect1.set_fill_color(128, 32, 64, 50) == tvg.Result.SUCCESS
    assert scene.add(rect1) == tvg.Result.SUCCESS
    assert scene.remove(None) == tvg.Result.SUCCESS

    rect2 = tvg.Shape(engine)
    assert rect2.append_rect(10, 10, 64, 64, 10, 10, True) == tvg.Result.SUCCESS
    assert rect2.set_fill_color(32, 64, 128, 100) == tvg.Result.SUCCESS
    assert scene.add(rect2) == tvg.Result.SUCCESS

    assert canvas.update() == tvg.Result.SUCCESS
    assert canvas.draw(True) == tvg.Result.SUCCESS
    assert canvas.sync() == tvg.Result.SUCCESS

    if PILLOW_LOADED:
        im = canvas.get_pillow()
        assert check_im_same(im, "test_canvas_ref.png") is True

    assert canvas.destroy() == tvg.Result.SUCCESS
    assert engine.term() == tvg.Result.SUCCESS


def _test_text(font: str, unicode: bool):
    font_name = font.split(".")[0]
    engine = tvg.Engine()
    canvas = tvg.SwCanvas(engine)
    canvas.set_target(512, 256, 512)

    text1 = tvg.Text(engine)
    assert text1.font_load(os.path.join("tests", font)) == tvg.Result.SUCCESS
    assert text1.set_font(font_name) == tvg.Result.SUCCESS
    assert text1.set_size(32) == tvg.Result.SUCCESS
    assert (
        text1.set_text(f"Solid Text {'テスト' if unicode is True else ''}")
        == tvg.Result.SUCCESS
    )
    assert text1.set_color(0, 0, 0) == tvg.Result.SUCCESS
    assert text1.wrap_mode(tvg.TextWrap.ELLIPSIS) == tvg.Result.SUCCESS
    assert text1.translate(10, 10) == tvg.Result.SUCCESS
    assert canvas.add(text1) == tvg.Result.SUCCESS

    text2 = tvg.Text(engine)
    assert text2.set_font(font_name) == tvg.Result.SUCCESS
    assert text2.set_size(32) == tvg.Result.SUCCESS
    assert (
        text2.set_text(f"Gradient Text {'テスト' if unicode is True else ''}")
        == tvg.Result.SUCCESS
    )
    assert text2.translate(10, 100) == tvg.Result.SUCCESS

    fill = tvg.LinearGradient(engine)
    assert fill.set(0, 0, 512, 256) == tvg.Result.SUCCESS
    colorstops = [
        tvg.ColorStop(0.0, 255, 0, 0, 100),
        tvg.ColorStop(1.0, 255, 255, 0, 255),
    ]
    assert fill.set_color_stops(colorstops) == tvg.Result.SUCCESS

    assert text2.set_gradient(fill) == tvg.Result.SUCCESS
    assert canvas.add(text2) == tvg.Result.SUCCESS

    assert canvas.update() == tvg.Result.SUCCESS
    assert canvas.draw(True) == tvg.Result.SUCCESS
    assert canvas.sync() == tvg.Result.SUCCESS

    if PILLOW_LOADED:
        im = canvas.get_pillow()
        assert check_im_same(im, f"test_text_{font_name}_ref.png") is True

    assert text1.font_unload(os.path.join("tests", font)) == tvg.Result.SUCCESS
    assert canvas.destroy() == tvg.Result.SUCCESS
    assert engine.term() == tvg.Result.SUCCESS


def test_text_arial():
    _test_text("Arial.ttf", False)


def test_text_notosans():
    _test_text("NotoSansJP.ttf", True)


def test_animation():
    engine = tvg.Engine()

    animation = tvg.LottieAnimation(engine)
    picture = animation.get_picture()
    assert isinstance(picture, tvg.Picture)
    assert picture.load(os.path.join(file_dir, "test.json")) == tvg.Result.SUCCESS
    assert animation.get_total_frame() == (tvg.Result.SUCCESS, 50)
    assert picture.set_size(512, 512) == tvg.Result.SUCCESS

    assert animation.set_frame(5) == tvg.Result.SUCCESS
    assert animation.set_segment(0, 25) == tvg.Result.SUCCESS

    result, duration = animation.get_duration()
    assert result == tvg.Result.SUCCESS
    assert duration == 1
    assert animation.get_frame() == (tvg.Result.SUCCESS, 5)
    assert animation.get_segment() == (tvg.Result.SUCCESS, 0, 25)
    assert animation.get_total_frame() == (tvg.Result.SUCCESS, 25)
    assert animation.get_markers_cnt() == (tvg.Result.SUCCESS, 0)
    assert engine.term() == tvg.Result.SUCCESS
