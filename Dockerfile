FROM python:3.7.2-alpine

RUN mkdir -p /usr/src/ddns
WORKDIR /usr/src/ddns

COPY requirements.txt .
RUN pip install -r requirements.txt -y

CMD ["python", "ddns.py"]