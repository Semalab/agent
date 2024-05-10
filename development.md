# Development

You will need to have these projects checked out as siblings of this project:

- backend-activitypersistence
- backend-commitanalysis
- backend-core
- backend-gitblame
- ai_engine

Additionally, you must have the AWS CLI installed and configured, to allow
downloading the tuned models for AI Engine from S3.

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

Note that this shell is actually run with the source mounted, rather than
copied, into the container. This means that you can run Poetry commands,
like for adding packages, in this shell.

To run only a subset of the scans, for faster testing during development, set
the `AGENT_ARGS` environment variable to a space-delimited list of lowercased
scan names:

```sh
 export AGENT_ARGS="linguist linters"
```

Note that the linters need the file list from the linguist step.
