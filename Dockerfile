FROM python:3.8.0-slim

WORKDIR /app
ENV GIOMON_DB_ADDRESS influx
ADD requirements.txt .
RUN pip3 install -r requirements.txt
ADD monitor.py .

CMD /usr/local/bin/python3 /app/monitor.py
