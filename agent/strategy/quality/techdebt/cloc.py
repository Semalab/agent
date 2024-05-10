from agent.utils import run_logged


class Cloc:
    def run(self, directories, techdebt_dir):
        # TODO: this call can be removed, as the second call includes the output
        # of this one at the end of the CSV.
        with open(techdebt_dir / "cloc.txt", "w") as output_file:
            run_logged(
                [
                    "cloc",
                    "--quiet",
                    "--csv",
                    "."
                ],
                log_dir=directories.log_dir,
                stdout=output_file,
                cwd=directories.repository
            )

        with open(techdebt_dir / "cloc_by_file_by_lang.txt", "w") as output_file:
            run_logged(
                [
                    "cloc",
                    "--quiet",
                    "--by-file-by-lang",
                    "--skip-uniqueness",
                    "--csv",
                    "."
                ],
                log_dir=directories.log_dir,
                stdout=output_file,
                cwd=directories.repository
            )
