FROM python:3.10-buster

WORKDIR "/"

COPY requirements.txt /cubebot/requirements.txt
RUN pip install -r /cubebot/requirements.txt
COPY . /

CMD ["python3", "-m", "bot"]
