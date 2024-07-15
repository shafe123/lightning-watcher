import unittest
import lightningwatcher

class Test_Example(unittest.TestCase):
    def test_basic_assert(self):
        self.assertTrue(lightningwatcher.test())