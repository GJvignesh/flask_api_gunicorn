# flask_api_gunicorn
## Free time - Custom project
### Demo Application to serve Flask Using Gunicorn with custom threads under linux box for Production grade

flask_api

This is flask application to deploy the application file (.zip) to targeted place (URL).

gunicorn application:app -c gunicorn.conf.py --daemon
Command to start Gunicorn
gunicorn <application_file>:app -c <config_file> --daemon
