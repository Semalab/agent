import os
from pathlib import Path
import shutil

from agent.utils import run_logged


class ESLint:
    def run(self, path, directories, linters_dir):
        output_path = linters_dir / "eslint.tmp"
        config_path = Path(os.environ["JSTOOLS_HOME"]) / "eslint.json"

        run_logged(
            [
                "eslint",
                "--config", config_path,
                "--format", "unix",
                "--output-file", output_path,
                path
            ],
            log_dir=directories.log_dir,
            cwd=directories.repository
        )

        if not output_path.is_file():
            return

        with open(output_path) as output_file, open(linters_dir / "eslint.txt", "a") as combined_file:
            shutil.copyfileobj(output_file, combined_file)
