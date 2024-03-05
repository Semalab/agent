from agent.utils import flatten, run_logged


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
        scancode_dir = directories.mkdir("scancode")
        ignore = flatten([["--ignore", pattern] for pattern in Scancode.IGNORE])

        run_logged(
            [
                "scancode",
                "--json-pp",
                scancode_dir / "scancode-output.json",
                *Scancode.ARGS,
                *ignore,
                directories.repository,
            ],
            log_dir=directories.log_dir
        )
