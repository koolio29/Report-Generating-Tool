# This is simple hack to allow the unit test classes to access the stat 
# generating classes from the main.py in the root directory.
import os
import sys

# Changes the sys.path to to the root directory of the project. This is to 
# import all the stat generating classes to the this 
# module which can be then imported by all unit test classes
sys.path.insert(0, os.path.abspath(os.path.join(
                os.path.dirname(__file__), '../..')))

from report_generating_tool.helpers import get_file_encoding
from report_generating_tool.helpers import get_max_value_from_dict
from report_generating_tool.helpers import to_two_decimals

TEST_DATA_DIR_PATH = sys.path[0] + "/data/testinputs for Encoding"

# Resetting the sys.path. If not changed back to its original state, the unit
# test classes will no longer be able to import this module
sys.path.insert(0, os.path.abspath(os.path.join(
                                        os.path.dirname(__file__), '')))