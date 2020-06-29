import unittest

from .context import overall_stats
from .context import mcq_stats
from .context import essay_stats

from .context import get_md_stats_table
from .context import get_md_difficulty_table
from .context import get_md_discrimination_table
from .context import get_md_to_be_reviewed_table

class TestMarkdownHelpers(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._test_difficulty = {1 : 29, 2 : 60, 3 : 98, 4 : 55, 5 : 30}
        self._test_discrimination = {1 : 0.5, 2 : 0.3, 3 : 0.6, 4 : -0.1, 5 : 0.1}

    def test_get_md_stats_table(self):
        result = get_md_stats_table(overall_stats, mcq_stats, essay_stats)

        self.assertMultiLineEqual(result, """
|        | All                    | MCQs               | Essays               |
|--------|------------------------|--------------------|----------------------|
| Mean   | 64.58   | 65.62   | 63.75   |
| Median | 72.22 | 62.5 | 65.0 |
| Stdev  | 19.23  | 26.52  | 28.25  |
| Min    | 27.78    | 25.0    | 10.0    |
| Max    | 83.33    | 100.0    | 100.0    |""")

    def test_get_md_difficulty_table(self):
        result = get_md_difficulty_table(self._test_difficulty)

        self.assertMultiLineEqual(result, """
| Number of Questions   | Difficulty Level | Percentage of Students Correct   |
|---------------------- |------------------|----------------------------------|
| 1   | Hard             | Less than 30%                    |
| 3 | Medium           | Between 30% to 80%               |
| 1   | Easy             | Greater than 80%                 |""")

    def test_get_md_discrimination_table(self):
        result = get_md_discrimination_table(self._test_discrimination)

        self.assertMultiLineEqual(result, """
| Number of Questions      | Discrimination Types                           |
|--------------------------|------------------------------------------------|
| 1     | Negative Discrimination (between -1.0 an 0.0)  |
| 2 | Bottom threshold (between 0.10 and 0.39)       |
| 2  | Great discriminators (between 0.40 and 0.90)   |
| 0        | Perfectly discriminating (equal to 1.0)        |""")

    def test_get_md_to_be_reviewed_table(self):
        result = get_md_to_be_reviewed_table(self._test_difficulty, 
                                            self._test_discrimination)

        self.assertMultiLineEqual(result, """
| Question Number | Difficulty | Discrimination |
|-----------------|------------|----------------|
|4|55|-0.1|
""")
    
if __name__ == "__main__":
    unittest.main()