# -*- coding: utf-8 -*-


class DatabaseAsAServiceApi(object):
    def __init__(self, databaseinfra, credentials):
        self.databaseinfra = databaseinfra
        self.credentials = credentials

    @property
    def user(self):
        return self.credentials.user

    @property
    def password(self):
        return self.credentials.password

    @property
    def endpoint(self):
        return self.credentials.endpoint

    @property
    def dscp_foreman_class(self):
        return self.credentials.get_parameter_by_name('dscp_foreman_class')

    @property
    def dscp_foreman_param_name(self):
        return self.credentials.get_parameter_by_name('dscp_foreman_param_name')
