# -*- coding: utf-8 -*-
from bottle import *
import json, pickle

@route('/<:re:.*>', method='OPTIONS')
def enable_cors_generic_route():
  add_cors_headers()

@hook('after_request')
def enable_cors_after_request_hook():
  """
  This executes after every route. We use it to attach CORS headers when applicable.
  """
  add_cors_headers()

def add_cors_headers():
  response.set_header('Access-Control-Allow-Origin', '*')
  response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
  response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

# 获取全部关键词信息，绘制词云图
@route('/getAllInfo', method=['OPTIONS', 'GET'])
def getInfo():
  res = []
  label_list = ['civilization', 'economy', 'education', 'military', 'polity', 'society', 'sports', 'other']
  for (index, label) in enumerate(label_list):
    with open('./data/wordcloud/news_' + label + '_keywords.pk', 'rb') as f:
      keywords = pickle.load(f)[:50]
      for (i, item) in enumerate(keywords):
        res.append({
          'id': item[0],
          'size': item[1],
          'group': label
        })
    
  response.headers['Content-type'] = 'application/json'
  return json.dumps(res)

run(host='localhost', port=31000, debug=True)
