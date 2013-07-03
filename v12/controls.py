
class Link(dict):
    pass

class Input(object):
    pass

class TextArea(object):

    @classmethod
    def create(cls, attrs):
        name = None
        for key, value in attrs:
            if key == "name":
                name = value

        return cls(name)

    def __init__(self, name):
        self.name = name

class InputText(Input):

    @classmethod
    def create(cls, attrs):
        name = None
        for key, value in attrs:
            if key == "name":
                name = value

        return cls(name)

    def __init__(self, name):
        self.name = name
        self.value = None

class InputHidden(Input):

    @classmethod
    def create(cls, attrs):
        hidden_value = None
        for key, value in attrs:
            if key == "name":
                name = value
            elif key == "value":
                hidden_value = value

        return cls(name, hidden_value)

    def __init__(self, name, value):
        self.name = name
        self.value = value

class InputPassword(InputText):
    pass

class CheckBox(Input):

    @classmethod
    def create(cls, attrs):
        for key, value in attrs:
            if key == "name":
                name = value

        return cls(name)

    def __init__(self, name):
        self.name = name
        self.value = False


class InputSource(Input):

    @classmethod
    def create(cls, attrs):
        raise NotImplementedError

class Select(object):

    @classmethod
    def create(cls, attrs):
        name = None
        for key, value in attrs:
            if key == "name":
                name = value

        return cls(name)

    def __init__(self, name):
        self.name = name
        self._options = []

    def add_option(self, option):
        if len(self._options) == 0:
            self.value = option.value
        self._options.append(option)


class Option(object):

    @classmethod
    def create(cls, attrs):
        text = None
        option_value = None
        for key, value in attrs:
            if key == "value":
               option_value = value
            if key == "text":
                text = value

        return cls(text, option_value)

    def __init__(self, text, option_value):
        self.text = text
        self.value = option_value

class Radio(object):

    @classmethod
    def create(cls, attrs):
        pass
        #raise NotImplementedError

class File(object):

    @classmethod
    def create(cls, attrs):
        pass
        #raise NotImplementedError

class Image(object):

    @classmethod
    def create(cls, attrs):
        import logging
        logging.debug('IMAGE attrs %s' % attrs)
        for key, value in attrs:
            if key == 'src':
                src = value

        return cls(src)

    def __init__(self, src):
        self.src = src

class Submit(object):

    @classmethod
    def create(cls, attrs):
        name_attr = None
        value_attr = None

        for key, value in attrs:
            if key == "value":
                value_attr = value
            if key == "name":
                name_attr = value

        return cls(name_attr, value_attr)

    def __init__(self, name, value):
        self.value = value
        self.name = name

    def click(self):
        raise NotImplementedError

class Button(object):

    @classmethod
    def create(cls, attrs):
        return cls()

    def __init__(self):
        pass

    def click(self):
        raise NotImplementedError

