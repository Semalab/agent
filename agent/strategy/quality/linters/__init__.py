import logging

from .cppcheck import CppCheck
from .flawfinder import FlawFinder
from .pmd import PMD
from .pylint import Pylint
from .rubocop import RuboCop
from .jshint import JSHint
from .eslint import ESLint
from .roslynator import Roslynator
from .swiftlint import SwiftLint


class Linters:
    """
    runs a variety of linters on the given repository
    """

    LINTERS = [
        CppCheck(),
        FlawFinder(),
        PMD(),
        Pylint(),
        RuboCop(),
        JSHint(),
        ESLint(),
        Roslynator(),
        SwiftLint()
    ]

    def run(self, directories):
        logger = logging.getLogger(__name__)

        linters_dir = directories.mkdir("linters")

        # TODO: parallelize
        for linter in self.LINTERS:
            logger.info(f"Running linter: {linter.__class__.__name__}")
            linter.run(directories, linters_dir=linters_dir)
