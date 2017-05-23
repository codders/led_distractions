import pytest
import colorgen

@pytest.fixture
def palette2():
    colorgen.palette = [
        (200, 200, 0),
        (100, 0, 200)
    ]
    return colorgen.palette


@pytest.fixture
def palette3():
    colorgen.palette = [
        (0, 0, 0),
        (100, 100, 100),
        (200, 200, 200)
    ]


def test_gradient_simple_interpolation(palette2):
    color = colorgen.sample_gradient_palette(0.2)
    assert color[0] == 180  # 20% of the way from 200 to 100
    assert color[1] == 160
    assert color[2] == 40


def test_gradient_alpha_max(palette2):
    color = colorgen.sample_gradient_palette(1.0)
    assert color == (100, 0, 200)


def test_gradient_interpolation_3_colors(palette3):
    color = colorgen.sample_gradient_palette(0.5)
    assert color == (100, 100, 100)
    color = colorgen.sample_gradient_palette(0.75)
    assert color == (150, 150, 150)
