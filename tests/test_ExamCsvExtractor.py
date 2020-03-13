import unittest
import os
from context import ExamCsvExtractor

class TestExamCsvExtractor(unittest.TestCase):

    def setUp(self):
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/testinputs')) + "/single_student_result.csv"
        self.csv_extractor = ExamCsvExtractor()
        self.exam_results = self.csv_extractor.get_exam_results(csv_path=self.data_dir)

    def test_get_exam_results(self):
        self.assertEqual(len(self.exam_results), 6)
        self.assertNotEqual(len(self.exam_results), "6")
        self.assertNotEqual(len(self.exam_results), 12.5)

if __name__ == "__main__":
    unittest.main()