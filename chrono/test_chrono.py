from nose.tools import with_setup
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def setup_func():
  pass

def teardown_func():
  pass

@with_setup(setup_func, teardown_func)
def test_request():
  headers = {'content-type': 'application/json'}
  payload = [
    {
      "time": 1351698990.812487,
      "data": {
        "host": "web14",
        "path": "/search",
        "query": {
          "q": "flowers"
          },
        "duration_ms": 241,
        "status": 200,
        "user_agent": "Chrome/13.0.782.112"
        }
      }
    ]
  url = "%s/1.0/event/party/put/" % BASE_URL
  r = requests.post(url, data=json.dumps(payload), headers=headers)
  assert r.text == """{"timestamped": 0, "errors": [], "inserted": 1}"""
