# -*- coding: utf-8 -*-
# (c) 2021, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

__metaclass__ = type


import pytest

from ansible_collections.community.internal_test_tools.tests.unit.compat.mock import MagicMock, patch

from ansible_collections.community.internal_test_tools.tests.unit.plugins.modules.utils import (
    set_module_args,
    ModuleTestCase,
    AnsibleExitJson,
    # AnsibleFailJson,
)

from ansible_collections.felixfontein.tools.plugins.modules import wait_for_txt

from ..module_utils.resolver_helper import (
    mock_resolver,
    mock_query_udp,
    create_mock_answer,
    create_mock_response,
)

# We need dnspython
dns = pytest.importorskip('dns')


def mock_sleep(delay):
    pass


class TestWaitForTXT(ModuleTestCase):
    def test_single(self):
        resolver = mock_resolver(['1.1.1.1'], {
            ('1.1.1.1', ): [
                {
                    'target': 'ns.com',
                    'lifetime': 10,
                    'result': create_mock_answer(dns.rrset.from_rdata(
                        'ns.com',
                        300,
                        dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.A, '2.2.2.2'),
                    )),
                },
                {
                    'target': 'ns.example.com',
                    'lifetime': 10,
                    'result': create_mock_answer(dns.rrset.from_rdata(
                        'ns.example.com',
                        300,
                        dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.A, '3.3.3.3'),
                    )),
                },
                {
                    'target': 'ns.org',
                    'lifetime': 10,
                    'result': create_mock_answer(dns.rrset.from_rdata(
                        'ns.com',
                        300,
                        dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.A, '2.2.3.3'),
                    )),
                },
                {
                    'target': 'ns.example.org',
                    'lifetime': 10,
                    'result': create_mock_answer(dns.rrset.from_rdata(
                        'ns.example.org',
                        300,
                        dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.A, '4.4.4.4'),
                    )),
                },
            ],
            ('3.3.3.3', '4.4.4.4', ): [
                {
                    'target': dns.name.from_unicode(u'example.org'),
                    'rdtype': dns.rdatatype.TXT,
                    'lifetime': 10,
                    'result': create_mock_answer(dns.rrset.from_rdata(
                        'example.org',
                        300,
                        dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.TXT, 'asdf'),
                    )),
                },
            ],
        })
        udp_sequence = [
            {
                'query_target': dns.name.from_unicode(u'com'),
                'query_type': dns.rdatatype.NS,
                'nameserver': '1.1.1.1',
                'kwargs': {
                    'timeout': 10,
                },
                'result': create_mock_response(dns.rcode.NOERROR, answer=[dns.rrset.from_rdata(
                    'com',
                    3600,
                    dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.NS, 'ns.com'),
                )]),
            },
            {
                'query_target': dns.name.from_unicode(u'example.com'),
                'query_type': dns.rdatatype.NS,
                'nameserver': '1.1.1.1',
                'kwargs': {
                    'timeout': 10,
                },
                'result': create_mock_response(dns.rcode.NOERROR, answer=[dns.rrset.from_rdata(
                    'example.com',
                    3600,
                    dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.NS, 'ns.example.com'),
                )], cname=dns.name.from_unicode(u'example.com')),
            },
            {
                'query_target': dns.name.from_unicode(u'www.example.com'),
                'query_type': dns.rdatatype.NS,
                'nameserver': '1.1.1.1',
                'kwargs': {
                    'timeout': 10,
                },
                'result': create_mock_response(dns.rcode.NOERROR, answer=[dns.rrset.from_rdata(
                    'www.example.com',
                    3600,
                    dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.SOA, 'ns.example.com. ns.example.com. 12345 7200 120 2419200 10800'),
                )], cname=dns.name.from_unicode(u'example.org')),
            },
            {
                'query_target': dns.name.from_unicode(u'org'),
                'query_type': dns.rdatatype.NS,
                'nameserver': '1.1.1.1',
                'kwargs': {
                    'timeout': 10,
                },
                'result': create_mock_response(dns.rcode.NOERROR, answer=[dns.rrset.from_rdata(
                    'org',
                    3600,
                    dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.NS, 'ns.org'),
                )]),
            },
            {
                'query_target': dns.name.from_unicode(u'example.org'),
                'query_type': dns.rdatatype.NS,
                'nameserver': '1.1.1.1',
                'kwargs': {
                    'timeout': 10,
                },
                'result': create_mock_response(dns.rcode.NOERROR, answer=[dns.rrset.from_rdata(
                    'example.org',
                    3600,
                    dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.NS, 'ns.example.org'),
                    dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.NS, 'ns.example.com'),
                )]),
            },
        ]
        with patch('dns.resolver.get_default_resolver', resolver):
            with patch('dns.resolver.Resolver', resolver):
                with patch('dns.query.udp', mock_query_udp(udp_sequence)):
                    with patch('time.sleep', mock_sleep):
                        with pytest.raises(AnsibleExitJson) as exc:
                            set_module_args({
                                'records': [
                                    {
                                        'name': 'www.example.com',
                                        'values': [
                                            'asdf',
                                        ]
                                    },
                                ],
                            })
                            wait_for_txt.main()

        print(exc.value.args[0])
        assert exc.value.args[0]['changed'] is False
        assert exc.value.args[0]['completed'] == 1
        assert len(exc.value.args[0]['records']) == 1
        assert exc.value.args[0]['records'][0]['name'] == 'www.example.com'
        assert exc.value.args[0]['records'][0]['done'] is True
        assert exc.value.args[0]['records'][0]['values'] == ['asdf']
        assert exc.value.args[0]['records'][0]['check_count'] == 1

    def test_double(self):
        resolver = mock_resolver(['1.1.1.1'], {
            ('1.1.1.1', ): [
                {
                    'target': 'ns.com',
                    'lifetime': 10,
                    'result': create_mock_answer(dns.rrset.from_rdata(
                        'ns.com',
                        300,
                        dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.A, '2.2.2.2'),
                    )),
                },
                {
                    'target': 'ns.example.com',
                    'lifetime': 10,
                    'result': create_mock_answer(dns.rrset.from_rdata(
                        'ns.example.com',
                        300,
                        dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.A, '3.3.3.3'),
                    )),
                },
            ],
            ('3.3.3.3', ): [
                {
                    'target': dns.name.from_unicode(u'www.example.com'),
                    'rdtype': dns.rdatatype.TXT,
                    'lifetime': 10,
                    'result': create_mock_answer(dns.rrset.from_rdata(
                        'www.example.com',
                        300,
                        dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.TXT, 'fdsa'),
                    )),
                },
                {
                    'target': dns.name.from_unicode(u'mail.example.com'),
                    'rdtype': dns.rdatatype.TXT,
                    'lifetime': 10,
                    'result': create_mock_answer(dns.rrset.from_rdata(
                        'mail.example.com',
                        300,
                        dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.TXT, '"any bar"'),
                    )),
                },
                {
                    'target': dns.name.from_unicode(u'www.example.com'),
                    'rdtype': dns.rdatatype.TXT,
                    'lifetime': 10,
                    'result': create_mock_answer(dns.rrset.from_rdata(
                        'www.example.com',
                        300,
                        dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.TXT, 'fdsa'),
                        dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.TXT, 'asdf'),
                    )),
                },
                {
                    'target': dns.name.from_unicode(u'www.example.com'),
                    'rdtype': dns.rdatatype.TXT,
                    'lifetime': 10,
                    'result': create_mock_answer(dns.rrset.from_rdata(
                        'www.example.com',
                        300,
                        dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.TXT, 'asdf'),
                    )),
                },
            ],
        })
        udp_sequence = [
            {
                'query_target': dns.name.from_unicode(u'com'),
                'query_type': dns.rdatatype.NS,
                'nameserver': '1.1.1.1',
                'kwargs': {
                    'timeout': 10,
                },
                'result': create_mock_response(dns.rcode.NOERROR, answer=[dns.rrset.from_rdata(
                    'com',
                    3600,
                    dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.NS, 'ns.com'),
                )]),
            },
            {
                'query_target': dns.name.from_unicode(u'example.com'),
                'query_type': dns.rdatatype.NS,
                'nameserver': '1.1.1.1',
                'kwargs': {
                    'timeout': 10,
                },
                'result': create_mock_response(dns.rcode.NOERROR, answer=[dns.rrset.from_rdata(
                    'example.com',
                    3600,
                    dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.NS, 'ns.example.com'),
                )], cname=dns.name.from_unicode(u'example.com')),
            },
            {
                'query_target': dns.name.from_unicode(u'www.example.com'),
                'query_type': dns.rdatatype.NS,
                'nameserver': '1.1.1.1',
                'kwargs': {
                    'timeout': 10,
                },
                'result': create_mock_response(dns.rcode.NOERROR, authority=[dns.rrset.from_rdata(
                    'www.example.com',
                    3600,
                    dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.SOA, 'ns.example.com. ns.example.com. 12345 7200 120 2419200 10800'),
                )]),
            },
            {
                'query_target': dns.name.from_unicode(u'mail.example.com'),
                'query_type': dns.rdatatype.NS,
                'nameserver': '1.1.1.1',
                'kwargs': {
                    'timeout': 10,
                },
                'result': create_mock_response(dns.rcode.NOERROR, authority=[dns.rrset.from_rdata(
                    'mail.example.com',
                    3600,
                    dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.SOA, 'ns.example.com. ns.example.com. 12345 7200 120 2419200 10800'),
                )]),
            },
        ]
        with patch('dns.resolver.get_default_resolver', resolver):
            with patch('dns.resolver.Resolver', resolver):
                with patch('dns.query.udp', mock_query_udp(udp_sequence)):
                    with patch('time.sleep', mock_sleep):
                        with pytest.raises(AnsibleExitJson) as exc:
                            set_module_args({
                                'records': [
                                    {
                                        'name': 'www.example.com',
                                        'values': [
                                            'asdf',
                                        ],
                                        'mode': 'equals',
                                    },
                                    {
                                        'name': 'mail.example.com',
                                        'values': [
                                            'foo bar',
                                            'any bar',
                                        ],
                                        'mode': 'superset',
                                    },
                                ],
                                'timeout': 10,
                            })
                            wait_for_txt.main()

        print(exc.value.args[0])
        assert exc.value.args[0]['changed'] is False
        assert exc.value.args[0]['completed'] == 2
        assert len(exc.value.args[0]['records']) == 2
        assert exc.value.args[0]['records'][0]['name'] == 'www.example.com'
        assert exc.value.args[0]['records'][0]['done'] is True
        assert exc.value.args[0]['records'][0]['values'] == ['asdf']
        assert exc.value.args[0]['records'][0]['check_count'] == 3
        assert exc.value.args[0]['records'][1]['name'] == 'mail.example.com'
        assert exc.value.args[0]['records'][1]['done'] is True
        assert exc.value.args[0]['records'][1]['values'] == ['any bar']
        assert exc.value.args[0]['records'][1]['check_count'] == 1
