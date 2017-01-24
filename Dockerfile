FROM python:3

# RUN apk update && apk add bash sqlite

RUN mkdir -p /usr/local/speedcontrol
RUN mkdir -p /usr/local/venvs

COPY . /usr/local/speedcontrol

WORKDIR /usr/local/speedcontrol

RUN pip install pip==9.0.1 virtualenv honcho
RUN pip install -r /usr/local/speedcontrol/requirements.txt
RUN ./manage.py makemigrations --merge --noinput
RUN ./manage.py migrate

EXPOSE 8000

ENTRYPOINT honcho start
CMD bash
