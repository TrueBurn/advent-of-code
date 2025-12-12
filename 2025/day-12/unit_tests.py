"""Unit tests for Day 12: Christmas Tree Farm."""

import os
import unittest
from textwrap import dedent

from solution import (
    can_fit_pieces,
    get_all_variants,
    normalize,
    parse_input,
    part1,
)


class TestDay12(unittest.TestCase):
    """Test cases for Day 12."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_file = "test_input.txt"

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_example_part1(self):
        """Test the example from the problem description."""
        with open(self.test_file, "w") as f:
            f.write(
                dedent(
                    """\
                    0:
                    ###
                    ##.
                    ##.

                    1:
                    ###
                    ##.
                    .##

                    2:
                    .##
                    ###
                    ##.

                    3:
                    ##.
                    ###
                    ##.

                    4:
                    ###
                    #..
                    ###

                    5:
                    ###
                    .#.
                    ###

                    4x4: 0 0 0 0 2 0
                    12x5: 1 0 1 0 2 2
                    12x5: 1 0 1 0 3 2
                    """
                )
            )

        result = part1(self.test_file)
        self.assertEqual(result, 2, "Example should have 2 regions that can fit")

    def test_parse_input(self):
        """Test input parsing."""
        with open(self.test_file, "w") as f:
            f.write(
                dedent(
                    """\
                    0:
                    ###
                    ##.
                    ##.

                    1:
                    ###
                    ##.
                    .##

                    4x4: 0 0 0 0 2 0
                    """
                )
            )

        shapes, regions = parse_input(self.test_file)

        self.assertEqual(len(shapes), 2, "Should parse 2 shapes")
        self.assertEqual(len(regions), 1, "Should parse 1 region")

        # Shape 0: ###/##./##. = 7 cells
        self.assertEqual(len(shapes[0]), 7, "Shape 0 should have 7 cells")
        # Shape 1: ###/##./.## = 7 cells
        self.assertEqual(len(shapes[1]), 7, "Shape 1 should have 7 cells")

        # Region
        w, h, counts = regions[0]
        self.assertEqual(w, 4)
        self.assertEqual(h, 4)
        self.assertEqual(counts, [0, 0, 0, 0, 2, 0])

    def test_normalize_shape(self):
        """Test shape normalization."""
        # Shape with offset
        cells = {(2, 3), (2, 4), (3, 3)}
        normalized = normalize(cells)
        expected = frozenset({(0, 0), (0, 1), (1, 0)})
        self.assertEqual(normalized, expected)

    def test_get_variants(self):
        """Test that variants are correctly generated."""
        # A simple L-shape
        cells = {(0, 0), (1, 0), (1, 1)}
        variants = get_all_variants(cells)

        # L-shape has 4 distinct orientations (no symmetry)
        self.assertEqual(len(variants), 4, "L-shape should have 4 variants")

        # All variants should have same number of cells
        for v in variants:
            self.assertEqual(len(v), 3)

    def test_symmetric_shape_variants(self):
        """Test that symmetric shapes have fewer variants."""
        # Square shape (fully symmetric)
        cells = {(0, 0), (0, 1), (1, 0), (1, 1)}
        variants = get_all_variants(cells)
        self.assertEqual(len(variants), 1, "Square should have 1 variant")

    def test_can_fit_simple(self):
        """Test simple fitting cases."""
        # L-shape in 2x2 grid - should fit
        l_shape = {(0, 0), (1, 0), (1, 1)}
        variants = get_all_variants(l_shape)
        self.assertTrue(can_fit_pieces(2, 2, [variants]))

    def test_cannot_fit_area(self):
        """Test that area check rejects impossible cases."""
        # 10-cell piece in 3x3 grid (9 cells) - impossible
        big_shape = {(0, i) for i in range(10)}
        variants = get_all_variants(big_shape)
        self.assertFalse(can_fit_pieces(3, 3, [variants]))

    def test_first_region_example(self):
        """Test the first example region: 4x4 with two shape-4 pieces."""
        # Shape 4 from example: ###/#../###
        shape4 = {(0, 0), (0, 1), (0, 2), (1, 0), (2, 0), (2, 1), (2, 2)}
        variants = get_all_variants(shape4)

        # Two shape-4 pieces in 4x4 grid
        self.assertTrue(can_fit_pieces(4, 4, [variants, variants]))

    def test_empty_region(self):
        """Test region with no pieces to place."""
        self.assertTrue(can_fit_pieces(5, 5, []))


def run_tests() -> bool:
    """Run all tests and return True if all pass."""
    print("Running unit tests...")
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDay12)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
