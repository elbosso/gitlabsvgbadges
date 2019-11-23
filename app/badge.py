from flask import make_response
import requests
from app.anybadge import Badge
from flask import request
import datetime
from app import app
import os
@app.route("/openIssues/<int:projid>")
def openIssues(projid):
    lbl=request.args.get('lbl', 'open issues')
    url = 'http://'+os.environ['GITLAB_HOST']+':'+os.environ['GITLAB_PORT']+'/api/v4/projects/'+str(projid)+'/issues?state=opened&scope=all&per_page=1'
    headers = {'Private-Token': os.environ['GITLAB_SECRET']}
    r = requests.get(url, headers=headers)
#    print (r.headers)
    if r.status_code!=200 :
        v=r.status_code
        lbl='HTTP Error'
    else :
        v=r.headers['x-total']
    thresh={5: 'green',
         10: 'yellowgreen',
         15: 'yellow',
         20: 'orange',
         25: 'red'}
    vfmt="%d"
    badge = Badge(label=lbl, value=v, value_format=vfmt,thresholds=thresh)
    resp = make_response(badge.badge_svg_text, 200)
    resp.headers['Content-Type'] = 'image/svg+xml;charset=utf-8'
    resp.headers['Content-Disposition'] = 'attachment; filename=badge.svg'
    return resp

@app.route("/closedIssues/<int:projid>")
def closedIssues(projid):
    lbl=request.args.get('lbl', 'closed Issues')
    url = 'http://'+os.environ['GITLAB_HOST']+':'+os.environ['GITLAB_PORT']+'/api/v4/projects/'+str(projid)+'/issues?state=closed&scope=all&per_page=1'
    headers = {'Private-Token': os.environ['GITLAB_SECRET']}
    r = requests.get(url, headers=headers)
    if r.status_code!=200 :
        v=r.status_code
        lbl='HTTP Error'
        thresh={0: 'red'}
    else :
        v=r.headers['x-total']
        thresh={0: 'green'}
    vfmt="%d"
    badge = Badge(label=lbl, value=v, value_format=vfmt,thresholds=thresh)
    resp = make_response(badge.badge_svg_text, 200)
    resp.headers['Content-Type'] = 'image/svg+xml;charset=utf-8'
    resp.headers['Content-Disposition'] = 'attachment; filename=badge.svg'
    return resp

@app.route("/newIssues/<int:projid>")
def newIssues(projid):
    lbl=request.args.get('lbl', 'new issues')
    days=request.args.get('weeks', '2')
    if days is not None:
        start_date = datetime.date.today() + datetime.timedelta(-(int(days) * 7))
        dateParam = start_date.strftime('%Y-%m-%d')
        lbl = lbl + ' last ' + days + ' weeks'
        url = 'http://'+os.environ['GITLAB_HOST']+':'+os.environ['GITLAB_PORT']+'/api/v4/projects/' + str(projid) + '/issues?scope=all&created_after='+dateParam+'&per_page=1'
        headers = {'Private-Token': os.environ['GITLAB_SECRET']}
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            v = r.status_code
            lbl = 'HTTP Error'
            thresh = {0: 'red'}
        else:
            v = r.headers['x-total']
            thresh = {0: 'green'}
        vfmt = "%d"
        badge = Badge(label=lbl, value=v, value_format=vfmt, thresholds=thresh)
        resp = make_response(badge.badge_svg_text, 200)
        resp.headers['Content-Type'] = 'image/svg+xml;charset=utf-8'
        resp.headers['Content-Disposition'] = 'attachment; filename=badge.svg'
        return resp
    else:
        v = 'error'
        vfmt = "%s"
        thresh = {0: 'red'}

@app.route("/modifiedIssues/<int:projid>")
def modifiedIssues(projid):
    lbl = request.args.get('lbl', 'issues worked on')
    days = request.args.get('weeks', '2')
    if days is not None:
        start_date = datetime.date.today() + datetime.timedelta(-(int(days) * 7))
        dateParam = start_date.strftime('%Y-%m-%d')
        lbl = lbl + ' last ' + days + ' weeks'
        url = 'http://'+os.environ['GITLAB_HOST']+':'+os.environ['GITLAB_PORT']+'/api/v4/projects/' + str(projid) + '/issues?scope=all&updated_after='+dateParam+'&per_page=1'
        headers = {'Private-Token': os.environ['GITLAB_SECRET']}
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            v = r.status_code
            lbl = 'HTTP Error'
            thresh = {0: 'red'}
        else:
            v = r.headers['x-total']
            thresh = {0: 'green'}
        vfmt = "%d"
        badge = Badge(label=lbl, value=v, value_format=vfmt, thresholds=thresh)
        resp = make_response(badge.badge_svg_text, 200)
        resp.headers['Content-Type'] = 'image/svg+xml;charset=utf-8'
        resp.headers['Content-Disposition'] = 'attachment; filename=badge.svg'
        return resp
    else:
        v = 'error'
        vfmt = "%s"
        thresh = {0: 'red'}

@app.route("/orphanedIssues/<int:projid>")
def orphanedIssues(projid):
    lbl = request.args.get('lbl', 'orphaned issues')
    days = request.args.get('weeks', '2')
    if days is not None:
        start_date = datetime.date.today() + datetime.timedelta(-(int(days) * 7))
        dateParam = start_date.strftime('%Y-%m-%d')
        lbl = lbl + ' last ' + days + ' weeks'
        url = 'http://'+os.environ['GITLAB_HOST']+':'+os.environ['GITLAB_PORT']+'/api/v4/projects/' + str(projid) + '/issues?state=opened&scope=all&updated_before='+dateParam+'&per_page=1'
        headers = {'Private-Token': os.environ['GITLAB_SECRET']}
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            v = r.status_code
            lbl = 'HTTP Error'
            thresh = {0: 'red'}
        else:
            v = r.headers['x-total']
            thresh = {2: 'green',
         4: 'yellowgreen',
         6: 'yellow',
         8: 'orange',
         10: 'red'}
        vfmt = "%d"
        badge = Badge(label=lbl, value=v, value_format=vfmt, thresholds=thresh)
        resp = make_response(badge.badge_svg_text, 200)
        resp.headers['Content-Type'] = 'image/svg+xml;charset=utf-8'
        resp.headers['Content-Disposition'] = 'attachment; filename=badge.svg'
        return resp
    else:
        v = 'error'
        vfmt = "%s"
        thresh = {0: 'red'}

