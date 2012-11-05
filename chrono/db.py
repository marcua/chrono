from chrono_log import log
from collections import defaultdict
from flask import json
from uuid import uuid1, UUID

class DBHandler(object):
  def insert(self, series, event):
    # if no ID is provided, generate a uuid1-like sequence from the
    # current time.  this isn't totally kosher: the UUID1 node comes
    # from the mac address of this machine rather than that of the
    # client, but we're using uuids as a proxy for unique
    # pseudotime-ordered strings anyway, so the damage has already
    # been done:)
    #
    # (bit-flipping logic from uuid1 implementation described in
    # http://docs.python.org/2/library/uuid.html and
    # http://stackoverflow.com/questions/7153844/uuid1-from-utc-timestamp-in-python)
    unique_id = event.get('id', None)
    if unique_id == None:
      nanoseconds = int(event['time'] * 1e9)
      timestamp = int(nanoseconds//100) + 0x01b21dd213814000L
      time_low = timestamp & 0xffffffffL
      time_mid = (timestamp >> 32L) & 0xffffL
      time_hi_version = (timestamp >> 48L) & 0x0fffL
      timeuuid = uuid1()
      unique_id = UUID(fields=(time_low, time_mid, time_hi_version,
                              timeuuid.clock_seq_hi_variant, timeuuid.clock_seq_low, 
                              timeuuid.node), version=1)
    floor_time = int(event['time'])
    bucket = floor_time - (floor_time % series['bucket_seconds'])
    self._insert(series['name'], event, bucket, unique_id)

  def _insert(self, series, event, unique_id):
    raise NotImplementedError("Must implement __insert method")

  def retrieve(self, series, start, end):
    pass

class InMemoryDBHandler(DBHandler):
  def __init__(self):
    self.__db = defaultdict(list)
  def _insert(self, series_name, event, bucket, unique_id):
    key = "%s-%d" % (series_name, bucket)
    self.__db[key].append((uniquetime, json.dumps(event)))
    print self.__db

db_handler = InMemoryDBHandler()
