from chrono_log import log

import db
import re
import settings

SERIES_RE = re.compile("^[a-zA-Z0-9\-\_]+$")

def load_settings_error():
  error = False
  for name in settings.SERIES.keys():
    if SERIES_RE.search(name) == None:
      log.error("'%s' is not a valid series name (in settings.py). Stick to alphanumeric characters, -, and _" % (name))
      error = True
    settings.SERIES[name]['name'] = name
  return error

def config_db_error():
  return False

def start_error():
  return load_settings_error() or config_db_error()
