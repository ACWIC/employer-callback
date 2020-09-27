import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.enrolments import router as v1_router

app = FastAPI(
    title='Enrolments API',
    openapi_prefix=os.environ.get('STAGE_PREFIX') or ''
)

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)

if __name__ == '__main__':
    # TODO: could be moved into a separate docs-specific entrypoint as
    # this is only called to run docs
    import uvicorn
    uvicorn.run(app)
