from flask import Flask
from flask_bootstrap import Bootstrap
import os 

class ReverseProxied(object):
    """Wrap the application in this middleware and configure the 
    front-end server to add these headers, to let you quietly bind 
    this to a URL other than / and to an HTTP scheme that is 
    different than what is used locally"""
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]
        scheme = environ.get('HTTP_X_SCHEME', 'https')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        remote_host = environ.get('HTTP_X_FORWARDED_SERVER', '')
        remote_port = environ.get('HTTP_X_FORWARDED_PORT', '')
        if remote_host and remote_port:
            environ['HTTP_HOST'] = f'{remote_host}:{remote_port}'
        return self.app(environ, start_response)

app = Flask(__name__)

app.secret_key = 'random'

upload_folder = 'flask_app/uploads'
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

app.config['UPLOAD_FOLDER'] = upload_folder

app.wsgi_app = ReverseProxied(app.wsgi_app)

Bootstrap(app)