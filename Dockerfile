# Dockerfile

# pull the official docker image
FROM python:3.10.8

RUN mkdir api
# set work directory
WORKDIR /api

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

CMD python src/main.py