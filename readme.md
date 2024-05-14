# Sema Agent

The agent scans a provided repository and generates a `.zip` file with analytics
that must be sent to Sema to be analyzed further.  This file may contain things
such as potential CVEs, dependencies, licenses, etc. This file does not, however,
contain any source code.

## Prerequisites

1. Docker must be installed and running. If using Windows, install [Docker Desktop][1]
   and configure it to use Linux containers.
2. Currently, the agent only supports repositories versioned with Git.
   - If your repository is versioned with SVN, the agent will attempt to convert
     this to a git repository. The agent will attempt to access your SVN repository
     using [`git svn`][2].
   - If your repository is versioned with something other than Git or SVN, you must
       first convert it to Git.
3. You must also have `curl` installed. On Windows, `curl.exe` is now included with
   Windows 10/11; if your system does not include it, you can [download][3] and
   install it.
4. You should have received a file named `download-url.txt` from Sema.

## Usage

Clone your repository to a local directory:

```sh
git clone https://github.com/Semalab/agent.git
```

Copy the `download-url.txt` file to the `agent` directory.

Run agent:

```sh
./scripts/agent [-h] <repository> <output-directory>
```

This command will work on macOS, Linux, and Windows (in PowerShell.) If using
`cmd`/Command Prompt on Windows, replace the slashes (`/`) with backslashes (`\`).

Use the `-h` argument for help.

On Windows, if you see an error about being unable to run agent.ps1 because of
the execution policy, run this command before the agent script:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process
```

### Email Generated Zip File

After running these commands, a zip file will have been created under the
specified output directory. Please send this file to [customers@semasoftware.com](mailto:customers@semasoftware.com)
to complete the analysis.

[1]: https://www.docker.com/products/docker-desktop/
[2]: https://git-scm.com/docs/git-svn
[3]: https://curl.se/windows/
