import subprocess
from agent.utils import run_logged
import os
from dotenv import load_dotenv

class GBOM:
    """
    runs AI Code monitor on given directories
    """
    def init():
        ## define required environment variables
        """
        Load environment variables from a .env file.

        :param env_file_path: Path to the .env file.
        """
        # Check if the .env file exists
        if not os.path.exists('./agent/strategy/ai_engine/ai_engine/.env.production'):
            print(f"Error: ./agent/strategy/ai_engine/ai_engine/.env.production -- does not exist.")
            return False 
        # Load environment variables from the .env file
        load_dotenv('./agent/strategy/ai_engine/ai_engine/.env.production')
        return True


    def run(self, directories):
        run_logged(
            [
                "python",
                "main.py",
                directories.repository,
            ],
            log_dir=directories.log_dir
        )
    
