import unittest

from context import EssayStats
from context import test_table as table

class TestMCQStats(unittest.TestCase):

    def setUp(self):
        self._exam_table = EssayStats(table)

    def test_get_essay_avgs(self):
        self.assertEqual(self._exam_table.get_essay_avgs(), 
            {'6': 2.92, '7': 2.67, '8': 2.92})
        self.assertEqual(str(type(self._exam_table.get_essay_avgs())), 
            "<class 'dict'>")

    def test_get_individual_essay_stats(self):
        self.assertEqual(
            str(type(self._exam_table.get_individual_essay_stats())), 
            "<class 'list'>"
        )

        self.assertEqual(self._exam_table.get_individual_essay_stats(), 
            [
                {'max': 4.5, 'mean': 2.92, 'mean_out_of_100': 58.4, 'min': 1.5,
                    'outof': 5.0, 'question_id': 6},
                {'max': 4.0, 'mean': 2.67, 'mean_out_of_100': 53.4, 'min': 1.0, 
                    'outof': 5.0, 'question_id': 7},
                {'max': 4.0, 'mean': 2.92, 'mean_out_of_100': 58.4, 'min': 1.5,
                    'outof': 5.0, 'question_id': 8}
            ]
        )

    def test_max_essay_mark(self):
        self.assertEqual(self._exam_table.max_essay_mark, 5.0)
        self.assertNotEqual(self._exam_table.max_essay_mark, "5.0")

if __name__ == "__main__":
    unittest.main()