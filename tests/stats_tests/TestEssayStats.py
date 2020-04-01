import unittest

from context import EssayStats
from context import test_table as table

class TestMCQStats(unittest.TestCase):

    def setUp(self):
        self._exam_table = EssayStats(table)

    def test_get_essay_avgs(self):
        self.assertEqual(self._exam_table.get_essay_avgs(), 
            {'5': 3.19})
        self.assertEqual(str(type(self._exam_table.get_essay_avgs())), 
            "<class 'dict'>")

    def test_get_individual_essay_stats(self):
        self.assertEqual(
            str(type(self._exam_table.get_individual_essay_stats())), 
            "<class 'list'>"
        )

        self.assertEqual(self._exam_table.get_individual_essay_stats(), 
            [{"max" : 5.0, "mean" : 3.19, "mean_out_of_100" : 63.8, 
            "min" : 0.5, "outof" : 5.0, "question_id" : 5}]
        )

    def test_max_essay_mark(self):
        self.assertEqual(self._exam_table.max_essay_mark, 5.0)
        self.assertNotEqual(self._exam_table.max_essay_mark, "5.0")

if __name__ == "__main__":
    unittest.main()