# Development

This is a python FastAPI app
built in the "clean architecture" style
(using functionally pure domain entities,
repository objects that encapsulate IO,
use-case classes that encapsulate business logic, etc).

See [DEPLOYMENT.md](DEPLOYMENT.md) for instructions on how to deploy this service

---

## Collaboration
We work in GitHub with a [github flow](https://guides.github.com/introduction/flow/),
and require all PR's to be reviewed before merging.
There are also guard-rails preventing merges
that violate test coverage or code style policies,
or failing tests.


## Coding Style guide

We use pre-commit hooks, including black, isort, flake8.

The suggested way to install these hooks it is by installing [pre-commit](https://pre-commit.com/),

then running `pre-commit install`

Note that on the first time you run `git commit`,
it's going to  take some time to install all the hooks,
but after that it will be fast.

## Local development

Everything is managed with `docker-compose`. The configuration for this is stored in
`local.yml`, so it can be convenient to set this in your shell first:
```
export COMPOSE_FILE=local.yml
```

1. `docker-compose build` - build everything
2. `docker-compose up -d` - run everything in daemon mode

There are two components:
2. API documentation (via uvicorn/FastAPI directly)
3. minio (mimics AWS lambda)


## Configuration
Default configuration is provided under `.envs/.local/`, which includes
everything required for the components to work together.

## Tests
Tests are managed with pytest, which can be executed with the shortcut make command:
```
make test
```

**A note about local resources:**

docker-compose will not auto-create S3 buckets in minio,
so this must be done manually first.
See the configuration in .envs/.local/.sls
to determine what buckets are needed.
