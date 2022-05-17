FROM detective/trino-base
LABEL maintainer="detective"

ADD etc /usr/local/trino/etc

EXPOSE 8080

WORKDIR /usr/local/trino

ENTRYPOINT ["bash", "./scripts/trino.sh"]