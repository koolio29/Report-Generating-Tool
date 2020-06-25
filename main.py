import argparse
import os
import errno

from report_generating_tool.reportgen import OverallReportGenerator
from report_generating_tool.reportgen import LecturerReportGenerator
from report_generating_tool.csvgen import LecturerFeedbackCsvGenerator

ABS_SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))

# This is here for the time being since the data directory is in root
# TODO: Probably need to add a flag to allow to specify a save path
DEFAULT_DATA_PATH = ABS_SCRIPT_PATH + "/data/full_exam.csv"
DEFAULT_TEMPLATE_PATH = ABS_SCRIPT_PATH + "/templates"

LECTURER_TEMPLATE = "lecturer_template.md"

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
        default=DEFAULT_DATA_PATH
    )
    argparser.add_argument(
        "-t", "--template", 
        help="Path for the report template to be used.", 
        default=DEFAULT_TEMPLATE_PATH
    )
    argparser.add_argument(
        "-m", "--multiple", 
        help="Tells the script that it needs to generate multiple reports. " \
            + "If this flag is True, it would treat the '--data' flag" \
            + " as a path to a directory containing all exam data where" \
            + " each exam data file is named after the course unit.", 
        action="store_true"
    )
    argparser.add_argument(
        "-g", "--generate_data",
        help="Generates a csv file containing statistics for lecturers use.",
        action="store_true"
    )

    args = argparser.parse_args()

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

    report_generator = OverallReportGenerator(template_dir, template_name)
    lecturer_report_gen = LecturerReportGenerator(template_dir, 
                                                    LECTURER_TEMPLATE)

    for index in range(0, len(course_names)):
        # will need to append ".." to create output directory in the project root
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
            csv_path = f"{args.data}/{csv_files[index]}" if args.multiple \
                else args.data,
            save_path = save_path
        )

        lecturer_report_gen.generate_report(
            course_id = course_names[index],
            csv_path = f"{args.data}/{csv_files[index]}" if args.multiple \
                else args.data,
            save_path = save_path
        )

        if args.generate_data:
            csv_generator = LecturerFeedbackCsvGenerator(
                csv_path =  f"{args.data}/{csv_files[index]}" 
                            if args.multiple else args.data,
                filename = f"{course_names[index]}-data.csv",
                save_path = save_path
            )
            csv_generator.generate_csv()
    
    print("Reports have been created in 'outputs' folder.")