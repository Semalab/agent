from agent.strategy.quality.techdebt.cloc_parser import ClocParser
from agent.strategy.quality.techdebt.pmdcpd_parser import PmdCpdParser

class TechDebt:
    """
    runs a variety of techdebt tools on the given repository
    """

    techdebt_parsers = [
        ClocParser(),
        PmdCpdParser()
    ]

    def run(self, directories):
        techdebt_dir = directories.mkdir("techdebt")

        for parser in self.techdebt_parsers:
            parser.run(directories, techdebt_dir=techdebt_dir)
