# We could use a smaller image here, like slim or even Alpine.
# Small images requires more testing, specially the Alpine one.
# For this challenge I'll use the default image.
FROM python:3.10

# Use a non-privileged port.
EXPOSE 8080

# Common directory used for Python apps.
WORKDIR /usr/src/app

# Run our app using a Python WSGI HTTP Server.
CMD [ "gunicorn", "-b", "0.0.0.0:8080", "flaskr:create_app()" ]

# Requirements usually don't change, so we copy it first and create a cached layer.
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# Put this as the last command and leverage docker layers to build images faster.
COPY . /usr/src/app/
