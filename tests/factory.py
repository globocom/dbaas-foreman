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


class Host(object):
    def __init__(self, address, dns):
        self.address = address
        self.hostname = dns


class Engine(object):
    def __init__(self, name, version='0.0.0'):
        self.engine_type = EngineType(name)
        self.version = version


class EngineType(object):
    def __init__(self, name):
        self.name = name


class Plan(object):
    def __init__(self, is_ha):
        self.is_ha = is_ha


class Instance(object):
    def __init__(self, dns, hostname):
        self.address = hostname.address
        self.dns = dns
        self.hostname = hostname


class Driver(object):
    def __init__(self, databaseinfra):
        self.databaseinfra = databaseinfra

    def get_database_instances(self):
        return self.databaseinfra.instances

    def get_non_database_instances(self):
        return self.databaseinfra.instances


class DatabaseInfra(object):
    def __init__(self, instances, environment, plan, name):
        self.instances = instances
        self.environment = environment
        self.name = name
        self.engine = Engine(name)
        self.plan = plan

    def get_driver(self):
        if hasattr(self, 'driver'):
            return self.driver

        self.driver = Driver(self)
        return self.driver


class InstanceList(list):
    def all(self):
        return self


def set_up_databaseinfra(is_ha=True, name="fake"):
    instances = InstanceList()
    plan = Plan(is_ha)
    for n in range(1, 4):
        address = '10.10.10.1{}'.format(n)
        dns = 'myhost_{}'.format(n)
        host = Host(address, dns + '.com')

        instance = Instance(dns + '.database.com', host)
        instances.append(instance)

    return DatabaseInfra(instances, 'development', plan, name)


class FakeCredential(object):
        def __init__(self):
            self.user = ''
            self.password = ''
            self.endpoint = ''

        def get_parameter_by_name(self, name):
            return ''

        def get_parameters_by_group(self, group_name):
            return {}
