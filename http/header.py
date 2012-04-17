# -*- coding: utf-8 -*-
import logging

class Headers(dict):
    
    def __init__(self, properties=None):
        self.encoding = 'utf-8'
        if properties:
            self.update(properties)
        self.update({
#                        "Accept-Encoding" : ["gzip,deflate,sdhc"],
                        "Accept-Lenguage" : ["en-US,en;q=0.8"],
                    })
        #self.add('UserAgent', user_agent)
        #super(Headers, self).__init__(seq)


    def __getitem__(self, key):
        try:
            return super(Headers, self).__getitem__(key)
        except IndexError:
            return None

    def normvalue(self, value):
        if not hasattr(value, '__iter__'): 
            value = [value]
        return [x.encode(self.encoding) if isinstance(x, unicode) else x \
                                                                    for x in value]

    def get(self, key, def_val=None):
        try:
            return super(Headers, self).get(key, def_val)
        except IndexError:
            return None

    def getlist(self, key, def_val=None):
        try:
            return super(Headers, self).__getitem__(key)
        except KeyError:
            if def_val is not None:
                return self.normvalue(def_val)
            return []

    def setlist(self, key, list_):
        self[key] = list_

    def add(self, key , value):
        lst = self.getlist(key)
        lst.extend(self.normvalue(value))
        self[key] = lst

    def items(self):
        return list(self.iteritems())

    def iteritems(self):
        return ((k, self.getlist(k)) for k in self.keys())

    def values(self):
        return [self[k] for k in self.keys()]

    def to_string(self):
        pass
#        return headers_dict_to_raw(self)

    def __copy__(self):
        return self.__class__(self)

    copy = __copy__
