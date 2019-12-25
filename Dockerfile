FROM python:3.8.0

WORKDIR /app
ENV GIOMON_DB_ADDRESS influx
ENV PYTHONUNBUFFERED 1
ADD requirements.txt .
RUN pip3 install -r requirements.txt
ADD . .

CMD ["/usr/local/bin/python3", "/app/monitor.py"]
