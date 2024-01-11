#!/usr/bin/env pwsh

<#
.SYNOPSIS
  Runs a Sema scan on the provided <RepoDir>, and outputs a .zip file in
  <OutDir>. This .zip file must be sent to Sema for further analysis.
#>

[CmdletBinding()]
param (
  # Run a Sema scan on this repository directory.
  [Parameter(Mandatory = $true, Position = 0, ParameterSetName = 'Default')]
  [ValidateNotNullOrEmpty()]
  [ValidateScript({ Test-Path $_ -PathType Container })]
  [string]
  $RepoDir,

  # Copy the output .zip file to this directory.
  [Parameter(Mandatory = $true, Position = 1, ParameterSetName = 'Default')]
  [ValidateNotNullOrEmpty()]
  [ValidateScript({ Test-Path $_ -PathType Container })]
  [string]
  $OutDir,

  # Use the specified Docker image tag. Defaults to "latest".
  [Parameter(ParameterSetName = 'Default')]
  [string]
  $Tag = 'latest',

  # Print this message.
  [Parameter(ParameterSetName = 'Help')]
  [Alias('h', '?')]
  [switch]
  $Help
)

#Requires -Version 5.1

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

if ($Help) {
  Get-Help $PSCommandPath -Detailed
  Exit
}

$dockerOs = docker version -f '{{.Server.Os}}'
if ($dockerOS -ne 'linux') {
  Write-Error 'Please make sure that Docker is installed, running, and is configured to run Linux containers.'
}

docker pull "ghcr.io/semalab/agent:$Tag"

docker run `
  --mount "type=bind,source=$(Resolve-Path $RepoDir),target=/repo,readonly" `
  --mount "type=bind,source=$(Resolve-Path $OutDir),target=/out" `
  "ghcr.io/semalab/agent:$Tag" --repository /repo --output /out
