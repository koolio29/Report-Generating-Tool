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

*__Note:__ For the latest features , pull `develop` branch.*

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

When you run this in the terminal, the script will create a new directory called 'outputs' and create new folders within this directory, named after the course ID, to save the generated reports along with the graphs. The 'output' can be found in the same directory as the `main.py`.

Two reports are saved to the newly created folders.

### Multiple Report Generation

To generate multiple reports, you will need to atleast pass the following flags:
* `--multiple` :- This flag tells the script to treat the `--data` flag as a path to a directory containing all the exam data in csv format where each csv file is named after the course id.
* `--data` :- This is the path to the directory containing all the csv files.

Example:
```
(venv)$ python3 main.py --data data --multiple
```
When you run this in the terminal, the script will create a new directory for each of the csv file found in the path passed in as `--data`. and the reports generated will be named after their respective csv file name. The files generated can be found in the 'outputs' directory.

### Generating csv files

The tool can generate the csv file containing the item analysis of the question by passing the `--generate_data` flag.

Example:
```
(venv)$ python3 main.py --course COMP612535 --data path/to/csv/file.csv --generate_data
```

When you run the command above, the csv file generated will be saved into the same directory as the rest of the files generated for a given course.

### Using a different template for overall feedback report

You can use a different template for the overall feedback report by passing the path of the new template to the `--template` flag. It should be noted that the template should follow the jinja2 syntax and use the required place holders.

By default, the tool looks for the template found in 'templates/default_template.md'

Example:
```
(venv)$ python3 main.py --course COMP612535 --data path/to/csv/file.csv --template path/to/template/newtemplate.md
```

When you run this in the terminal, it will use the new template when creating the report.

#### Template placeholders

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