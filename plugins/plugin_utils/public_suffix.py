# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os.path
import re

from ansible.errors import AnsibleError
from ansible.module_utils.six import raise_from
from ansible.module_utils._text import to_text


_NO_IDN_MATCHER = re.compile(r'^[a-zA-Z0-9.-]+$')


def is_idn(domain):
    return _NO_IDN_MATCHER.match(domain) is None


class InvalidDomainName(Exception):
    '''
    The provided domain name is not valid.
    '''
    pass


def split_into_labels(domain):
    '''
    Split domain name to a list of labels. Start with the top-most label.

    Returns a list of labels and a tail, which is either ``''`` or ``'.'``.
    Raises ``InvalidDomainName`` if the domain name is not valid.
    '''
    result = []
    index = len(domain)
    tail = ''
    if domain.endswith('.'):
        index -= 1
        tail = '.'
    if index > 0:
        while index >= 0:
            next_index = domain.rfind('.', 0, index)
            label = domain[next_index + 1:index]
            if label == '' or label[0] == '-' or label[-1] == '-' or len(label) > 63:
                raise InvalidDomainName(domain)
            result.append(label)
            index = next_index
    return result, tail


def normalize_label(label):
    '''
    Normalize a domain label. Returns a lower-case alabel.
    '''
    if label not in ('', '*') and is_idn(label):
        # Convert ulabel to alabel
        label = to_text(b'xn--' + to_text(label).encode('punycode'))
    # Always convert to lower-case
    return label.lower()


class PublicSuffixEntry(object):
    '''
    Contains a Public Suffix List entry with metadata.
    '''

    def __init__(self, labels, exception_rule=False, part=None):
        self.labels = labels
        self.exception_rule = exception_rule
        self.part = part

    def matches(self, normalized_labels):
        '''
        Match PSL entry with a given normalized list of labels.
        '''
        if len(normalized_labels) < len(self.labels):
            return False
        for i, label in enumerate(self.labels):
            normalized_label = normalized_labels[i]
            if normalized_label != label and label != '*':
                return False
        return True


def select_prevailing_rule(rules):
    '''
    Given a non-empty set of rules matching a domain name, finds the prevailing rule.

    It uses the algorithm specified on https://publicsuffix.org/list/.
    '''
    max_length_rule = rules[0]
    max_length = len(max_length_rule.labels)
    for rule in rules:
        if rule.exception_rule:
            return rule
        if len(rule.labels) > max_length:
            max_length = len(rule.labels)
            max_length_rule = rule
    return max_length_rule


class PublicSuffixList(object):
    '''
    Contains the Public Suffix List.
    '''

    def __init__(self, rules):
        self._generic_rule = PublicSuffixEntry(('*', ))
        self._rules = sorted(rules, key=lambda entry: entry.labels)

    @classmethod
    def load(cls, filename):
        '''
        Load Public Suffix List from the given filename.
        '''
        rules = []
        part = None
        with open(filename, 'rb') as f:
            content = f.read().decode('utf-8')
        for line in content.splitlines():
            line = line.strip()
            if line.startswith('//') or not line:
                if '===BEGIN ICANN DOMAINS===' in line:
                    part = 'icann'
                if '===BEGIN PRIVATE DOMAINS===' in line:
                    part = 'private'
                if '===END ICANN DOMAINS===' in line or '===END PRIVATE DOMAINS===' in line:
                    part = None
                continue
            if part is None:
                raise Exception('Internal error: found PSL entry with no part!')
            exception_rule = False
            if line.startswith('!'):
                exception_rule = True
                line = line[1:]
            if line.startswith('.'):
                line = line[1:]
            labels = tuple(normalize_label(label) for label in split_into_labels(line)[0])
            rules.append(PublicSuffixEntry(labels, exception_rule=exception_rule, part=part))
        return cls(rules)

    def get_suffix_length_and_rule(self, normalized_labels, icann_only=False):
        '''
        Given a list of normalized labels, searches for a matching rule.

        Returns the tuple ``(suffix_length, rule)``. The ``rule`` is never ``None``
        except if ``normalized_labels`` is empty, in which case ``(0, None)`` is returned.

        If ``icann_only`` is set to ``True``, only official ICANN rules are used. If
        ``icann_only`` is ``False`` (default), also private rules are used.
        '''
        if not normalized_labels:
            return 0, None

        # Find matching rules
        rules = []
        for rule in self._rules:
            if icann_only and rule.part != 'icann':
                continue
            if rule.matches(normalized_labels):
                rules.append(rule)
        if not rules:
            rules.append(self._generic_rule)

        # Select prevailing rule
        rule = select_prevailing_rule(rules)

        # Determine suffix
        suffix_length = len(rule.labels)
        if rule.exception_rule:
            suffix_length -= 1

        # Return result
        return suffix_length, rule

    def get_suffix(self, domain, keep_unknown_suffix=True, normalize_result=False,
                   icann_only=False):
        '''
        Given a domain name, extracts the public suffix.

        If ``keep_unknown_suffix`` is set to ``False``, only suffixes matching explicit
        entries from the PSL are returned. If ``keep_unknown_suffix`` is ``True`` (default),
        the implicit ``*`` rule is used if no other rule matches.

        If ``normalize_result`` is set to ``True``, the result is re-combined form the
        normalized labels. In that case, the result is lower-case ASCII. If
        ``normalize_result`` is ``False`` (default), the result ``result`` always satisfies
        ``domain.endswith(result)``.

        If ``icann_only`` is set to ``True``, only official ICANN rules are used. If
        ``icann_only`` is ``False`` (default), also private rules are used.
        '''
        # Split into labels and normalize
        try:
            labels, tail = split_into_labels(domain)
            normalized_labels = [normalize_label(label) for label in labels]
        except InvalidDomainName:
            return ''
        if normalize_result:
            labels = normalized_labels

        # Get suffix length
        suffix_length, rule = self.get_suffix_length_and_rule(normalized_labels, icann_only=icann_only)
        if rule is None:
            return ''
        if not keep_unknown_suffix and rule is self._generic_rule:
            return ''
        return '.'.join(reversed(labels[:suffix_length])) + tail

    def get_registrable_domain(self, domain, keep_unknown_suffix=True, only_if_registerable=True,
                               normalize_result=False, icann_only=False):
        '''
        Given a domain name, extracts the registrable domain. This is the public suffix
        including the last label before the suffix.

        If ``keep_unknown_suffix`` is set to ``False``, only suffixes matching explicit
        entries from the PSL are returned. If no suffix can be found, ``''`` is returned.
        If ``keep_unknown_suffix`` is ``True`` (default), the implicit ``*`` rule is used
        if no other rule matches.

        If ``only_if_registerable`` is set to ``False``, the public suffix is returned
        if there is no label before the suffix. If ``only_if_registerable`` is ``True``
        (default), ``''`` is returned in that case.

        If ``normalize_result`` is set to ``True``, the result is re-combined form the
        normalized labels. In that case, the result is lower-case ASCII. If
        ``normalize_result`` is ``False`` (default), the result ``result`` always satisfies
        ``domain.endswith(result)``.

        If ``icann_only`` is set to ``True``, only official ICANN rules are used. If
        ``icann_only`` is ``False`` (default), also private rules are used.
        '''
        # Split into labels and normalize
        try:
            labels, tail = split_into_labels(domain)
            normalized_labels = [normalize_label(label) for label in labels]
        except InvalidDomainName:
            return ''
        if normalize_result:
            labels = normalized_labels

        # Get suffix length
        suffix_length, rule = self.get_suffix_length_and_rule(normalized_labels, icann_only=icann_only)
        if rule is None:
            return ''
        if not keep_unknown_suffix and rule is self._generic_rule:
            return ''
        if suffix_length < len(labels):
            suffix_length += 1
        elif only_if_registerable:
            return ''
        return '.'.join(reversed(labels[:suffix_length])) + tail


# The official Public Suffix List
PUBLIC_SUFFIX_LIST = PublicSuffixList.load(os.path.join(os.path.dirname(__file__), '..', 'public_suffix_list.dat'))
