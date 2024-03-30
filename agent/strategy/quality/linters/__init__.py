from .cppcheck import CppCheck
from .flawfinder import FlawFinder
from .pmd import PMD
from .pylint import Pylint
from .rubocop import RuboCop
from .jshint import JSHint
from .eslint import ESLint


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
        ESLint()
    ]

    def run(self, directories):
        linters_dir = directories.mkdir("linters")

        # TODO: parallelize
        for linter in self.LINTERS:
            linter.run(directories, linters_dir=linters_dir)
