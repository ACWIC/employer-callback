import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.enrolments import router as v1_router

API_GATEWAY_STAGE_PREFIX = os.environ.get("STAGE_PREFIX", default="")
API_GATEWAY_SERVICE_PREFIX = os.environ.get("SERVICE_PREFIX", default="")

app = FastAPI(
    title="Enrolments API",
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
