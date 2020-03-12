import csv

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

def main():
    extractor = ExamCsvExtractor()
    exam_results = extractor.get_exam_results(csv_path="data/Test_1.csv")

    for result in exam_results:
        print(f"""id: {result.question_id}
type: {result.question_type}
username: {result.username}
lastname: {result.lastname}
firstname: {result.firstname}
max_marks: {result.max_marks}
marks: {result.marks}""", end="\n\n")

if __name__ == "__main__":
    main()