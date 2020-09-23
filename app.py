from chalice import Chalice, BadRequestError, CORSConfig, Response
from robot import run
import boto3
import io
import json
from os import environ
import re

app = Chalice(app_name='rf-runner')
cors_config = CORSConfig(
    allow_origin=environ.get('FRONTEND_URL'),
    allow_credentials=True
)

ALLOWED_LIBRARIES = [
    'Builtin',
    'String',
    'Dialogs',
    'DateTime',
    'Collections',
    'XML',
    'RequestsLibrary'
]

@app.middleware('http')
def validation_middleware(event, get_response):
    libraries = re.findall("Library\s{2,}(.*)", event.raw_body.decode("utf-8"))
    for library in libraries:
        if library not in ALLOWED_LIBRARIES:
            response = {
                "error": "{} is not in the allowed libraries list".format(library),
                "output": None
            }
            return Response(
                headers={'Access-Control-Allow-Origin': environ.get('FRONTEND_URL')},
                status_code=400,
                body=response
            )
    return get_response(event)

@app.route('/', methods=['POST'], content_types=['text/plain'], api_key_required=True, cors=cors_config)
def run_test():
    try:
        with open("/tmp/test.robot", "wb") as r:
            r.write(app.current_request.raw_body)
    except IOError as error:
        raise BadRequestError(error)
    try:
        with io.StringIO() as v:
            run('/tmp/test.robot', outputdir='/tmp/output', stdout=v, stderr=v)
            response = {
                "output": v.getvalue(),
                "error": None
            }
            return Response(
                status_code=200,
                body=response
            )
    except IOError as error:
        raise BadRequestError(error)
    
