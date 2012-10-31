from chrono_log import log
from datetime import datetime
from db import db_handler

import json
import time

def insert_event(series, event, resp):
  error = False
  tval = event.get('time', None)
  if tval == None:
    tval = time.time()
    resp['timestamped'] += 1
  elif type(tval) != int and type(tval) != float:
    resp['errors'].append("'%s' is not a valid integer or floating point UTC timestamp" % (time))
    error = True

  if not error:
    event['time'] = tval
    db_handler.insert(series, event)
    resp['inserted'] += 1

if __name__ == "__main__":
  insert_event({'data': {}})
