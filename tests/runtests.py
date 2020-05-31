from unittest import TestSuite, TestLoader, TextTestRunner

from test_statsgen import context
from test_statsgen import test_examstats
from test_statsgen import test_essaystats
from test_statsgen import test_overallstats 
from test_statsgen import test_mcqstats

if __name__ == "__main__":
    test_loader = TestLoader()
    test_suite = TestSuite()

    # All tests related to statsgen
    test_suite.addTests(test_loader.loadTestsFromModule(test_examstats))
    test_suite.addTests(test_loader.loadTestsFromModule(test_essaystats))
    test_suite.addTests(test_loader.loadTestsFromModule(test_overallstats))
    test_suite.addTests(test_loader.loadTestsFromModule(test_mcqstats))

    test_runner = TextTestRunner(verbosity=3)
    test_runner.run(test_suite)