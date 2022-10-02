FROM python:3.10-slim@sha256:7e8d32d9e8c20a3626146a932ecf98c3fc2a4b1100b008193b835acc2ab88018

ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1

# Add non-root user
RUN groupadd detective && \
    useradd -r --no-create-home detective -g detective

# Handle folder permissions
RUN mkdir /app && chown detective:detective /app
WORKDIR /app

# Install external dependencies separately (can be cached)
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY --chown=detective:detective . .

RUN pip install -e . && \
    rm requirements.txt

# Run application as non-root user
USER detective

CMD python ./src/detective_query_service/service/consumer.py
