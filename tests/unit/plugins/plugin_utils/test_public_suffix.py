# -*- coding: utf-8 -*-
# (c) 2021, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

__metaclass__ = type


import pytest

from ansible_collections.felixfontein.tools.plugins.plugin_utils.public_suffix import (
    split_into_labels,
    normalize_label,
    PUBLIC_SUFFIX_LIST,
)


TEST_LABEL_SPLIT = [
    ('foo.bar', ['bar', 'foo'], ''),
    ('foo.bar.', ['bar', 'foo'], '.'),
    ('.bar.', ['bar', ''], '.'),
    ('*.bar.', ['bar', '*'], '.'),
    ('..bar', ['bar', '', ''], ''),
    ('☺.A', ['A', '☺'], ''),
]

@pytest.mark.parametrize("domain, labels, tail", TEST_LABEL_SPLIT)
def test_split_into_labels(domain, labels, tail):
    _labels, _tail = split_into_labels(domain)
    assert _labels == labels
    assert _tail == tail


TEST_LABEL_NORMALIZE = [
    ('', ''),
    ('*', '*'),
    ('foo', 'foo'),
    ('Foo', 'foo'),
]

@pytest.mark.parametrize("label, normalized_label", TEST_LABEL_NORMALIZE)
def test_normalize_label(label, normalized_label):
    assert normalize_label(label) == normalized_label


TEST_GET_SUFFIX = [
    ('foo.com', 'com', 'foo.com'),
    ('bar.foo.com.', 'com.', 'foo.com.'),
]

@pytest.mark.parametrize("domain, suffix, reg_domain", TEST_GET_SUFFIX)
def test_get_suffix(domain, suffix, reg_domain):
    assert PUBLIC_SUFFIX_LIST.get_suffix(domain) == suffix
    assert PUBLIC_SUFFIX_LIST.get_registrable_domain(domain) == reg_domain
