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

    def run(self, directories):
        scancode_dir = directories.sema_output / "scancode"
        scancode_dir.mkdir()

        ignore = flatten([["--ignore", pattern] for pattern in Scancode.IGNORE])

        subprocess.run(
            [
                "scancode",
                "--csv",
                scancode_dir / "scancode-output.csv",
                *Scancode.ARGS,
                *ignore,
                directories.repository,
            ]
        )
