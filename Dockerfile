FROM python@sha256:850b7f7626e5ca9822cc9ac36ce1f712930d8c87eb31b5937dba4037fe204034

RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev unixodbc-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .
RUN rm requirements.txt

CMD python ./src/detective_query_service/service/consumer.py
