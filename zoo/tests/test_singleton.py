import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zoo import Zoo
import unittest


class TestZooSingleton(unittest.TestCase):
    def test_singleton_behavior(self):
        zoo1 = Zoo("Central Park Zoo")

        zoo2 = Zoo("San Diego Zoo")

        self.assertIs(zoo1, zoo2)

        self.assertEqual(zoo1.name, "Central Park Zoo")
        self.assertEqual(zoo2.name, "Central Park Zoo")

        zoo1.set_name("New York Zoo")
        self.assertEqual(zoo2.name, "New York Zoo")

if __name__ == '__main__':
    unittest.main()