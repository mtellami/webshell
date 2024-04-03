FROM python:3.11

WORKDIR /home/python/app
COPY . .
RUN pip install pipenv
RUN pipenv sync

EXPOSE 8000

CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
