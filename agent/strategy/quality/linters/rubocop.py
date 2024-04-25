import shutil

from agent.utils import run_logged


class RuboCop:
    def run(self, path, directories, linters_dir):
        output_path = linters_dir / "rubocop.tmp"

        run_logged(
            [
                "rubocop",
                "--cache", "false",
                # "--lint",
                # "--format", "emacs",
                "--out", output_path,
                path
            ],
            log_dir=directories.log_dir,
            cwd=directories.repository
        )

        if not output_path.is_file():
            return

        with open(output_path) as output_file, open(linters_dir / "rubocop.txt", "a") as combined_file:
            shutil.copyfileobj(output_file, combined_file)
