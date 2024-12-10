from io import BytesIO
from wsgiref.util import setup_testing_defaults
import sys
import os

# Add the project root directory to sys.path to allow importing from `src`
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from src.server import application

def wsgi_test_request(path='/', method='GET', headers=None, body=b''):
    if headers is None:
        headers = {}

    env = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'wsgi.input': BytesIO(body),
        'CONTENT_LENGTH': str(len(body)),
        'wsgi.errors': BytesIO(),
        'wsgi.version': (1, 0),
        'wsgi.run_once': False,
        'wsgi.url_scheme': 'http',
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
    }
    for k, v in headers.items():
        env['HTTP_' + k.upper().replace('-', '_')] = v
    setup_testing_defaults(env)

    status = []
    response_headers = []
    def start_response(s, h):
        status.append(s)
        response_headers.extend(h)

    body_iter = application(env, start_response)
    response_body = b''.join(body_iter)
    return status[0], dict(response_headers), response_body
