FROM python:3.6.2

WORKDIR /HeadlineAPI

ADD requirements.txt /HeadlineAPI/
RUN apt-get update && \
    apt-get install -y postgresql python-psycopg2 libpq-dev cython && \
    pip install --upgrade pip && pip install -r requirements.txt && \
    su - postgres

ADD run.sh /HeadlineAPI/

# create unprivileged user
RUN adduser --disabled-password --gecos '' headlineuser
COPY . /HeadlineAPI/

RUN chmod u+x ./run.sh
ENTRYPOINT ["./run.sh"]
