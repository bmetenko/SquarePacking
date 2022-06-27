import unittest
from squares import Square

class TestSquare(unittest.TestCase):

    def test_movement_locations(self):
        s1 = Square(side=1)
        self.assertEqual(s1.area, 1)
        self.assertEqual(s1.center, [0.5, 0.5])

        s1.add_x(1)
        self.assertEqual(s1.area, 1)
        self.assertEqual(s1.center, [1.5, 0.5]) 

        s1.add_y(1)
        self.assertEqual(s1.area, 1)
        self.assertEqual(s1.center, [1.5, 1.5]) 

        s1.add_xy(1, 1)
        self.assertEqual(s1.area, 1)
        self.assertEqual(s1.center, [2.5, 2.5])  
        self.assertEqual(
            s1.coordinates, 
            [[2, 2], [2, 3], [3, 2], [3, 3]]
            )

        self.assertEqual(s1.length, 1)
        self.assertEqual(s1.rotate_times, 1)
        self.assertEqual(s1.side, 1)

        with self.assertRaises(TypeError):
            s1.add_xy("l", "j")


if __name__ == '__main__':
    unittest.main()