# -*- coding: utf-8 -*-
import logging
from time import sleep
from foreman.client import (Foreman, ForemanException)
from dbaas_foreman import exceptions

LOG = logging.getLogger(__name__)


class ForemanProvider(object):
    def __init__(self, dbaas_api, api_version=2, foreman_client_class=Foreman):
        self._dbaas_api = dbaas_api
        self._foreman_url = self._dbaas_api.endpoint
        self._foreman_username = self._dbaas_api.user
        self._foreman_password = self._dbaas_api.password
        self._api_version = api_version
        self._foreman_client_class = foreman_client_class

        self._foreman_client = self._init_foreman_client()

    def _init_foreman_client(self):
        try:
            result = self._foreman_client_class(
                url=self._foreman_url,
                auth=(self._foreman_username, self._foreman_password),
                api_version=self._api_version
            )
        except ForemanException as e:
            LOG.warn(e)
            result = None

        return result

    def _do_show(self, resource, resource_id):
        try:
            result = getattr(
                self._foreman_client, resource
            ).show(id=resource_id)
        except ForemanException as e:
            LOG.warn(e)
            result = {}

        return result

    def _search_host(self, host_name):
        return self._do_show(resource='hosts', resource_id=host_name)

    def _search_puppet_class(self, puppet_class_name):
        return self._do_show(
            resource='puppetclasses', resource_id=puppet_class_name
        )

    def _add_puppet_class_to_host(self, host_name, puppet_class_name):
        puppet_class = self._search_puppet_class(puppet_class_name)

        if not puppet_class:
            raise exceptions.PuppetClassNotFound

        response = self._foreman_client.hosts.host_classes_create(
            host_id=host_name,
            puppetclass_id=puppet_class['id']
        )

        if not response:
            raise exceptions.HostPuppetClassNotCreatedError()

    def _add_parameter_to_host(self, host_name, parameter_name, parameter_value):
        parameters = {'name': parameter_name, 'value': parameter_value}

        response = self._foreman_client.hosts.parameters_create(
            parameters, host_id=host_name
        )

        if not response:
            raise exceptions.HostParameterNotCreatedError()

    def setup_database_dscp(
        self, fqdn, vip_ip, dsrc, port, attempts=50, sleep_time=10
    ):
        puppet_class_name = self._dbaas_api.dscp_foreman_class
        dscp_foreman_param_name = self._dbaas_api.dscp_foreman_param_name
        dscp_foreman_param_value = '{}:{}:{}'.format(vip_ip, dsrc, port)

        attempt = 0
        while attempt <= attempts:
            attempt += 1
            try:
                response = self._search_host(fqdn)
            except Exception as e:
                LOG.warn(e)
            else:
                if response:
                    self._add_puppet_class_to_host(fqdn, puppet_class_name)
                    self._add_parameter_to_host(
                        fqdn, dscp_foreman_param_name, dscp_foreman_param_value
                    )
                    return True

            sleep(sleep_time)
        else:
            raise exceptions.HostNotFoundException(
                "Host {} not found".format(fqdn)
            )
