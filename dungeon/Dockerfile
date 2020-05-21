FROM python:3.7-slim
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY . /code
WORKDIR /code
CMD uvicorn main:app --host 0.0.0.0 --port 8300 --reload