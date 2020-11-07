# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os.path
import re


PUBLIC_SUFFIX_LIST_FILENAME = os.path.join(os.path.dirname(__file__), '..', 'public_suffix_list.dat')


def get_processed_list():
    result = []
    with open(PUBLIC_SUFFIX_LIST_FILENAME, 'rt') as f:
        for line in f:
            line = line.strip()
            if line.startswith('//') or not line:
                continue
            if not line.startswith('.'):
                line = '.' + line
            result.append(line)
    return sorted(result, key=lambda line: -len(line))


PUBLIC_SUFFIX_LIST = get_processed_list()


def get_suffix(domain, processed_list):
    for suffix in processed_list:
        if domain.endswith(suffix):
            return suffix
    return ''


def remove_trailing_period(domain):
    if domain.endswith('.'):
        return domain[:-1], '.'
    return domain, ''


def dns_zone(domain):
    '''Given domain name, returns the zone name.'''
    domain, result_suffix = remove_trailing_period(domain)
    suffix = get_suffix(domain, PUBLIC_SUFFIX_LIST)
    last_dot_before_suffix = domain.rfind('.', 0, -len(suffix))
    return domain[last_dot_before_suffix + 1:] + result_suffix


def dns_zone_prefix(domain, keep_trailing_period=False):
    '''Given domain name, returns the part before the zone name.'''
    domain, dummy = remove_trailing_period(domain)
    suffix = get_suffix(domain, PUBLIC_SUFFIX_LIST)
    last_dot_before_suffix = domain.rfind('.', 0, -len(suffix))
    if last_dot_before_suffix < 0:
        return ''
    return domain[:last_dot_before_suffix + (1 if keep_trailing_period else 0)]


def get_domain_suffix(domain):
    '''Given domain name, returns the public suffix.'''
    domain, result_suffix = remove_trailing_period(domain)
    return get_suffix(domain, PUBLIC_SUFFIX_LIST) + result_suffix


def remove_domain_suffix(domain):
    '''Given domain name, returns the part before the public suffix.'''
    domain, dummy = remove_trailing_period(domain)
    suffix = get_suffix(domain, PUBLIC_SUFFIX_LIST)
    return domain[:-len(suffix)]


class FilterModule(object):
    '''Ansible jinja2 filters'''

    def filters(self):
        return {
            'dns_zone': dns_zone,
            'dns_zone_prefix': dns_zone_prefix,
            'get_domain_suffix': get_domain_suffix,
            'remove_domain_suffix': remove_domain_suffix,
        }
