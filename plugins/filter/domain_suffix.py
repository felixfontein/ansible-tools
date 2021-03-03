# -*- coding: utf-8 -*-

# Copyright: (c) 2020-2021, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.felixfontein.tools.plugins.plugin_utils.public_suffix import PUBLIC_SUFFIX_LIST


def registrable_domain(domain):
    '''Given domain name, returns the registrable domain.'''
    return PUBLIC_SUFFIX_LIST.get_registrable_domain(domain, only_if_registerable=False, keep_unknown_suffix=False)


def dns_zone(domain):
    '''Given domain name, returns the zone name (essentially the registrable domain).'''
    return PUBLIC_SUFFIX_LIST.get_registrable_domain(domain, only_if_registerable=False)


def dns_zone_prefix(domain, keep_trailing_period=False):
    '''Given domain name, returns the part before the zone name.'''
    suffix = PUBLIC_SUFFIX_LIST.get_registrable_domain(domain, only_if_registerable=False)
    result = domain[:-len(suffix)]
    if not keep_trailing_period and result:
        result = result[:-1]
    return result


def get_domain_suffix(domain):
    '''Given domain name, returns the public suffix.'''
    suffix = PUBLIC_SUFFIX_LIST.get_suffix(domain, keep_unknown_suffix=False)
    if suffix and len(suffix) < len(domain):
        suffix = '.' + suffix
    return suffix


def remove_domain_suffix(domain):
    '''Given domain name, returns the part before the public suffix.'''
    suffix = PUBLIC_SUFFIX_LIST.get_suffix(domain, keep_unknown_suffix=False)
    suffix_len = len(suffix)
    if suffix_len and suffix_len < len(domain):
        suffix_len += 1
    return domain[:-suffix_len]


class FilterModule(object):
    '''Ansible jinja2 filters'''

    def filters(self):
        return {
            'dns_zone': dns_zone,
            'dns_zone_prefix': dns_zone_prefix,
            'get_domain_suffix': get_domain_suffix,
            'registrable_domain': registrable_domain,
            'remove_domain_suffix': remove_domain_suffix,
        }
