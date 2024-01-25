import os
import platform
import subprocess
from pathlib import Path

from agent.utils import flatten


class Linguist:
    """
    runs https://github.com/github-linguist/linguist
    """

    def run(self, directories):
        linguist_dir = directories.sema_output / "linguist"
        linguist_dir.mkdir()

        self.git_config(directories)
        self.list_files(directories, linguist_dir)
        self.linguist(directories, linguist_dir)
        self.wc(directories, linguist_dir)
        self.mime(directories, linguist_dir)

    def files(self, directories, linguist_dir):
        with open(linguist_dir / "git-ls-tree") as git_ls_tree_file:
            for path in git_ls_tree_file:
                path = Path(directories.repository, path.strip())

                if path.is_file():
                    yield path

    def git_config(self, directories):
        """
        run any git configuration necessary before linguist scan
        """

        subprocess.run(
            ["git", "config", "--global", "core.quotePath", "false"],
            cwd=directories.repository,
            check=True,
        )

        subprocess.run(
            ["git", "config", "--global", "--add", "safe.directory", "*"],
            cwd=directories.repository,
            check=True,
        )

    def list_files(self, directories, linguist_dir):
        """
        lists all committed files
        """
        with open(linguist_dir / "git-ls-tree", "w") as git_ls_tree_file:
            subprocess.run(
                ["git", "ls-tree", "--full-tree", "-r", "--name-only", "HEAD"],
                cwd=directories.repository,
                stdout=git_ls_tree_file,
                check=True,
            )

    def linguist(self, directories, linguist_dir):
        """
        run github-linguist on repo
        """
        with open(linguist_dir / "github-linguist", "w") as github_linguist_file:
            subprocess.run(
                ["github-linguist", "--breakdown"],
                cwd=directories.repository,
                stdout=github_linguist_file,
                check=True,
            )

    def wc(self, directories, linguist_dir):
        with open(linguist_dir / "wc", "w") as wc_file:
            for path in self.files(directories, linguist_dir):
                output = subprocess.run(
                    ["wc", path],
                    cwd=directories.repository,
                    capture_output=True,
                    check=True,
                )
                wc_file.write(output.stdout.decode("utf-8"))

    def mime(self, directories, linguist_dir):
        with open(linguist_dir / "mime", "w") as mime_file:
            for path in self.files(directories, linguist_dir):
                output = subprocess.run(
                    ["file", "-i", path],
                    cwd=directories.repository,
                    capture_output=True,
                    check=True,
                )
                mime_file.write(output.stdout.decode("utf-8"))
