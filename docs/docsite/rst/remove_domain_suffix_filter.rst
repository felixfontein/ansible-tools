.. _ansible_collection.felixfontein.tools.docsite.remove_domain_suffix_filter:

felixfontein.tools.remove_domain_suffix -- Return part before the public suffix from DNS name
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This plugin is part of the `felixfontein.tools collection <https://galaxy.ansible.com/felixfontein/tools>`_.

    To install it use: :code:`ansible-galaxy collection install felixfontein.tools`.

    To use it in a playbook, specify: :code:`felixfontein.tools.remove_domain_suffix`.

.. version_added

.. versionadded:: 1.1.0 of felixfontein.tools

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Given a DNS name, like ``www.ansible.com``, removes the `public suffix <https://publicsuffix.org/>`_ and returns the remainder, in this case ``www.ansible``.


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
          - '"www.ansible.com" | felixfontein.tools.remove_domain_suffix == "www.ansible"'
          - '"some.random.prefixes.ansible.co.uk" | felixfontein.tools.remove_domain_suffix == "some.random.prefixes.ansible"'


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
                <div class="ansibleOptionAnchor" id="return-remainder"></div>
                <b>remainder</b>
                <a class="ansibleOptionLink" href="#return-remainder" title="Permalink to this return value"></a>
                <div style="font-size: small">
                <span style="color: purple">str</span>
                </div>
            </td>
            <td>success</td>
            <td>
                <div>The remainder before the public suffix.</div>
                <br/>
                <div style="font-size: smaller"><b>Sample:</b></div>
                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">www.ansible</div>
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

