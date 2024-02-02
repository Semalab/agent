import os
from pathlib import Path

from agent.directories import Directories


class FullAnalysis:
    userdir = '/home/siddharthshishulkar'
    jar_name = 'backend-commitanalysis-1.0-SNAPSHOT-jar-with-dependencies.jar'
    basepath = f"{userdir}/.m2/repository/backend/backend-commitanalysis/1.0-SNAPSHOT"

    def __init__(self, repo_path: Path, out_path: Path):
        self.repo = repo_path
        self.out = out_path

    def run(self, directories: Directories):
        try:
            os.system(f"java -jar {self.basepath}/{self.jar_name}")
        except Exception as e:
            print(f"Failed to run commit analysis because: {e}")

