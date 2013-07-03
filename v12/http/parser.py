# -*- coding: utf-8 -*-
import sgmllib

from v12.controls import Link
from v12.controls import File
from v12.controls import Image
from v12.controls import Radio
from v12.controls import Submit
from v12.controls import Button
from v12.controls import Select
from v12.controls import Option
from v12.controls import TextArea
from v12.controls import CheckBox
from v12.controls import InputText
from v12.controls import InputHidden
from v12.controls import InputPassword

from v12.form import FormApplication
from v12.form import FormMultiPart


CONTROLS = {
    "text": InputText,
    "hidden": InputHidden,
    "submit": Submit,
    "button": Button,
    "password": InputPassword,
    "checkbox": CheckBox,
    "radio": Radio,
    "file": File,
    "image": Image,
    "textarea": TextArea,
    "select": Select,
    "option": Option,
}

FORMS = {
    "application/x-www-form-urlencoded": FormApplication,
    "multipart/form-data": FormMultiPart,
}


class HTTPParser(sgmllib.SGMLParser):

    def __init__(self):
        sgmllib.SGMLParser.__init__(self)
        self.forms = []
        self.links = []
        self.form_nr = 0

    def feed(self, data):
        try:
            sgmllib.SGMLParser.feed(self, data.body)
        except sgmllib.SGMLParseError, exc:
            raise sgmllib.ParseError(exc)


    def start_label(self, attrs):
        pass

    def start_textarea(self, attrs):
        control = CONTROLS.get('textarea')
        if control is None:
            raise Exception("Control not Supported textarea")
        control_obj = control.create(attrs)
        self._form[control_obj.name] = control_obj

    def start_select(self, attrs):
        import logging
        logging.debug('Parsing select %s' % attrs)
        control = CONTROLS.get('select')
        if control is None:
            raise Exception("Control not Supported select")
        control_obj = control.create(attrs)
        try:
            self._form[control_obj.name] = control_obj
        except Exception:
            pass
        self._select = control_obj

    def start_option(self, attrs):
        import logging
        logging.debug('Option %s' % attrs)
        attrs.append(('text', self.get_starttag_text()))
        control = CONTROLS.get('option')
        if control is None:
            raise Exception("Control not Supported option")
        control_obj = control.create(attrs)
        self._select.add_option(control_obj)

    def end_select(self):
        self._select = None

    def start_input(self, attrs):
        for key, value in attrs:
            if key == "type":
                control = CONTROLS.get(value)
                if control is None:
                    raise Exception("Control not Supported %s" % value)
                control_obj = control.create(attrs)
                try:
                    self._form[control_obj.name] = control_obj
                except Exception:
                    pass

    def start_form(self, attrs):
        """ This method is called to process an opening tag form.
        """
        name = None
        action = None
        form_id = None
        enctype = None
        method = None
        for key, value in attrs:
            if key == "name":
                name = value#self.unescape_attr_if_required(value)
            elif key == "method":
                method = value.upper()
            elif key == "action":
                action = value
            elif key == "enctype":
                enctype = value
            elif key == "id":
                form_id = value

        if name is None and form_id:
            name = form_id
        if name is None and form_id is None:
            name = action

        self._form_name = name
        form_cls = FORMS.get(enctype, FormApplication)
        self._form = form_cls(name=name, action=action, method=method)

    def end_form(self):
        self.forms.append((self.form_nr, self._form))
        self.form_nr += 1

    def start_a(self, attrs):
        self.links.append(Link(attrs))
