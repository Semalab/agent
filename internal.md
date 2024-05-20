# Using Agent internally at Sema

When AWS credentials are available to access internal resources, the
`./scripts/agent` script will automatically download the latest release. You
can specify a development branch to use with the `-t SQ-xxxx` argument as
usual; this will work provided the GitHub Actions workflow has succeeded for
that branch.

## Providing download links to customers

Clone this repository and run this command:

```sh
make presign
```

This will create a file called `download-url.txt` in the `out` directory. You
can send this file to customers, who will then need to copy the file to the
cloned `agent` directory, as explained in the readme.

This command accepts some optional parameters:

```sh
make presign AGENT_VERSION=main EXPIRES_IN_DAYS=7
```

- `AGENT_VERSION`: you will usually not need to specify anything other than
  `main`. This represents the latest released version of Agent.
- `EXPIRES_IN_DAYS`: the generated download link expires in 7 days, by default.
  Change this number to specify a different expiration window.
