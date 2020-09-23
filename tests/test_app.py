import unittest
from chalice.test import Client
from app import app


test_cases = [
    b"""
    \n*** Test Cases ***\nEvaluate that 9 is less than 10\n    Should Be True  9 < 10
    """
]

responses = [
    b"==============================================================================\nTest                                                                          \n==============================================================================\nEvaluate that 9 is less than 10                                       | PASS |\n------------------------------------------------------------------------------\nTest                                                                  | PASS |\n1 critical test, 1 passed, 0 failed\n1 test total, 1 passed, 0 failed\n==============================================================================\nOutput:  /tmp/output/output.xml\nLog:     /tmp/output/log.html\nReport:  /tmp/output/report.html\n"
]

class TestApp(unittest.TestCase):

    def test_that_test_run_success(self):
        with Client(app) as client:
            result = client.http.post('/', headers={'Content-Type': 'text/plain'}, body=test_cases[0])
            assert result.body == responses[0]


if __name__ == '__main__':
    unittest.main()