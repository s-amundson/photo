FROM python:3.11-bullseye

# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install netcat for entry script
RUN apt-get update && apt-get install -y netcat

# Create an app user in the app group.
#RUN useradd --user-group --create-home --no-log-init --shell /bin/bash app
RUN mkdir -p /home/app/web

ENV APP_HOME=/home/app/web

# Create the staticfiles directory. This avoids permission errors.
RUN mkdir -p $APP_HOME/staticfiles
RUN mkdir -p $APP_HOME/media

# Change the workdir.
WORKDIR $APP_HOME

# Copy the requirements.txt file.
COPY ./requirements.txt $APP_HOME

# Upgrade pip
RUN pip install --upgrade pip

# Install the requirements.
RUN pip install -r requirements.txt

# Copy the rest of the code.
COPY ./photo_project $APP_HOME
#RUN chown -R app:app $APP_HOME
#USER app:app

ENTRYPOINT ["/home/app/web/entrypoint.sh"]

