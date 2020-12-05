# This is simple hack to allow the unit test classes to access the stat 
# generating classes from the main.py in the root directory.
import os
import sys

# Changes the sys.path to to the root directory of the project. This is to 
# import all the stat generating classes to the this 
# module which can be then imported by all unit test classes
sys.path.insert(0, os.path.abspath(os.path.join(
                os.path.dirname(__file__), '../..')))

from report_generating_tool.statsgen import ExamStats
from report_generating_tool.statsgen import OverallStats
from report_generating_tool.statsgen import MCQStats
from report_generating_tool.statsgen import EssayStats

from report_generating_tool.helpers import simplify_agate_table
from report_generating_tool.helpers import get_exam_agate_table

# The test agate table loaded beforehand to make sure the unit test classes
# dont have to load the table repeatedly
test_table = simplify_agate_table(
    get_exam_agate_table(f"{sys.path[0]}/data/full_exam.csv")
)

# Resetting the sys.path. If not changed back to its original state, the unit
# test classes will no longer be able to import this module
sys.path.insert(0, os.path.abspath(os.path.join(
                                        os.path.dirname(__file__), '')))