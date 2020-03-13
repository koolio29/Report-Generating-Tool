import unittest
import os
from context import ExamCsvExtractor, OverallExamStats, DatabaseAccess

class TestOverallExamStats(unittest.TestCase):

    def setUp(self):
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/testinputs')) + "/six_student_results.csv"
        csv_extractor = ExamCsvExtractor()
        exam_results = csv_extractor.get_exam_results(csv_path=data_dir)

        self.examstats = OverallExamStats(DatabaseAccess(exam_results))

    def test_total_marks(self):
        self.assertEqual(len(self.examstats.total_marks), 6)
        self.assertEqual(self.examstats.total_marks, [35.0, 50.0, 50.0, 65.0, 70.0, 85.0])
        self.assertNotEqual(self.examstats.total_marks, ["35.0", "50.0", "50.0", "65.0", "70.0", "85.0"])

    def test_mean(self):
        self.assertEqual(self.examstats.mean, 59.2)
        self.assertNotEqual(self.examstats.mean, "59.2")

    def test_median(self):
        self.assertEqual(self.examstats.median, 57.5)
        self.assertNotEqual(self.examstats.median, "59.2")

    def test_maximum(self):
        self.assertEqual(self.examstats.maximum, 85.0)
        self.assertNotEqual(self.examstats.maximum, "85.0")

    def test_minimum(self):
        self.assertEqual(self.examstats.minimum, 35.0)
        self.assertNotEqual(self.examstats.minimum, "35.0")

    def test_standard_deviation(self):
        self.assertEqual(self.examstats.standard_deviation, 35.0)
        self.assertNotEqual(self.examstats.standard_deviation, "35.0")

    def test_get_marks_distribution(self):
        distributions = self.examstats.get_marks_distribution()
        self.assertEqual(str(type(distributions)), "<class 'dict'>")
        self.assertEqual(distributions, {'<30': 0, '30-40s': 1, '50s': 2, '60s': 1, '70s': 1, '≥80': 1})


if __name__ == "__main__":
    unittest.main()