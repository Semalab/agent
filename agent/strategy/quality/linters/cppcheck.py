import subprocess


class CppCheck:
    def run(self, *, repository, linters_dir):
        with open(linters_dir / "cppcheck.txt", "w") as cppcheck_output:
            subprocess.run(
                [
                    "cppcheck",
                    "--enable=all",
                    "--force",
                    '--template="{file}:{line}:{column}: {severity}: {message}"',
                ],
                stdout=cppcheck_output,
            )
