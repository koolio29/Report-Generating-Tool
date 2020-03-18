import csv
import sqlite3
import pygal
import jinja2
import argparse
import os
import errno
import statistics as stat

class ExamResults:
	
	def __init__(self, question_id, question_type, username, lastname, firstname, max_marks, marks):
		self._question_id = question_id
		self._question_type = question_type
		self._username = username
		self._lastname = lastname
		self._firstname = firstname
		self._max_marks = max_marks
		self._marks = marks

	@property
	def question_id(self):
		return self._question_id

	@property
	def question_type(self):
		return self._question_type

	@property
	def username(self):
		return self._username

	@property
	def lastname(self):
		return self._lastname

	@property
	def firstname(self):
		return self._firstname

	@property
	def max_marks(self):
		return self._max_marks

	@property
	def marks(self):
		return self._marks

class ExamCsvExtractor:

	def __extract_info(self, row):
		return ExamResults(
			question_id = row[3].split(" ")[-1],
			question_type = "auto" if row[5] != "" else "manual",
			username = row[0],
			lastname = row[1],
			firstname = row[2],
			max_marks = row[4],
			marks = row[5] if row[5] != "" else row[6]
		)

	def get_exam_results(self, csv_path):
		exam_results = []

		with open(csv_path, newline="") as csv_file:
			rows = csv.reader(csv_file, delimiter=",")

			for row in list(rows)[1:]:
				exam_results.append(self.__extract_info(row))

		return exam_results

class DatabaseAccess:

	def __init__(self, exam_results):
		self._connection = sqlite3.connect(":memory:")

		self._connection.execute("""
		CREATE TABLE Results 
		(
			id          INTEGER,
            type        VARCHAR(20),
			username	VARCHAR(20),
            lastname    VARCHAR(20),
            firstname   VARCHAR(20),
            max_marks   DOUBLE,
			marks       DOUBLE
		)
		""")

		for result in exam_results:

			self._connection.execute(
				"""INSERT INTO Results VALUES (?, ?, ?, ?, ?, ?, ?)""",
				[result.question_id, result.question_type, result.username, result.lastname, result.firstname, result.max_marks, result.marks]
			)

		self._connection.commit()

	def get_connection(self):
		return self._connection


class OverallExamStats:

    def __init__(self, database_obj):
        self._db = database_obj
        self._total_marks = self.__get_all_student_marks()

    def __get_all_student_marks(self):
        cursor = self._db.get_connection().cursor()

        results = cursor.execute("""
		SELECT (SUM(marks) / 
			(SELECT SUM(max_marks) / COUNT(DISTINCT username) 
			FROM Results
		)) * 100 AS X 
		FROM Results 
		GROUP BY username 
		ORDER BY X ASC
		""").fetchall()

        marks_list = []

        for result in results:
            marks_list.append(result[0])

        return marks_list

    @property
    def total_marks(self):
        return self._total_marks

    @property
    def mean(self):
        return round(stat.mean(self.total_marks), 1)

    @property
    def median(self):
        return round(stat.median(self.total_marks), 1)

    @property
    def maximum(self):
        return round(max(self.total_marks), 1)

    @property
    def minimum(self):
        return round(min(self.total_marks), 1)

    @property
    def standard_deviation(self):
        return round(min(self.total_marks), 1)

    def get_marks_distribution(self):
        marks_distributions = {
            "<30" : 0,
            "30-40s" : 0,
            "50s" : 0,
            "60s" : 0,
            "70s" : 0,
            "≥80" : 0
        }

        for mark in self.total_marks:
            if mark < 30:
                marks_distributions["<30"] += 1
            elif mark >= 30 and mark < 50:
                marks_distributions["30-40s"] += 1
            elif mark >= 50 and mark < 60:
                marks_distributions["50s"] += 1
            elif mark >= 60 and mark < 70:
                marks_distributions["60s"] += 1
            elif mark >= 70 and mark < 80:
                marks_distributions["70s"] += 1
            else:
                marks_distributions["≥80"] += 1

        return marks_distributions

class OverallMcqStats:

    def __init__(self, database_obj):
        self._db = database_obj
        self._all_mcq_marks = self.__get_all_student_mcq_marks()
        self._mcq_max_marks = self.__get_max_marks()

    def __get_all_student_mcq_marks(self):
        cursor = self._db.get_connection().cursor()

        marks_list = []

        results = cursor.execute("""
		SELECT (SUM(marks) / (
				(SELECT SUM(max_marks) FROM Results WHERE type="auto") / 
				(SELECT COUNT(DISTINCT username) FROM Results WHERE type="auto"))) * 100 AS X
		FROM Results
		WHERE type="auto"
		GROUP BY username
		ORDER BY X ASC
		""").fetchall()

        for result in results:
            marks_list.append(result[0])

        return marks_list

    def __get_max_marks(self):
        cursor = self._db.get_connection().cursor()

        result = cursor.execute("""
        SELECT max_marks 
        FROM Results 
        WHERE type="auto"
        LIMIT 1 
        """).fetchone()

        return round(result[0], 1)

    @property
    def all_mcq_marks(self):
        return self._all_mcq_marks

    @property
    def mcq_max_marks(self):
        return self._mcq_max_marks

    @property
    def overall_mean(self):
        return round(stat.mean(self.all_mcq_marks), 1)

    @property
    def overall_median(self):
        return round(stat.median(self.all_mcq_marks), 1)

    @property
    def overall_maximum(self):
        return round(max(self.all_mcq_marks), 1)

    @property
    def overall_minimum(self):
        return round(min(self.all_mcq_marks), 1)

    @property
    def overall_standard_deviation(self):
        return round(stat.stdev(self.all_mcq_marks), 1)

    def get_individual_mcq_avgs(self):
        cursor = self._db.get_connection().cursor()

        results = cursor.execute("""
		SELECT id, AVG(marks) 
		FROM Results
		WHERE type="auto"
		GROUP BY id
		ORDER BY id ASC 
		""").fetchall()

        individual_avgs = {}

        for result in results:
            individual_avgs[str(result[0])] = result[1]

        return individual_avgs

class OverallEssayStats:

    def __init__(self, database_obj):
        self._db = database_obj
        self._all_essay_marks = self.__get_all_student_essay_marks()
        self._essay_max_marks = self.__get_max_marks()

    def __get_all_student_essay_marks(self):
        cursor = self._db.get_connection().cursor()

        marks_list = []

        results = cursor.execute("""
		SELECT (SUM(marks) / (
				(SELECT SUM(max_marks) FROM Results WHERE type="manual") / 
				(SELECT COUNT(DISTINCT username) FROM Results WHERE type="manual"))) * 100 AS X
		FROM Results
		WHERE type="manual"
		GROUP BY username
		ORDER BY X ASC
		""").fetchall()

        for result in results:
            marks_list.append(result[0])

        return marks_list

    def __get_max_marks(self):
        cursor = self._db.get_connection().cursor()

        result = cursor.execute("""
        SELECT max_marks 
        FROM Results 
        WHERE type="manual" 
        LIMIT 1
        """).fetchone()

        return round(result[0], 1)

    @property
    def all_essay_marks(self):
        return self._all_essay_marks

    @property
    def essay_max_marks(self):
        return self._essay_max_marks

    @property
    def overall_mean(self):
        return round(stat.mean(self.all_essay_marks), 1)

    @property
    def overall_median(self):
        return round(stat.median(self.all_essay_marks), 1)

    @property
    def overall_maximum(self):
        return round(max(self.all_essay_marks), 1)

    @property
    def overall_minimum(self):
        return round(min(self.all_essay_marks), 1)

    @property
    def overall_standard_deviation(self):
        return round(stat.stdev(self.all_essay_marks), 1)

    def get_individual_essay_avgs(self):
        cursor = self._db.get_connection().cursor()

        results = cursor.execute("""
		SELECT id, AVG(marks) 
		FROM Results
		WHERE type="manual"
		GROUP BY id
		ORDER BY id ASC 
		""").fetchall()

        individual_avgs = {}

        for result in results:
            individual_avgs[str(result[0])] = result[1]

        return individual_avgs

class GraphGenerator:

    def __init__(self, path2save, graph_name, save_format="svg"):
        self._save_path = path2save
        self._graph_name = f"{graph_name}.{save_format}"
        self._abs_path_to_graph = f"{path2save}/{graph_name}.{save_format}" 

    def generate_bar_graph(self, data_dict, title="COMP000000 Stats", min_y=0, max_y=None):
        x_labels = tuple(data_dict.keys())
        data_points = []

        for key in data_dict.keys():
            data_points.append(data_dict[key])

        bar_chart = pygal.Bar(
            style=pygal.style.BlueStyle, 
            show_legend=False, 
            title=title, 
            range=(min_y, max_y) if max_y != None else None,
            width=500,
            height=500,
            min_scale=0,
            max_scale=100
        )

        bar_chart.x_labels = x_labels
        bar_chart.add("y_label", data_dict)

        self.__save_graph(bar_chart)

    def __save_graph(self, graphObj):
        graphObj.render_to_file(self.abs_path_to_graph)

    @property
    def abs_path_to_graph(self):
        return self._abs_path_to_graph

    @property
    def graph_name(self):
        return self._graph_name

class MarkDownGenerator:

    def __init__(self, path2save, template_dst, template_name, report_name, data):
        self._template_dst = template_dst
        self._template_name = template_name
        self._data = data
        self._abs_path_to_md = f"{path2save}/{report_name}"

    def __write_file(self, contents):
        try:
            file2write = open(self.abs_path_to_md, "w")
            file2write.write(contents)
            file2write.close()
        except Exception as e:
            print("Error: Error writing markdown file")
            print(e)
            return False
        
        return True
            
    def __read_template(self):
        fileloader = jinja2.FileSystemLoader(f"{self._template_dst}")
        environment = jinja2.Environment(loader=fileloader)

        template_to_use = environment.get_template(self._template_name)
        template_output = template_to_use.render(data=self._data)

        return template_output

    def generate_file(self):
        return self.__write_file(self.__read_template())

    @property
    def abs_path_to_md(self):
        return self._abs_path_to_md

def get_max_value_from_dict(mydict):
    return mydict[max(mydict, key=mydict.get)]

def generate_report(course_id, csv_path, report_save_path, template_dir, template2use):
    extractor = ExamCsvExtractor()
    exam_results = extractor.get_exam_results(csv_path=csv_path)

    db = DatabaseAccess(exam_results)
    
    overallstats = OverallExamStats(db)
    overallmcqstats = OverallMcqStats(db)
    overallessaystats = OverallEssayStats(db)

    # report_save_path
    overallgraph = GraphGenerator(path2save=report_save_path, graph_name="exam_distribution")
    overallgraph.generate_bar_graph(overallstats.get_marks_distribution(), title=f"{course_id} Exam Distribution", max_y=get_max_value_from_dict(overallstats.get_marks_distribution()))

    overallmcq = GraphGenerator(path2save=report_save_path, graph_name="mcq_averages")
    overallmcq.generate_bar_graph(overallmcqstats.get_individual_mcq_avgs(), title="Automarked Question Average", max_y=overallmcqstats.mcq_max_marks)

    overallessay = GraphGenerator(path2save=report_save_path, graph_name="essay_averages")
    overallessay.generate_bar_graph(overallessaystats.get_individual_essay_avgs(), title="Manually Marked Question Averages", max_y=overallessaystats.essay_max_marks)

    mdgenerator = MarkDownGenerator(path2save=report_save_path, template_dst=template_dir, template_name=template2use, report_name=f"{course_id}.md", data={
        "unit_code" : course_id,
        "exam_mean" : overallstats.mean,
        "exam_median" : overallstats.median,
        "exam_stdev" : overallstats.standard_deviation,
        "exam_min" : overallstats.minimum,
        "exam_max" : overallstats.maximum,
        "exam_distr_graph" : overallgraph.graph_name,
        "mcq_overall_mean" : overallmcqstats.overall_mean,
        "mcq_overall_median" : overallmcqstats.overall_median,
        "mcq_overall_stdev" : overallmcqstats.overall_standard_deviation,
        "mcq_overall_min" : overallmcqstats.overall_minimum,
        "mcq_overall_max" : overallmcqstats.overall_maximum,
        "mcq_avgs" : overallmcq.graph_name,
        "essay_overall_mean" : overallessaystats.overall_mean,
        "essay_overall_median" : overallessaystats.overall_median,
        "essay_overall_stdev" : overallessaystats.overall_standard_deviation,
        "essay_overall_min" : overallessaystats.overall_minimum,
        "essay_overall_max" : overallessaystats.overall_maximum,
        "essay_avgs" : overallessay.graph_name 
    })

    mdgenerator.generate_file()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Create exam feedback reports")

    argparser.add_argument("-c", "--course", help="Course id. By Default it is COMP000000", default="COMP000000")
    argparser.add_argument("-d", "--data", help="path or filename to the exam data. If '--multi-report' is passed in, this becomes a path for the directory containing all exam data files.'", default="data/exam.csv")
    argparser.add_argument("-t", "--template", help="Path for the report template to be used.", default="templates")
    argparser.add_argument("-m", "--multiple", help="Tells the script that it needs to generate multiple reports. If this flag is True, it would treat the '--data' flag as a path to a directory containing all exam data where each exam data file is named after the course unit.", action="store_true")

    args = argparser.parse_args()

    template_dir = args.template if  args.template == "templates" else os.path.dirname(args.template)
    template_name = "default_template.md" if args.template == "templates" else os.path.basename(args.template)

    # Checking if the template exists
    if not os.path.exists(f"{template_dir}/{template_name}"):
        print(f"Cannot find template in the provided path: '{template_dir}/{template_name}'.")
        exit(1)
    elif os.path.isdir(f"{template_dir}/{template_name}"):
        print(f"'{template_dir}/{template_name}' is a path to a directory. Please pass in a path for the template file.")
        exit(1)

    csv_files = None
    course_names = None

    if not os.path.exists(args.data):
        print(f"'{args.data}' does not exist!. Please pass in a valid path for '--data'.")
        exit(1)
    elif args.multiple:

        if os.path.isfile(args.data):
            print(f"'{args.data}' is a path to a file. Please pass in a path to a directory containing csv files when using '--multiple' flag.")
            exit(1)

        csv_files = [file for file in os.listdir(args.data) if file.endswith(".csv")]
        course_names = [name.split(".")[0] for name in csv_files]

        if len(csv_files) == 0:
            print("No csv files in the directory!.")
            exit(1)
    elif os.path.isdir(args.data): # checks if the data "path" provided is not a directory
        print(f"'{args.data}' is a path to directory. Please use the '--multiple' flag if you want to generate multiple reports.")
        exit(1)
    else:
        course_names = [args.course]

    # creating an output directory to save the reports to
    if not os.path.isdir("outputs"):
        os.mkdir("outputs")

    for index in range(0, len(course_names)):
        save_path = f"{os.getcwd()}/outputs/{course_names[index]}"

        try:
            os.mkdir(save_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Cannot make 'output' directory!.")
                print(e)
                exit(1)

        generate_report(
            csv_path = f"{args.data}/{csv_files[index]}" if args.multiple else args.data,
            course_id = course_names[index],
            report_save_path = save_path, 
            template_dir = template_dir,
            template2use = template_name
        )

    print("Reports have been created in 'outputs' folder.")