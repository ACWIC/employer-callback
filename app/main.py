"""
This API is used by Training Providers
to send information to Aged Care Providers ("employers")
about the delivery of training services.
It is called *Employer Callback*
(rather than *Training Provider Callback*)
because the service is operated by the Employer.

The current implementation allows Training Provider
to send arbitary messages.


This employer-callback microservice is used
in conjunction with the employer-admin microservice.
Together, these two microservices can be deployed
by an Aged Care Provider as a proxy for
interactions with one or many Training Providers.
Examples of how to deploy this microservice
(along with the employer-admin)
are documented in the
[Aged Care Provider Integration Guide](https://acwic-employer-coordinator.readthedocs.io).

The reference implementation for this microservice
is open source and avilable at the
[ACWIC GitHub site](https://github.com/acwic/employer-callback).
"""
import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.callbacks import router as v1_router

API_GATEWAY_STAGE_PREFIX = os.environ.get("STAGE_PREFIX", default="")
API_GATEWAY_SERVICE_PREFIX = os.environ.get("SERVICE_PREFIX", default="")

app = FastAPI(
    title="Employer Callback",
    description=__doc__,
    root_path=API_GATEWAY_STAGE_PREFIX,
    openapi_url=API_GATEWAY_SERVICE_PREFIX + "/openapi.json",
    docs_url=API_GATEWAY_SERVICE_PREFIX + "/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix=API_GATEWAY_SERVICE_PREFIX)

if __name__ == "__main__":
    # TODO: could be moved into a separate docs-specific entrypoint as
    # this is only called to run docs
    import uvicorn

    uvicorn.run(app)
