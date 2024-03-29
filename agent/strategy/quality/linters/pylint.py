import json

from agent.utils import run_logged


class Pylint:
    def run(self, directories, linters_dir):
        output_path = linters_dir / "pylint.txt"

        run_logged(
            [
                "pylint",
                f"--output-format=json:{output_path}",
                "--recursive=y",
                "."
            ],
            log_dir=directories.log_dir,
            cwd=directories.repository
        )

        if not output_path.is_file():
            return

        with open(output_path) as output_file, open(linters_dir / "pylint.json", "w") as json_file:
            records = json.load(output_file)

            json.dump(
                [{
                    "filename": record["path"],
                    "line_num": record["line"],
                    "col_num": record["column"],
                    "err_message": record["message"]
                } for record in records],
                json_file)
