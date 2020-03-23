import agate
import jinja2
import pygal
import argparse
import os
import errno

def get_max_value_from_dict(mydict):
    return mydict[max(mydict, key=mydict.get)]

def to_two_decimals(value):
    return round(float(value), 2)

def simplify_agate_table(exam_table):
    column_names = ["username", "last_name", "first_name", "question_id",
        "question_type", "max_marks", "marks"]

    column_types = [agate.Text(), agate.Text(), agate.Text(), agate.Number(),
        agate.Text(), agate.Number(), agate.Number()]

    rows = []
    for row in exam_table:
        rows.append((
            row["Username"],
            row["Last Name"],
            row["First Name"],
            row["Question ID"].split(" ")[-1],
            "Auto" if row["Auto Score"] is not None else "Manual",
            row["Possible Points"],
            row["Auto Score"] if row["Auto Score"] is not None else \
                row["Manual Score"]
        ))
    
    return agate.Table(rows, column_names, column_types)

def get_exam_agate_table(csv_name):
    # Overriding the default types guessed by agate
    type_tester = agate.TypeTester(force={
        "Username" : agate.Text(),
        "Last Name" : agate.Text(),
        "First Name" : agate.Text(),
        "Question ID" : agate.Text(),
        "Possible Points" : agate.Text(),
        "Auto Score" : agate.Number(),
        "Manual Score" : agate.Number()
    })

    return agate.Table.from_csv(csv_name, column_types=type_tester)

def get_md_stats_table(overall_stats, mcq_stats, essay_stats):
    return f"""
|        | All                    | MCQs               | Essays               |
|--------|------------------------|--------------------|----------------------|  
| Mean   | {overall_stats.mean}   | {mcq_stats.mean}   | {essay_stats.mean}   |  
| Median | {overall_stats.median} | {mcq_stats.median} | {essay_stats.median} |  
| Stdev  | {overall_stats.stdev}  | {mcq_stats.stdev}  | {essay_stats.stdev}  |  
| Min    | {overall_stats.min}    | {mcq_stats.min}    | {essay_stats.min}    |  
| Max    | {overall_stats.max}    | {mcq_stats.max}    | {essay_stats.max}    |
"""

class ExamStats:

    def __init__(self, agateTable):
        self._max_marks = agateTable.aggregate(agate.Sum("max_marks")) \
            / agateTable.distinct("username").aggregate(agate.Count())

        self._out_of_100_table = agateTable \
            .group_by("username") \
            .aggregate([("outof", agate.Sum("marks"))]) \
            .compute([
                ("outof100", agate.Formula(agate.Number(), 
                    lambda row: (row["outof"] / self._max_marks) * 100))
            ])

        self._mean = to_two_decimals(
            self._out_of_100_table.aggregate(agate.Mean("outof100")))

        self._median = to_two_decimals(
            self._out_of_100_table.aggregate(agate.Median("outof100")))

        self._maximum = to_two_decimals(
            self._out_of_100_table.aggregate(agate.Max("outof100")))

        self._minimum = to_two_decimals(
            self._out_of_100_table.aggregate(agate.Min("outof100")))

        self._standard_deviation = to_two_decimals(
            self._out_of_100_table.aggregate(agate.StDev("outof100")))

    @property
    def mean(self):
        return self._mean

    @property
    def median(self):
        return self._median

    @property
    def max(self):
        return self._maximum

    @property
    def min(self):
        return self._minimum

    @property
    def stdev(self):
        return self._standard_deviation

class OverallStats(ExamStats):

    def __init__(self, agateTable):
        super().__init__(agateTable)

    def get_marks_distribution(self):
        return {
            "<30" : self._out_of_100_table.where(
                lambda row: row["outof100"] < 30).aggregate(agate.Count()),

            "30-40s" : self._out_of_100_table.where(
                lambda row: row["outof100"] >= 30 and row["outof100"] < 50) \
                    .aggregate(agate.Count()),

            "50s" :  self._out_of_100_table.where(
                lambda row: row["outof100"] >= 50 and row["outof100"] < 60) \
                    .aggregate(agate.Count()),

            "60s" :  self._out_of_100_table.where(
                lambda row: row["outof100"] >= 60 and row["outof100"] < 70) \
                    .aggregate(agate.Count()),

            "70s" :  self._out_of_100_table.where(
                lambda row: row["outof100"] >= 70 and row["outof100"] < 80) \
                    .aggregate(agate.Count()),

            "≥80" :  self._out_of_100_table.where(
                lambda row: row["outof100"] >= 80).aggregate(agate.Count())
        }

class MCQStats(ExamStats):

    def __init__(self, agateTable):
        self._init_table = agateTable \
            .where(lambda row: row["question_type"] == "Auto")

        self._max_mcq_mark = self._init_table \
            .select(["max_marks"]) \
            .limit(1)[0]["max_marks"]

        super().__init__(self._init_table)

    def get_mcq_avgs(self):
        mcq_avgs_table = self._init_table \
            .group_by("question_id") \
            .aggregate([("Sum of marks", agate.Sum("marks"))]) \
            .compute([
                ("question avg", agate.Formula(agate.Number(), 
                    lambda row: to_two_decimals(row["Sum of marks"]
                    / self._init_table.aggregate(agate.Count("question_id", 
                    row["question_id"]))))
            )])

        individual_avgs = {}

        for row in mcq_avgs_table:
            key = str(row["question_id"])
            value = to_two_decimals(row["question avg"])
            individual_avgs[key] = value 

        return individual_avgs

    @property
    def max_mcq_mark(self):
        return float(self._max_mcq_mark)

class EssayStats(ExamStats):

    def __init__(self, agateTable):
        self._init_table = agateTable \
            .where(lambda row: row["question_type"] == "Manual")

        self._max_essay_mark = self._init_table \
            .select(["max_marks"]) \
            .limit(1)[0]["max_marks"]

        super().__init__(self._init_table)

    def get_essay_avgs(self):
        essay_avgs_table = self._init_table \
            .group_by("question_id") \
            .aggregate([("Sum of marks", agate.Sum("marks"))]) \
            .compute([
                ("question avg",  agate.Formula(agate.Number(), 
                    lambda row: to_two_decimals(row["Sum of marks"] 
                    / self._init_table.aggregate(agate.Count("question_id", 
                    row["question_id"])) ) )
            )])

        individual_avgs = {}

        for row in essay_avgs_table:
            key = str(row["question_id"])
            value = to_two_decimals(row["question avg"])
            individual_avgs[key] = value 

        return individual_avgs

    def get_individual_essay_stats(self):
        essay_stats = self._init_table \
            .select(["question_id", "max_marks", "marks"]) \
            .group_by("question_id") \
            .aggregate([
                ("min", agate.Min("marks")),
                ("max", agate.Max("marks")),
                ("sum of marks", agate.Sum("marks")),
                ("sum of max marks", agate.Sum("max_marks"))
            ]) \
            .compute([
                ("mean", agate.Formula(agate.Number(), 
                    lambda row: to_two_decimals(row["sum of marks"] 
                    / self._init_table.aggregate(agate.Count("question_id", 
                    row["question_id"])))))
            ]) \
            .compute([
                ("max_marks", agate.Formula(agate.Number(), 
                lambda row: row["sum of max marks"] 
                / self._init_table.aggregate(agate.Count("question_id", 
                row["question_id"]))))
            ]) \
            .order_by("question_id")

        stats = []

        for row in essay_stats:
            stats.append({
                "question_id" : int(row["question_id"]),
                "mean" : to_two_decimals(row["mean"]),
                "outof" : to_two_decimals(row["max_marks"]),
                "mean_out_of_100" : to_two_decimals((row["mean"] \
                                                    / row["max_marks"]) * 100),
                "min" : to_two_decimals(row["min"]),
                "max" : to_two_decimals(row["max"]),
            })

        return stats
    
    @property
    def max_essay_mark(self):
        return float(self._max_essay_mark)

class GraphGenerator:

    def __init__(self, path2save, graph_name, save_format="svg"):
        self._save_path = path2save
        self._graph_name = f"{graph_name}.{save_format}"
        self._abs_path_to_graph = f"{path2save}/{graph_name}.{save_format}" 

    def generate_bar_graph(self, data_dict, title="COMP000000 Stats", 
                                                    min_y=0, max_y=None):
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
        graphObj.render_to_file(self._abs_path_to_graph)

    @property
    def graph_name(self):
        return self._graph_name

class MarkDownGenerator:

    def __init__(self, save_path, template_dst, template_name, md_name, data):
        self._template_dst = template_dst
        self._template_name = template_name
        self._data = data
        self._abs_path_to_md = f"{save_path}/{md_name}"

    def __write_file(self, contents):
        try:
            file2write = open(self._abs_path_to_md, "w")
            file2write.write(contents)
            file2write.close()
        except Exception as e:
            print("Error: Error writing markdown file: ", e)
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

def generate_md(course_id, csv_path, save_path, template_dir, template_name):
    exam_table = get_exam_agate_table(csv_path)
    simplified_table = simplify_agate_table(exam_table)

    overall_stats = OverallStats(simplified_table)
    mcq_stats = MCQStats(simplified_table)
    essay_stats = EssayStats(simplified_table)

    overall_graph = GraphGenerator(save_path, "exam_distribution")
    overall_graph.generate_bar_graph(
        data_dict = overall_stats.get_marks_distribution(),
        title = f"{course_id} Exam Distribution",
        max_y = get_max_value_from_dict(overall_stats.get_marks_distribution())
    )

    mcq_graph = GraphGenerator(save_path, "mcq_averages")
    mcq_graph.generate_bar_graph(
        data_dict = mcq_stats.get_mcq_avgs(),
        title = "Automarked Question Averages",
        max_y = mcq_stats.max_mcq_mark
    )
    essay_graph = GraphGenerator(save_path, "essay_averages")
    essay_graph.generate_bar_graph(
        data_dict = essay_stats.get_essay_avgs(),
        title = "Manually Marked Question Averages",
        max_y = essay_stats.max_essay_mark
    )

    data = {
        "unit_code" : course_id,
        "exam_stat_table" : get_md_stats_table(overall_stats, mcq_stats, 
                                                                essay_stats),
        "distribution_graph" : overall_graph.graph_name,
        "mcq_graph" : mcq_graph.graph_name,
        "essay_graph" : essay_graph.graph_name,
        "essay_feedback" : essay_stats.get_individual_essay_stats()
    }

    md_gen = MarkDownGenerator(
        save_path = save_path,
        template_dst = template_dir,
        template_name = template_name,
        md_name = f"{course_id}.md",
        data = data
    )

    md_gen.generate_file()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Create exam feedback reports"
    )

    argparser.add_argument(
        "-c", "--course", 
        help="Course id. By Default it is COMP000000", 
        default="COMP000000"
    )
    argparser.add_argument(
        "-d", "--data", 
        help="path or filename to the exam data. If '--multi-report' is " \
            + "passed in, this becomes a path for the directory " \
            + " containing all exam data files.", 
        default="data/exam.csv"
    )
    argparser.add_argument(
        "-t", "--template", 
        help="Path for the report template to be used.", 
        default="templates"
    )
    argparser.add_argument(
        "-m", "--multiple", 
        help="Tells the script that it needs to generate multiple reports. " \
            + "If this flag is True, it would treat the '--data' flag" \
            + " as a path to a directory containing all exam data where" \
            + " each exam data file is named after the course unit.", 
        action="store_true"
    )

    args = argparser.parse_args()

    # Checking if we need the default values
    template_dir = args.template if args.template == "templates" \
        else os.path.dirname(args.template)
    template_name = "default_template.md" if args.template == "templates" \
        else os.path.basename(args.template)

    # Checking if we are getting a valid path for template
    if not os.path.exists(f"{template_dir}/{template_name}"):
        print(f"Cannot find template in: '{template_dir}/{template_name}'.")
        exit(1)
    elif os.path.isdir(f"{template_dir}/{template_name}"):
        print(f"'{template_dir}/{template_name}' is a path for a directory.")
        exit(1)

    # These are gonna be basically lists
    csv_files = None
    course_names = None

    if not os.path.exists(args.data):
        print(f"'{args.data}' does not exist!.")
        exit(1)
    elif args.multiple:
        # -d should not be a file
        if os.path.isfile(args.data):
            print(f"'{args.data}' is a path to a file. " \
                + "Please pass in a path to a directory containing csv files" \
                + " when using '--multiple' flag.")
            exit(1)

        csv_files = [f for f in os.listdir(args.data) if f.endswith(".csv")]
        course_names = [name.split(".")[0] for name in csv_files]

        # Checking if the directory contained any csv files
        if len(csv_files) == 0:
            print("No csv files in the directory!.")
            exit(1)
    elif os.path.isdir(args.data): 
        # -d should not be a folder since -m is false
        print(f"'{args.data}' is a path to directory." \
            + " Please use the '--multiple' flag if you want to " \
            + "generate multiple reports.")
        exit(1)
    else:
        course_names = [args.course]

    # All generated files should be saved in outputs
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

        generate_md(
            csv_path = f"{args.data}/{csv_files[index]}" if args.multiple \
                else args.data,
            course_id = course_names[index],
            save_path = save_path, 
            template_dir = template_dir,
            template_name = template_name
        )
    
    print("Reports have been created in 'outputs' folder.")