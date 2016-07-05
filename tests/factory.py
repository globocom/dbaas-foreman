# -*- coding: utf-8 -*-


class FakeForeman(object):
    def __init__(self, url, auth, api_version):
        self.url = url,
        self.auth = auth,
        self.api_version = api_version
        self.last_call = []

    def do_request(self, method, params):
        self.last_call.append({'method': method, 'params': params})

        if any((1 for key, value in params.items() if 'id' in key and value.endswith('_fails'))):
            return {}
        elif method == 'puppetclasses.show':
            if 'id' in params:
                return {'id': '171'}

        return {'something': 'new'}

    def __getattr__(self, attr):
        return ForemanMethodHandler(attr, self)


class ForemanMethodHandler(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def __getattr__(self, attr):
        def fn(*args, **kwargs):
            params = {}
            params['args'] = args
            params.update(kwargs)
            return self.parent.do_request(
                '{0}.{1}'.format(self.name, attr),
                params
            )
        return fn
