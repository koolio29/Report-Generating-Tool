import unittest

from context import ExamStats
from context import test_table as table

import context

class TestExamStats(unittest.TestCase):

    def setUp(self):
        self._exam_stats = ExamStats(table)
    
    def test_mean(self):
        self.assertEqual(self._exam_stats.mean, 57.5)
        self.assertNotEqual(self._exam_stats.mean, "57.5")
        self.assertGreaterEqual(self._exam_stats.mean, 0)

    def test_median(self):
        self.assertEqual(self._exam_stats.median, 62.5)
        self.assertNotEqual(self._exam_stats.median, "62.5")
        self.assertGreaterEqual(self._exam_stats.median, 0)

    def test_max(self):
        self.assertEqual(self._exam_stats.max, 67.5)
        self.assertNotEqual(self._exam_stats.max, "67.5")
        self.assertGreaterEqual(self._exam_stats.max, 0)

    def test_min(self):
        self.assertEqual(self._exam_stats.min, 37.5)
        self.assertNotEqual(self._exam_stats.min, "37.5")
        self.assertGreaterEqual(self._exam_stats.min, 0)

    def test_stdev(self):
        self.assertEqual(self._exam_stats.stdev, 11.62)
        self.assertNotEqual(self._exam_stats.stdev, "11.62")
        self.assertGreaterEqual(self._exam_stats.stdev, 0)

if __name__ == "__main__":
    unittest.main()