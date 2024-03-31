from agent.utils import run_logged
from . import utils


class SwiftLint:
    def run(self, directories, linters_dir):
        output_path = linters_dir / "swiftlint.txt"

        run_logged(
            [
                "swiftlint",
                "lint",
                "--output", output_path,
                "."
            ],
            log_dir=directories.log_dir,
            cwd=directories.repository
        )

        if not output_path.is_file():
            return

        with open(output_path) as output_file, open(linters_dir / "swiftlint.json", "w") as json_file:
            utils.parse_to_json(output_file, json_file, utils.MATCHER_GCC)
