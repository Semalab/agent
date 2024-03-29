from agent.strategy.quality.linters.cppcheck import CppCheck
from agent.strategy.quality.linters.flawfinder import FlawFinder
from agent.strategy.quality.linters.pmd import PMD


class Linters:
    """
    runs a variety of linters on the given repository
    """

    LINTERS = [
        CppCheck(),
        FlawFinder(),
        PMD()
    ]

    def run(self, directories):
        linters_dir = directories.mkdir("linters")

        # TODO: parallelize
        for linter in self.LINTERS:
            linter.run(directories, linters_dir=linters_dir)
