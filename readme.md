# Agent

## Usage
Run the script using `poetry run cli`:
```
Usage: agent [OPTIONS] REPOSITORY

  Run local scan on REPOSITORY.

Options:
  -o, --output TEXT  output zip filename
  --help             Show this message and exit.
```

## Building
To build for windows and/or linux.
```
make windows
make linux
```
This will produce executables that appear under `dist/`. To test these executables
use `./scripts/run-bin.sh`:
```
./scripts/run-bin.sh windows <args>
./scripts/run-bin.sh linux <args>
```
