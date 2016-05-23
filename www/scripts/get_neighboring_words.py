#!/usr/bin/env python

import os
import sys
import timeit
from wsgiref.handlers import CGIHandler

import simplejson
from philologic.DB import DB

from philologic.app import WebConfig
from philologic.app import WSGIHandler


def get_neighboring_words(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'application/json; charset=UTF-8'),
               ("Access-Control-Allow-Origin", "*")]
    start_response(status, headers)

    config = WebConfig(os.path.abspath(os.path.dirname(__file__)).replace('scripts', ''))
    db = DB(config.db_path + '/data/')
    request = WSGIHandler(environ, config)

    try:
        index = int(request.hits_done)
    except:
        index = 0

    max_time = int(request.max_time)

    kwic_words = []
    start_time = timeit.default_timer()
    hits = db.query(request["q"], request["method"], request["arg"], **
                    request.metadata)
    c = db.dbh.cursor()

    for hit in hits[index:]:
        word_id = ' '.join([str(i) for i in hit.philo_id])
        query = 'select rowid, philo_name, parent from words where philo_id="%s" limit 1' % word_id
        c.execute(query)
        results = c.fetchone()

        parent_sentence = results['parent']

        if request.direction == "left":
            c.execute(
                'select philo_name, philo_id from words where parent=? and rowid < ?',
                (parent_sentence, results['rowid']))
            string = []
            for i in c.fetchall():
                string.append(i['philo_name'].decode('utf-8'))
            string.reverse()
            string = ' '.join(string)
        elif request.direction == "right":
            c.execute(
                'select philo_name, philo_id from words where parent=? and rowid > ?',
                (parent_sentence, results['rowid']))
            string = []
            for i in c.fetchall():
                string.append(i['philo_name'].decode('utf-8'))
            string = ' '.join(string)
        else:
            string = ""

        metadata_fields = {}
        for metadata in config.kwic_metadata_sorting_fields:
            metadata_fields[metadata] = hit[metadata].lower()

        kwic_words.append((string, index, metadata_fields))

        index += 1

        elapsed = timeit.default_timer() - start_time
        if elapsed > max_time:  # avoid timeouts by splitting the query if more than 10 seconds has been spent in the loop
            break

    yield simplesimplejson.dumps({"results": kwic_words, "hits_done": index})


if __name__ == "__main__":
    CGIHandler().run(get_neighboring_words)
