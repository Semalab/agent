from agent.strategy.quality.linters.cppcheck import CppCheck


class Linters:
    """
    runs a variety of linters on the given repository
    """

    LINTERS = [CppCheck()]

    def run(self, directories):
        linters_dir = directories.sema_output / "linters"
        linters_dir.mkdir()

        # TODO: parallelize
        for linter in self.LINTERS:
            linter.run(repository=directories.repository, linters_dir=linters_dir)
