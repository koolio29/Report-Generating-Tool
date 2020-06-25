# Report Generating Tool

This Python script allows lecturers to generate exam feedback reports. In the current version of the script, lecturers can generate single or multiple feedback reports (in markdown) using csv files downloaded from BlackBoard.

The report generated contains:
* Basic statistics of the overall exam.
* Basic statistics of the overall auto/manually marked questions.
* Graphs to visualize the averages individual questions.

*__Note:__ For the latest features, pull `develop` branch.*

## Getting Started
The following instructions will help you to get the script up and running on your local machine.

To run the script, Python 3.6 or greater is required. After cloning this repository, you will need to create a virtual environment. To create a virtual enviroment type in the following command (after opening the terminal in the directory where the repository located):
```
$ python3 -m venv venv
```

Now you can activate the virtual environment by typing the following command:
```
$ source venv/bin/activate
```

Now install the dependencies for the script by typing:
```
(venv)$ pip3 install -r requirements.txt
```

You can now pass in the `--help` flag to view the flags used by the script.

```
(venv)$ python3 main.py --help

usage: main.py [-h] [-c COURSE] [-d DATA] [-t TEMPLATE] [-m] [-g]

Create exam feedback reports

optional arguments:
  -h, --help            show this help message and exit
  -c COURSE, --course COURSE
                        Course id. By Default it is COMP000000
  -d DATA, --data DATA  path or filename to the exam data. If '--multi-report'
                        is passed in, this becomes a path for the directory
                        containing all exam data files.
  -t TEMPLATE, --template TEMPLATE
                        Path for the report template to be used.
  -m, --multiple        Tells the script that it needs to generate multiple
                        reports. If this flag is True, it would treat the '--
                        data' flag as a path to a directory containing all
                        exam data where each exam data file is named after the
                        course unit.
  -g, --generate_data   Generates a csv file containing statistics for
                        lecturers use.
```

## Usage

### Single Report Generation
In order to generate a single report, you will need to atleast pass following flags:
* `--course` :- This is the course ID. By default this is set by 'COMP000000'.
* `--data` :- This is the path to the csv file. By default this is set to 'data/full_exam.csv'.

Example:
```
(venv)$ python3 main.py --data data/full_exam.csv --course COMP111111
```

When you run this in the terminal, the script will create a new directory called 'outputs' and create new folders within this directory, named after the course ID, to save the generated report along with the graphs. The 'output' can be found in the same directory as the `main.py`.

### Multiple Report Generation
To generate multiple reports, you will need to atleast pass the following flags:
* `--multiple` :- This flag tells the script to treat the `--data` flag as a path to a directory containing all the exam data in csv format where each csv file is named after the course id.
* `--data` :- This is the path to the directory containing all the csv files.

Example:
```
(venv)$ python3 main.py --data data --multiple
```
When you run this in the terminal, the script will create a new directory for each of the csv file found in the path passed in as `--data` and will be named after their respective csv file name. The files generated can be found in the 'outputs' directory.

### Using a Different Template
To use a different template for the report, you will need to use `--template` flag to pass in the path of the template you want to use. It should be noted that the template should follow the jinja2 syntax and use the required placeholders regardless of whether it is a markdown or a latex file.

By default, the script looks for the template found in 'templates/default_template.md'

Example:
```
(venv)$ python3 main.py --course COMP612535 --data path/to/csv/file.csv --template path/to/template/newtemplate.md
```

When you run this in the terminal, it will use the new template when creating the report.

### Template Placeholders
The table below shows the placeholders to use when creating your own templates for the report.

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