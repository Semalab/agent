import csv
import json

from agent.utils import run_logged


class PMD:
    def run(self, directories, linters_dir):
        output_path = linters_dir / "pmd.csv"

        run_logged(
            [
                "pmd",
                "check",
                "--rulesets", "rulesets/java/quickstart.xml",
                "--no-progress",
                "--format", "csv",
                "--report-file", output_path,
                "--dir", "."
            ],
            log_dir=directories.log_dir,
            cwd=directories.repository
        )

        if not output_path.is_file():
            return

        with open(output_path, newline='') as output_file, open(linters_dir / "pmd.json", "w") as json_file:
            reader = csv.DictReader(output_file)

            json.dump(
                [{
                    "filename": row["File"],
                    "line_num": row["Line"],
                    "col_num": 0,
                    "err_message": row["Description"]
                } for row in reader],
                json_file
            )
