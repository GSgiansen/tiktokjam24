FROM apache/airflow:2.9.2-python3.10
# RUN apt-get update
# ENV HNSWLIB_NO_NATIVE=1
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
RUN pip3 install langchain-chroma
RUN pip install langchain
RUN pip install langchain-openai
RUN pip install langchain-core
RUN pip install langchain-community
RUN pip install langchain-text-splitters
