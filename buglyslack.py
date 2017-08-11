# coding: utf-8

import json
import requests
from werkzeug.wrappers import BaseRequest

try:
    import gevent
except ImportError:
    gevent = None

HOMEPAGE = 'http://apidoc.haierzhongyou.com/'

BUGLY_ICON = (
    'http://image.i.haierzhongyou.com/dz/bugly/123.png'
)

class BuglySlack(object):
    def __init__(self, name='Bugly', icon=BUGLY_ICON, timeout=2):
        self.name = name
        self.icon = icon
        self.timeout = timeout

    def send_payload(self, payload, url, channel=None):
        if self.name:
            payload['username'] = self.name
        if self.icon:
            payload['icon_url'] = self.icon
        if channel:
            payload['channel'] = channel

        kwargs = dict(
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'},
            timeout=self.timeout,
        )

        if gevent:
            gevent.spawn(http_post, url, **kwargs)
        else:
            http_post(url, **kwargs)

    @staticmethod
    def create_payload(body, event):

        event_content = body["eventContent"]
        event_type = body["eventType"]

        appId = event_content["appId"]
        appName = event_content["appName"]
        happenDate = event_content["date"]
        appUrl = event_content["appUrl"]

        attachment = {}

        attachment['author_name'] = appName
        attachment['author_link'] = 'https://bugly.qq.com/v2/analytics/dashboard/4390f8350d?pid=1'

        text = u'%s %s%s <%s|%s>' % (
            happenDate,
            u'发生异常类型:', event_type,
            appUrl, appId,
        )

        attachment['text'] = text
        attachment['mrkdwn_in'] = ['text']
        return {'attachments': [attachment]}

    def __call__(self, environ, start_response):
        req = BaseRequest(environ)

        if req.method != 'POST':
            return redirect_homepage(start_response)

        # event = req.headers.get('X-Tower-Event')
        # if not event:
        #     return bad_request(start_response)

        # signature = req.headers.get('X-Tower-Signature')
        # if signature and signature[0] not in ('@', '#'):
        #     signature = None

        payload = self.create_payload(json.load(req.stream), None)
        url = 'https://hooks.slack.com/services/%s' % (req.path.lstrip('/'))
        self.send_payload(payload, url, "#software")
        return response(start_response)


def get_subject_url(project_url, event, guid):
    if event == 'topics':
        event = 'messages'
    elif event == 'documents':
        event = 'docs'
    return '%s%s/%s/' % (project_url, event, guid)


def response(start_response, code='200 OK', body='ok', headers=None):
    if headers is None:
        headers = []
    headers.extend([
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(body))),
    ])
    start_response(code, headers)
    return [body]


def redirect_homepage(start_response):
    body = 'Redirect to %s' % HOMEPAGE
    headers = [('Location', HOMEPAGE)]
    code = '301 Moved Permanently'
    return response(start_response, code, body, headers)


def bad_request(start_response):
    return response(start_response, code='400 Bad Request', body='400')


def http_post(url, **kwargs):
    requests.post(url, **kwargs)
