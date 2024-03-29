import csv
import json
import re

from agent.utils import run_logged


class FlawFinder:
    def run(self, directories, linters_dir):
        output_path = linters_dir / "flawfinder.csv"

        with open(output_path, "w+", newline='') as output_file:
            run_logged(
                ["flawfinder", "--csv", "."],
                log_dir=directories.log_dir,
                cwd=directories.repository,
                stdout=output_file
            )

            output_file.seek(0)
            reader = csv.DictReader(output_file)

            with open(linters_dir / "flawfinder.json", "w") as json_file:
                json.dump(
                    [{
                        "filename": row["File"],
                        "line_num": row["Line"],
                        "col_num": row["Column"],
                        "err_message": f'{row["Category"]},{row["Name"]}: {row["Warning"]}'
                    } for row in reader],
                    json_file
                )
