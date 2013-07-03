from urlparse import urlparse

class Request(object):
    """ 
        This request object must support the methods :
            get_full_url(), get_host(), get_type(), unverifiable(),
            get_origin_req_host(), has_header(), get_header(), header_items(), and
            add_unredirected_header(), as documented by urllib2.

    """

    def __init__(self, url, headers, method, cookies, body=None,
            encoding='utf-8', meta=None):
        self.headers = headers
        self.cookies = cookies 
        self.url = str(url)
        parsed_url = urlparse(url)
        self.host = parsed_url.netloc
        self.headers.add('Host', self.host)
        self.hostname = parsed_url.hostname
        self.scheme = parsed_url.scheme
        self.path = parsed_url.path
        self.method = method
        self.body = body
        self.cookies.add_cookie_header(self)

    def get_full_url(self):
        return self.url

    def get_host(self):
        return self.host

    def get_type(self):
        return self.request_type

    def is_unverifiable(self):
        """RFC 2965
        """
        return False

    def get_origin_req_host(self):
        return self.hostname

    def has_header(self, name):
        return name in self.headers

    def get_header(self, name, default=None):
        self.headers.get(name, default)

    def header_items(self):
        return self.headers.items()

    def add_unredirected_header(self, name, value):
        self.headers.add(name, value)

    def __str__(self):
        return self.url

    def strip(self):
        return self.url
