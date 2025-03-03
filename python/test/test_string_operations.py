import unittest
from app.string_operations import to_uppercase#, to_lowercase

class TestStringOperations(unittest.TestCase):
    def test_to_uppercase(self):
        self.assertEqual(to_uppercase('hello'), 'HELLO')

#    def test_to_lowercase(self):
#        self.assertEqual(to_lowercase('HELLO'), 'hello')