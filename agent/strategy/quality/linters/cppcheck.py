from agent.utils import run_logged


class CppCheck:
    def run(self, *, directories, linters_dir):
        repository = directories.repository
        with open(linters_dir / "cppcheck.txt", "w") as output_file:
            run_logged(
                [
                    "cppcheck",
                    "--enable=all",
                    "--force",
                    '--template="{file}:{line}:{column}: {severity}: {message}"',
                    repository,
                ],
                log_dir=directories.log_dir,
                stdout=output_file,
            )
