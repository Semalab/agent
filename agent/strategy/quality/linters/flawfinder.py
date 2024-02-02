from agent.utils import run_logged


class FlawFinder:
    def run(self, directories, linters_dir):
        with open(linters_dir / "flawfinder.csv", "w") as output_file:
            run_logged(
                ["flawfinder", "--csv", "--quiet", "-i", directories.repository],
                log_dir=directories.log_dir,
                stdout=output_file,
            )
