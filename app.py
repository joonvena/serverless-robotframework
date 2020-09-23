from chalice import Chalice, BadRequestError, CORSConfig, Response
from robot import run
import boto3
from botocore.exceptions import ClientError
import io
import json
import uuid
from os import environ
import re

app = Chalice(app_name='rf-runner')
cors_config = CORSConfig(
    allow_origin=environ.get('FRONTEND_URL'),
    allow_credentials=True
)

FRONTEND_URL = environ.get('FRONTEND_URL')
RF_REPORTS_BUCKET = environ.get('REPORT_BUCKET')

ALLOWED_LIBRARIES = [
    'Builtin',
    'String',
    'Dialogs',
    'DateTime',
    'Collections',
    'XML',
    'RequestsLibrary'
]

REPORTS = ['output.xml', 'log.html', 'report.html']

@app.middleware('http')
def validation_middleware(event, get_response):
    libraries = re.findall("Library\s{2,}(.*)", event.raw_body.decode("utf-8"))
    for library in libraries:
        if library not in ALLOWED_LIBRARIES:
            response = {
                "output": None,
                "report_urls": None,
                "error": "{} is not in the allowed libraries list".format(library)
                
            }
            return Response(
                headers={'Access-Control-Allow-Origin': FRONTEND_URL},
                status_code=400,
                body=response
            )
    return get_response(event)

def upload_reports():
    report_urls = {"output": "", "log": "", "report": ""}
    s3 = boto3.resource("s3")
    s3_client = boto3.client("s3")
    report_id = uuid.uuid4()
    for file in REPORTS:
        s3.Bucket(RF_REPORTS_BUCKET).upload_file("/tmp/output/{}".format(file), "{}/{}".format(report_id.hex, file))
        try:
            response = s3_client.generate_presigned_url("get_object", Params={'Bucket': RF_REPORTS_BUCKET, 'Key': '{}/{}'.format(report_id.hex, file)}, ExpiresIn=60)
            file_name = file.split(".")
            report_urls[file_name[0]] = response
        except ClientError as error:
            print(error)

    return report_urls

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
            reports = upload_reports()
            response = {
                "output": v.getvalue(),
                "report_urls": reports,
                "error": None
            }
            return Response(
                status_code=200,
                body=response
            )
    except IOError as error:
        raise BadRequestError(error)
    
