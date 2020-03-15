# Report Generating Tool

This Python script allows lecturers to generate exam feedback reports. In the current version of the script, lecturers can generate single or multiple feedback reports using csv files downloaded from BlackBoard.

The report generated contains:
* Basic statistics of the overall exam.
* Basic statistics of the overall auto/manually marked questions.
* Graphs to visualize the averages individual questions.

## Getting Started
The following instructions will help you to get the script up and running on your local machine.

To run the script, Python 3.6 or greater is required. After cloning this repository, you will need to create a virtual environment. To create a virtual enviroment type in the following command (after opening the terminal in the directory where the repository is):
```
$ python3 -m venv venv
```

Now you can activate the virtual environment by typing the following command:
```
$ source venv/bin/activate
```

Now install the dependencies for the script by typing:
```
$(venv) pip3 install -r requirements.txt
```

You can now pass in the `--help` flag to view the flags used by the script.

```
$(venv) python3 main.py --help

usage: main.py [-h] [-c COURSE] [-d DATA] [-t TEMPLATE] [-m]

Create exam feedback reports

optional arguments:
  -h, --help            show this help message and exit
  -c COURSE, --course COURSE
                        Course id. By Default it is COMP000000
  -d DATA, --data DATA  path or filename to the exam data. If '--multi-report'
                        is passed in, this becomes a path for the directory
                        containing all exam data files.'
  -t TEMPLATE, --template TEMPLATE
                        Path for the report template to be used.
  -m, --multiple        Tells the script that it needs to generate multiple
                        reports. If this flag is True, it would treat the '--
                        data' flag as a path to a directory containing all
                        exam data where each exam data file is named after the
                        course unit
```

## Usage