import unittest

from context import ExamStats
from context import test_table as table

import context

class TestExamStats(unittest.TestCase):

    def setUp(self):
        self._exam_stats = ExamStats(table)
    
    def test_mean(self):
        self.assertEqual(self._exam_stats.mean, 64.58)
        self.assertNotEqual(self._exam_stats.mean, "64.58")
        self.assertGreaterEqual(self._exam_stats.mean, 0)

    def test_median(self):
        self.assertEqual(self._exam_stats.median, 72.22)
        self.assertNotEqual(self._exam_stats.median, "72.22")
        self.assertGreaterEqual(self._exam_stats.median, 0)

    def test_max(self):
        self.assertEqual(self._exam_stats.max, 83.33)
        self.assertNotEqual(self._exam_stats.max, "83.33")
        self.assertGreaterEqual(self._exam_stats.max, 0)

    def test_min(self):
        self.assertEqual(self._exam_stats.min, 27.78)
        self.assertNotEqual(self._exam_stats.min, "27.78")
        self.assertGreaterEqual(self._exam_stats.min, 0)

    def test_stdev(self):
        self.assertEqual(self._exam_stats.stdev, 19.23)
        self.assertNotEqual(self._exam_stats.stdev, "19.23")
        self.assertGreaterEqual(self._exam_stats.stdev, 0)

if __name__ == "__main__":
    unittest.main()