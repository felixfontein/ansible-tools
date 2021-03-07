.. _ansible_collections.felixfontein.tools.docsite.is_registrable_domain_test:

felixfontein.tools.is_registrable_domain -- Test whether DNS name is a registrable domain name
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This plugin is part of the `felixfontein.tools collection <https://galaxy.ansible.com/felixfontein/tools>`_.

    To install it use: :code:`ansible-galaxy collection install felixfontein.tools`.

    To use it in a playbook, specify: :code:`felixfontein.tools.is_registrable_domain`.

.. version_added

.. versionadded:: 1.4.0 of felixfontein.tools

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- This tests whether a DNS name like ``www.ansible.com`` is a *registrable domain name*, also called *registered domain name*.
  The registrable domain name is defined as the label before the `public suffix <https://publicsuffix.org/>`_ together with the public suffix.
- For example ``ansible.com`` is a registrable domain, since there is exactly one label before the public suffix ``.com``.
  On the other hand, ``www.ansible.com`` and ``com`` are *not* registrable domains, since there are two respectively zero labels
  before the public suffix.


.. Aliases


.. Requirements


.. Options

Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
        <tr>
            <td colspan="1">
                <div class="ansibleOptionAnchor" id="parameter-dns_name"></div>
                    <b>dns_name</b>
                    <a class="ansibleOptionLink" href="#parameter-dns_name" title="Permalink to this option"></a>
                    <div style="font-size: small">
                    <span style="color: purple">str</span>
                    / <span style="color: red">required</span>
                </div>
            </td>
            <td>
            </td>
            <td>
            </td>
            <td>
                <div>A DNS name to test.</div>
            </td>
        </tr>
    </table>
    <br/>

.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    - name: The following conditions are true
      ansible.builtin.assert:
        that:
          - '"www.ansible.com" is not felixfontein.tools.is_registrable_domain'
          - '"ansible.co.uk" is felixfontein.tools.is_registrable_domain'

..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Felix Fontein (@felixfontein)


.. Parsing errors

