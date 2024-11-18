import logging
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import click
from click import ClickException

from agent.directories import Directories
from agent.repository import Repository
from agent.strategy.backend_analysis import BackendAnalysis
from agent.strategy.oss import Dependencies, DependencyCheck, Scancode
from agent.strategy.quality import Linguist, Linters, TechDebt
from agent.strategy.ai_engine import GBOM


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
@click.argument('scantypes', nargs=-1)
def main(repository: Path, output: Path, scantypes: tuple[str, ...]):
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
            Linguist(),
            Linters(),
            TechDebt(),
            BackendAnalysis("backend-commitanalysis"),
            BackendAnalysis("backend-gitblame"),
            GBOM()
        ]
        directories = Directories(repository=repository.path, output=archive_root)

        logging.basicConfig(
            level=logging.INFO,
            handlers=[
                logging.FileHandler(directories.log_dir / "agent.log"),
                logging.StreamHandler()
            ]
        )
        logger = logging.getLogger("agent")

        if Path("version.txt").is_file():
            with open("version.txt") as f:
                version = f.read().strip()
                logger.info(f"Running Agent version: {version}")

        for strategy in strategies:
            strategy_name = strategy.__class__.__name__

            if scantypes and strategy_name.lower() not in scantypes:
                continue

            try:
                logger.info(f"Running SQ-5978")
                logger.info(f"Running scan: {strategy_name}")
                strategy.run(directories)
            except:
                logger.exception(f"Scan failed: {strategy_name}")

        archive_name = make_archive(
            output=output, repo_name=repository.name, root=archive_root, directories=directories
        )

        click.echo(
            f"A zip file has been created at '{archive_name}.zip'. Please send this file to "
            "customers@semasoftware.com to complete the analysis."
        )


def make_archive(output: Path, repo_name: str, root: Path, directories: Path) -> Path:
    """
    create an archive of `directory` in `{output}/{repo_name}_timestamp.zip`
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

    try:
        linguist_dir = directories.mkdir("linguist")
        with open(linguist_dir / "git-remotes") as git_remotes_file:
            project_name = Path(urlparse(git_remotes_file.readline().split()[1]).path).stem or repo_name
    except Exception:
        project_name = repo_name

    archive_name = f"{project_name}_{timestamp}"
    archive_dest = output / archive_name

    shutil.make_archive(archive_dest, "zip", root)

    return archive_name


if __name__ == "__main__":
    main()
