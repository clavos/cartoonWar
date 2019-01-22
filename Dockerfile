FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install Pillow
RUN pip install django-bootstrap3
COPY . /code/
RUN python manage.py migrate