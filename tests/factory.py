# -*- coding: utf-8 -*-


class FakeForeman(object):
    def __init__(self, url, auth, api_version):
        self.url = url,
        self.auth = auth,
        self.api_version = api_version
        self.last_call = None

    def do_request(self, method, params):
        self.last_call = {"method": method, "params": params}
        return {}

    def __getattr__(self, attr):
        return ForemanMethodHandler(attr, self)


class ForemanMethodHandler(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def __getattr__(self, attr):
        def fn(*args, **kwargs):
            if args and kwargs:
                raise TypeError("Found both args and kwargs")
            return self.parent.do_request(
                '{0}.{1}'.format(self.name, attr),
                args or kwargs
            )
        return fn
