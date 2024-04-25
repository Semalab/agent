import shutil

from agent.utils import run_logged


class Roslynator:
    def run(self, path, directories, linters_dir):
        output_path = linters_dir / "roslynator.tmp"

        with open(output_path, "w+") as output_file:
            run_logged(
                [
                    "roslynator",
                    "analyze",
                    # Required for newer versions of Roslynator
                    # "--analyzer-assemblies", (Path.home() / ".nuget" / "packages"),
                    # "--severity-level", "info",
                    # "--output", output_path
                    path
                ],
                log_dir=directories.log_dir,
                cwd=directories.repository,
                stdout=output_file
            )

            output_file.seek(0)

            with open(linters_dir / "roslynator.txt", "a") as combined_file:
                shutil.copyfileobj(output_file, combined_file)
