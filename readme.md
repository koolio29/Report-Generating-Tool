# Report Generating Tool

The tool allows to create reports using a csv file which contains the results of the student. In the current version of the tool, it can generate two types of report. They are overall feedback reports and lecturer specific reports.

The overall feedback report contains:
* Basic statistics of the overall exam.
* Basic statistics of the overall auto/manually marked questions.
* Graphs to visualize the averages of individual questions.

The lecturer specific report contains:
* Common item analysis statistics such as difficulty and discrimination of questions.
* Graphs to visulaize the difficulty and discriminations of questions
* Details of the questions which are flagged for review.

In addition, the tool can generate csv files which contains the item analysis of the questions.

*__Note:__ For the latest features , pull `develop_gui` branch.*

## Getting Started
The following instructions will help you to get the tool up and running on your local machine.

To run the tool, Python 3.6 or greater is required. After cloning this repository, you will need to create a virtual environment. To create a virtual enviroment type in the following command (after opening the terminal in the directory where the repository located):

```
$ python3 -m venv venv
```

Now you can activate the virtual environment by typing the following command:
```
$ source venv/bin/activate
```

Now install the dependencies for the tool by typing:
```
(venv)$ pip3 install -r requirements.txt
```

You can now run the GUI by typing:

```
(venv)$ python3 main.py
```

### Template placeholders

The table below shows the placeholders to use when creating your own templates for the overall feedback report.

| Placeholder             | Description                                                                                                                         |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| data.unit_code          | Unit code of the course (Course ID).                                                                                                |
| data.exam_stat_table    | A markdown table containing basic statistics of the exam. Overall MCQ and Essay statistics included.                                |  
| data.distribution_graph | A path to a graph in `svg` format showing the exam mark distributions.                                                              |
| data.mcq_graph          | A path to a graph in `svg` format showing the averages of each MCQ question in the exam.                                            |
| data.essay_graph        | A path to a graph in `svg` format showing the averages of each essay question in the exam.                                          |
| data.essay_feedback     | A list containing dictionaries which contains basic statistics for each essay question. See the default_template.md for an example. |

## Running the tests
`runtests.py` is the test suite module which can be used to run all the unit tests. To run the tests, enter the following command in the terminal:

```
(venv)$ python3 tests/runtests.py.py
```

Expected output:
```
test_max (test_statsgen.test_examstats.TestExamStats) ... ok
test_mean (test_statsgen.test_examstats.TestExamStats) ... ok
test_median (test_statsgen.test_examstats.TestExamStats) ... ok
test_min (test_statsgen.test_examstats.TestExamStats) ... ok
test_stdev (test_statsgen.test_examstats.TestExamStats) ... ok
test_get_essay_avgs (test_statsgen.test_essaystats.TestEssayStats) ... ok
test_get_individual_essay_stats (test_statsgen.test_essaystats.TestEssayStats) ... ok
test_max_essay_mark (test_statsgen.test_essaystats.TestEssayStats) ... ok
test_get_marks_distribution (test_statsgen.test_overallstats.TestOverallStats) ... ok
test_get_mcq_avgs (test_statsgen.test_mcqstats.TestMCQStats) ... ok
test_max_mcq_marks (test_statsgen.test_mcqstats.TestMCQStats) ... ok
test_difficulty (test_itemanalysis.test_agateplugin.TestAgatePlugin) ... ok
test_discrimination (test_itemanalysis.test_agateplugin.TestAgatePlugin) ... ok
test_standardDeviation (test_itemanalysis.test_agateplugin.TestAgatePlugin) ... ok
test_standardError (test_itemanalysis.test_agateplugin.TestAgatePlugin) ... ok

----------------------------------------------------------------------
Ran 15 tests in 0.047s

OK
```

## Built With

* [Pygal](http://www.pygal.org/en/stable/documentation/) - Used to create and save graphs.
* [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) - Used to render templates.
* [Agate](https://agate.readthedocs.io/en/1.6.1/) - Used to process csv files and generate statistics.
* [Chardet](https://chardet.readthedocs.io/en/latest/index.html) - Used to indentify file encoding type.
* [Gooey](https://github.com/chriskiehl/Gooey) - Used to automaticatlly generate GUI.