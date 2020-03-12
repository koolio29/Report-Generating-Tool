import csv
import sqlite3

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

def main():
    extractor = ExamCsvExtractor()
    exam_results = extractor.get_exam_results(csv_path="data/Test_1.csv")

    db = DatabaseAccess(exam_results)
    overallstats = OverallExamStats(db)

    print("All results (out of 100): ", overallstats.total_marks)

if __name__ == "__main__":
    main()