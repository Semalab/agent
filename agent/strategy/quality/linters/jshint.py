import json

from agent.utils import run_logged
from . import utils


class JSHint:
    def run(self, directories, linters_dir):
        output_path = linters_dir / "jshint.txt"

        with open(output_path, "w+") as output_file, open("/dependencies/js/.jshintrc.json", mode="w+") as config_file:
            json.dump({
                "esversion": 21
            }, config_file)
            config_file.flush()

            run_logged(
                [
                    "jshint",
                    "--config", config_file.name,
                    "--reporter", "unix",
                    "."
                ],
                log_dir=directories.log_dir,
                cwd=directories.repository,
                stdout=output_file
            )

            output_file.seek(0)

            with open(linters_dir / "jshint.json", "w") as json_file:
                utils.parse_to_json(output_file, json_file, utils.MATCHER_UNIX)
