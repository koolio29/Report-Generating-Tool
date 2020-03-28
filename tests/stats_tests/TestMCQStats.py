import unittest

from context import MCQStats
from context import test_table as table

class TestMCQStats(unittest.TestCase):

    def setUp(self):
        self._exam_table = MCQStats(table)

    def test_get_mcq_avgs(self):
        self.assertEqual(self._exam_table.get_mcq_avgs(), 
            {'1': 0.67, '2': 0.83, '3': 0.33, '4': 0.5, '5': 0.67})
        self.assertEqual(str(type(self._exam_table.get_mcq_avgs())), 
            "<class 'dict'>")

    def test_max_mcq_marks(self):
        self.assertEqual(self._exam_table.max_mcq_mark, 1.0)
        self.assertNotEqual(self._exam_table.max_mcq_mark, "1.0")

if __name__ == "__main__":
    unittest.main()
