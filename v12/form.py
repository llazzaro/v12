import random
import urllib


class Form(dict):

    def __init__(self,name, method, action):
        self.name = name
        self.method = method
        self.action = action
        self.controls = []
        for control in self.controls:
            self.__setattr__(control.name, control.value)

    def __repr__(self):
        dict_str = super(Form, self).__repr__()
        return 'Form %s %s %s \n %s' % (self.name, self.method, self.action, dict_str)

    def data(self):
        raise NotImplementedError

class FormApplication(Form):

    def __init__(self, name, method, action):
        super(FormApplication, self).__init__(name, method, action)
        self.enctype = 'application/x-www-form-urlencoded'

    def content_type(self):
        return self.enctype

    def data(self):
        data = {}
        for control in self.values():
            try:
                data.update({control.name: control.value})
            except Exception:
                pass
        data = urllib.urlencode(data)
        return data

class FormMultiPart(Form):
    
    def __init__(self, name, method, action):
        super(FormMultiPart, self).__init__(name, method, action)
        rand_strs = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz1234567890') for i in xrange(30))
        self.boundary = 'sarasa%s' % rand_strs 
        self.enctype = 'multipart/form-data'
        self.contenttype = ', '.join([self.enctype, 'boundary=' + self.boundary])

    def content_type(self):
        return self.contenttype

    def data(self):
        import logging
        logging.debug('FormMultiPart values %s' % self.values())
        values = []
        for control in self.values():
            if control.value:
                data = ''
                logging.debug('Add data %s' % control)
                data += 'Content-Disposition: form-data;name=\"%s\" \r\n\r\n' % control.name
                data += '%s' % control.value
                values.append(data)
        data = ('\r\n--%s\r\n' % self.boundary).join(values)
        data += '\r\n--%s--\r\n' % self.boundary
        return data

