FROM trino:372-SNAPSHOT-amd64
LABEL maintainer="detective"

COPY --chown=trino:trino etc /usr/local/trino/etc
EXPOSE 8081

WORKDIR /usr/local/trino

# Create data dir
RUN mkdir -p /usr/local/trino/data
VOLUME ["/usr/local/trino/data"]

ENTRYPOINT ["bash", "./scripts/trino.sh"]
# CMD ["/usr/lib/trino/bin/run-trino"]