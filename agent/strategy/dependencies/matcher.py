import fnmatch
import functools
import re

# constructed by looking at `rg globsForDefinitionFiles` from within the ort repo,
# https://github.com/oss-review-toolkit/ort
PATTERNS = {
    "stack": ["stack.yaml"],
    "node": ["package.json", "pnpm-lock.yaml"],
    "spdxdocumentfile": ["*.spdx.yml", "*.spdx.yaml", "*.spdx.json"],
    "cocoapods": ["Podfile"],
    "bundler": ["Gemfile"],
    "conan": ["conanfile*.txt", "conanfile*.py"],
    "carthage": ["Cartfile.resolved"],
    "nuget": ["*.csproj", "*.fsproj", "*.vcxproj", "packages.config"],
    "composer": ["composer.json"],
    "cargo": ["Cargo.toml"],
    "pip": ["*requirements*.txt", "setup.py"],
    "pipenv": ["Pipfile.lock"],
    "poetry": ["poetry.lock"],
    "bower": ["bower.json"],
    "gomod": ["go.mod"],
    "maven": ["pom.xml"],
    "sbt": ["build.sbt", "build.scala"],
    "pub": ["pubspec.yaml", "pubspec.lock"],
    "godep": ["Gopkg.toml", "glide.yaml", "glide.lock", "Godeps.json"],
    "gradle": [
        "build.gradle",
        "build.gradle.kts",
        "settings.gradle",
        "settings.gradle.kts",
    ],
}


@functools.cache
class Matcher:
    regexes: dict[str, list[re.Pattern]]

    def __init__(self):
        self.regexes = {
            manager: [re.compile(fnmatch.translate(pattern)) for pattern in patterns]
            for manager, patterns in PATTERNS.items()
        }

    def matches_any(self, text: str):
        """
        returns True if the provided text matches any of the `self.regexes`.
        """
        for regexes in self.regexes.values():
            for regex in regexes:
                if regex.match(text):
                    return True

        return False
