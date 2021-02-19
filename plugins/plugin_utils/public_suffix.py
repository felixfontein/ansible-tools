# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os.path
import re

try:
    import idna
except ImportError as imp_exc:
    HAS_IDNA = False
    IDNA_IMPORT_ERROR = imp_exc
else:
    HAS_IDNA = True

from ansible.errors import AnsibleError
from ansible.module_utils.six import raise_from
from ansible.module_utils._text import to_text


_NO_IDN_MATCHER = re.compile(r'^[a-zA-Z0-9.-]+$')


def is_idn(domain):
    return _NO_IDN_MATCHER.match(domain) is None


class InvalidDomainName(Exception):
    pass


class IDNANotInstalled(Exception):
    def __init__(self):
        super(IDNANotInstalled, self).__init__('Cannot handle International Domain Names (IDNs) if `idna` is not installed')


def split_into_labels(domain):
    '''
    Split domain in a list of labels. Start with the top-most label.

    Returns a list of labels and a tail, which is either '' or '.'.
    '''
    result = []
    index = len(domain)
    tail = ''
    if domain.endswith('.'):
        index -= 1
        tail = '.'
    while index >= 0:
        next_index = domain.rfind('.', 0, index)
        label = domain[next_index + 1:index]
        if label == '' or label[0] == '-' or label[-1] == '-':
            raise InvalidDomainName(domain)
        result.append(label)
        index = next_index
    return result, tail


def normalize_label(label):
    if label not in ('', '*') and is_idn(label):
        if not HAS_IDNA:
            raise_from(IDNANotInstalled(), IDNA_IMPORT_ERROR)
        label = to_text(idna.encode(label))
    return label.lower()


class PublicSuffixEntry(object):
    def __init__(self, labels, exception_rule=False, part=None):
        self.labels = labels
        self.exception_rule = exception_rule
        self.part = part

    def matches(self, normalized_labels):
        if len(normalized_labels) < len(self.labels):
            return False
        for i, label in enumerate(self.labels):
            normalized_label = normalized_labels[i]
            if normalized_label != label and label != '*':
                return False
        return True


def select_prevailing_rule(rules):
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
    def __init__(self, rules):
        self._generic_rule = PublicSuffixEntry(('*', ))
        self._rules = sorted(rules, key=lambda entry: entry.labels)

    @classmethod
    def load(cls, filename):
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
            try:
                labels = tuple(normalize_label(label) for label in split_into_labels(line)[0])
                rules.append(PublicSuffixEntry(labels, exception_rule=exception_rule, part=part))
            except IDNANotInstalled:
                # This happens when `idna` is not installed and we try to process IDNs.
                pass
        return cls(rules)

    def get_suffix_length_and_rule(self, normalized_labels):
        if not normalized_labels:
            return 0, None

        # Find matching rules
        rules = []
        for rule in self._rules:
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

    def get_suffix(self, domain, keep_unknown_suffix=True, normalize_result=False):
        # Split into labels and normalize
        try:
            labels, tail = split_into_labels(domain)
            normalized_labels = [normalize_label(label) for label in labels]
        except InvalidDomainName:
            return ''
        if normalize_result:
            labels = normalized_labels

        # Get suffix length
        suffix_length, rule = self.get_suffix_length_and_rule(normalized_labels)
        if not keep_unknown_suffix and rule is self._generic_rule:
            suffix_length = 0
        return '.'.join(reversed(labels[:suffix_length])) + tail

    def get_registrable_domain(self, domain, keep_unknown_suffix=True, only_if_registerable=True, normalize_result=False):
        # Split into labels and normalize
        try:
            labels, tail = split_into_labels(domain)
            normalized_labels = [normalize_label(label) for label in labels]
        except InvalidDomainName:
            return ''
        if normalize_result:
            labels = normalized_labels

        # Get suffix length
        suffix_length, rule = self.get_suffix_length_and_rule(normalized_labels)
        if not keep_unknown_suffix and rule is self._generic_rule:
            suffix_length = 0
            tail = ''
        if suffix_length < len(labels):
            suffix_length += 1
        elif only_if_registerable:
            suffix_length = 0
            tail = ''
        return '.'.join(reversed(labels[:suffix_length])) + tail


PUBLIC_SUFFIX_LIST = PublicSuffixList.load(os.path.join(os.path.dirname(__file__), '..', 'public_suffix_list.dat'))
