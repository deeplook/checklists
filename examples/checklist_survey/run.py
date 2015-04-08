# -*- coding: utf-8 -*-
"""
This is a prototypical Flask app implementing a checkbox only "checklist" survey.

It uses bootstrap for a decent HTML layout, bootstraptoogles for modern,
mobile-friendly checkboxes, and D3 for rendering result as bubbles.
"""

import os
import sys
import json
import datetime
# import shutil
from os.path import join
from functools import update_wrapper

from flask import Flask, render_template, request, make_response, redirect, Response
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig

from flask_cache_response_decorator import cache


def nocache(f):
    """"
    A decorator for Flask to not cache a response.
    """
    def new_func(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.cache_control.no_cache = True
        return resp
    return update_wrapper(new_func, f)


app = Flask(__name__)

# Flask-Appconfig is not necessary, but highly recommend
AppConfig(app, None)
Bootstrap(app)
# in a real app, these should be configured through Flask-Appconfig
app.config['SECRET_KEY'] = 'devkey'
# app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'


def convert_jsrec_to_json(survey_id, inpath, outpath):
    """
    Convert logged jsrec entries into a json tree suitable for D3 bubbles.

    Return a dictionary containing some statistics.
    """
    num_votings = 0
    num_checks = 0
    ips = set()
    dates = []
    totals = {'name': 'survey', 'children': []}
    with open(inpath) as infile:
        for line in infile:
            j = json.loads(line)
            if survey_id and j['id'] != survey_id:
                continue
            selection = j['selection']
            if selection:
                num_votings += 1
                ips.add(j['ip'])
                dates.append(j['datetime'])
            for section, modules in selection.items():
                if not section in [ch['name'] for ch in totals['children']]:
                    totals['children'].append({'name': section, 'children': []})
                for mod in modules:
                    for s in totals['children']:
                        if s['name'] == section:
                            break
                    if not mod in [ch['name'] for ch in s['children']]:
                        s['children'].append({'name': mod, 'size': 0, 'children': []})
                    for mods in s['children']:
                        if mods['name'] == mod:
                            break
                    mods['size'] += 1
                    num_checks += 1
    num_ips = len(ips)
    dates = sorted(dates)
    start_date, end_date = dates[0], dates[-1]

    # convert empty children lists to None
    if totals['children'] == []:
        totals['children'] = None
    else:
        for ch in totals['children']:
            if ch['children'] == []:
                ch['children'] = None
            else:
                for ch in ch['children']:
                    if ch['children'] == []:
                        ch['children'] = None

    with open(outpath, 'w') as outfile:
        outfile.write(json.dumps(totals, indent=4))
    
    stats = {
        'num_ips': num_ips,
        'num_votings': num_votings,
        'num_checks': num_checks,
        'start_date': start_date,
        'end_date': end_date
    }
    return stats


@app.route('/')
def index():
    """
    Home handler.
    """
    return render_template('index.html')


@app.route('/surveys/<survey_id>', methods=['GET', 'POST'])
@app.route('/surveys/', methods=['GET', 'POST'])
@app.route('/surveys', methods=['GET', 'POST'])
def surveys(survey_id=None):
    """
    Render a page with a form for a survey with some given ID.
    """
    extended = request.args.get("extended", None)
    survey = None
    if survey_id:
        path = 'data/survey_%s.json' % survey_id
        if os.path.exists(path):
            survey = json.load(open(path))
    result = render_template('survey.html',
                             survey=survey, extended=extended!=None)
    return result


def form_to_dict(request_form):
    """
    Convert data from request form to a dictionary.
    """
    # ['py.dev:yapf', 'py.impl:cpython', 'py.dev:2to3']
    keys = request_form.keys()

    # [['py.dev', 'yapf'], ['py.impl', 'cpython'], ['py.dev', '2to3']]
    items = [key.split(':') for key in keys if key != 'id']

    # {'py.impl': ['cpython'], 'py.dev': ['autopep8', 'coverage']}
    d = {}
    for k, v in items:
        if not k in d:
            d[k] = []
        if not v.endswith('other'):
            d[k].append(v)
        else:
            for x in request_form.get(k + ':other').split():
                if x not in d[k]:
                    d[k].append(x)
    for k, v in d.items():
        if v == []:
            del d[k]

    return d


@app.route('/results/<survey_id>', methods=['GET', 'POST'])
@app.route('/results/', methods=['GET', 'POST'])
@app.route('/results', methods=['GET', 'POST'])
@cache()
def results(survey_id=None):
    """
    Render a result page for some given survey.
    """

    # handle missing or wrong survey_id
    survey_name = None
    stats = {}
    if survey_id:
        path = 'data/survey_%s.json' % survey_id
        if os.path.exists(path):
            survey_name = json.load(open(path))['description']
    if request.method == 'GET' and not survey_id or not survey_name:
        return render_template('result_bubbles.html', 
            survey_id=survey_id,
            survey_name=survey_name, 
            stats=stats)

    stats = {}
    ballots_path = join('data', 'ballots_all.jsrec')
    if request.method == 'POST':
        d = form_to_dict(request.form)
        payload = {
            'ip': request.remote_addr, 
            'id': survey_id, 
            'datetime': datetime.datetime.now().isoformat(), 
            'selection': d
        }
        jsrec = json.dumps(payload) # must be a single line
        open(ballots_path, 'a').write(jsrec + '\n')
    result_path = join('static', 'js', 'final_%s.json' % survey_id)
    stats = convert_jsrec_to_json(survey_id, ballots_path, result_path)
    # shutil.copy(result_path, join('static', 'js', 'final_%s.json' % survey_id))
    return render_template('result_bubbles.html', 
        survey_id=survey_id,
        survey_name=survey_name, 
        stats=stats)


if __name__ == '__main__':
    app.run(debug=True)
