# Employer Callback API

This is a reference implementation of a proposed API
enabling Training Providers to interact with Aged Care Providers
(employers) in a standardised way.

Specifically, it provides the endpoints for sending information
to the employer, to be used by the training provider.

This is a companion service to https://github.com/ACWIC/employer-admin

Detailed technical documentation is in the docs/ folder.
DEPLOYMENT.md and DEVELOPMENT.md contain information about running
the software and making changes to it.

There is a test endpoint
with a self-documenting API specification here:

* https://izu2v5346l.execute-api.us-east-1.amazonaws.com/dev/cb/docs

This is equivalent to what you will have running locally
if you create a local development environment
(per DEPLOYMENT.md)

The test endpoint is continuously deployed
from the `main` branch in this repository,
so should be considered unstable.
It is also completely open
(do not require authentication),
which is not a realistic simulation
of any kind of production environment.
