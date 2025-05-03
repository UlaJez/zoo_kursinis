import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from datetime import datetime
from zoo import Lion, Penguin, Monkey

class TestAnimalFeeding(unittest.TestCase):
    def setUp(self):
        self.lion = Lion("Simba")
        self.penguin = Penguin("Pingu")
        self.monkey = Monkey("George")
        
    def test_feed_animal(self):
        self.assertIsNone(self.lion.last_fed)
        self.assertIsNone(self.penguin.last_fed)
        self.assertIsNone(self.monkey.last_fed)

        lion_result = self.lion.feed()
        penguin_result = self.penguin.feed()
        monkey_result = self.monkey.feed()

        self.assertIn("Simba was fed meat", lion_result)
        self.assertIn("Pingu was fed fish", penguin_result)
        self.assertIn("George was fed bananas", monkey_result)

        self.assertIsNotNone(self.lion.last_fed)
        self.assertIsNotNone(self.penguin.last_fed)
        self.assertIsNotNone(self.monkey.last_fed)

        self.assertLess((datetime.now() - self.lion.last_fed).total_seconds(), 60)
        self.assertLess((datetime.now() - self.penguin.last_fed).total_seconds(), 60)
        self.assertLess((datetime.now() - self.monkey.last_fed).total_seconds(), 60)

if __name__ == '__main__':
    unittest.main()