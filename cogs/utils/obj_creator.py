#!/usr/bin/env python3

import json

def as_obj(dct):
  '''
  convert json obj to python obj
  currently supports:
    - Reminders
    - Timeouts
  '''
  from cogs.utils.role_removals import RoleRemove
  from cogs.utils.reminders import Reminder
  from cogs.utils.timeout import Timeout
  from cogs.utils.heap import Heap
  from cogs.utils.poll import Poll

  if '__reminder__' in dct:
    return Reminder.from_dict(dct)
  elif '__poll__' in dct:
    return Poll.from_dict(dct)
  elif '__timeout__' in dct:
    return Timeout.from_dict(dct)
  elif '__role_rem__' in dct:
    return RoleRemove.from_dict(dct)
  elif '__heap__' in dct:
    return Heap.from_dict(dct)
  return dct

def get_type(name):
  from cogs.utils.role_removals import RoleRemove
  from cogs.utils.reminders import Reminder
  from cogs.utils.timeout import Timeout
  from cogs.utils.heap import Heap, HeapNode
  from cogs.utils.poll import Poll
  return locals()[name]


class ObjEncoder(json.JSONEncoder):
  '''
  convert python obj to json obj
  supports same conversions as the function that goes the other way
  '''
  def default(self, obj):
    from cogs.utils.heap import Heap, HeapNode
    for dictable_type in (Heap, HeapNode):
      if isinstance(obj, dictable_type):
        return obj.to_dict()
    # Let the base class default method raise the TypeError
    return json.JSONEncoder.default(self, obj)
