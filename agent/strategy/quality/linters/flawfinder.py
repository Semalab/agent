import subprocess


class FlawFinder:
    def run(self, *, repository, linters_dir):
        with open(linters_dir / "flawfinder.csv", "w") as output_file:
            subprocess.run(
                ["flawfinder", "--csv", "--quiet", "-i", repository],
                stdout=output_file,
            )
