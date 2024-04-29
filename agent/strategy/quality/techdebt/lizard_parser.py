from agent.utils import run_logged
from pathlib import Path
from agent.strategy.quality.linguist import Linguist
import os

class lizardParser:

    

    def run(self, directories, techdebt_dir):
        
        linguist = Linguist()
        linguist_dir = directories.mkdir("linguist")
 
        # Lizard Parser
        supportedLizardLanguages = ["c", "cpp", "cc", "mm", "cxx", "h", "hpp", "cs", "gd", "go", "java", "js",
        "lua", "m", "php", "py", "rb", "rs", "scala", "swift", "sdl", "ttcn", "ttcnpp", "ts"]

        file_counter = 1
        for file in linguist.files(directories, linguist_dir):
            print(f"file -- {file}")

            file_extension = os.path.splitext(file)[-1].lower().strip('.')
            print(f"file_extension -- {file_extension}")

            if file_extension in supportedLizardLanguages:

                # logger.info(f"running command ~ lizard --ignore_warnings -1 {file}")

                output_file_path = f"{techdebt_dir}/lizardParser/lizard_output_{file_counter}.txt"
                print(f"output_file_path -- {output_file_path}")
                
                with open(output_file_path, "w") as output_file:
                    run_logged(
                        [
                            "lizard",
                            "--ignore_warnings",
                            "-1",
                            file
                        ],
                        log_dir=directories.log_dir,
                        cwd=directories.repository,
                        stdout=output_file
                    )
                file_counter += 1
                
               
        # Cloc parser
        with open(techdebt_dir / "lizard_cloc_output.txt", "w") as output_file:
            run_logged(
                [   "cloc",
                    "--quiet",
					"--by-file-by-lang", 
                    "--skip-uniqueness", 
                    "--csv", 
                    directories.repository
                ],
                log_dir=directories.log_dir,
                stdout=output_file,
            )