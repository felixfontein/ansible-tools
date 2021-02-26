# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.felixfontein.tools.plugins.plugin_utils.public_suffix import PUBLIC_SUFFIX_LIST


def is_registrable_domain(domain):
    '''Given domain name, returns the registrable domain.'''
    registrable_domain = PUBLIC_SUFFIX_LIST.get_registrable_domain(domain, only_if_registerable=True, keep_unknown_suffix=False)
    return bool(registrable_domain) and registrable_domain == domain


class TestModule(object):
    '''Ansible jinja2 tests'''

    def tests(self):
        return {
            'is_registrable_domain': is_registrable_domain,
        }
