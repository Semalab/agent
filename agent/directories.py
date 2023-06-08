import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Directories:
    SEMA_DIR = ".sema"

    repository: Path
    output: Path

    @property
    def sema_output(self):
        sema_output = self.output / self.SEMA_DIR
        sema_output.mkdir(exist_ok=True)

        return sema_output

    def __post_init__(self):
        if not os.path.isabs(self.repository):
            raise ValueError("repository is not an absolute path")

        if not os.path.isabs(self.output):
            raise ValueError("output is not an absolute path")
