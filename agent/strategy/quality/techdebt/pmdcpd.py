from agent.utils import run_logged


class PmdCpd:
    def run(self, directories, techdebt_dir):
        languages = ["cpp", "cs", "ecmascript", "java",
                     "objectivec", "php", "python", "ruby", "scala"]

        pmdcpdparser_output_folder_path = techdebt_dir / "pmdcpd"
        pmdcpdparser_output_folder_path.mkdir(exist_ok=True)

        for language in languages:
            # Run for each language
            with open(pmdcpdparser_output_folder_path / f"{language}.txt", "w") as output_file:
                run_logged(
                    [
                        "run-pmd",
                        "cpd",
                        "--files", directories.repository,
                        "--language", language,
                        "--minimum-tokens", "100",
                        "--skip-lexical-errors",
                        "--format", "csv_with_linecount_per_file"
                    ],
                    log_dir=directories.log_dir,
                    stdout=output_file
                )
