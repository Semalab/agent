import os
import subprocess
import click


class VCSConverter:
    def __init__(self, repository: str, repo_type: str, tempdir):
        self.repository = repository
        self.repo_type = repo_type
        self.tempdir = tempdir
        self.repo_name = os.path.basename(repository)

    def run_command(self, command: str):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output, _ = process.communicate()
        return output.decode().strip()

    def convert(self) -> str:
        if self.repo_type == "SVN":
            return self._convertsvn2git()
        else:
            return self.repository

    def _convertsvn2git(self) -> str:
        """
        Function to convert svn working copy to git
        """
        click.echo("Initiated SVN to GIT conversion")

        # Create a temp folder at location temp_path
        temp_path = os.path.join(os.path.dirname(self.tempdir), "temp")
        os.makedirs(temp_path, exist_ok=True)
        click.echo(f"temp path created at {temp_path}")

        svn_exported_path = os.path.join(temp_path, f"{self.repo_name}_exported")

        dummy_repo_name = f"{self.repo_name}_dummy_svn"
        svn_repo_path = os.path.join(temp_path, dummy_repo_name)

        # Create a dummy repo
        self.run_command(f"svnadmin create {svn_repo_path}")

        # Clean copy of the latest version of your files
        self.run_command(f"svn export {self.repository} {svn_exported_path}")

        remote_repo_url = f"file://{svn_repo_path}"
        self.run_command(f"svn checkout {remote_repo_url} {svn_exported_path}")

        # svn add
        self.run_command(f"svn add --force {svn_exported_path}")

        # svn commit
        self.run_command(
            f'svn commit -m "Migrating local SVN folder to new remote repository" {svn_exported_path}'
        )

        # Convert to git
        destination_folder = os.path.join(temp_path, f"{self.repo_name}_git")
        self.run_command(f"git svn clone {remote_repo_url} {destination_folder}")

        click.echo(f"Converted git is stored at {destination_folder}")

        return destination_folder
