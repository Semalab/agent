import logging

from .cloc import Cloc
from .lizard import Lizard
from .pmdcpd import PmdCpd

from agent.strategy.quality.linguist import Linguist

class TechDebt:
    """
    runs a variety of techdebt tools on the given repository
    """

    techdebt_per_repo = [
        Cloc(),
        PmdCpd()
    ]

    def run(self, directories):
        logger = logging.getLogger(__name__)

        techdebt_dir = directories.mkdir("techdebt")

        for tool in self.techdebt_per_repo:
            logger.info(f"Running tool: {tool.__class__.__name__}")
            tool.run(directories, techdebt_dir=techdebt_dir)

        linguist = Linguist()
        linguist_dir = directories.mkdir("linguist")

        lizard = Lizard()
        logger.info(f"Running tool: {lizard.__class__.__name__}")

        for file in linguist.files(directories, linguist_dir):
            lizard.run(file, directories, techdebt_dir=techdebt_dir)

        for t in techdebt_dir.glob("*.tmp"):
            t.unlink()
