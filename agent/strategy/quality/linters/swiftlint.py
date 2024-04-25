import shutil

from agent.utils import run_logged


class SwiftLint:
    def run(self, path, directories, linters_dir):
        output_path = linters_dir / "swiftlint.tmp"

        run_logged(
            [
                "swiftlint",
                "lint",
                "--output", output_path,
                path
            ],
            log_dir=directories.log_dir,
            cwd=directories.repository
        )

        if not output_path.is_file():
            return

        with open(output_path) as output_file, open(linters_dir / "swiftlint.txt", "a") as combined_file:
            shutil.copyfileobj(output_file, combined_file)
