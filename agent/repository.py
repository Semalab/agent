import logging
import subprocess
import tempfile
from enum import Enum
from pathlib import Path
from typing import Optional, Self


logger = logging.getLogger(__name__)


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
        self.name = repository.stem
        self.path = Repository.convert(repository)

    @classmethod
    def convert(cls, repository: Path) -> Path:
        match VCS.detect(repository):
            case VCS.SVN:
                return cls.svn_to_git(repository)

            case None:
                logger.warning("Unknown repository version control system")

            case VCS.MERCURIAL:
                logger.warning("Unsupported version control system")

        return repository

    @classmethod
    def svn_to_git(cls, repository_svn: Path) -> Path:
        logger.info(f"converting svn repository '{repository_svn}' to git")
        repository_git = Path(tempfile.mkdtemp(suffix=f"{repository_svn.name}_git"))

        svn_info = subprocess.run(
            ["svn", "info", "--show-item", "repos-root-url", repository_svn],
            check=True,
            capture_output=True,
        )

        subprocess.run(
            ["git", "svn", "clone", svn_info.stdout.strip(), repository_git],
            check=True,
        )

        return repository_git
