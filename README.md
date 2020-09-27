# Aged Care Provider Callback API

This is a FastAPI app that is built to run on AWS Lambda via the API Gateway.
It is deployed with the `serverless` tool, which manges dealing with AWS. It can
also run locally with `serverless-offline` in a mode which mimics API Gateway/lambda
infrastructure. This mode leverages local services like Minio as replacements for 
AWS resources like S3.

## Installation

Everything is managed with docker-compose. The configuration for this is stored in
`local.yml`, so it can be convenient to set this in your shell first:
```
export COMPOSE_FILE=local.yml
```

1. `docker-compose build` - build everything
2. `docker-compose up -d` - run everything in daemon mode

There are three components:
1. serverless
2. API documentation (via uvicorn/FastAPI directly)
3. minio

## Configuration

Default configuration is provided under `.envs/.local/`, which includes
everything required for the components to work together. These variables
are also used to configure the serverless stages (local, dev).

Serverless additionally needs AWS credentials in order to deploy. This can be provided
either automatically via the `~/.aws` home directory, which is mounted to the container
home directory, or via AWS environment variables provided in `.env`.

## Serverless

This component is used to containerise serverless build tooling. It is a python3.8 image
with node v12.x installed in order to run the serverless CLI tool. Serverless is responsible
for building and packaging the underlying python app, but also can serve a local version via
the `offline` command, which is the default command when bringin the container up.

The entrypoint for the container is `serverless`, so this container can be used to do most things
that the `serverless` CLI tool can.

The `serverless.yml` file is used to configure the CLI, and defines all of the endpoints,
resources, IAM policies and stages. The configuration file defines stages that map to
deployed stages (e.g. dev) as well as a local stage which is used to provide configuration
for serverless-offline.

### Running locally
```
docker-compose up -d serverless
```

This command will run the container in offline mode on port 3000, using `serverless-offline`.
This plugin mimics the API gateway and lambda context which the deployed code would operate
in, which is particularly helpful for debugging the interface between code and infrastructure.
The offline runner uses the API gateway configuration described in serverless.yml (the same that
is used to deploy with).

**A note about local resources**

Serverless will not auto-create S3 buckets in minio, so this must be done manually first.

### Deploying
```
docker-compose run --rm serverless deploy --stage dev
```

This command packages the app with configuration defined in the serverless dev stage. Serverless
will use AWS credentials in one of two locations:
- in the user's aws directory `~/.aws`
- a `.env` with the following variables defined:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`


## Tests

Tests are run with pytest, which can be executed with the following command:
```
docker-compose run --rm test
```
