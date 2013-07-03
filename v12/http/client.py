from time import time
from urlparse import urlparse
import logging

from cookielib import CookieJar
from twisted.python import failure
from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet.ssl import ClientContextFactory
from twisted.web.client import HTTPClientFactory
from twisted.web.client import PartialDownloadError
from twisted.web.http import HTTPClient

from response import Response
from request import Request
from header import Headers

class v12HTTPPageGetter(HTTPClient):

    delimiter = '\n'
    
    def connectionMade(self):
        self.headers = Headers()
        query = ''
        if len(self.factory.query) > 0:
            query = '?' + self.factory.query
        self.sendCommand(self.factory.method, self.factory.path + query)

        # Headers
        for key, values in self.factory.headers.iteritems():
            logging.debug('Header incoming key %s value %s' % (key, values))
            if type(values) == str:
                values = [values]
            for value in values:
                self.sendHeader(key, value)     
        self.endHeaders()      
        # Body
        if self.factory.body is not None:
            self.transport.write(str(self.factory.body))
    
    def lineReceived(self, line):
        return HTTPClient.lineReceived(self, line.rstrip())

    def handleHeader(self, key, value):
        self.headers.add(key, value)

    def handleEndHeaders(self):
        self.factory.gotHeaders(self.headers)
 
    def connectionLost(self, reason):
        HTTPClient.connectionLost(self, reason)
        self.factory.noPage(reason)

    def handleStatus(self, version, status, message):
        logging.debug('Response status %s' % status)
        self.factory.gotStatus(version, status, message)

    def handleResponse(self, response):
        if self.factory.method.upper() == 'HEAD':
            self.factory.page('')
        elif self.length != None and self.length != 0:
            self.factory.noPage(failure.Failure(PartialDownloadError(self.factory.status, None, response)))
        else:
            self.factory.page(response)
        self.transport.loseConnection()

    def timeout(self):
        self.transport.loseConnection()
        self.factory.noPage(\
                defer.TimeoutError("Getting %s took longer than %s seconds." % \
                                            (self.factory.url, self.factory.timeout)))

class v12HTTPClientFactory(HTTPClientFactory):

    protocol = v12HTTPPageGetter
    waiting = 1 
    noisy = False
    followRedirect = False
    afterFoundGet = False

    def __init__(self, request):
        HTTPClientFactory.__init__(self, request)
        
        self.method = request.method
        self.body = request.body or None
        self.headers = request.headers
        self.cookies = request.cookies
        
        self.start_time = time()
        self.status = None
        #self.deferred.addCallback(
        #        lambda data: (data, self.status, self.response_headers))
        self._set_connection_attributes(request)
        self.deferred = defer.Deferred().addCallback(self._build_response, request)

        if self.body is not None:
            self.headers['Content-length'] = [len(self.body)]
            # just in case a broken http/1.1 decides to keep connection alive
            self.headers.setdefault("Connection", "close")

    def _build_response(self, body, request):
        logging.debug('BUILD RESPONSE %s' % request)
        status = int(self.status)
        return Response.get(self.url, self.response_headers, status, body)

    def gotHeaders(self, headers):
        self.response_headers = headers

    def _set_connection_attributes(self, request):
        parsed_url = urlparse(request.url)
        self.scheme, self.netloc, self.path, self.host, self.query = (parsed_url.scheme,
                parsed_url.netloc, parsed_url.path, parsed_url.hostname,
                parsed_url.query)
        self.port = 80
        if self.scheme == 'https':
            self.port = 443
#        proxy = request.meta.get('proxy')
#        if proxy:
#            self.scheme, _,self.host, self.port, _= _parse(proxy) self.path = self.url

#    def noPage(self, reason):
#        if self.status == '304': #Page hadnt changed
#            HTTPClientFactory(self, '')
#        else:
#            HTTPClientFactory.noPage(self, reason)

#    def checkStatus(self, contextFactory=None, *args, **kwargs):
#        pass


class v12HTTPAgent(object):
    
    def __init__(self):
        self.cookies = CookieJar()

    def inspect_cookies(self, response):
        self.cookies.extract_cookies(response, self._request)
        return response

    def request(self, method, url, headers, body=None):
        self._request = Request(method=method, url=url, headers=headers,
                                        cookies=self.cookies, body=body)
        factory = v12HTTPClientFactory(self._request)
        if factory.scheme == 'https':
            reactor.connectSSL(self._request.host, 443, factory, ClientContextFactory())
        else:
            reactor.connectTCP(self._request.host, 80, factory)

        factory.deferred.addCallback(self.inspect_cookies)
        return factory.deferred
