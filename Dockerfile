FROM python:3.9-bullseye

WORKDIR /app

# update pip and install pipenv
RUN pip3 install --upgrade pip pipenv

COPY . .

RUN pipenv install --system
