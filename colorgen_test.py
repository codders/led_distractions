import pytest
import colorgen

@pytest.fixture
def palette():
    colorgen.palette = [
        (200, 200, 0),
        (100, 0, 200)
    ]
    return colorgen.palette


def test_gradient_interpolation(palette):
    color = colorgen.sample_gradient_palette(0.2)
    assert color[0] == 180  # 20% of the way from 200 to 100
    assert color[1] == 160
    assert color[2] == 40


def test_gradient_alpha1(palette):
    color = colorgen.sample_gradient_palette(1.0)
    assert color == (100, 0, 200)
