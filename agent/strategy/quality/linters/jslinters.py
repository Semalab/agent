import shutil

from agent.utils import run_logged


class JSLinters:
    def run(self, path, directories, linters_dir):
        output_path = linters_dir / "jslinters.tmp"

        run_logged(
            [
                "jslinters",
                "-o", output_path,
                "-i", path
            ],
            log_dir=directories.log_dir,
            cwd=directories.repository
        )

        if not output_path.is_file():
            return

        with open(output_path) as output_file, open(linters_dir / "jslinters.txt", "a") as combined_file:
            shutil.copyfileobj(output_file, combined_file)
