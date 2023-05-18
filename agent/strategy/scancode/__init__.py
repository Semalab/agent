import os
import platform
import subprocess


class Scancode:
    """
    runs https://github.com/nexB/scancode-toolkit
    """

    def __init__(self, scancode):
        self.bin_scancode = os.path.join(scancode, "scancode")

    def run(self, directories):
        match platform.system():
            case "Linux":
                bin = self.bin_scancode
            case system:
                raise RuntimeError(f"Unsupported system '{system}'")

        os.makedirs(os.path.join(directories.sema_output, "scancode"), exist_ok=True)

        subprocess.run(
            [
                bin,
                "--csv",
                os.path.join(
                    directories.sema_output, "scancode", "scancode-output.csv"
                ),
                "--copyright",
                "--license",
                "--package",
                directories.repository,
            ]
        )
