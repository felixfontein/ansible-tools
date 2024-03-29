===========================
Felix's Tools Release Notes
===========================

.. contents:: Topics


v1.5.0
======

Release Summary
---------------

Deprecation release.

Deprecated Features
-------------------

- This collection is deprecated. Please use `community.dns <https://galaxy.ansible.com/community/dns>`_ and `community.general <https://galaxy.ansible.com/community/general>`_ instead, which are both included in Ansible 4+. They contains improved versions of the plugins and modules of this collection and receive updates.

Bugfixes
--------

- Update Public Suffix List.

v1.4.3
======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- Update Public Suffix list.
- wait_for_txt - fix handling of too long TXT values.
- wait_for_txt - resolving nameservers sometimes resulted in an empty list, yielding wrong results.

v1.4.2
======

Release Summary
---------------

Regular maintenance release.

Bugfixes
--------

- Update Public Suffix List.

v1.4.1
======

Release Summary
---------------

Improve documentation and update PSL.

Minor Changes
-------------

- Add documentation for all filter and test plugins to the `collection's docsite <https://ansible.fontein.de/collections/felixfontein/tools/index.html#plugins-in-felixfontein-tools>`_ (https://github.com/felixfontein/ansible-tools/pull/16).

Bugfixes
--------

- Update Public Suffix List.

v1.4.0
======

Release Summary
---------------

This release adds several DNS-related new plugins, and two filters which make creating dictionaries easier.

New Plugins
-----------

Filter
~~~~~~

- felixfontein.tools.dict - The ``dict`` function as a filter: converts a list of tuples to a dictionary
- felixfontein.tools.list_to_dict - Given a list of values and a list of keys, converts them to a dictionary
- felixfontein.tools.registrable_domain - Given domain name, returns the registrable domain

Test
~~~~

- felixfontein.tools.is_registrable_domain - Given domain name, tests whether it is a registrable domain

New Modules
-----------

- felixfontein.tools.wait_for_txt - Wait for TXT entries to be available on all authoritative nameservers

v1.3.0
======

Release Summary
---------------

Completely rewrote the Public Suffix List handling code.

Minor Changes
-------------

- The public suffix list (PSL) matching algorithm as specified on https://publicsuffix.org/list/ is now used.
- The public suffix list (PSL) was updated.

v1.2.0
======

Minor Changes
-------------

- Update Public Suffix List to latest version (https://github.com/felixfontein/ansible-tools/pull/4).

v1.1.0
======

Release Summary
---------------

This release enables CI and adds several useful filters.

Minor Changes
-------------

- Added ``felixfontein.tools.path_join`` filter. For ansible-base 2.10 or newer, it redirects to ``ansible.builtin.path_join``. For Ansible 2.9 and before, it provides an own implementation for the most important case: joining a list of path fragments.

New Plugins
-----------

Filter
~~~~~~

- felixfontein.tools.dns_zone - Return the DNS zone of a domain name (``www.ansible.com`` → ``ansible.com``)
- felixfontein.tools.dns_zone_prefix - Return the prefix before the DNS zone for a domain name (``www.ansible.com`` → ``www``)
- felixfontein.tools.get_domain_suffix - Return the public suffix for a domain name (``www.ansible.com`` → ``.com``)
- felixfontein.tools.path_join - Ansible 2.9 compatibility shim for the ``ansible.builtin.path_join`` filter included in ansible-base 2.10
- felixfontein.tools.remove_domain_suffix - Return the part before the public suffix for a domain name (``www.ansible.com`` → ``www.ansible``)

v1.0.1
======

Release Summary
---------------

Maintenance release for internal changes. Visible external change is that the changelog moved one directory up.


v1.0.0
======

Release Summary
---------------

Initial release of this collection.

New Plugins
-----------

Lookup
~~~~~~

- felixfontein.tools.dependent - Composes a list with nested elements of other lists or dicts which can depend on previous indices
