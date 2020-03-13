import csv
import sqlite3
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

    @property
    def all_mcq_marks(self):
        return self._all_mcq_marks

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


    @property
    def all_essay_marks(self):
        return self._all_essay_marks

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


def main():
    extractor = ExamCsvExtractor()
    exam_results = extractor.get_exam_results(csv_path="data/testinputs/six_student_results.csv")

    db = DatabaseAccess(exam_results)
    overallstats = OverallExamStats(db)
    overallmcqstats = OverallMcqStats(db)
    overallessaystats = OverallEssayStats(db)

    print("Overall Exam Stats")
    print("All results (out of 100): ", overallstats.total_marks)
    print("mean (out of 100): ", overallstats.mean)
    print("median (out of 100): ", overallstats.median)
    print("maximum (out of 100): ", overallstats.maximum)
    print("minimum (out of 100): ", overallstats.minimum)
    print("standard deviation (out of 100): ", overallstats.standard_deviation)
    print("marks distribution (out of 100): ", overallstats.get_marks_distribution(), end="\n\n")

    print("Overall MCQ stats (only)")
    print("All results (out of 100): ", overallmcqstats.all_mcq_marks)
    print("mean (out of 100): ", overallmcqstats.overall_mean)
    print("median (out of 100): ", overallmcqstats.overall_median)
    print("maximum (out of 100): ", overallmcqstats.overall_maximum)
    print("minimum (out of 100): ", overallmcqstats.overall_minimum)
    print("standard deviation (out of 100): ", overallmcqstats.overall_standard_deviation)
    print("MCQ averages (out of 1): ", overallmcqstats.get_individual_mcq_avgs(), end="\n\n")

    print("Overall ESSAY stats (only)")
    print("All results (out of 100): ", overallessaystats.all_essay_marks)
    print("mean (out of 100): ", overallessaystats.overall_mean)
    print("median (out of 100): ", overallessaystats.overall_median)
    print("maximum (out of 100): ", overallessaystats.overall_maximum)
    print("minimum (out of 100): ", overallessaystats.overall_minimum)
    print("standard deviation (out of 100): ", overallessaystats.overall_standard_deviation)
    print("ESSAY averages (out of 5): ", overallessaystats.get_individual_essay_avgs())

def h():
    print("h")

if __name__ == "__main__":
    main()