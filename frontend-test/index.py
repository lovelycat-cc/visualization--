# -*- coding: utf-8 -*-
from bottle import *
import json, pickle
from collections import defaultdict
from get_words_connection import get_words_connection
from search_engineer import search_engine

# 跨域
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

# 输入关键词，获取关键词相关的词
@route('/getNodesByKeyword', method='get')
def getConnectedNodes():
  keyword = request.query.keyword
  nodes = set()
  nodes_with_type = defaultdict(str)
  links = []
  label_list = ['civilization', 'economy', 'education', 'military', 'polity', 'society', 'sports', 'other']
  for (index, label) in enumerate(label_list):
    words_dict = get_words_connection(keyword, './data/forcegraph/news_' + label + '_word2vec.w2v')
    for (k, v) in words_dict.items():
      nodes.add(k)
      nodes.update(v)
      if k not in nodes_with_type.keys():
        nodes_with_type[k] = label
      for item in v:
        links.append((k,item))        
        if item not in nodes_with_type.keys():
          nodes_with_type[item] = label
  res = {}
  res['nodes'] = []
  res['links'] = []
  for n in list(nodes):
    res['nodes'].append({
      'id': n,
      'group': nodes_with_type[n]
    })
  for l in list(set(links)):
    res['links'].append({
      'source': l[0],
      'target': l[1]
    })
  response.headers['Content-type'] = 'application/json'
  return json.dumps(res)

# 通过关键词获取具体信息
@route('/getInfoByKeyword', method='get')
def getDetail():
  keyword = request.query.keyword
  label = str(request.query.label)
  res = search_engine(keyword, './data/searchengineer/news_' + label +'_content.pk', './data/searchengineer/news_' + label + '_add_opinion.pk')
  response.headers['Content-type'] = 'application/json; charset=utf-8'
  return json.dumps(res)

# 静态文件
@route('/static/img/<filename>')
def send_image(filename):
    return static_file(filename, root='./dist/static/img/')
@route('/static/css/<filename>')
def send_css(filename):
  return static_file(filename, root='./dist/static/css/')
@route('/static/js/<filename>')
def send_js(filename):
  return static_file(filename, root='./dist/static/js/')
@route('/static/fonts/<filename>')
def send_fonts(filename):
  return static_file(filename, root='./dist/static/fonts/')

@route('/')
def index():
  return template('./dist/index.html')

run(host='localhost', port=31000, debug=True)
