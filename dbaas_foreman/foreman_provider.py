# -*- coding: utf-8 -*-
import logging
from foreman.client import (Foreman, ForemanException)
from dbaas_foreman import exceptions

LOG = logging.getLogger(__name__)


class ForemanProvider(object):
    def __init__(
        self, foreman_url, foreman_username, foreman_password, api_version=2,
        foreman_client_class=Foreman
    ):
        self._foreman_url = foreman_url
        self._foreman_username = foreman_username
        self._foreman_password = foreman_password
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
