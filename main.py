import argparse
import os
import errno

from gooey import Gooey
from gooey import GooeyParser

from report_generating_tool.reportgen import OverallReportGenerator
from report_generating_tool.reportgen import LecturerReportGenerator
from report_generating_tool.csvgen import LecturerFeedbackCsvGenerator

ABS_SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))

# This is here for the time being since the data directory is in root
# TODO: Probably need to add a flag to allow to specify a save path
DEFAULT_DATA_PATH = ABS_SCRIPT_PATH + "/data/full_exam.csv"
DEFAULT_TEMPLATE_PATH = ABS_SCRIPT_PATH + "/templates"

LECTURER_TEMPLATE = "lecturer_template.md"

@Gooey(
    program_name='Exam Feedback Generating Tool', 
    default_size=(625, 550)
)
def main():
    argparser = GooeyParser(
        description="Create exam feedback reports"
    )

    argparser.add_argument(
        "-c", "--CourseId", 
        help="Course Id which will be used for the files created. Only when "
            + "using a single dataset", 
        default="COMP000000"
    )
    argparser.add_argument(
        "-d", "--DatasetFile", 
        help="Select the CSV file from which the report will be generated."
        + " This Will not be used when generating multiple feedback reports", 
        widget='FileChooser'
    )
    argparser.add_argument(
        "-t", "--template", 
        help="Select the template to be used.", 
        default=DEFAULT_TEMPLATE_PATH,
        widget='FileChooser'
    )
    argparser.add_argument(
        "-f", "--DatasetFolder", 
        help="Selects a folder containing multiple csv dataset files. Only "
            + "used when generating multiple reports", 
        widget="DirChooser"
    )
    argparser.add_argument(
        "-m", "--multiple", 
        help="Uses the directory specified in DatasetFolder to get a set of"
            + " csv data files to create multiple reports", 
        action="store_true"
    )
    argparser.add_argument(
        "-g", "--generate_data",
        help="Generates a csv file containing statistics for lecturers use.",
        action="store_true"
    )

    args = argparser.parse_args()

    if args.multiple:
        if args.DatasetFolder is None:
            print("You are trying to generate multiple feedback reports"
            + " but you have not passed in a folder containing multiple csv"
            + " files containing exam data")
            exit(1)

    if args.DatasetFile is None:
        print("You were trying to genereate a feedback report but you have not" 
        + "passed in a csv file containing the exam data")
        exit(1)

    if args.template is None:
        print("You have not selected a template to use for generating the"
        + " overall feedback report")
        exit(1) 

    # Checking if we need the default values
    template_dir = args.template if args.template == DEFAULT_TEMPLATE_PATH \
        else os.path.dirname(args.template)
    template_name = "default_template.md" if args.template == DEFAULT_TEMPLATE_PATH \
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

    csv_location = args.DatasetFolder if args.multiple else args.DatasetFile

    if not os.path.exists(csv_location):
        print(f"'{csv_location}' does not exist!.")
        exit(1)
    elif args.multiple:
        # -d should not be a file
        if os.path.isfile(csv_location):
            print(f"'{csv_location}' is a path to a file. " \
                + "Please pass in a path to a directory containing csv files" \
                + " when using '--multiple' flag.")
            exit(1)

        csv_files = [f for f in os.listdir(csv_location) if f.endswith(".csv")]
        course_names = [name.split(".")[0] for name in csv_files]

        # Checking if the directory contained any csv files
        if len(csv_files) == 0:
            print("No csv files in the directory!.")
            exit(1)
    elif os.path.isdir(csv_location): 
        # -d should not be a folder since -m is false
        print(f"'{csv_location}' is a path to directory." \
            + " Please use the '--multiple' flag if you want to " \
            + "generate multiple reports.")
        exit(1)
    else:
        course_names = [args.CourseId]

    # All generated files should be saved in outputs
    if not os.path.isdir("outputs"):
        os.mkdir("outputs")

    report_generator = OverallReportGenerator(template_dir, template_name)
    lecturer_report_gen = LecturerReportGenerator(template_dir, 
                                                    LECTURER_TEMPLATE)

    for index in range(0, len(course_names)):
        save_path = f"{os.getcwd()}/outputs/{course_names[index]}"

        try:
            os.mkdir(save_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Cannot make 'output' directory!.")
                print(e)
                exit(1)

        report_generator.generate_report(
            course_id = course_names[index],
            csv_path = f"{csv_location}/{csv_files[index]}" if args.multiple \
                else csv_location,
            save_path = save_path
        )

        lecturer_report_gen.generate_report(
            course_id = course_names[index],
            csv_path = f"{csv_location}/{csv_files[index]}" if args.multiple \
                else csv_location,
            save_path = save_path
        )

        if args.generate_data:
            csv_generator = LecturerFeedbackCsvGenerator(
                csv_path =  f"{csv_location}/{csv_files[index]}" 
                            if args.multiple else csv_location,
                filename = f"{course_names[index]}_data.csv",
                save_path = save_path
            )
            csv_generator.generate_csv()
    
    print("Files have been created in 'outputs' folder.")

if __name__ == "__main__":
    main()