# Copyright (c) 2020, Manfred Moitzi
# License: MIT License
import pytest

from ezdxf.tools import pattern


def test_load_iso_pattern():
    p = pattern.load()
    assert p['ANSI31'][0] == [45.0, (0.0, 0.0), (-2.2450640303, 2.2450640303),
                              []]


def test_load_scaled_iso_pattern():
    p = pattern.load(factor=2)
    assert p['ANSI31'][0] == [45.0, (0.0, 0.0), (-4.4901280606, 4.4901280606), []]


def test_load_imperial_pattern():
    p = pattern.load(measurement=0)
    assert p['ANSI31'][0] == [45.0, (0.0, 0.0), (-0.0883883476, 0.0883883476), []]


def test_scale_pattern():
    p = pattern.load()
    ansi31 = p['ANSI31']
    s = pattern.scale_pattern(ansi31, 2, angle=90)

    angle, base, offset, lines = s[0]
    assert angle == 135
    assert base == (0, 0)
    assert offset == (-4.4901280606, -4.4901280606)


def test_scale_all_pattern():
    r = pattern.scale_all(pattern.ISO_PATTERN)
    assert len(r) == len(pattern.ISO_PATTERN)


TEST_PATTERN = """; Hatch Patterns adapted to ISO scaling

;; Note: Dummy pattern description used for 'Solid fill'.
*SOLID, Solid fill
45, 0,0, 0,.125
*ANSI31, ANSI Iron, Brick, Stone masonry
45, 0,0, 0,3.175 
*ANSI32, ANSI Steel
45, 0,0, 0,9.525 
45, 4.490128053,0, 0,9.525 
*ANSI33, ANSI Bronze, Brass, Copper
45, 0,0, 0,6.35 
45, 4.490128053,0, 0,6.35, 3.175,-1.5875
*ANSI34, ANSI Plastic, Rubber
45, 0,0, 0,19.05 
45, 4.490128053,0, 0,19.05 
45, 8.9802561314,0, 0,19.05 
45, 13.4703841844,0, 0,19.05 
*ANSI35, ANSI Fire brick, Refractory material
45, 0,0, 0,6.35 
45, 4.490128053,0, 0,6.35, 7.9375,-1.5875,0,-1.5875
*ANSI36, ANSI Marble, Slate, Glass
45, 0,0, 5.55625,3.175, 7.9375,-1.5875,0,-1.5875
*ANSI37, ANSI Lead, Zinc, Magnesium, Sound/Heat/Elec Insulation
45, 0,0, 0,3.175 
135, 0,0, 0,3.175 
*ANSI38, ANSI Aluminum
45, 0,0, 0,3.175 
135, 0,0, 6.35,3.175, 7.9375,-4.7625

"""


def test_parse_pattern_file():
    result = pattern.parse(TEST_PATTERN)
    assert len(result) == 9
    assert result['SOLID'] == [
        [45.0, (0.0, 0.0), (-0.0883883476, 0.0883883476), []]]
    assert result['ANSI33'] == [
        [45.0, (0.0, 0.0), (-4.4901280605, 4.4901280605), []],
        [45.0, (4.490128053, 0.0), (-4.4901280605, 4.4901280605),
         [3.175, -1.5875]]
    ]


if __name__ == '__main__':
    pytest.main([__file__])
