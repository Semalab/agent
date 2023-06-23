function Print-Usage {
  Write-Host "Usage: agent.ps1 <repository> <output-directory>"
  Write-Host ""
  Write-Host "Runs a Sema scan on the provided <repository>, and outputs a .zip file in"
  Write-Host "<output-directory>. This .zip file must be sent to Sema for further analysis."
  Write-Host ""
  Write-Host "Options:"
  Write-Host "  -h, --help        Print this message."
}

function Check-Usage($arg1, $arg2) {
  if ($arg1 -eq "-h" -or $arg1 -eq "--help") {
    Print-Usage

    exit
  }

  if ($arg1 -eq $null -or $arg2 -eq $null) {
    Write-Host "Expected 2 arguments."
    Write-Host ""
    Print-Usage

    exit 1
  }

  # check that arguments are valid directories
  foreach ($DIR in $arg1, $arg2) {
    if (-not (Test-Path $DIR -PathType Container)) {
      Write-Host "'$DIR' is not a directory."
      Write-Host ""
      Print-Usage

      exit 1
    }
  }
}

function Main {
  param($repo, $out)

  Check-Usage $repo $out

  docker build -t sema-agent -f ./docker/Dockerfile ./

  docker run `
    --mount "type=bind,source=$(Resolve-Path $repo),target=/repo,readonly" `
    --mount "type=bind,source=$(Resolve-Path $out),target=/out" `
    sema-agent --repository /repo --output /out
}

Main @args
