import os
import platform
import subprocess


class DependencyCheck:
    """
    runs https://github.com/jeremylong/DependencyCheck
    """

    def run(self, directories):
        subprocess.run(
            [
                "dependency-check",
                "--format",
                "CSV",
                "--scan",
                directories.repository,
                "--out",
                directories.sema_output / "dependency_check",
            ]
        )
