# -*- coding: utf-8 -*-
# (c) 2021, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

__metaclass__ = type


import pytest

from ansible_collections.community.internal_test_tools.tests.unit.compat.mock import MagicMock

from ansible_collections.felixfontein.tools.plugins.module_utils import resolver

from ansible_collections.felixfontein.tools.plugins.module_utils.resolver import (
    ResolveDirectlyFromNameServers,
    assert_requirements_present,
)

# We need dnspython
pytest.importorskip('dns')


def test_assert_requirements_present():
    global DNSPYTHON_IMPORTERROR

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
