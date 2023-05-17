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

    repository = os.path.abspath(repository)
    output = os.path.abspath(output)

    with tempfile.TemporaryDirectory() as tempdir:
        dependencies = Dependencies(repository, tempdir)
        dependencies.run()

        output_basename, output_ext = os.path.splitext(output)
        output_ext = output_ext[1:]
        if not output_ext:
            click.echo("output has no extension, assuming .zip")
            output_ext = "zip"

        shutil.make_archive(output_basename, output_ext, tempdir)


if __name__ == "__main__":
    main()
