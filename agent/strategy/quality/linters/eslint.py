import json

from agent.utils import run_logged
from . import utils


class ESLint:
    def run(self, directories, linters_dir):
        output_path = linters_dir / "eslint.txt"

        with open("/dependencies/js/.eslintrc.json", "w+") as config_file:
            json.dump({
                "extends": ["eslint:recommended", "plugin:@typescript-eslint/recommended"]
            }, config_file)
            config_file.flush()

            run_logged(
                [
                    "eslint",
                    "--config", config_file.name,
                    "--format", "unix",
                    "--output-file", output_path,
                    "."
                ],
                log_dir=directories.log_dir,
                cwd=directories.repository
            )

        if not output_path.is_file():
            return

        with open(output_path) as output_file, open(linters_dir / "eslint.json", "w") as json_file:
            utils.parse_to_json(output_file, json_file, utils.MATCHER_UNIX)
