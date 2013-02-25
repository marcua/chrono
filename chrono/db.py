from chrono_log import log
from collections import defaultdict
from flask import json
from itertools import chain
from operator import itemgetter
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

  def retrieve(self, series, start_time, start_id, end_time, max_events):
    bucket_seconds = series['bucket_seconds']
    if start_id != None:
      start_time = ((start_id.time - 0x01b21dd213814000L)*100/1e9)
    floor_start = int(start_time)
    start_bucket = floor_start - (floor_start % bucket_seconds)
    floor_end = int(end_time)
    end_bucket = floor_end - (floor_end % bucket_seconds) + bucket_seconds
    
    return chain(self._retrieve(series, bucket, start_time, start_id, end_time)
                 for bucket in xrange(start_bucket, end_bucket, bucket_seconds))

  def _insert(self, series, event, unique_id):
    '''
    TODO(marcua): Add batching in the interface/implementation for
    improved throughput
    '''
    raise NotImplementedError("Must implement __insert method")

  def _retrieve(self, series, bucket, start_time, end_time):
    raise NotImplementedError("Must implement __insert method")

  def retrieve(self, series, start, end):
    pass


class InMemoryDBHandler(DBHandler):
  def __init__(self):
    self.__db = defaultdict(list)
  def _insert(self, series_name, event, bucket, unique_id):
    key = '%s-%d' % (series_name, bucket)
    self.__db[key].append((unique_id, json.dumps(event)))
    print self.__db
  def _retrieve(self, series, bucket, start_time, start_id, end_time, max_items):
    key = '%s-%d' % (series_name, bucket)
    bucket = self.__db[key]
    items = sorted(bucket, key=itemgetter(0))
    if start_id != None:
      items = (item for item in items if item['id'] > start_id)
#    items = (item 
    return (event for unique_id, event in ordered if
            (event['time'] < end_time) and (event['time'] > start_time))


db_handler = InMemoryDBHandler()
