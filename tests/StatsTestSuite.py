from unittest import TestSuite, TestLoader, TextTestRunner

from stats_tests import context, TestExamStats, TestOverallStats 
from stats_tests import TestMCQStats, TestEssayStats

if __name__ == "__main__":
    test_loader = TestLoader()
    test_suite = TestSuite()

    test_suite.addTests(test_loader.loadTestsFromModule(TestExamStats))
    test_suite.addTests(test_loader.loadTestsFromModule(TestOverallStats))
    test_suite.addTests(test_loader.loadTestsFromModule(TestMCQStats))
    test_suite.addTests(test_loader.loadTestsFromModule(TestEssayStats))

    test_runner = TextTestRunner(verbosity=3)
    test_runner.run(test_suite)