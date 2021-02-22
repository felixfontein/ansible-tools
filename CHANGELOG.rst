===========================
Felix's Tools Release Notes
===========================

.. contents:: Topics


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
- Added filter plugins ``dns_zone``, ``dns_zone_prefix``, ``get_domain_suffix`` and ``remove_domain_suffix``.

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
