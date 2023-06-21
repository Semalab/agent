import os
import shutil

from agent.strategy.oss.dependencies.matcher import Matcher


class Dependencies:
    """
    copies all package management files from `directories.repository` into
    `directories.output` reproducing their original file structure.
    """

    def run(self, directories):
        matcher = Matcher()
        paths = []

        for root, _, files in os.walk(directories.repository):
            for filename in files:
                if matcher.matches_any(filename):
                    abspath = os.path.join(root, filename)
                    paths.append(abspath)

        for abssrc in paths:
            relsrc = os.path.relpath(abssrc, start=directories.repository)
            absdst = os.path.join(directories.output, relsrc)

            os.makedirs(os.path.dirname(absdst), exist_ok=True)
            shutil.copy(abssrc, absdst)
