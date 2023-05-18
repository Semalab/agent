import os
import platform
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
        match platform.system():
            case "Linux":
                bin = self.bin_linux
            case "Windows":
                bin = self.bin_windows
            case system:
                raise RuntimeError(f"Unsupported system '{system}'")

        subprocess.run(
            [
                bin,
                "--format",
                "CSV",
                "--scan",
                directories.repository,
                "--out",
                os.path.join(directories.sema_output, "dependency_check"),
            ]
        )
