#!/usr/bin/env python

import sys
import timeit
from operator import itemgetter
from philologic.DB import DB
sys.path.append('..')
from functions.wsgi_handler import WSGIHandler
from wsgiref.handlers import CGIHandler
import reports as r
import functions as f
from functions.ObjectFormatter import format_strip, convert_entities, adjust_bytes
try:
    import simplejson as json
except ImportError:
    import json


def get_sorted_kwic(environ,start_response):
    status = '200 OK'
    headers = [('Content-type', 'application/json; charset=UTF-8'),("Access-Control-Allow-Origin","*")]
    start_response(status,headers)
    config = f.WebConfig()
    db = DB(config.db_path + '/data/')
    environ['QUERY_STRING'] = environ['HTTP_REFERER'].replace(config.db_url + '/query?', '')
    request = WSGIHandler(db, environ)
    input_object = json.loads(environ['wsgi.input'].read())
    indices = input_object['results']
    sorted_hits = get_sorted_hits(indices, request, config, db)
    yield json.dumps(sorted_hits)


def get_sorted_hits(indices, q, config, db):
    hits = db.query(q["q"],q["method"],q["arg"],**q.metadata)
    start, end, n = f.link.page_interval(q.results_per_page, hits, q.start, q.end)
    kwic_object = {"description": {"start": start, "end": end, "results_per_page": q.results_per_page},
                    "query": dict([i for i in q])}
    
    kwic_results = []
    
    for index in indices:
        hit = hits[index[1]]
        kwic_result = r.kwic_hit_object(hit, config, db)
        kwic_results.append(kwic_result)
        
    kwic_object['results'] = kwic_results
    kwic_object['results_length'] = len(hits)
    kwic_object["query_done"] = hits.done

    return kwic_object


if __name__ == "__main__":
    CGIHandler().run(get_sorted_kwic)