from agent.utils import run_logged

class GBOM:
    """
    runs AI Code monitor on given directories
    """

    def run(self, directories):
        run_logged(
            [
                "ai_engine",
                directories.repository,
                "--output-dir", directories.mkdir("GBOM"),
            ],
            log_dir=directories.log_dir
        )
