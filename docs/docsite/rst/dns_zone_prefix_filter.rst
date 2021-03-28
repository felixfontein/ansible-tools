.. _ansible_collections.felixfontein.tools.docsite.dns_zone_prefix_filter:

felixfontein.tools.dns_zone_prefix -- Return part before registrable domain from DNS name
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This plugin is part of the `felixfontein.tools collection <https://galaxy.ansible.com/felixfontein/tools>`_.

    To install it use: :code:`ansible-galaxy collection install felixfontein.tools`.

    To use it in a playbook, specify: :code:`felixfontein.tools.dns_zone_prefix`.

.. version_added

.. versionadded:: 1.1.0 of felixfontein.tools

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Removes the label before the `public suffix <https://publicsuffix.org/>`_ and the public suffix from a DNS name.
- The label before the public suffix and the public suffix is usually equal to the *registrable domain name* or *registered domain name*, as well as the *DNS zone* name.
  So this returns the part before that.


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
                <div>A DNS name.</div>
            </td>
        </tr>
        <tr>
            <td colspan="1">
                <div class="ansibleOptionAnchor" id="parameter-keep_trailing_period"></div>
                    <b>keep_trailing_period</b>
                    <a class="ansibleOptionLink" href="#parameter-keep_trailing_period" title="Permalink to this option"></a>
                    <div style="font-size: small">
                    <span style="color: purple">bool</span>
                </div>
            </td>
            <td>
                <b>Default:</b><br/><div style="color: blue">false</div>
            </td>
            <td>
            </td>
            <td>
                <div>Whether to keep the trailing period if the prefix is non-trivial, or not.</div>
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
      assert:
        that:
          - '"www.ansible.com" | felixfontein.tools.dns_zone_prefix == "www"'
          - '"some.random.prefixes.ansible.co.uk" | felixfontein.tools.dns_zone_prefix == "some.random.prefixes"'
          - '"ansible.com" | felixfontein.tools.dns_zone_prefix == ""'
          - '"www.ansible.com" | felixfontein.tools.dns_zone_prefix(keep_trailing_period=True) == "www."'

.. Facts


.. Return values

Return Values
-------------

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
        <tr>
            <td colspan="1">
                <div class="ansibleOptionAnchor" id="return-prefix"></div>
                <b>prefix</b>
                <a class="ansibleOptionLink" href="#return-prefix" title="Permalink to this return value"></a>
                <div style="font-size: small">
                <span style="color: purple">str</span>
                </div>
            </td>
            <td>success</td>
            <td>
                <div>The prefix before the registrable domain name/DNS zone name.</div>
                <br/>
                <div style="font-size: smaller"><b>Sample:</b></div>
                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">www</div>
            </td>
        </tr>
    </table>
    <br/><br/>

..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Felix Fontein (@felixfontein)


.. Parsing errors

