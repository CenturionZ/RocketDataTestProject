FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/TestProject

COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/TestProject/

EXPOSE 8000
ENTRYPOINT python manage.py migrate
#CMD ["docker", "run", "-it", "--rm", "--name", "rabbitmq", "-p", "5672:5672", "-p", "15672:15672", "rabbitmq:3.9-management"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "createsuperuser", "boss", "boss@gmail.com", "boss", "boss", "y"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]