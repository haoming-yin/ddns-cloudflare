FROM python:3.7.2-alpine

RUN mkdir -p /usr/src/ddns
WORKDIR /usr/src/ddns

RUN apk update && apk add --virtual build-dependencies build-base gcc

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apk del build-dependencies

COPY . .

CMD ["python", "ddns.py"]