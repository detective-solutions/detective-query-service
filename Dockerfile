FROM python:3.8

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev unixodbc-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install -e .

CMD ["python", "src/detective_query_service/service/consumer.py" ]
