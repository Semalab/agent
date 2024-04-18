from agent.utils import run_logged

class lizardParser:
    def run(self, directories, techdebt_dir):

        # get currentFilelist

        # Run lizard parser
        with open(techdebt_dir / "lizard.txt", "w") as output_file:
            run_logged(
                [
                    "lizard",
                    "ignore_warnings",
                    "-1",
                    directories.repository
                ],
                log_dir=directories.log_dir,
                stdout=output_file,
           )

        # run cloc
        with open(techdebt_dir / "lizard_cloc.txt", "w") as output_file:
            run_logged(
                [
                    "--quiet",
					"--by-file-by-lang", 
                    "--skip-uniqueness", 
                    "--csv", 
                    directories.repository
                ],
                log_dir=directories.log_dir,
                stdout=output_file,
            )