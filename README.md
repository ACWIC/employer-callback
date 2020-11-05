# Employer Admin API
[![codecov](https://codecov.io/gh/ACWIC/employer-callback/branch/main/graph/badge.svg?token=QYL43W2ELE)](https://codecov.io/gh/ACWIC/employer-callback/branch/main)
[![CircleCI](https://circleci.com/gh/ACWIC/employer-callback.svg?style=svg&circle-token=d8c23923ca82ad4e383eaca19010d69fa420f481)](https://circleci.com/gh/circleci/circleci-docs)

This is a reference implementation of a proposed API enabling Aged Care
providers to interact with training providers in a standardised way.


Specifically, it provides the endpoints for registering a proposed
enrolment and accessing information sent to the employer, by the
training provider.

This is a companion service to
- [Employer Callback](https://github.com/ACWIC/employer-callback)

[DEVELOPMENT.md](DEVELOPMENT.md) and [DEPLOYMENT.md](DEPLOYMENT.md)
contain information about running
the software and making changes to it.

There is a test endpoint with a self-documenting API specification

[Dev](https://ngkkz39vx8.execute-api.us-east-1.amazonaws.com/dev/cb/docs)
[Prod](https://prekb2sflh.execute-api.us-east-1.amazonaws.com/prod/cb/docs)

This is equivalent to what you will have running locally
if you create a local development environment
(per [DEVELOPMENT.md](DEVELOPMENT.md))

The test endpoint is continuously deployed from the `main` branch in this
repository, so should be considered unstable.
It is also completely open (do not require authentication),
which is not a realistic simulation of any kind of production environment.
