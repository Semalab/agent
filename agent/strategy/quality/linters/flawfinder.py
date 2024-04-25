from agent.utils import run_logged


class FlawFinder:
    def run(self, path, directories, linters_dir):
        output_path = linters_dir / "flawfinder.tmp"

        with open(output_path, "w+") as output_file:
            run_logged(
                [
                    "flawfinder",
                    "--csv",
                    "--quiet",
                    "--immediate",
                    path
                ],
                log_dir=directories.log_dir,
                cwd=directories.repository,
                stdout=output_file
            )

            output_file.seek(0)

            with open(linters_dir / "flawfinder.txt", "a") as combined_file:
                skip_header = combined_file.tell() != 0

                for line in output_file:
                    if skip_header:
                        skip_header = False
                        continue

                    combined_file.write(line)
