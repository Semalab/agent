import os
import subprocess
import tempfile
from enum import Enum
from pathlib import Path
from typing import Optional, Self

import click


class VCS(Enum):
    GIT = "git"
    SVN = "svn"
    MERCURIAL = "mercurial"

    @classmethod
    def detect(cls, path: Path) -> Optional[Self]:
        if (path / ".git").is_dir():
            return VCS.GIT

        if (path / ".svn").is_dir():
            return VCS.SVN

        if (path / ".hg").is_dir():
            return VCS.MERCURIAL

        return None


class Repository:
    def __init__(self, repository: Path):
        self.name = repository.name
        self.path = Repository.convert(repository)

    @classmethod
    def convert(cls, repository: Path) -> Path:
        match VCS.detect(repository):
            case VCS.GIT:
                return repository
            case VCS.SVN:
                return cls.svn_to_git(repository)
            case None:
                raise RuntimeError(
                    "unknown repository version control system for repository {repository}"
                )

            case other_vcs:
                raise RuntimeError(
                    f"unsupported version control system {other_vcs} for repository {repository}"
                )

    @classmethod
    def svn_to_git(repository_svn: Path) -> Path:
        click.echo(f"converting svn repository '{repository_svn}' to git")
        repository_git = Path(tempfile.mkdtemp(suffix=f"{repository_svn.name}_git"))

        subprocess.run(
            ["git", "svn", "clone", f"file://{repository_svn}", repository_git],
            check=True,
        )

        return repository_git
