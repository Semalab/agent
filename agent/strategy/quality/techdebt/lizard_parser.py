from agent.utils import run_logged
from pathlib import Path
from agent.strategy.quality.linguist import Linguist

class lizardParser:

    

    def run(self, directories, techdebt_dir):
        
        """
        We need to run command - "git ls-tree --full-tree -r --name-only HEAD this.projectDir" to get the list of all files in the repository

        But the list of files is already being generated in the linguist class and stored at ".sema/linguist/git-ls-tree"

        Therefore, getting list of files from the linguist class and using it here
        
        May need to make a generic function for generating git outputs which can be used by all classes
        
        """
        
        # Fetch file list
        git_ls_file_path = directories.mkdir("linguist") / "git-ls-tree"

        # read the list of files from file
        with open(git_ls_file_path) as git_ls_tree_file:
            files = git_ls_tree_file.readlines()
 
        # Lizard Parser
        supportedLizardLanguages = ["c", "cpp", "cc", "mm", "cxx", "h", "hpp", "cs", "gd", "go", "java", "js",
        "lua", "m", "php", "py", "rb", "rs", "scala", "swift", "sdl", "ttcn", "ttcnpp", "ts"]

        with open(techdebt_dir / "lizard_output.txt", "w") as output_file:
            for file in files:

                file_extension = str(file.split(".")[-1]).strip()

                if file_extension in supportedLizardLanguages:
    
                    # logger.info(f"running command ~ lizard --ignore_warnings -1 {file}")

                    run_logged(
                        [
                            "lizard",
                            "--ignore_warnings",
                            "-1",
                            file.strip()
                        ],
                        log_dir=directories.log_dir,
                        cwd=directories.repository,
                        stdout=output_file
                    )

        # Cloc parser
        with open(techdebt_dir / "lizard_cloc.txt", "w") as output_file:
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