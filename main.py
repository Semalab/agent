import os
import shutil
import tempfile
from zipfile import ZipFile
from datetime import datetime

import click
from click import ClickException

from agent.directories import Directories
from agent.strategy import Dependencies, DependencyCheck, Scancode
from agent.utils import detect_version_control_system
from agent.vcs_converter import VCSConverter


@click.command()
@click.option(
    "-o",
    "--output",
    default="repository.zip",
    metavar="FILE",
    help="Output zip filename.",
)
@click.option(
    "--dependency-check",
    metavar="PATH",
    help="Path to dependency-check directory. Can also be set through the environment variable AGENT_DEPENDENCY_CHECK.",
)
@click.option(
    "--scancode",
    metavar="PATH",
    help="Path to scancode directory. Can also be set through the environment variable AGENT_SCANCODE.",
)
@click.argument("repository")
def main(repository, output, dependency_check, scancode):
    """
    Run local scan on REPOSITORY and generate a zip file.
    """

    if not os.path.isdir(repository):
        raise ClickException(f"directory '{repository}' does not exist")

    ts_now = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    repository = os.path.abspath(repository)
    output = os.path.abspath(output)

    with tempfile.TemporaryDirectory() as tempdir:
        repo_type = detect_version_control_system(repository)
        click.echo(f"Given repo is {repo_type} repo")
        convertor = VCSConverter(repository, repo_type, tempdir)
        repository = convertor.convert()

        strategies = [Dependencies()]

        if dependency_check:
            strategies.append(DependencyCheck(dependency_check))

        if scancode:
            strategies.append(Scancode(scancode))

        directories = Directories(repository=repository, output=tempdir)
        for strategy in strategies:
            strategy.run(directories)

        output_basename, output_ext = os.path.splitext(output)
        output_basename = create_output_basename(output_basename, ts_now)
        output_ext = output_ext[1:]
        if not output_ext:
            click.echo("output has no extension, assuming .zip")
            output_ext = "zip"

        shutil.make_archive(output_basename, output_ext, tempdir)


def create_output_basename(output_basename: str, ts_now: str) -> str:
    """
    Create the output zipfile name.
    output format - "timestamp_reponame.zip"
    """
    zipname = output_basename.split("/")[-1]
    new_name = output_basename.replace(zipname, f"{ts_now}_{zipname}")
    return new_name


if __name__ == "__main__":
    main(auto_envvar_prefix="AGENT")
