# Development

You will need to have these projects checked out as siblings of this project:

- backend-activitypersistence
- backend-commitanalysis
- backend-core
- backend-gitblame
- ai_engine

## Testing

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

To run only a subset of the scans, for faster testing during development, set
the `AGENT_ARGS` environment variable to a space-delimited list of lowercased
scan names:

```sh
 export AGENT_ARGS="linguist linters"
```

Note that the linters need the file list from the linguist step.
