import shutil

from agent.utils import run_logged


class Tailor:
    def run(self, path, directories, linters_dir):
        output_path = linters_dir / "tailor.tmp"

        with open(output_path, "w+") as output_file:
            run_logged(
                [
                    "tailor",
                    "--no-color",
                    path
                ],
                log_dir=directories.log_dir,
                cwd=directories.repository,
                stdout=output_file
            )

            output_file.seek(0)

            with open(linters_dir / "tailor.txt", "a") as combined_file:
                shutil.copyfileobj(output_file, combined_file)
