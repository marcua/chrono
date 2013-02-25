from argparse import ArgumentParser
from errors import add_param_errors, get_param_errors
from event_handling import insert_event, retrieve_events
from chrono_setup import start_error
from flask import Flask, request, json
import settings

app = Flask(__name__)

@app.route('/1.0/event/<series_name>/put/', methods=['POST'])
def add_events(series_name):
  resp = {'errors': [], 'inserted': 0, 'timestamped': 0}
  if not add_param_errors(series_name, request.json, resp):
    for event in request.json:
      insert_event(settings.SERIES[series_name], event, resp)
  # TODO(marcua): set status code to 400 if errors
  return json.dumps(resp)


@app.route('/1.0/event/<series_name>/get/', methods=['POST'])
def get_events(series_name):
  resp = {'errors': [], 'results': None, 'done': False}
  if not get_param_errors(series_name, request.json, resp):
    series = settings.SERIES[series_name]
    retrieve_events(series, request.json, resp)
  # TODO(marcua): set status code to 400 if errors
  return json.dumps(resp)


if __name__ == "__main__":
  parser = ArgumentParser(description='Run the Chrono webserver')
  parser.add_argument('--debug', action='store_true')
  args = parser.parse_args()
  if not start_error():
    app.run(debug=args.debug)
