import os
import shutil
from zipfile import ZipFile

import click

import agent
import agent.oss as oss


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
    matcher = oss.Matcher()
    paths = []

    for root, _, files in os.walk(repository):
        for filename in files:
            if matcher.matches_any(filename):
                rel_root = os.path.relpath(root, start=repository)
                paths.append(os.path.join(rel_root, filename))

    with ZipFile(output, "w") as zipfile:
        for path in paths:
            zipfile.write(os.path.join(repository, path), arcname=path)


if __name__ == "__main__":
    main()
