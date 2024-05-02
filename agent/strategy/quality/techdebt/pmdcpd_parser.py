from agent.utils import run_logged
import os

class PmdCpdParser:
    def run(self, directories, techdebt_dir):

        languages = ["cpp","cs","ecmascript","java","objectivec","php","ruby", "scala"]
        pmdcpdparser_output_folder_path = os.path.join(techdebt_dir,'PMDCPDParser')
        if not os.path.exists(pmdcpdparser_output_folder_path):
            os.makedirs(pmdcpdparser_output_folder_path)
        for language in languages:
            # Run for each language parser
            #print(f"Running for language {language}")
            with open(os.path.join(pmdcpdparser_output_folder_path,language +".txt"), "w") as output_file:
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
                    stdout=output_file,
            )