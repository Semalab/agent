from agent.strategy.quality.techdebt.lizard_parser import lizardParser


class TechDebt:
    """
    runs a variety of techdebt tools on the given repository
    """

    techdebt_parsers = [
                        lizardParser()
                    ]

    def run(self, directories):
        techdebt_dir = directories.mkdir("techdebt")

        for parser in self.techdebt_parsers:
            parser.run(directories, techdebt_dir=techdebt_dir)