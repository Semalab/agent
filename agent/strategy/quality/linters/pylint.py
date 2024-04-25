import shutil

from agent.utils import run_logged


class Pylint:
    def run(self, path, directories, linters_dir):
        output_path = linters_dir / "pylint.tmp"

        run_logged(
            [
                "pylint",
                f"--output-format=text:{output_path}",
                path
            ],
            log_dir=directories.log_dir,
            cwd=directories.repository
        )

        if not output_path.is_file():
            return

        with open(output_path) as output_file, open(linters_dir / "pylint.txt", "a") as combined_file:
            shutil.copyfileobj(output_file, combined_file)
