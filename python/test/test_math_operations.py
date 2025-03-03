import unittest
from app.math_operations import add#, subtract, multiply#, divide

class TestMathOperations(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

#    def test_subtract(self):
#        self.assertEqual(subtract(5, 3), 2)

#    def test_multiply(self):
#        self.assertEqual(multiply(2, 3), 6)

#    def test_divide(self):
#        self.assertEqual(divide(6, 2), 3)
#        self.assertEqual(divide(5, 2), 2.5)
#
#    def test_divide_by_zero(self):
#        with self.assertRaises(ValueError):
#            divide(5, 0)