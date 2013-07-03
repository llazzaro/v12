import logging

class Response(object):
    """ Abstract response
    """
 
    @classmethod
    def get(cls, url, headers, status, body):
        return cls(url=url, headers=headers, status=status, body=body)

    def __init__(self, url, headers, status, body):
        self.url = url
        self.headers = headers
        self.status = status
        self.body = body

    def info(self):
        return self

    def read(self):
        return self.body

    def getheaders(self, name):
        return self.headers.getlist(name)
