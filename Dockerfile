FROM python@sha256:1b5da60b78075e88141b5d61bbb29e0d312c1029f9932628e1ccad35ac852956

RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .
RUN rm requirements.txt

CMD python ./src/detective_query_service/service/consumer.py