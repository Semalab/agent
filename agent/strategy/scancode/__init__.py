import os
import platform
import subprocess

from agent.utils import flatten


class Scancode:
    """
    runs https://github.com/nexB/scancode-toolkit
    """

    ARGS = [
        "--processes",
        "2",
        "--only-findings",
        "--timeout",
        "120",
        "--copyright",
        "--package",
        "--license",
        "--license-score",
        "10",
    ]

    IGNORE = [
        "*.min.js",
        "*.jpg",
        "*.gif",
        "*.bmp",
        "*.tiff",
        "*.psd",
        "*.mp4",
        "*.mkv",
        "*.avi",
        "*.mov",
        "*.mpg",
        "*.vob",
        "*.mp3",
        "*.aac",
        "*.wav",
        "*.flac",
        "*.ogg",
        "*.mka",
        "*.wma",
        "*.sql",
        "*Debug0*",
        "*sqlite*",
        "*.png",
        "*.dll",
        "*.exe",
    ]

    def __init__(self, scancode):
        self.bin_scancode = os.path.join(scancode, "scancode")

    def run(self, directories):
        match platform.system():
            case "Linux":
                bin = self.bin_scancode
            case system:
                raise RuntimeError(f"Unsupported system '{system}'")

        os.makedirs(os.path.join(directories.sema_output, "scancode"), exist_ok=True)

        ignore = flatten([["--ignore", pattern] for pattern in Scancode.IGNORE])

        subprocess.run(
            [
                bin,
                "--csv",
                os.path.join(
                    directories.sema_output, "scancode", "scancode-output.csv"
                ),
                *Scancode.ARGS,
                *ignore,
                directories.repository,
            ]
        )
