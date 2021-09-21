# python base image in the container from Docker Hub
FROM python:3.8.10-slim

# copy files to the /app folder in the container
COPY ./handsy /app/handsy
COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock

# set the working directory in the container to be /app
WORKDIR /app

# install the packages from the Pipfile in the container
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 80
# execute the command python main.py (in the WORKDIR) to start the app
CMD ["uvicorn", "handsy.api:app", "--host", "0.0.0.0", "--port", "80"]