# Development

This is a python FastAPI app
built in the "clean architecture" style
(using functionally pure domain entities,
repository objects that encapsulate IO,
use-case classes that encapsulate business logic, etc).

See DEPLOYMENT.md for instructions on running
a local development environment using docker-compose

We work in GitHub with a pull-request workflow,
and require all PR's to be reviewd before merging.
There are also guard-rails preventing merges
that violate test coverage or code style policies,
or failing tests.


## Tests

Tests are run with pytest, which can be executed with the shortcut make command:
```
make test
```

TODO: include pre-commit checks in make-test


## Style guide

We use pre-commit hooks, including black, isort, flake8.

The suggested way to install these hooks it is by installing [pre-commit](https://pre-commit.com/), 

then running 
`pre-commit install`

Note that on the first time you run `git commit`,
it's going to  take some time to install all the hooks,
but after that it will be fast.
