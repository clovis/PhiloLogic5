#!/usr/bin/env python

import os
import sys
import urlparse
sys.path.append('..')
from functions.wsgi_handler import parse_cgi
from wsgiref.handlers import CGIHandler
import reports as r
import functions as f
import cgi
import json

def get_more_context(environ,start_response):
    status = '200 OK'
    headers = [('Content-type', 'application/json; charset=UTF-8'),("Access-Control-Allow-Origin","*")]
    start_response(status,headers)
    environ["SCRIPT_FILENAME"] = environ["SCRIPT_FILENAME"].replace('scripts/get_more_context.py', '')
    cgi = urlparse.parse_qs(environ["QUERY_STRING"],keep_blank_values=True)
    hit_num = int(cgi.get('hit_num',[0])[0])
    db, path_components, q = parse_cgi(environ)
    config = f.WebConfig()
    if q['start'] == 0:
        start = 0
    else:
        start = q['start'] - 1
    end = (q['end'] or q['results_per_page']) + 1
    hit_range = range(start, end)
    hits = db.query(q["q"],q["method"],q["arg"],**q["metadata"])
    context_size = config['concordance_length'] * 3
    html_list = []
    for i in hit_range:
        try:
            html_list.append(r.fetch_concordance(db, hits[i], environ["SCRIPT_FILENAME"], context_size))
        except IndexError:
            break
    yield json.dumps(html_list)

if __name__ == "__main__":
    CGIHandler().run(get_more_context)
