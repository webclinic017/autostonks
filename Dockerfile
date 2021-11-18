FROM python:3.9-bullseye

# update pip and install pipenv
RUN pip3 install --upgrade pip pipenv

RUN pipenv install --system
