.. _ansible_collections.felixfontein.tools.docsite.registrable_domain_filter:

felixfontein.tools.registrable_domain -- Return registrable domain name from DNS name
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This plugin is part of the `felixfontein.tools collection <https://galaxy.ansible.com/felixfontein/tools>`_.

    To install it use: :code:`ansible-galaxy collection install felixfontein.tools`.

    To use it in a playbook, specify: :code:`felixfontein.tools.registrable_domain`.

.. version_added

.. versionadded:: 1.4.0 of felixfontein.tools

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- This returns the *registrable domain name*, also called *registered domain name*, for a DNS name.
  The registrable domain name is defined as the label before the `public suffix <https://publicsuffix.org/>`_ together with the public suffix.
- For example ``ansible.com`` is the registrable domain name for ``www.ansible.com``, since there is exactly one label before the public suffix ``.com``.


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
          - '"www.ansible.co.uk" | felixfontein.tools.registrable_domain == "ansible.co.uk"'
          - '"ansible.co.uk" | felixfontein.tools.registrable_domain == "ansible.co.uk"'
          # A public suffix has no registrable domain:
          - '"co.uk" | felixfontein.tools.registrable_domain == ""'


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
                <div class="ansibleOptionAnchor" id="return-registrable_domain"></div>
                <b>registrable_domain</b>
                <a class="ansibleOptionLink" href="#return-registrable_domain" title="Permalink to this return value"></a>
                <div style="font-size: small">
                <span style="color: purple">str</span>
                </div>
            </td>
            <td>success</td>
            <td>
                <div>The registrable domain, or an empty string if there is no registrable domain for this DNS name.</div>
                <br/>
                <div style="font-size: smaller"><b>Sample:</b></div>
                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">ansible.co.uk</div>
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

