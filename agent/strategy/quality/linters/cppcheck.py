from agent.utils import run_logged
from . import utils


class CppCheck:
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

        if not output_path.is_file():
            return

        with open(output_path) as output_file, open(linters_dir / "cppcheck.json", "w") as json_file:
            utils.parse_to_json(output_file, json_file, utils.MATCHER_GCC)
