FROM python:3.11

WORKDIR /tagize

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
COPY main.py ./
COPY .streamlit ./.streamlit

RUN pip install -r requirements.txt

EXPOSE 8045

CMD [ "streamlit", "run", "--server.address=0.0.0.0", "--server.port=8045", "main.py"]