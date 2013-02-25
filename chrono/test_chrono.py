from nose.tools import with_setup
import requests
import json

BASE_URL = "http://127.0.0.1:5000"
HEADERS = {'content-type': 'application/json'}

def setup():
  pass

def teardown():
  pass

@with_setup(setup, teardown)
def test_add_request():
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
  r = requests.post(url, data=json.dumps(payload), headers=HEADERS)
  print r.text
  assert r.text == """{"timestamped": 0, "errors": [], "inserted": 1}"""

def setup_gets():
  payload = [
    {
      "time": 1351790542.445142,
      "id": 'b26fc7d4-2448-11e2-bca8-68a86d1dc518',
      "data": {'boo':'123'}
      }
    ]
  url = "%s/1.0/event/party/put/" % BASE_URL
  r = requests.post(url, data=json.dumps(payload), headers=HEADERS)

def teardown_gets():
  pass

'''
@with_setup(setup_gets, teardown_gets)
def test_get_requests():
  headers = {'content-type': 'application/json'}
  start_and_end_time = {
    "start_time": 1351695890.812487,
    "end_time": 1351699890,
  }
  start_id_end_time = {
    "start_id": 1351698990.812487,
    "end_time": 1351698990.812487,
  }

  url = "%s/1.0/event/party/get/" % BASE_URL
  r = requests.post(url, data=json.dumps(start_and_end_time), headers=HEADERS)
  assert r.text == """{"timestamped": 0, "errors": [], "inserted": 1}"""
'''
