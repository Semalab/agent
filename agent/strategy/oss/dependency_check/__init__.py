from agent.utils import run_logged


class DependencyCheck:
    """
    runs https://github.com/jeremylong/DependencyCheck
    """

    def run(self, directories):
        run_logged(
            [
                "dependency-check",
                "--format",
                "CSV",
                "--scan",
                directories.repository,
                "--out",
                directories.sema_output / "dependency_check",
            ],
            log_dir=directories.log_dir
        )
