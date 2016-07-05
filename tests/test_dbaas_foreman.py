#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from dbaas_foreman.foreman_provider import ForemanProvider
from dbaas_foreman.dbaas_api import DatabaseAsAServiceApi
from dbaas_foreman import exceptions
from .factory import FakeForeman, set_up_databaseinfra, FakeCredential


def assert_last_call(foreman_provider, method, params, args=()):
    last_call = foreman_provider._foreman_client.last_call.pop()
    params.update({'args': args})

    assert last_call['method'] == method
    assert last_call['params'] == params


@pytest.fixture
def foreman_provider():
    databaseinfra = set_up_databaseinfra()
    dbaas_api = DatabaseAsAServiceApi(databaseinfra, FakeCredential())
    return ForemanProvider(
        dbaas_api=dbaas_api,
        foreman_client_class=FakeForeman
    )


def test_search_host_succesfuly(foreman_provider):
    foreman_provider._search_host('example01.does.not.exists.com')
    assert_last_call(
        foreman_provider, 'hosts.show',
        {'id': 'example01.does.not.exists.com'}
    )


def test_search_puppet_class_succesfuly(foreman_provider):
    foreman_provider._search_puppet_class('my_puppet_class')
    assert_last_call(
        foreman_provider, 'puppetclasses.show', {'id': 'my_puppet_class'}
    )


def test_add_parameter_to_host_succesfuly(foreman_provider):
    foreman_provider._add_parameter_to_host(
        'test_host', 'test_param_name', 'test_param_value'
    )

    assert_last_call(
        foreman_provider, 'hosts.parameters_create',
        {'host_id': 'test_host'},
        ({'name': 'test_param_name', 'value': 'test_param_value'},)
    )


def test_add_parameter_to_host_fails(foreman_provider):
    with pytest.raises(exceptions.HostParameterNotCreatedError):
        foreman_provider._add_parameter_to_host(
            'test_host_fails', 'test_param_name', 'test_param_value'
        )


def test_add_puppet_class_to_host_succesfuly(foreman_provider):
    foreman_provider._add_puppet_class_to_host(
        'test_host', 'my_puppet_class_with_id'
    )

    assert_last_call(
        foreman_provider, 'hosts.host_classes_create',
        {'host_id': 'test_host', 'puppetclass_id': '171'},
    )


def test_add_puppet_class_to_host_puppet_class_not_found(foreman_provider):
    with pytest.raises(exceptions.PuppetClassNotFound):
        foreman_provider._add_puppet_class_to_host(
            'test_host', 'my_puppet_class_with_id_fails'
        )


def test_add_puppet_class_to_host_puppet_class_not_created_error(foreman_provider):
    with pytest.raises(exceptions.HostPuppetClassNotCreatedError):
        foreman_provider._add_puppet_class_to_host(
            'test_host_fails', 'my_puppet_class_with_id'
        )
