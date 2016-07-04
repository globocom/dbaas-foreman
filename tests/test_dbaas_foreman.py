#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from dbaas_foreman.foreman_provider import ForemanProvider
from .factory import FakeForeman


def assert_last_call(foreman_provider, method, params):
    assert foreman_provider._foreman_client.last_call['method'] == method
    assert foreman_provider._foreman_client.last_call['params'] == params


@pytest.fixture
def foreman_provider():
    return ForemanProvider(
        foreman_url='http://example.does.not.exists.com',
        foreman_username='a_ruby_fan_boy',
        foreman_password='I am',
        foreman_client_class=FakeForeman
    )


def test_search_host_succesfuly(foreman_provider):
    foreman_provider._search_host('example01.does.not.exists.com')
    assert_last_call(
        foreman_provider, 'hosts.show',
        {"id": "example01.does.not.exists.com"}
    )


def test_search_puppet_class_succesfuly(foreman_provider):
    foreman_provider._search_puppet_class('my_puppet_class')
    assert_last_call(
        foreman_provider, 'puppetclasses.show', {"id": "my_puppet_class"}
    )
