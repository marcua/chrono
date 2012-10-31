from argparse import ArgumentParser
from event_handling import insert_event
from chrono_setup import start_error
from flask import Flask, request, json
import settings

app = Flask(__name__)

def param_errors(series_name, req, resp):
  error = False
  if series_name not in settings.SERIES:
    resp['errors'].append("Series configuration must be set in settings.py (edit SERIES)")
    error = True
  if type(req) != list:
    resp['errors'].append("Submit a request with 'Content-type: application/json' and a list of events")
    error = True
  return error

@app.route('/1.0/event/<series_name>/put/', methods=['POST'])
def add_events(series_name):
  resp = {'errors': [], 'inserted': 0, 'timestamped': 0}
  if not param_errors(series_name, request.json, resp):
    for event in request.json:
      insert_event(settings.SERIES[series_name], event, resp)
  return json.dumps(resp)

@app.route('/1.0/event/<series_name>/get/', methods=['POST'])
def get_events(series_name):
  assert(request.json)
  # TODO: process {'type': ..., 'start': ..., 'end': ...}

if __name__ == "__main__":
  parser = ArgumentParser(description='Run the Chrono webserver')
  parser.add_argument('--debug', action='store_true')
  args = parser.parse_args()
  if not start_error():
    app.run(debug=args.debug)
