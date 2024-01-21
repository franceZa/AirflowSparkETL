FROM apache/airflow:2.7.1-python3.11

USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y python3-dev && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y procps && \
    apt-get install -y ant && \
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

USER airflow

RUN pip install --upgrade pip
RUN pip install --no-cache-dir apache-airflow apache-airflow-providers-apache-spark 
#pyspark==3.3.0