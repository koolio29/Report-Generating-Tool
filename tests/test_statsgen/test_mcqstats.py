import unittest

from .context import MCQStats
from .context import test_table as table

class TestMCQStats(unittest.TestCase):

    def setUp(self):
        self._exam_table = MCQStats(table)

    def test_get_mcq_avgs(self):
        self.assertEqual(self._exam_table.get_mcq_avgs(), 
            {'1': 0.5, '2': 0.62, '3': 0.75, '4': 0.75})
        self.assertEqual(str(type(self._exam_table.get_mcq_avgs())), 
            "<class 'dict'>")

    def test_max_mcq_marks(self):
        self.assertEqual(self._exam_table.max_mcq_mark, 1.0)
        self.assertNotEqual(self._exam_table.max_mcq_mark, "1.0")

if __name__ == "__main__":
    unittest.main()
