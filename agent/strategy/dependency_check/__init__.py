import os
import subprocess


class DependencyCheck:
    """
    runs https://github.com/jeremylong/DependencyCheck
    """

    def __init__(self, dependency_check_path):
        self.bin_linux = os.path.join(
            dependency_check_path, "bin", "dependency-check.sh"
        )
        self.bin_windows = os.path.join(
            dependency_check_path, "bin", "dependency-check.bat"
        )

    def run(self, directories):
        subprocess.run(
            [
                self.bin_linux,
                "--scan",
                directories.repository,
                "--out",
                os.path.join(directories.sema_output, "dependency-check.csv"),
            ]
        )
