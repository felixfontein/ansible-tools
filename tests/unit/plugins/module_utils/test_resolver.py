# -*- coding: utf-8 -*-
# (c) 2021, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

__metaclass__ = type


import pytest

from ansible_collections.community.internal_test_tools.tests.unit.compat.mock import MagicMock, patch

from ansible_collections.felixfontein.tools.plugins.module_utils import resolver

from ansible_collections.felixfontein.tools.plugins.module_utils.resolver import (
    ResolveDirectlyFromNameServers,
    assert_requirements_present,
)

# We need dnspython
dns = pytest.importorskip('dns')


def test_assert_requirements_present():
    class ModuleFailException(Exception):
        pass

    def fail_json(**kwargs):
        raise ModuleFailException(kwargs)

    module = MagicMock()
    module.fail_json = MagicMock(side_effect=fail_json)

    orig_importerror = resolver.DNSPYTHON_IMPORTERROR
    resolver.DNSPYTHON_IMPORTERROR = None
    assert_requirements_present(module)

    resolver.DNSPYTHON_IMPORTERROR = 'asdf'
    with pytest.raises(ModuleFailException) as exc:
        assert_requirements_present(module)

    assert 'dnspython' in exc.value.args[0]['msg']
    assert 'asdf' == exc.value.args[0]['exception']

    resolver.DNSPYTHON_IMPORTERROR = orig_importerror


def mock_resolver(default_nameservers, nameserver_resolve_sequence):
    def create_resolver(configure=True):
        resolver = MagicMock()
        resolver.nameservers = default_nameservers if configure else []

        def mock_resolver_resolve(target, lifetime=None):
            resolve_sequence = nameserver_resolve_sequence[tuple(sorted(resolver.nameservers))]
            resolve_data = resolve_sequence[0]
            del resolve_sequence[0]

            assert target == resolve_data['target'], 'target: {0!r} vs {1!r}'.format(target, resolve_data['target'])
            assert lifetime == resolve_data['lifetime'], 'lifetime: {0!r} vs {1!r}'.format(lifetime, resolve_data['lifetime'])

            if 'raise' in resolve_data:
                raise resolve_data['raise']

            return resolve_data['result']

        resolver.resolve = MagicMock(side_effect=mock_resolver_resolve)
        return resolver

    return create_resolver


def mock_query_udp(call_sequence):
    def udp(query, nameserver, **kwargs):
        call = call_sequence[0]
        del call_sequence[0]

        assert query.question[0].name == call['query_target'], 'query_target: {0!r} vs {1!r}'.format(query.question[0].name, call['query_target'])
        assert query.question[0].rdtype == call['query_type'], 'query_type: {0!r} vs {1!r}'.format(query.question[0].rdtype, call['query_type'])
        assert nameserver == call['nameserver'], 'nameserver: {0!r} vs {1!r}'.format(nameserver, call['nameserver'])
        assert kwargs == call['kwargs'], 'kwargs: {0!r} vs {1!r}'.format(kwargs, call['kwargs'])

        if 'raise' in call:
            raise call['raise']

        return call['result']

    return udp


def create_mock_answer(rrset):
    answer = MagicMock()
    answer.rrset = rrset
    return answer


def create_mock_response(rcode, authority=None, answer=None, cname=None):
    response = MagicMock()
    response.rcode = MagicMock(return_value=rcode)
    response.authority = authority or []
    response.answer = answer or []
    response.canonical_name = MagicMock(return_value=cname)
    return response


def test_resolver():
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
            )]),
        },
    ]
    with patch('dns.resolver.get_default_resolver', resolver):
        with patch('dns.resolver.Resolver', resolver):
            with patch('dns.query.udp', mock_query_udp(udp_sequence)):
                resolver = ResolveDirectlyFromNameServers()
                assert resolver.resolve_nameservers('example.com') == ['3.3.3.3']
                # The following results should be cached:
                assert resolver.resolve_nameservers('com') == ['2.2.2.2']
                assert resolver.resolve_nameservers('example.com') == ['3.3.3.3']
