import os
from dataclasses import dataclass


@dataclass
class Strategy:
    SEMA_DIR = ".sema"

    repository: str
    output: str

    @property
    def sema_output(self):
        return os.path.join(self.output, self.SEMA_DIR)

    def __post_init__(self):
        if not os.path.isabs(self.repository):
            raise ValueError("repository is not an absolute path")

        if not os.path.isabs(self.output):
            raise ValueError("output is not an absolute path")
