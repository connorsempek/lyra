# code to build spec for timeseries plot


def data_obj(data, time_col, measure_col, fmt='%Y-%m-%d %H:%M:%S',
  group_col=None, lower_conf=None, upper_conf=None):
  '''builds data object for spec
  '''

  obj = {
    "name": 'table',
    "format":{
      "parse": {
        measure_col: "number", 
        time_col: "date:'{}'".format(fmt)
      }
    }
  }
  if isinstance(data, str):
    obj['url'] = data
  elif isinstance(data, list):
    obj['values'] = data

  if lower_conf:
    obj['format']['parse'][lower_conf] = 'number'
  if upper_conf:
    obj['format']['parse'][lower_conf] = 'number'
  return [obj]


def scales_obj(time_col, measure_col, group_col=None, x_nice='hour', y_nice=True,
  y_zero=True):
  '''
  '''

  x = {
    "name": "x",
    "range": "width",
    "type": "time",
    "domain": {
      "field": time_col,
      "data": 'table'
    },
    "nice": x_nice
  }

  y = {
    "name": "y",
    "range": "height",
    "type": "linear",
    "domain": {
      "field": measure_col,
      "data": 'table'
    },
    "zero": y_zero,
    "nice": y_nice
  }
  
  obj = [x,y]

  if group_col:
    obj.append({
      "name": "color",
      "type": "ordinal",
      "range": "category",
      "domain": {"data": "table", "field": group_col}
    })
  return obj


def marks_obj(time_col, measure_col, group_col=None, lower_conf=None, upper_conf=None, alpha=0.5):
  '''
  '''

  line_mark = {
    "type": "line",
    "from": {"data": "table"},
    "encode": {
      "enter": {
        "interpolate": {"value": "monotone"},
        "x": {"scale": "x", "field": time_col},
        "y": {"scale": "y", "field": measure_col}
      }
    }
  }
  marks = [line_mark]

  if lower_conf is not None or lower_conf is not None:
    
    lower = lower_conf if lower_conf is not None else measure_col
    upper = upper_conf if upper_conf is not None else measure_col
    area_mark = {
      "type": "area",
      "from": {"data": "table"},
      "encode": {
        "enter": {
          "interpolate": {"value": "monotone"},
          "x": {"scale": "x", "field": "hr"},
          "y": {"scale": "y", "field": lower},
          "y2": {"scale": "y", "field": upper},
          "fillOpacity": {"value": alpha}
        }
      }
    }
    marks.append(area_mark)

  if group_col is not None:
    facet = {
      "type": "group",
      "from": {
        "facet": {
          "name": "facet",
          "data": "table",  
          "groupby": group_col
        }
      }
    }
    for mark in marks:
      mark['from']['data'] = 'facet'
      group_color = {"scale": "color", "field": group_col}
      if mark['type'] == 'line':
        mark['encode']['enter']['stroke'] = group_color
      elif mark['type'] == 'area':
        mark['encode']['enter']['fill'] = group_color
    
    facet.update({'marks': marks})
    marks = facet

  return marks


def make_spec(data, time_col, measure_col, fmt='%Y-%m-%d %H:%M:%S',
  group_col=None, lower_conf=None, upper_conf=None, x_nice='hour', y_nice=True,
  y_zero=True, alpha=0.5):
  '''
  '''

  spec = {
    "$schema": "https://vega.github.io/schema/vega/v3.0.json",
    "height": 400,
    "padding": 5,
    "width": 700,

    "axes": [
      {
        "scale": "x",
        "orient": "bottom"
      },
      {
        "scale": "y",
        "orient": "left"
      }
    ]
  }
  spec['data'] = data_obj(data, time_col, measure_col, fmt=fmt, 
    group_col=group_col, lower_conf=lower_conf, upper_conf=upper_conf)
  spec['scales'] = scales_obj(time_col, measure_col, group_col=group_col, x_nice=x_nice, 
    y_nice=y_nice, y_zero=y_zero)
  spec['marks'] = marks_obj(time_col, measure_col, group_col=group_col, 
    lower_conf=lower_conf, upper_conf=upper_conf, alpha=alpha)

  if group_col:
    spec['legends'] = [
      {
        "orient": "right", 
        "fill": "color", 
        "offset": 50, 
        "zindex": 1,
        "title": group_col 
      }
    ]

  return spec

