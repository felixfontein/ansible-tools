# -*- coding: utf-8 -*-
# (c) 2021, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Note that this file contains some public domain test data from
# https://raw.githubusercontent.com/publicsuffix/list/master/tests/test_psl.txt
# The data is marked and documented as public domain appropriately.

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

__metaclass__ = type


import pytest

from ansible_collections.felixfontein.tools.plugins.plugin_utils.public_suffix import (
    is_idn,
    normalize_label,
    split_into_labels,
    HAS_IDNA,
    InvalidDomainName,
    PUBLIC_SUFFIX_LIST,
)


TEST_LABEL_SPLIT = [
    ('foo.bar', ['bar', 'foo'], ''),
    ('foo.bar.', ['bar', 'foo'], '.'),
    ('*.bar.', ['bar', '*'], '.'),
    ('☺.A', ['A', '☺'], ''),
]


@pytest.mark.parametrize("domain, labels, tail", TEST_LABEL_SPLIT)
def test_split_into_labels(domain, labels, tail):
    _labels, _tail = split_into_labels(domain)
    assert _labels == labels
    assert _tail == tail


TEST_LABEL_SPLIT_ERRORS = [
    '.bar.',
    '..bar',
    '-bar',
    'bar-',
    '',
]


@pytest.mark.parametrize("domain", TEST_LABEL_SPLIT_ERRORS)
def test_split_into_labels(domain):
    with pytest.raises(InvalidDomainName):
        split_into_labels(domain)


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


# -------------------------------------------------------------------------------------------------
# The following list is taken from https://raw.githubusercontent.com/publicsuffix/list/master/tests/test_psl.txt
# Any copyright for this list is dedicated to the Public Domain. (https://creativecommons.org/publicdomain/zero/1.0/)
# This list has been provided by Rob Stradling of Comodo (see last section on https://publicsuffix.org/list/).
TEST_SUFFIX_OFFICIAL_TESTS = [
    # '' input.
    ('', '', False),
    # Mixed case.
    ('COM', '', False),
    ('example.COM', 'example.com', True),
    ('WwW.example.COM', 'example.com', True),
    # Leading dot.
    ('.com', '', False),
    ('.example', '', False),
    ('.example.com', '', False),
    ('.example.example', '', False),
    # Unlisted TLD.
    ('example', '', False),
    ('example.example', 'example.example', False),
    ('b.example.example', 'example.example', False),
    ('a.b.example.example', 'example.example', False),
    # Listed, but non-Internet, TLD.
    # ('local', '', False),
    # ('example.local', '', False),
    # ('b.example.local', '', False),
    # ('a.b.example.local', '', False),
    # TLD with only 1 rule.
    ('biz', '', False),
    ('domain.biz', 'domain.biz', False),
    ('b.domain.biz', 'domain.biz', False),
    ('a.b.domain.biz', 'domain.biz', False),
    # TLD with some 2-level rules.
    ('com', '', False),
    ('example.com', 'example.com', False),
    ('b.example.com', 'example.com', False),
    ('a.b.example.com', 'example.com', False),
    ('uk.com', '', False),
    ('example.uk.com', 'example.uk.com', False),
    ('b.example.uk.com', 'example.uk.com', False),
    ('a.b.example.uk.com', 'example.uk.com', False),
    ('test.ac', 'test.ac', False),
    # TLD with only 1 (wildcard) rule.
    ('mm', '', False),
    ('c.mm', '', False),
    ('b.c.mm', 'b.c.mm', False),
    ('a.b.c.mm', 'b.c.mm', False),
    # More complex TLD.
    ('jp', '', False),
    ('test.jp', 'test.jp', False),
    ('www.test.jp', 'test.jp', False),
    ('ac.jp', '', False),
    ('test.ac.jp', 'test.ac.jp', False),
    ('www.test.ac.jp', 'test.ac.jp', False),
    ('kyoto.jp', '', False),
    ('test.kyoto.jp', 'test.kyoto.jp', False),
    ('ide.kyoto.jp', '', False),
    ('b.ide.kyoto.jp', 'b.ide.kyoto.jp', False),
    ('a.b.ide.kyoto.jp', 'b.ide.kyoto.jp', False),
    ('c.kobe.jp', '', False),
    ('b.c.kobe.jp', 'b.c.kobe.jp', False),
    ('a.b.c.kobe.jp', 'b.c.kobe.jp', False),
    ('city.kobe.jp', 'city.kobe.jp', False),
    ('www.city.kobe.jp', 'city.kobe.jp', False),
    # TLD with a wildcard rule and exceptions.
    ('ck', '', False),
    ('test.ck', '', False),
    ('b.test.ck', 'b.test.ck', False),
    ('a.b.test.ck', 'b.test.ck', False),
    ('www.ck', 'www.ck', False),
    ('www.www.ck', 'www.ck', False),
    # US K12.
    ('us', '', False),
    ('test.us', 'test.us', False),
    ('www.test.us', 'test.us', False),
    ('ak.us', '', False),
    ('test.ak.us', 'test.ak.us', False),
    ('www.test.ak.us', 'test.ak.us', False),
    ('k12.ak.us', '', False),
    ('test.k12.ak.us', 'test.k12.ak.us', False),
    ('www.test.k12.ak.us', 'test.k12.ak.us', False),
    # IDN labels.
    (u'食狮.com.cn', u'食狮.com.cn', False),
    (u'食狮.公司.cn', u'食狮.公司.cn', False),
    (u'www.食狮.公司.cn', u'食狮.公司.cn', False),
    (u'shishi.公司.cn', u'shishi.公司.cn', False),
    (u'公司.cn', u'', False),
    (u'食狮.中国', u'食狮.中国', False),
    (u'www.食狮.中国', u'食狮.中国', False),
    (u'shishi.中国', u'shishi.中国', False),
    (u'中国', u'', False),
    # Same as above, but punycoded.  (TODO: punycode not supported yet!)
    ('xn--85x722f.com.cn', 'xn--85x722f.com.cn', False),
    ('xn--85x722f.xn--55qx5d.cn', 'xn--85x722f.xn--55qx5d.cn', False),
    ('www.xn--85x722f.xn--55qx5d.cn', 'xn--85x722f.xn--55qx5d.cn', False),
    ('shishi.xn--55qx5d.cn', 'shishi.xn--55qx5d.cn', False),
    ('xn--55qx5d.cn', '', False),
    ('xn--85x722f.xn--fiqs8s', 'xn--85x722f.xn--fiqs8s', False),
    ('www.xn--85x722f.xn--fiqs8s', 'xn--85x722f.xn--fiqs8s', False),
    ('shishi.xn--fiqs8s', 'shishi.xn--fiqs8s', False),
    ('xn--fiqs8s', '', False),
]
# End of public domain test data
# -------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("domain, registrable_domain, normalize_result", TEST_SUFFIX_OFFICIAL_TESTS)
def test_get_suffix_official(domain, registrable_domain, normalize_result):
    if is_idn(domain) and not HAS_IDNA:
        pytest.skip('Need `idna` to run test with IDN')
    reg_domain = PUBLIC_SUFFIX_LIST.get_registrable_domain(domain, normalize_result=normalize_result)
    print(reg_domain)
    assert reg_domain == registrable_domain
