import unittest

from .context import get_file_encoding
from .context import get_max_value_from_dict
from .context import to_two_decimals

from .context import TEST_DATA_DIR_PATH as path

class TestUtils(unittest.TestCase):
    
    def test_get_file_encoding(self):
        self.assertEqual(get_file_encoding(f"{path}/ascii.csv"), "ascii")
        self.assertEqual(get_file_encoding(f"{path}/utf-8 bom.csv"), "UTF-8-SIG")
        self.assertEqual(get_file_encoding(f"{path}/utf-16 be.csv"), "UTF-16")
        self.assertEqual(get_file_encoding(f"{path}/utf-16 le.csv"), "UTF-16")

    def test_get_max_value_from_dict(self):
        test_dict = {1 : 5, 3 : 25, 2 : 55}
        self.assertEqual(get_max_value_from_dict(test_dict), 55)

    def test_to_two_decimals(self):
        self.assertEqual(to_two_decimals(2.569), 2.57)
        self.assertEqual(to_two_decimals("2.569"), 2.57)
        self.assertEqual(to_two_decimals("2.564"), 2.56)

if __name__ == "__main__":
    unittest.main()