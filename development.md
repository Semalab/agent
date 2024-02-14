# Development

For testing the agent locally, [Makefile](./Makefile) has some convenience scripts.

For a full test run, which will first build the Docker image locally:

```sh
export AGENT_REPO=../path/to/test/repo
export AGENT_OUT=../temp
make
```

To just get a shell into the container, without running a scan:

```sh
make shell
```
