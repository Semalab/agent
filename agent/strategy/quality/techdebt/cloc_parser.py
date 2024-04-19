from agent.utils import run_logged

class ClocParser:
    def run(self, directories, techdebt_dir):

        # get currentFilelist

        # Run lizard parser
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