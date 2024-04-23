from agent.strategy.ai_engine.ai_engine import main
import subprocess
from agent.utils import run_logged


class GBOM:
    """
    runs AI Code monitor on given directories
    """
    
    def run(self, directories):
        run_logged(
            [
                "python",
                "main.py",
                directories.repository,
            ],
            log_dir=directories.log_dir
        )
    
