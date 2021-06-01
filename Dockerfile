FROM python:3.8

#My direcory with project
WORKDIR /home/counter/programming_projects/flask_ecommerce

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY ecommerce.py config.py boot.sh ./
COPY media media
RUN chmod a+x boot.sh

ENV FLASK_APP=ecommerce.py

ENTRYPOINT ["./boot.sh"]
