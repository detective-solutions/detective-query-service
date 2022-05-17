FROM detective/trino-base
LABEL maintainer="detective"

COPY etc /usr/local/trino/etc
EXPOSE 8081

WORKDIR /usr/local/trino
ENTRYPOINT ["bash", "./scripts/trino.sh"]