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
    ('foo.com', {}, 'com', 'foo.com'),
    ('bar.foo.com.', {}, 'com.', 'foo.com.'),
    ('BaR.fOo.CoM.', {'normalize_result': True}, 'com.', 'foo.com.'),
    ('BaR.fOo.CoM.', {}, 'CoM.', 'fOo.CoM.'),
    ('com', {}, 'com', ''),
    ('com', {'keep_unknown_suffix': False}, 'com', ''),
    ('foo.com', {}, 'com', 'foo.com'),
    ('foo.com', {'keep_unknown_suffix': False}, 'com', 'foo.com'),
    ('foobarbaz', {}, 'foobarbaz', ''),
    ('foobarbaz', {'keep_unknown_suffix': False}, '', ''),
    ('foo.foobarbaz', {}, 'foobarbaz', 'foo.foobarbaz'),
    ('foo.foobarbaz', {'keep_unknown_suffix': False}, '', ''),
    ('-a.com', {}, '', ''),  # invalid domain name (leading dash in label)
    ('a-.com', {}, '', ''),  # invalid domain name (trailing dash in label)
    ('-.com', {}, '', ''),  # invalid domain name (leading and trailing dash in label)
    ('.com', {}, '', ''),  # invalid domain name (empty label)
]


@pytest.mark.parametrize("domain, kwargs, suffix, reg_domain", TEST_GET_SUFFIX)
def test_get_suffix(domain, kwargs, suffix, reg_domain):
    assert PUBLIC_SUFFIX_LIST.get_suffix(domain, **kwargs) == suffix
    assert PUBLIC_SUFFIX_LIST.get_registrable_domain(domain, **kwargs) == reg_domain


# -------------------------------------------------------------------------------------------------
# The following list is taken from https://raw.githubusercontent.com/publicsuffix/list/master/tests/test_psl.txt
# Any copyright for this list is dedicated to the Public Domain. (https://creativecommons.org/publicdomain/zero/1.0/)
# This list has been provided by Rob Stradling of Comodo (see last section on https://publicsuffix.org/list/).
TEST_SUFFIX_OFFICIAL_TESTS = [
    # '' input.
    ('', '', {}),
    # Mixed case.
    ('COM', '', {}),
    ('example.COM', 'example.com', {'normalize_result': True}),
    ('WwW.example.COM', 'example.com', {'normalize_result': True}),
    ('example.COM', 'example.COM', {}),
    ('WwW.example.COM', 'example.COM', {}),
    # Leading dot.
    ('.com', '', {}),
    ('.example', '', {}),
    ('.example.com', '', {}),
    ('.example.example', '', {}),
    # Unlisted TLD.
    ('example', '', {}),
    ('example.example', 'example.example', {}),
    ('b.example.example', 'example.example', {}),
    ('a.b.example.example', 'example.example', {}),
    # Listed, but non-Internet, TLD.
    # ('local', '', {}),
    # ('example.local', '', {}),
    # ('b.example.local', '', {}),
    # ('a.b.example.local', '', {}),
    # TLD with only 1 rule.
    ('biz', '', {}),
    ('domain.biz', 'domain.biz', {}),
    ('b.domain.biz', 'domain.biz', {}),
    ('a.b.domain.biz', 'domain.biz', {}),
    # TLD with some 2-level rules.
    ('com', '', {}),
    ('example.com', 'example.com', {}),
    ('b.example.com', 'example.com', {}),
    ('a.b.example.com', 'example.com', {}),
    ('uk.com', '', {}),
    ('example.uk.com', 'example.uk.com', {}),
    ('b.example.uk.com', 'example.uk.com', {}),
    ('a.b.example.uk.com', 'example.uk.com', {}),
    ('test.ac', 'test.ac', {}),
    # TLD with only 1 (wildcard) rule.
    ('mm', '', {}),
    ('c.mm', '', {}),
    ('b.c.mm', 'b.c.mm', {}),
    ('a.b.c.mm', 'b.c.mm', {}),
    # More complex TLD.
    ('jp', '', {}),
    ('test.jp', 'test.jp', {}),
    ('www.test.jp', 'test.jp', {}),
    ('ac.jp', '', {}),
    ('test.ac.jp', 'test.ac.jp', {}),
    ('www.test.ac.jp', 'test.ac.jp', {}),
    ('kyoto.jp', '', {}),
    ('test.kyoto.jp', 'test.kyoto.jp', {}),
    ('ide.kyoto.jp', '', {}),
    ('b.ide.kyoto.jp', 'b.ide.kyoto.jp', {}),
    ('a.b.ide.kyoto.jp', 'b.ide.kyoto.jp', {}),
    ('c.kobe.jp', '', {}),
    ('b.c.kobe.jp', 'b.c.kobe.jp', {}),
    ('a.b.c.kobe.jp', 'b.c.kobe.jp', {}),
    ('city.kobe.jp', 'city.kobe.jp', {}),
    ('www.city.kobe.jp', 'city.kobe.jp', {}),
    # TLD with a wildcard rule and exceptions.
    ('ck', '', {}),
    ('test.ck', '', {}),
    ('b.test.ck', 'b.test.ck', {}),
    ('a.b.test.ck', 'b.test.ck', {}),
    ('www.ck', 'www.ck', {}),
    ('www.www.ck', 'www.ck', {}),
    # US K12.
    ('us', '', {}),
    ('test.us', 'test.us', {}),
    ('www.test.us', 'test.us', {}),
    ('ak.us', '', {}),
    ('test.ak.us', 'test.ak.us', {}),
    ('www.test.ak.us', 'test.ak.us', {}),
    ('k12.ak.us', '', {}),
    ('test.k12.ak.us', 'test.k12.ak.us', {}),
    ('www.test.k12.ak.us', 'test.k12.ak.us', {}),
    # IDN labels.
    (u'食狮.com.cn', u'食狮.com.cn', {}),
    (u'食狮.公司.cn', u'食狮.公司.cn', {}),
    (u'www.食狮.公司.cn', u'食狮.公司.cn', {}),
    (u'shishi.公司.cn', u'shishi.公司.cn', {}),
    (u'公司.cn', u'', {}),
    (u'食狮.中国', u'食狮.中国', {}),
    (u'www.食狮.中国', u'食狮.中国', {}),
    (u'shishi.中国', u'shishi.中国', {}),
    (u'中国', u'', {}),
    # Same as above, but punycoded.  (TODO: punycode not supported yet!)
    ('xn--85x722f.com.cn', 'xn--85x722f.com.cn', {}),
    ('xn--85x722f.xn--55qx5d.cn', 'xn--85x722f.xn--55qx5d.cn', {}),
    ('www.xn--85x722f.xn--55qx5d.cn', 'xn--85x722f.xn--55qx5d.cn', {}),
    ('shishi.xn--55qx5d.cn', 'shishi.xn--55qx5d.cn', {}),
    ('xn--55qx5d.cn', '', {}),
    ('xn--85x722f.xn--fiqs8s', 'xn--85x722f.xn--fiqs8s', {}),
    ('www.xn--85x722f.xn--fiqs8s', 'xn--85x722f.xn--fiqs8s', {}),
    ('shishi.xn--fiqs8s', 'shishi.xn--fiqs8s', {}),
    ('xn--fiqs8s', '', {}),
]
# End of public domain test data
# -------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("domain, registrable_domain, kwargs", TEST_SUFFIX_OFFICIAL_TESTS)
def test_get_suffix_official(domain, registrable_domain, kwargs):
    if is_idn(domain) and not HAS_IDNA:
        pytest.skip('Need `idna` to run test with IDN')
    reg_domain = PUBLIC_SUFFIX_LIST.get_registrable_domain(domain, **kwargs)
    print(reg_domain)
    assert reg_domain == registrable_domain
