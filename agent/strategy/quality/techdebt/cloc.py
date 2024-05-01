from agent.utils import run_logged


class Cloc:
    def run(self, directories, techdebt_dir):
        with open(techdebt_dir / "cloc.txt", "w") as output_file:
            run_logged(
                [
                    "cloc",
                    "--quiet",
                    "--csv",
                    directories.repository
                ],
                log_dir=directories.log_dir,
                stdout=output_file,
            )

        with open(techdebt_dir / "clock_by_file_by_lang.txt", "w") as output_file:
            run_logged(
                [
                    "cloc",
                    "--quiet",
                    "--by-file-by-lang",
                    "--skip-uniqueness",
                    "--csv",
                    directories.repository
                ],
                log_dir=directories.log_dir,
                stdout=output_file,
            )
