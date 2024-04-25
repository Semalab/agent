from agent.strategy.quality.techdebt.cloc_parser import ClocParser


class TechDebt:
    """
    runs a variety of techdebt tools on the given repository
    """

    techdebt_parsers = [
        ClocParser()
    ]

    def run(self, directories):
        techdebt_dir = directories.mkdir("techdebt")

        for parser in self.techdebt_parsers:
            parser.run(directories, techdebt_dir=techdebt_dir)
