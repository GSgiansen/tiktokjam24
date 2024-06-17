FROM apache/airflow:2.7.0
COPY requirements.txt ./requirements.txt
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
