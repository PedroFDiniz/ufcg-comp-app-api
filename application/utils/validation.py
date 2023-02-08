def myAssert( condition, action ):
    if not condition: raise action

def http_data_field(http_data, field):
  try:
      result = http_data[field]
  except KeyError:
      result = None
  
  return result