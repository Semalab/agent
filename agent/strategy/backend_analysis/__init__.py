import logging

from agent.utils import run_logged


class BackendAnalysis:
    """
    Runs a backend service that implements CLIRunner.
    """

    def __init__(self, service_name) -> None:
        self.service_name = service_name

    def run(self, directories):
        logger = logging.getLogger(__name__)
        logger.info(f"Running backend analysis: {self.service_name}")

        jar_path = f"/dependencies/{self.service_name}/{self.service_name}-jar-with-dependencies.jar"
        run_logged(
            [
                "java",
                "-jar",
                jar_path,
                "-agent",
                "-inputPath",
                directories.repository,
                "-outPath",
                directories.mkdir(self.service_name),
                "-branch",
                "master"
            ],
            log_dir=directories.log_dir
        )
