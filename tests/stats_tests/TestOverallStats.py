import unittest

from context import OverallStats
from context import test_table as table

class TestOverallStats(unittest.TestCase):

    def setUp(self):
        self._exam_table = OverallStats(table)

    def test_get_marks_distribution(self):
        self.assertEqual(self._exam_table.get_marks_distribution(), 
            {'<30': 1, '30-40s': 1, '50s': 0, '60s': 1, '70s': 4, '≥80': 1})
        self.assertEqual(str(type(self._exam_table.get_marks_distribution())), 
            "<class 'dict'>")

if __name__ == "__main__":
    unittest.main()