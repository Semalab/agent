@echo off
powershell.exe -ExecutionPolicy Bypass -File "%~dp0\agent.ps1" %*
