from agent.utils import run_logged


class CppCheck:
    def run(self, directories, linters_dir):
        with open(linters_dir / "cppcheck.txt", "w") as output_file:
            run_logged(
                [
                    "cppcheck",
                    "--enable=all",
                    "--force",
                    '--template="{file}:{line}:{column}: {severity}: {message}"',
                    directories.repository,
                ],
                log_dir=directories.log_dir,
                stdout=output_file,
            )
