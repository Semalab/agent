import os
from pathlib import Path
import shutil

from agent.utils import run_logged


class TSLint:
    def run(self, path, directories, linters_dir):
        output_path = linters_dir / "tslint.tmp"
        config_path = Path(os.environ["JSTOOLS_HOME"]) / "tslint.json"

        run_logged(
            [
                "tslint",
                "--config", config_path,
                "--out", output_path,
                path
            ],
            log_dir=directories.log_dir,
            cwd=directories.repository
        )

        if not output_path.is_file():
            return

        with open(output_path) as output_file, open(linters_dir / "tslint.txt", "a") as combined_file:
            shutil.copyfileobj(output_file, combined_file)
