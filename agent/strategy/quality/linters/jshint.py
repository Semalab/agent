import os
from pathlib import Path
import shutil

from agent.utils import run_logged


class JSHint:
    def run(self, path, directories, linters_dir):
        output_path = linters_dir / "jshint.tmp"
        config_path = Path(os.environ["JSTOOLS_HOME"]) / "jshint.json"

        with open(output_path, "w+") as output_file:
            run_logged(
                [
                    "jshint",
                    "--config", config_path,
                    "--reporter", "unix",
                    path
                ],
                log_dir=directories.log_dir,
                cwd=directories.repository,
                stdout=output_file
            )

            output_file.seek(0)

            with open(linters_dir / "jshint.txt", "a") as combined_file:
                shutil.copyfileobj(output_file, combined_file)
