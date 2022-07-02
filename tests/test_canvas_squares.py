import unittest

from numpy import array
import numpy as np
from squares import SquareCanvas, Square

class TestSquareCanvas(unittest.TestCase):

    def test_canvas_locations(self):
        canvas = SquareCanvas(max_bound=10,
            contents= [Square(i) for i in [1,2,3,4,5]]
        )

        expected_frame = \
            array(
                [
                    [1, 2, 2, 3, 3, 3, 4, 4, 4, 4],
                    [0, 2, 2, 3, 3, 3, 4, 4, 4, 4],
                    [0, 0, 0, 3, 3, 3, 4, 4, 4, 4],
                    [5, 5, 5, 5, 5, 0, 4, 4, 4, 4],
                    [5, 5, 5, 5, 5, 0, 0, 0, 0, 0],
                    [5, 5, 5, 5, 5, 0, 0, 0, 0, 0],
                    [5, 5, 5, 5, 5, 0, 0, 0, 0, 0],
                    [5, 5, 5, 5, 5, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    ]
        )

        expected_centers = [
            '[0.5, 0.5]', '[1.0, 2.0]', 
            '[1.5, 4.5]', '[2.0, 8.0]', 
            '[5.5, 2.5]'
            ]

        self.assertTrue(np.array_equal(canvas.frame, expected_frame))
        self.assertEqual(canvas.y_max, 10)
        self.assertEqual(canvas.x_max, 10)
        self.assertEqual(canvas.rotation, True)

        self.assertEqual(canvas.center_list, expected_centers)

        full_2_extra_frame = array(
            [
                [ 1,  2,  2,  3,  3,  3,  4,  4,  4,  4],
                [18,  2,  2,  3,  3,  3,  4,  4,  4,  4],
                [15, 15, 19,  3,  3,  3,  4,  4,  4,  4],
                [ 5,  5,  5,  5,  5, 20,  4,  4,  4,  4],
                [ 5,  5,  5,  5,  5,  6,  6,  7,  7, 16],
                [ 5,  5,  5,  5,  5,  6,  6,  7,  7, 16],
                [ 5,  5,  5,  5,  5,  8,  8,  9,  9, 17],
                [ 5,  5,  5,  5,  5,  8,  8,  9,  9, 17],
                [10, 10, 11, 11, 12, 12, 13, 13, 14, 14],
                [10, 10, 11, 11, 12, 12, 13, 13, 14, 14]
            ]
            )

        canvas.autofill(2)

        self.assertTrue(np.array_equal(canvas.frame, full_2_extra_frame))



if __name__ == '__main__':
    unittest.main()