FROM python:3.10-slim

WORKDIR /app

COPY . .
COPY airflow.cfg ~/airflow/airflow.cfg
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN pip install apache-airflow==2.8.1
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y supervisor

EXPOSE 5000
EXPOSE 5001

CMD ["/usr/bin/supervisord"]
