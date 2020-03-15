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

### Single Report Generation
In order to generate a single report, you will need to atleast pass following flags:
* __--course__: This is the course ID. By default this is set by 'COMP000000'.
* __--data__: This is the path to the csv file. By default this is set to 'data/exam.csv'.

Example:
```
$(venv) python3 main.py --data path/to/exam.csv --course COMP123456
```

When you run this in the terminal, the script will create a new directory named after the course ID and place the generated markdown file and graphs inside it. The new directory can be found in the same directory as the `main.py`.

### Multiple Report Generation
To generate multiple reports, you will need to atleast pass the following flags:
* __--multiple__: This flag tells the script to treat the '--data' flag as a path to a directory containing all the exam data in csv format where each csv file is named after the course id.
* __--data__: This is the path to the directory containing all the csv files.

Example:
```
$(venv) python3 main.py --data path/to/csv/files --multiple
```
When you run this in the terminal, the script will a new directory for each of the csv file found in the path passed in as '--data' and will name the directory after their respective csv file name.