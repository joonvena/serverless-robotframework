from chalice import Chalice, BadRequestError
from robot import run
import subprocess
import boto3
import io
import re
from os import popen, listdir, environ, getcwd

app = Chalice(app_name='rf-runner')

 

@app.route('/', methods=['POST'], content_types=['text/plain'], api_key_required=True)
def run_test():
    try:
        with open("/tmp/test.robot", "wb") as r:
            r.write(app.current_request.raw_body)
    except KeyError:
        raise BadRequestError("Can't read test input")
    try:
        with io.StringIO() as v:
            run('/tmp/test.robot', outputdir='/tmp/output', stdout=v)
            return str(v.getvalue())
    except Error:
        raise BadRequestError("Can't read test input")
    
