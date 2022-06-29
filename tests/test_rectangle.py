import unittest
from squares import Rect

class TestRect(unittest.TestCase):

    def test_movement_locations(self):
        s1 = Rect(length=1, width=1)
        self.assertEqual(s1.area, 1)
        self.assertEqual(s1.center, [0.5, 0.5])

        s1.add_x(1)
        self.assertEqual(s1.center, [1.5, 0.5]) 

        s1.add_y(1)
        self.assertEqual(s1.center, [1.5, 1.5]) 

        s1.add_xy(1, 1)
        self.assertEqual(s1.center, [2.5, 2.5])  
        self.assertEqual(
            s1.coordinates, 
            [[2, 2], [2, 3], [3, 2], [3, 3]]
            )

        self.assertEqual(s1.rotate_times, 4)
        self.assertEqual(s1.length, 1)
        self.assertEqual(s1.width, 1)

        with self.assertRaises(TypeError):
            s1.add_xy("l", "j")

    def test_area(self):
        s1 = Rect(length=2, width=3)
        self.assertEqual(s1.area, 6)
        self.assertEqual(s1.center, [1.0, 1.5])

        s1 = Rect(length=1, width=1)
        self.assertEqual(s1.area, 1)   
        self.assertEqual(s1.center, [2.0, 3.5])

if __name__ == '__main__':
    unittest.main()