import os
import shutil

from agent.strategy.dependencies.matcher import Matcher
from agent.strategy.strategy import Strategy


class Dependencies(Strategy):
    """
    copies all package management files from self.repository into self.output
    in the same file structure they were discovered
    """

    def run(self):
        matcher = Matcher()
        paths = []

        for root, _, files in os.walk(self.repository):
            for filename in files:
                if matcher.matches_any(filename):
                    abspath = os.path.join(root, filename)
                    paths.append(abspath)

        for abssrc in paths:
            relsrc = os.path.relpath(self.repository, abspath)
            absdst = os.path.join(self.sema_output, relsrc)

            os.makedirs(os.path.dirname(absdst), exist_ok=True)
            shutil.copy(abssrc, absdst)
