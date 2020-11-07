# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type


import os.path


def path_join(list):
    '''Join list of paths.

    This is a minimal shim for ansible.builtin.path_join included in ansible-base 2.10.
    This should only be called by Ansible 2.9 or earlier. See meta/runtime.yml for details.
    '''
    return os.path.join(*list)


class FilterModule(object):
    '''Ansible jinja2 filters'''

    def filters(self):
        return {
            'path_join': path_join,
        }
