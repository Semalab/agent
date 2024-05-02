import json

from agent.utils import run_logged


class Lizard:
    supported_languages = ["c", "cpp", "cc", "mm", "cxx", "h", "hpp", "cs", "gd", "go", "java", "js",
                                "lua", "m", "php", "py", "rb", "rs", "scala", "swift", "sdl", "ttcn", "ttcnpp", "ts"]

    def run(self, path, directories, techdebt_dir):
        if any(ext == path.suffix[1:] for ext in self.supported_languages):
            output_path = techdebt_dir / "lizard.tmp"

            with open(output_path, "w+") as output_file:
                run_logged(
                    [
                        "lizard",
                        "--ignore_warnings",
                        "-1",
                        path
                    ],
                    log_dir=directories.log_dir,
                    cwd=directories.repository,
                    stdout=output_file
                )

                output_file.seek(0)

                # Save the output in JSON-Lines format
                # This avoids unbounded growth of the number of output files,
                # and can be read/written in a streaming fashion.
                with open(techdebt_dir / "lizard.txt", "a") as combined_file:
                    json.dump(
                        {
                            "filename": str(path.relative_to(directories.repository)),
                            "lizard": output_file.read()
                        }, combined_file)
                    combined_file.write("\n")
