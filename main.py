import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile

import click
from click import ClickException

from agent.directories import Directories
from agent.repository import Repository
from agent.strategy.oss import Dependencies, DependencyCheck, Scancode
from agent.strategy.quality import Linguist, Linters


@click.command()
@click.option(
    "--output",
    type=Path,
    required=True,
    metavar="DIRECTORY",
    help="Directory to save the output zip file to.",
)
@click.option(
    "--repository",
    type=Path,
    required=True,
    metavar="DIRECTORY",
    help="Repository to scan.",
)
def main(repository: Path, output: Path):
    """
    Run local scan on REPOSITORY and generate a zip file.
    """

    if not repository.is_dir():
        raise ClickException(f"repository '{repository}' does not exist")

    if not output.is_dir():
        raise ClickException(f"output directory '{output}' does not exist")

    repository = Repository(repository)
    output = output.absolute()

    with tempfile.TemporaryDirectory() as archive_root:
        archive_root = Path(archive_root)

        strategies = [
            Dependencies(),
            DependencyCheck(),
            Scancode(),
            Linters(),
            Linguist(),
        ]

        directories = Directories(repository=repository.path, output=archive_root)
        for strategy in strategies:
            strategy.run(directories)

        archive_name = make_archive(
            output=output, repo_name=repository.name, root=archive_root
        )

        click.echo(
            f"A zip file has been created at '{archive_name}.zip'. Please send this file to "
            "customers@semasoftware.com to complete the analysis."
        )


def make_archive(output: Path, repo_name: str, root: Path) -> Path:
    """
    create an archive of `directory` in `{output}/{repo_name}_timestamp.zip`
    """

    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    archive_name = f"{repo_name}_{timestamp}"
    archive_dest = output / archive_name

    shutil.make_archive(archive_dest, "zip", root)

    return archive_name


if __name__ == "__main__":
    main()
