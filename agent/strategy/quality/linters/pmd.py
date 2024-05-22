import shutil

from agent.utils import run_logged


class PMD:
    def run(self, path, directories, linters_dir):
        output_path = linters_dir / "pmd.tmp"

        run_logged(
            [
                "run-pmd",
                "pmd",
                "--rulesets", "rulesets/internal/all-java.xml",
                "--report-file", output_path,
                "--dir", path
            ],
            # For PMD 7+:
            # [
            #     "pmd",
            #     "check",
            #     "--rulesets", "rulesets/java/quickstart.xml",
            #     "--no-progress",
            #     "--format", "csv",
            #     "--report-file", output_path,
            #     "--dir", "."
            # ],
            log_dir=directories.log_dir,
            cwd=directories.repository
        )

        if not output_path.is_file():
            return

        with open(output_path) as output_file, open(linters_dir / "pmd.java.all.txt", "a") as combined_file:
            shutil.copyfileobj(output_file, combined_file)
