from pathlib import Path

from agent.utils import run_logged


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

        run_logged(
            ["git", "config", "--global", "core.quotePath", "false"],
            log_dir=directories.log_dir,
            cwd=directories.repository,
            check=True
        )

        run_logged(
            ["git", "config", "--global", "--add", "safe.directory", "*"],
            log_dir=directories.log_dir,
            cwd=directories.repository,
            check=True
        )

    def list_files(self, directories, linguist_dir):
        """
        lists all committed files
        """
        with open(linguist_dir / "git-ls-tree", "w") as git_ls_tree_file:
            run_logged(
                ["git", "ls-tree", "--full-tree", "-r", "--name-only", "HEAD"],
                log_dir=directories.log_dir,
                cwd=directories.repository,
                stdout=git_ls_tree_file,
                check=True
            )

    def linguist(self, directories, linguist_dir):
        """
        run github-linguist on repo
        """
        with open(linguist_dir / "github-linguist", "w") as github_linguist_file:
            run_logged(
                ["github-linguist", "--breakdown"],
                log_dir=directories.log_dir,
                cwd=directories.repository,
                stdout=github_linguist_file,
                check=True
            )

    def wc(self, directories, linguist_dir):
        with open(linguist_dir / "wc", "w") as wc_file:
            for path in self.files(directories, linguist_dir):
                run_logged(
                    ["wc", path],
                    log_dir=directories.log_dir,
                    cwd=directories.repository,
                    stdout=wc_file,
                    check=True
                )

    def mime(self, directories, linguist_dir):
        with open(linguist_dir / "mime", "w") as mime_file:
            for path in self.files(directories, linguist_dir):
                run_logged(
                    ["file", "-i", path],
                    log_dir=directories.log_dir,
                    cwd=directories.repository,
                    stdout=mime_file,
                    check=True
                )
