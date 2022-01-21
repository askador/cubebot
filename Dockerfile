FROM python:3.10-slim-buster

WORKDIR "/cubebot"

COPY requirements.txt /cubebot/requirements.txt
RUN pip install -r /cubebot/requirements.txt
COPY . /cubebot/

CMD ["python3", "/cubebot/__main__.py"]
