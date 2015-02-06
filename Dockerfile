FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements /code/requirements
RUN pip install -r /code/requirements/dev.txt

