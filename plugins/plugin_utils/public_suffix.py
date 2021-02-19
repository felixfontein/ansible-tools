# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os.path


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
        result.append(domain[next_index + 1:index])
        index = next_index
    return result, tail


def normalize_label(label):
    # FIXME: handle IDNs / Punycode
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
        with open(filename, 'rt') as f:
            for line in f:
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

    def get_suffix(self, domain, keep_unknown_suffix=True):
        # Split into labels and normalize
        labels, tail = split_into_labels(domain)
        normalized_labels = [normalize_label(label) for label in labels]

        # Get suffix length
        suffix_length, rule = self.get_suffix_length_and_rule(normalized_labels)
        if not keep_unknown_suffix and rule is self._generic_rule:
            suffix_length = 0
        return '.'.join(reversed(labels[:suffix_length])) + tail

    def get_registrable_domain(self, domain, keep_unknown_suffix=True):
        # Split into labels and normalize
        labels, tail = split_into_labels(domain)
        normalized_labels = [normalize_label(label) for label in labels]

        # Get suffix length
        suffix_length, rule = self.get_suffix_length_and_rule(normalized_labels)
        if not keep_unknown_suffix and rule is self._generic_rule:
            suffix_length = 0
        if suffix_length < len(labels):
            suffix_length += 1
        return '.'.join(reversed(labels[:suffix_length])) + tail


PUBLIC_SUFFIX_LIST = PublicSuffixList.load(os.path.join(os.path.dirname(__file__), '..', 'public_suffix_list.dat'))
