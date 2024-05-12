FROM python:3.11-slim

RUN apt-get update
RUN apt-get install -y git

WORKDIR /app

COPY req.txt .

RUN pip install -r req.txt


COPY . .

# RUN pip install git+https://github.com/Myortv/fastapi-plugins.git@dev


CMD [ "python3", "main.py" ]
