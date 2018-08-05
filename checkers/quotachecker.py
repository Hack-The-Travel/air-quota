# -*- coding: utf-8 -*-
import os
import requests
from jinja2 import Environment, FileSystemLoader

here = os.path.dirname(os.path.abspath(__file__))


class QuotaResponse(object):
    def __init__(self):
        self.tickets: int = None
        self.emds: int = None


class QuotaChecker(object):
    def __init__(self, template_dir: str = None):
        #: String contains text of HTTP body request
        self.last_sent = None

        #: Content of the response, in bytes
        self.last_received = None

        #: Requests template environment
        self.__template_env = None
        if template_dir is not None:
            template_dir = os.path.join(here, template_dir)
            self.__template_env = Environment(loader=FileSystemLoader(template_dir))

    def get_quota(self) -> QuotaResponse:
        raise NotImplementedError

    def render_template(self, template_filename: str, context: dict = None) -> str:
        """Renders a template into a string.

        To use this method you must set `template_dir` argument of `__init__()` method.
        """
        context = {} if context is None else context
        template = self.__template_env.get_template(template_filename)
        return template.render(context)

    def request(self, url: str, method: str = 'post', auth=None, headers=None, data=None) -> str:
        r = requests.request(method, url, auth=auth, headers=headers, data=data)
        self.last_sent = data
        self.last_received = r.content
        r.raise_for_status()
        return r.text  # content of the response, in unicode
