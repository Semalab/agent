# Sema Agent

The agent scans a provided repository and generates a `.zip` file with analytics
that must be sent to Sema to be analyzed further.  This file may contain things
such as potential CVEs, dependencies, licenses, etc. This file does not, however,
contain any source code.

## Prerequisites

1. Docker must be installed. If using Windows, install [Docker Desktop][1].
2. Currently, the agent only supports repositories versioned with Git.
   - If your repository is versioned with SVN, the agent will attempt to convert
     this to a git repository. The agent will attempt to access your SVN repository
     using [`git svn`][2].
   - If your repository is versioned with something other than Git or SVN, you must
       first convert it to Git.

## Usage

Clone your repository to a local directory then, dependending on your operating
system, follow one of the following instructions:

### macOS / Linux
```
./scripts/agent.sh <repository> <output-directory>
```

### Windows
> **Warning**
> This script doesn't actually exist yet, but this is likely what the invocation
> will look like:
```
./scripts/agent.ps1 <repository> <output-directory>
```

[1]: https://www.docker.com/products/docker-desktop/
[2]: https://git-scm.com/docs/git-svn
