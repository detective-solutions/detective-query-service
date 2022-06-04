
#
# This docker image is for launching test purpose trino cluster.
#

FROM openjdk:11-slim
LABEL maintainer="detective"

ENV TRINO_VERSION=380
ENV TRINO_HOME=/usr/local/trino
ENV BASE_URL=https://repo1.maven.org/maven2

# install dev tools
RUN apt-get update
RUN apt-get install -y \
    curl \
    tar \
    sudo \
    rsync \
    python \
    wget \
    python3-pip \
    python-dev \
    build-essential \
    uuid-runtime \
    less

RUN pip install jinja2

ENV JAVA_HOME /usr/java/default
ENV PATH $PATH:$JAVA_HOME/bin

# Add trino-cli
WORKDIR /usr/local/bin
RUN wget -q ${BASE_URL}/io/trino/trino-cli/${TRINO_VERSION}/trino-cli-${TRINO_VERSION}-executable.jar
RUN chmod +x trino-cli-${TRINO_VERSION}-executable.jar
RUN mv trino-cli-${TRINO_VERSION}-executable.jar trino-cli

WORKDIR /usr/local
# ADD trino-server-${TRINO_VERSION}.tar.gz /usr/local
RUN wget -q ${BASE_URL}/io/trino/trino-server/${TRINO_VERSION}/trino-server-${TRINO_VERSION}.tar.gz
RUN tar xvzf trino-server-${TRINO_VERSION}.tar.gz -C /usr/local/
RUN ln -s /usr/local/trino-server-${TRINO_VERSION} $TRINO_HOME

ADD scripts ${TRINO_HOME}/scripts

# Create data dir
RUN mkdir -p $TRINO_HOME/data
VOLUME ["$TRINO_HOME/data"]