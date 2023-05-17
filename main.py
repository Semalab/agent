import os
import shutil
import tempfile
from zipfile import ZipFile

import click

from agent.strategy import Dependencies


@click.command()
@click.option(
    "-o",
    "--output",
    default="repository.zip",
    metavar="FILE",
    help="output zip filename",
)
@click.argument("repository")
def main(repository, output):
    """
    Run local scan on REPOSITORY and generate a zip file.
    """
    with tempfile.TemporaryDirectory() as tempdir:
        dependencies = Dependencies(repository, tempdir)
        dependencies.run()


if __name__ == "__main__":
    main()
