# flask_api_gunicorn
flask_api

This is flask application to deploy the application file to targeted runtime (JVM) in Anypoint cloud.

gunicorn application:app -c gunicorn.conf.py --daemon

Command to start Gunicorn

gunicorn <application_file>:app -c <config_file> --daemon
