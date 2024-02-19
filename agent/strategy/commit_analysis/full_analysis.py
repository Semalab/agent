import os
from pathlib import Path


class FullAnalysis:
    userdir = '/home/root'
    jar_name = 'backend-commitanalysis-1.0-SNAPSHOT-jar-with-dependencies.jar'
    basepath = f"{userdir}/.m2/repository/backend/backend-commitanalysis/1.0-SNAPSHOT"

    def __init__(self, repo_path: Path, out_path: Path):
        self.repo = repo_path
        self.out = out_path

    def run(self, _):
        out_path = Path(self.out, '.sema', 'commit_analysis')
        try:
            Path.mkdir(out_path, parents=True) if not Path.exists(out_path) else None
            cmd = f"java -jar {self.basepath}/{self.jar_name} -agent -inputPath {self.repo} -outPath {out_path} -branch master"
            os.system(cmd)
        except Exception as e:
            print(f"Failed to run commit analysis because: {e}")

