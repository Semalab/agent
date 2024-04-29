from agent.utils import run_logged
import os

class GBOM:
    """
    runs AI Code monitor on given directories
    """

    def move_output_file(self,source_dir, output_path: str):
        import shutil
        source_dir= os.path.dirname(source_dir)
        for filename in os.listdir(source_dir):
            if filename.endswith('.csv'):
                # Create the full file paths
                source_file = os.path.join(source_dir, filename)
                destination_file = os.path.join(output_path, filename)
                # Move the file to the destination directory
                shutil.move(source_file, destination_file)
                print(f"Moved '{filename}' to '{output_path}'")
        

    def run(self, directories):
        curr_work_dir= os.getcwd()
        os.chdir("./agent/strategy/ai_engine/ai_engine/")
        run_logged(
            [
                "python",
                "main.py",
                directories.repository,
            ],
            log_dir=directories.log_dir
        )
        os.chdir(curr_work_dir)
        self.move_output_file(directories.repository, directories.mkdir("GBOM"))
    
