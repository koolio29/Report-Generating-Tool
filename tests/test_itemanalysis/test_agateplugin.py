import unittest

import agate

from .context import test_table as table
from .context import agateplugin

class TestAgatePlugin(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._exam_table = table

    def test_difficulty(self):
        dict_to_test = self._exam_table.difficulty(
            filter_items=True, 
            in_percentage=True
        )

        self.assertEqual(str(type(dict_to_test)), "<class 'dict'>")
        self.assertEqual(dict_to_test, {1: 50.0, 2: 62.5, 3: 75.0, 4: 75.0})

        dict_to_test = self._exam_table.difficulty(in_percentage=False)
        self.assertEqual(dict_to_test, {1: 0.5, 2: 0.625, 3: 0.75, 4: 0.75})

    def test_discrimination(self):
        dict_to_test = self._exam_table.discrimination()

        self.assertEqual(str(type(dict_to_test)), "<class 'dict'>")
        self.assertEqual(dict_to_test, {1: 1.0, 2: 1.0, 3: 0.0, 4: 0.5})

    def test_standardDeviation(self):
        dict_to_test = self._exam_table.standardDeviation()

        self.assertEqual(str(type(dict_to_test)), "<class 'dict'>")
        self.assertEqual(
            dict_to_test, 
            {
                1: 0.5345224838248488, 
                2: 0.5175491695067657, 
                3: 0.4629100498862757, 
                4: 0.4629100498862757, 
                5: 1.412634317254722
            }
        )

    def test_standardError(self):
        dict_to_test = self._exam_table.standardError()

        self.assertEqual(str(type(dict_to_test)), "<class 'dict'>")
        self.assertEqual(
            dict_to_test, 
            {
                1: 0.1889822365046136, 
                2: 0.18298126367784995, 
                3: 0.16366341767699427, 
                4: 0.16366341767699427, 
                5: 0.4994416525338213
            }
        )

if __name__ == "__main__":
    unittest.main()

