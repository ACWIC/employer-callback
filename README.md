# Employer Callback API
[![codecov](https://codecov.io/gh/ACWIC/employer-callback/branch/main/graph/badge.svg?token=QYL43W2ELE)](https://codecov.io/gh/ACWIC/employer-callback/branch/main)
[![CircleCI](https://circleci.com/gh/ACWIC/employer-callback.svg?style=svg&circle-token=d8c23923ca82ad4e383eaca19010d69fa420f481)](https://circleci.com/gh/circleci/circleci-docs)

This is a reference implementation of a proposed API enabling Aged Care
providers to interact with training providers in a standardised way.
Specifically, it provides the endpoints that Aged Care Providers
(employers) use to receive data from Training Prividers,
in relation to specific enrolments.

See the Swagger API documentation:

* [Development version](https://ngkkz39vx8.execute-api.us-east-1.amazonaws.com/dev/cb/docs)
* [Preview version](https://prekb2sflh.execute-api.us-east-1.amazonaws.com/prod/cb/docs)

This is a companion service to
- [Employer Admin](https://github.com/ACWIC/employer-admin)

Overall pattern of use:

1. Enrolments are created by the Aged Care Provider
   (employer) using Employer Admin API
2. payments occur out-of-band
   (or an existing credit arangements is used)
3. **Training Providers use this Callback API
   to send data to the employer**
   about progres of this specific enrolment.
4. Aged Care Providers query information
   about the delivery of training service
   using the Employer Admin API

See the files:

* [DEPLOYMENT.md](DEPLOYMENT.md) for information about running this software
* [DEVELOPMENT.md](DEVELOPMENT.md) for information about changing this software

The Development version is continuously deployed
from the `main` branch in this repository,
so should be considered unstable.
It is also completely open (do not require authentication),
which is not a realistic simulation of any kind of production environment.

For more information about running this service, see the
[Aged Care Provider Integration Guide](https://acwic-employer-coordinator.readthedocs.io).
