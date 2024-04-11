import shutil

from agent.utils import run_logged


class CppCheck:
    def run(self, path, directories, linters_dir):
        output_path = linters_dir / "cppcheck.tmp"

        run_logged(
            [
                "cppcheck",
                "--enable=all",
                "--force",
                "--template={file}:{line}:{column}: {severity}: {message}",
                f"--output-file={output_path}",
                path
            ],
            log_dir=directories.log_dir,
            cwd=directories.repository
        )

        if not output_path.is_file():
            return

        with open(output_path) as output_file, open(linters_dir / "cppcheck.txt", "a") as combined_file:
            shutil.copyfileobj(output_file, combined_file)
