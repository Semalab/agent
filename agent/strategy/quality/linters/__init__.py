import logging
import time

from .cppcheck import CppCheck
from .flawfinder import FlawFinder
from .pmd import PMD
from .pylint import Pylint
from .rubocop import RuboCop
from .jshint import JSHint
from .eslint import ESLint
from .jslinters import JSLinters
from .roslynator import Roslynator
from .swiftlint import SwiftLint
from .tailor import Tailor
from .tslint import TSLint

from agent.strategy.quality.linguist import Linguist

# Show a progress update every few seconds
REPORT_INTERVAL = 60

class Linters:
    """
    runs a variety of linters on the given repository
    """


    cppcheck = CppCheck()
    flawfinder = FlawFinder()
    pmd = PMD()
    pylint = Pylint()
    rubocop = RuboCop()
    jshint = JSHint()
    eslint = ESLint()
    jslinters = JSLinters()
    roslynator = Roslynator()
    swiftlint = SwiftLint()
    tailor = Tailor()
    tslint = TSLint()

    LINTERS = [
        cppcheck,
        flawfinder,
        pmd,
        pylint,
        rubocop,
        jshint,
        eslint,
        swiftlint
    ]

    def run(self, directories):
        logger = logging.getLogger(__name__)
        last_report_time = time.monotonic()
        count = 0

        linters_dir = directories.mkdir("linters")

        # TODO: parallelize

        # To revert to linting the entire repo in one go:
        # (Note that Roslynator will still need to be fed paths to .sln/.csproj/.vbproj)
        # for linter in self.LINTERS:
        #     logger.info(f"Running linter: {linter.__class__.__name__}")
        #     linter.run(".", directories, linters_dir=linters_dir)

        linguist = Linguist()
        linguist_dir = directories.mkdir("linguist")

        for file in linguist.files(directories, linguist_dir):
            linters = []

            match file.suffix.lower():  # noqa: F999
                case ".java":
                    linters = [self.pmd]
                case ".cpp":
                    linters = [self.cppcheck, self.flawfinder]
                case ".py":
                    linters = [self.pylint]
                case ".swift":
                    linters = [self.tailor]
                case ".js":
                    linters = [self.jslinters]
                case ".ts":
                    linters = [self.tslint]
                case ".rb":
                    linters = [self.rubocop]
                case ".sln":
                    linters = [self.roslynator]

            for linter in linters:
                linter.run(file, directories, linters_dir=linters_dir)

            count += 1
            if time.monotonic() - last_report_time > REPORT_INTERVAL:
                logger.info(f"Processed {count} files")
                last_report_time = time.monotonic()

        for t in linters_dir.glob("*.tmp"):
            t.unlink()

