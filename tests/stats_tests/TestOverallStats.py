import unittest

from context import OverallStats
from context import test_table as table

class TestOverallStats(unittest.TestCase):

    def setUp(self):
        self._exam_table = OverallStats(table)

    def test_get_marks_distribution(self):
        self.assertEqual(self._exam_table.get_marks_distribution(), 
            {'<30': 0, '30-40s': 1, '50s': 1, '60s': 4, '70s': 0, '≥80': 0})
        self.assertEqual(str(type(self._exam_table.get_marks_distribution())), 
            "<class 'dict'>")

if __name__ == "__main__":
    unittest.main()