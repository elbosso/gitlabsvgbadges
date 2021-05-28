from flask import make_response
import requests
from app.anybadge import Badge
from flask import request
import datetime
from app import app
from app import api
import os
from flask_restplus import Api, Resource, fields
from flask_restplus import reqparse

ns = api.namespace('', description='badges for gitlab')
@ns.route('/openIssues/<int:projid>')
@ns.param('projid', 'The project identifier')
@ns.param('lbl', 'The label for the badge - default: open issues')
class OpenIssue(Resource):
    def get(self, projid):
        """
        Badge displaying the number of open issues

        generates an SVG graphic with the specified label and the number of
        open issues in the given project"""
        lbl = request.args.get('lbl', 'open issues')
        url = 'http://' + os.environ['GITLAB_HOST'] + ':' + os.environ['GITLAB_PORT'] + '/api/v4/projects/' + str(
            projid) + '/issues?state=opened&scope=all&per_page=1'
        headers = {'Private-Token': os.environ['GITLAB_SECRET']}
        trustedCertPath='./trustedCerts/'+os.environ['GITLAB_HOST']+'.crt'
        print(trustedCertPath)
        print(os.path.exists(trustedCertPath))
        if os.path.exists(trustedCertPath):
            r = requests.get(url, headers=headers,verify=trustedCertPath)
        else:
            r = requests.get(url, headers=headers)
        #    print (r.headers)
        if r.status_code != 200:
            v = r.status_code
            lbl = 'HTTP Error'
        else:
            v = r.headers['x-total']
        thresh = {5: 'green',
                  10: 'yellowgreen',
                  15: 'yellow',
                  20: 'orange',
                  25: 'red'}
        vfmt = "%d"
        badge = Badge(label=lbl, value=v, value_format=vfmt, thresholds=thresh)
        resp = make_response(badge.badge_svg_text, 200)
        resp.headers['Content-Type'] = 'image/svg+xml;charset=utf-8'
        resp.headers['Content-Disposition'] = 'attachment; filename=badge.svg'
        return resp


@ns.route('/closedIssues/<int:projid>')
@ns.param('projid', 'The project identifier')
@ns.param('lbl', 'The label for the badge - default: closed Issues')
class ClosedIssue(Resource):
    def get(self, projid):
        """
        Badge displaying the number of closed issues

        generates an SVG graphic with the specified label and the number of
        closed issues in the given project"""
        lbl=request.args.get('lbl', 'closed Issues')
        url = 'http://'+os.environ['GITLAB_HOST']+':'+os.environ['GITLAB_PORT']+'/api/v4/projects/'+str(projid)+'/issues?state=closed&scope=all&per_page=1'
        headers = {'Private-Token': os.environ['GITLAB_SECRET']}
        trustedCertPath='./trustedCerts/'+os.environ['GITLAB_HOST']+'.crt'
        print(trustedCertPath)
        print(os.path.exists(trustedCertPath))
        if os.path.exists(trustedCertPath):
            r = requests.get(url, headers=headers,verify=trustedCertPath)
        else:
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

@ns.route('/newIssues/<int:projid>')
@ns.param('projid', 'The project identifier')
@ns.param('lbl', 'The label for the badge - default: new issues')
@ns.param('weeks', 'The timespan in weeks - default: 2')
class NewIssue(Resource):
    def get(self, projid):
        """
        Badge displaying the number of new issues

        generates an SVG graphic with the specified label and the number of
        new issues in the given project and in the given timespan"""
        lbl=request.args.get('lbl', 'new issues')
        days=request.args.get('weeks', '2')
        if days is not None:
            start_date = datetime.date.today() + datetime.timedelta(-(int(days) * 7))
            dateParam = start_date.strftime('%Y-%m-%d')
            lbl = lbl + ' last ' + days + ' weeks'
            url = 'http://'+os.environ['GITLAB_HOST']+':'+os.environ['GITLAB_PORT']+'/api/v4/projects/' + str(projid) + '/issues?scope=all&created_after='+dateParam+'&per_page=1'
            headers = {'Private-Token': os.environ['GITLAB_SECRET']}
            trustedCertPath = './trustedCerts/' + os.environ['GITLAB_HOST'] + '.crt'
            print(trustedCertPath)
            print(os.path.exists(trustedCertPath))
            if os.path.exists(trustedCertPath):
                r = requests.get(url, headers=headers, verify=trustedCertPath)
            else:
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

@ns.route('/modifiedIssues/<int:projid>')
@ns.param('projid', 'The project identifier')
@ns.param('lbl', 'The label for the badge - default: issues worked on')
@ns.param('weeks', 'The timespan in weeks - default: 2')
class ModifiedIssue(Resource):
    def get(self, projid):
        """
        Badge displaying the number of modified issues

        generates an SVG graphic with the specified label and the number of
        modified issues in the given project and in the given timespan"""
        lbl = request.args.get('lbl', 'issues worked on')
        days = request.args.get('weeks', '2')
        if days is not None:
            start_date = datetime.date.today() + datetime.timedelta(-(int(days) * 7))
            dateParam = start_date.strftime('%Y-%m-%d')
            lbl = lbl + ' last ' + days + ' weeks'
            url = 'http://'+os.environ['GITLAB_HOST']+':'+os.environ['GITLAB_PORT']+'/api/v4/projects/' + str(projid) + '/issues?scope=all&updated_after='+dateParam+'&per_page=1'
            headers = {'Private-Token': os.environ['GITLAB_SECRET']}
            trustedCertPath = './trustedCerts/' + os.environ['GITLAB_HOST'] + '.crt'
            print(trustedCertPath)
            print(os.path.exists(trustedCertPath))
            if os.path.exists(trustedCertPath):
                r = requests.get(url, headers=headers, verify=trustedCertPath)
            else:
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

@ns.route('/orphanedIssues/<int:projid>')
@ns.param('projid', 'The project identifier')
@ns.param('lbl', 'The label for the badge - default: orphaned issues')
@ns.param('weeks', 'The timespan in weeks - default: 2')
class OrphanedIssue(Resource):
    def get(self, projid):
        """
        Badge displaying the number of orphaned issues

        generates an SVG graphic with the specified label of issues as default and the number of
        issues not modified in the given project and in the given timespan"""
        lbl = request.args.get('lbl', 'orphaned issues')
        days = request.args.get('weeks', '2')
        if days is not None:
            start_date = datetime.date.today() + datetime.timedelta(-(int(days) * 7))
            dateParam = start_date.strftime('%Y-%m-%d')
            lbl = lbl + ' last ' + days + ' weeks'
            url = 'http://'+os.environ['GITLAB_HOST']+':'+os.environ['GITLAB_PORT']+'/api/v4/projects/' + str(projid) + '/issues?state=opened&scope=all&updated_before='+dateParam+'&per_page=1'
            headers = {'Private-Token': os.environ['GITLAB_SECRET']}
            trustedCertPath = './trustedCerts/' + os.environ['GITLAB_HOST'] + '.crt'
            print(trustedCertPath)
            print(os.path.exists(trustedCertPath))
            if os.path.exists(trustedCertPath):
                r = requests.get(url, headers=headers, verify=trustedCertPath)
            else:
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

