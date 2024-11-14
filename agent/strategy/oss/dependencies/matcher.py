import fnmatch
import functools
import re

# constructed by looking at `rg globsForDefinitionFiles` from within the ort repo,
# https://github.com/oss-review-toolkit/ort
PATTERNS = {
    "Gulp (not ORT)": ["gulpfile.js"],
    "ant (not ORT)": ["build.xml"],
    "Rake (not ORT)": ["Rakefile"],
    "setuptools (not ORT)": ["setup.cfg"],
    "stack": ["stack.yaml"],
    "npm": ["package.json", "pnpm-lock.yaml"],
    "spdxdocumentfile": ["*.spdx.yml", "*.spdx.yaml", "*.spdx.json"],
    "cocoapods": ["Podfile"],
    "bundler": ["Gemfile", "Gemfile.lock"],
    "conan": ["conanfile*.txt", "conanfile*.py"],
    "carthage": ["Cartfile.resolved"],
    "nuget": ["*.csproj", "*.fsproj", "*.vcxproj", "packages.config", "project.lock.json", "project.assets.json", "packages.lock.json"],
    "composer": ["composer.json"],
    "cargo": ["Cargo.toml", "Cargo.lock"],
    "pip": ["*requirements*.txt", "setup.py"],
    "pipenv": ["Pipfile.lock"],
    "poetry": ["poetry.lock", "pyproject.toml"],
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
    "yarn": ["yarn.lock"], 
    "CMake": ["CMakeLists.txt"],
    "yarn2": [".yarnrc.yml"],  
    "Cargo": ["Cargo.lock", "Cargo.toml"],
    "RubyGems": ["*.gemspec"],
    "swift": ["Package.swift"],
    "Bower": ["bower.json"],
    "Swift Package Manager": ["Package.swift"],
    "Dep": ["Gopkg.toml", "Gopkg.lock"],
    "Go Vendor": ["vendor/vendor.json"],
    "Conan": ["conanfile.txt", "conanfile.py"],
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
