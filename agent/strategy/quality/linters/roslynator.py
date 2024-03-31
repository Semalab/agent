import json
from pathlib import Path
import xml.etree.ElementTree as ET

from agent.utils import run_logged
from agent.strategy.quality.linguist import Linguist


class Roslynator:
    def run(self, directories, linters_dir):
        linguist = Linguist()
        files = [str(file)
                 for file in linguist.files(directories, directories.mkdir("linguist"))
                 if file.suffix.endswith((".sln", ".csproj", ".vbproj"))]

        output_path = linters_dir / "roslynator.xml"

        run_logged(
            [
                "roslynator",
                "analyze",
                "--analyzer-assemblies", (Path.home() / ".nuget" / "packages"),
                "--severity-level", "info",
                "--output", output_path
            ],
            log_dir=directories.log_dir,
            cwd=directories.repository,
            input="\n".join(files).encode()
        )

        if not output_path.is_file():
            return

        with open(linters_dir / "roslynator.json", "w") as json_file:
            root = ET.parse(output_path).getroot()

            json.dump(
                [{
                    "filename": str(Path(diag.find("FilePath").text).relative_to(directories.repository)),
                    "line_num": diag.find("Location").get("Line"),
                    "col_num": diag.find("Location").get("Character"),
                    "err_message": f'({diag.find("Severity").text}) {diag.find("Message").text}'
                } for diag in root.findall(".//Diagnostics/Diagnostic")],
                json_file
            )
