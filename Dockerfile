FROM python:3.8

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install -e .

EXPOSE 7798

CMD ["python", "src/detective_query_service/service/consumer.py" ]