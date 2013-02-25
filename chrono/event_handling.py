from db import db_handler

import time
import uuid

def insert_event(series, event, resp):
  error = False
  tval = event.get('time', None)
  if tval == None:
    tval = time.time()
    resp['timestamped'] += 1
  elif type(tval) != int and type(tval) != float:
    resp['errors'].append("'%s' is not a valid integer or floating point UTC timestamp" % (time))
    error = True

  unique_id = event.get('id', None)
  if unique_id != None:
    try:
      event['id'] = uuid.UUID(unique_id)
    except:
      resp['errors'].append("'%s' is not a valid UUID" % unique_id)
      error = True

  if not error:
    event['time'] = tval
    db_handler.insert(series, event)
    resp['inserted'] += 1

MAX_RETRIEVE = 1000
def get_events(series, params, resp):
  start_id = request.json.get('start_id', None)
  start_time = request.json.get('start_time', None)
  end_time = request.json.get('end_time', None)
  resp['events'], resp['done'] = (
    db_handler.retrieve(series, start_time, start_id, end_time, MAX_RETRIEVE))
  

