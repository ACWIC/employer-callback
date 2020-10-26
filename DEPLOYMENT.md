# Deployment

This is a python FastAPI app that is built to run on AWS Lambda
via the API Gateway.
It should also be able to run on other platforms
(such as MS Azure, or any platform supporting docker containers)
although those are not currently being actively tested
by the development team.

Deployments are managed with the `serverless` tool,
which manges dealing underlying platform.

For first time installation, you have to use the coordination service
[here](https://github.com/ACWIC/employer-coordinator)

it's responsible for installing everything on AWS for the first time.
It's also responsible for creating S3 buckets needed for this service to run.


## Continuous Delivery
After the first deployment, you can either enable the CI/CD pipeline using
the provided `.circleci` configuration or you can deploy manually using
the commands in `Makefile` file.

The command `make deploy_lambda` deploys your local
version directly to AWS lambda.

## Configuration:

#### AWS CLI:
to be able to use serverless or `make deploy_lambda` commands, you need to have
the aws cli set up locally, with an AWS default profile enabled.
You can consult the AWS configuration for more details.

There's two expected environment variables [managed by serverless on AWS]:

`STAGE_PREFIX`: API gateways add a prefix after the domain, but it's not passed down to the service.
But if the service is called from a Javascript application like swagger UI, the prefix has be provided.
`STAGE_PREFIX` should is expected to be provided by the serverless runner.


`SERVICE_PREFIX`: When deploying more than one service under the same API gateway, a prefix is used to
map to each service. this prefix is passed to the service itself, and all URLs are expected to be prepended
with it. (unlike the `STAGE_PREFIX`)

Note that all both variables are managed and provided from serverless, and you don't need to think about them
during development.
