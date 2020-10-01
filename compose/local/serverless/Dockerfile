FROM python:3.8.5-alpine

RUN apk update \
    # node12, npm depedencies
    && apk add nodejs npm \
    # (python)magnum:cryptography dependencies
    && apk add gcc musl-dev python3-dev libffi-dev openssl-dev


# Install global serverless
RUN npm install -g serverless

# Ensure terminal output is sent directly to logs
ENV PYTHONBUFFERED 1

# Install requirements
COPY ./requirements /requirements
RUN pip install -r /requirements/serverless.txt

# Copy scripts
COPY ./compose/local/serverless/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
