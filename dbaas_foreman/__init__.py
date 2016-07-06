# -*- coding: utf-8 -*-
from dbaas_foreman.dbaas_api import DatabaseAsAServiceApi
from dbaas_foreman.foreman_provider import ForemanProvider


__author__ = 'Felippe da Motta Raposo'
__email__ = 'raposo.felippe@gmail.com'
__version__ = '0.1.3'


def get_foreman_provider(databaseinfra, credentials):
    dbaas_api = DatabaseAsAServiceApi(databaseinfra, credentials)
    return ForemanProvider(dbaas_api)
