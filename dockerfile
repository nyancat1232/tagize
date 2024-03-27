FROM python:3.12

WORKDIR /tagize

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
COPY main.py ./
COPY pre.py ./
COPY pyplus ./pyplus
COPY hashprocessor ./hashprocessor
COPY .streamlit ./.streamlit

RUN pip install -r requirements.txt

EXPOSE 8045

CMD [ "streamlit", "run", "--server.address=0.0.0.0", "--server.port=8045", "main.py"]