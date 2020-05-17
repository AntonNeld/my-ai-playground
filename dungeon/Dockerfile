FROM python:3.7-alpine
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY . /code
CMD python /code/main.py