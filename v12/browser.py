# -*- coding: utf-8 -*-

import logging



from zope.interface import implements

from twisted.python.log import err
from twisted.web.iweb import IBodyProducer
from twisted.internet import defer
from twisted.python import log
from twisted.internet.protocol import Protocol

from http.parser import HTTPParser
from http.client import v12HTTPAgent
from http.header import Headers

class BeginningPrinter(Protocol):
    def __init__(self, finished, browser):
        self.finished = finished
        self.browser = browser
        self.response_data = ''

    def dataReceived(self, bytes):
        self.response_data += bytes#[:self.remaining]

    def connectionLost(self, reason):
        self.browser.response_received(self.response_data)
        self.finished.callback(None)

class StringProducer(object):
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return defer.succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass

class Response(object):

    def __init__(self, data):
        self.data = data

    def read(self):
        return self.data


class Browser(object):
    
    def __init__(self, url=None):
        self.url = url
        self._forms = {}
        self.agent = v12HTTPAgent()#RedirectAgent(CookieAgent((Agent(reactor)),
        self.response_data = ''
        self.form = None
        #self.cookies = []
        self.addheaders = []

    def _response_received(self, response):
        finished = defer.Deferred()
#        response.deliverBody(BeginningPrinter(finished, self))
        return finished

    def response_received(self, response_data):
        self.response_data = response_data

    def set_proxies(self, proxy):
        pass

    def set_cookiejar(self, cookiejar):
        pass

    def set_handle_equiv(self, handler):
        pass

    def set_handle_redirect(self, handle):
        pass

    def set_handle_referer(self, handle):
        pass

    def set_handle_robots(self, handle):
        pass

    def set_handle_refresh(self, handle):
        pass

    def _prepare_headers(self):
        headers = Headers()
        for key, value in self.addheaders:
            headers.add(key, value)

#        if self.cookies:
#            logging.debug('Prepare headers cookies : %s' % self.cookies)
#            headers.add('Cookie', ';'.join(self.cookies))
        headers.add('Accept', ['text/html, text/plain, text/css, text/sgml, */*;q=0.01'])
        headers.add('Pragma', ['no-cache'])
        headers.add('Cache-Control', ['no-cache'])
        if self.form:
            headers.add('Content-type', self.form.content_type())

        return headers

    @defer.inlineCallbacks
    def open(self, url):
        logging.debug('Opening URL %s' % url)
        url = str(url)
        self.url = url
        response = yield self.agent.request(
                            'GET',
                            url,
                            self._prepare_headers(),
                            None)

#        for set_cookie in response.headers.get('Set-Cookie') or []:
#            self.cookies.extend(set_cookie.split(';'))
            
        self._response = response
        self._find_controls(response)
#        defer.returnValue(self._response_received(response))
#        d.addErrback(log.err)

    def links(self):
        return self._links

    def forms(self):
        return self._forms

    @defer.inlineCallbacks
    def submit(self, data=None, method='POST', action=None, name=None):
        logging.debug('Submit %s' % method)
        if self.form is None:
            raise Exception("Select a form first")

        selected_form = self.form
        if action:
            form_action = action
        else:
            form_action = self.form.action
        
        data = selected_form.data()
        logging.debug('data body %s' % data)

        if method == 'POST':
            response = yield self.agent.request(
                    method,
                    form_action,
                    self._prepare_headers(),
                    data)

        if method == 'GET':
            response = yield self.agent.request(
                    method,
                    self.url+ '/#' + data,#TODO CHECK URL
                    self._prepare_headers())

#        for set_cookie in response.headers.get('Set-Cookie') or []:
#            self.cookies.extend(set_cookie.split(';'))

        self._response = response
        self._find_controls(response)
        self._response_received(response)

        if response.status in [301, 302, 303, 307] and 'Location' in response.headers:
            #raise NotImplementedError
            yield self.open(response.headers['Location'][0])


    def _find_controls(self, response):
        parser = HTTPParser()
        parser.feed(response)
        self._forms = parser.forms
        self._links = parser.links
#        for (name, action, method, enctype), ettrs, controls in form_parser.forms:
#            pass
    
    def response(self):
        return self._response

    def select_form(self, nr=None, name=None, action=None):
        if nr:
            for order_no, form in self._forms:
                if nr == order_no:
                    self.form = form
        if name:
            for order_no, form in self._forms:
                if form.name == name:
                    self.form = form
        if action:
            for order_no, form in self._forms:
                if form.action == action:
                    self.form = form


    def new_control(self, one, two, three):
        pass

    def fixup(self):
        pass
