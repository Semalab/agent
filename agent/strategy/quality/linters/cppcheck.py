import json
import re

from agent.utils import run_logged


class CppCheck:
    message_re = r'^(?P<filename>.*?):(?P<line_num>\d+):(?P<col_num>\d*):\s+\w+:\s+(?P<err_message>.*)$'

    def run(self, directories, linters_dir):
        output_path = linters_dir / "cppcheck.txt"

        run_logged(
            [
                "cppcheck",
                "--enable=all",
                "--force",
                "--template={file}:{line}:{column}: {severity}: {message}",
                f"--output-file={output_path}",
                "."
            ],
            log_dir=directories.log_dir,
            cwd=directories.repository
        )

        with open(output_path) as output_file, open(linters_dir / "cppcheck.json", "w") as json_file:
            json.dump(
                [match.groupdict()
                    for line in output_file
                    if (match := re.match(self.message_re, line)) is not None],
                json_file)
