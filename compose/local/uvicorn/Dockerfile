FROM python:3.8.5-alpine

# uvicorn/uvloop need make
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev make

# Ensure terminal output is sent directly to logs
ENV PYTHONBUFFERED 1

# Install requirements
COPY ./requirements /requirements
RUN pip install -r /requirements/uvicorn.txt

# Copy scripts
COPY ./compose/local/uvicorn/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

WORKDIR /app

# ENTRYPOINT ["/entrypoint"]
