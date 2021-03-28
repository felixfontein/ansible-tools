.. _ansible_collections.felixfontein.tools.docsite.list_to_dict_filter:

felixfontein.tools.list_to_dict -- Convert a list of values and keys to a dictionary
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This plugin is part of the `felixfontein.tools collection <https://galaxy.ansible.com/felixfontein/tools>`_.

    To install it use: :code:`ansible-galaxy collection install felixfontein.tools`.

    To use it in a playbook, specify: :code:`felixfontein.tools.list_to_dict`.

.. version_added

.. versionadded:: 1.4.0 of felixfontein.tools

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Given a list of values and a list of keys, creates a dictionary of these key-value pairs.
- If one of the sequences is shorter than the other, the extra elements of the other sequence are ignored.
- This filter can be used with `map <https://jinja.palletsprojects.com/en/2.11.x/templates/#map>`_ to transform lists of lists of lists of dictionaries.


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
                <div class="ansibleOptionAnchor" id="parameter-values"></div>
                    <b>values</b>
                    <a class="ansibleOptionLink" href="#parameter-values" title="Permalink to this option"></a>
                    <div style="font-size: small">
                    <span style="color: purple">list</span>
                    / <span style="color: purple">elements=raw</span>
                    / <span style="color: red">required</span>
                </div>
            </td>
            <td>
            </td>
            <td>
            </td>
            <td>
                <div>A list of dictionary values.</div>
            </td>
        </tr>
        <tr>
            <td colspan="1">
                <div class="ansibleOptionAnchor" id="parameter-keys"></div>
                    <b>keys</b>
                    <a class="ansibleOptionLink" href="#parameter-keys" title="Permalink to this option"></a>
                    <div style="font-size: small">
                    <span style="color: purple">list</span>
                    / <span style="color: purple">elements=raw</span>
                    / <span style="color: red">required</span>
                </div>
            </td>
            <td>
            </td>
            <td>
            </td>
            <td>
                <div>A list of dictionary keys.</div>
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

    - name: Convert the list of keys to list of dictionaries
      assert:
        that:
          - key_list | map('felixfontein.tools.list_to_dict', ['name', 'address']) | list == expected_result
      vars:
        key_list:
          - - localhost
            - 127.0.0.1
          - - other
            - 1.2.3.4
        expected_result:
          - name: localhost
            address: 127.0.0.1
          - name: other
            address: 1.2.3.4


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
                <div class="ansibleOptionAnchor" id="return-dictionary"></div>
                <b>dictionary</b>
                <a class="ansibleOptionLink" href="#return-dictionary" title="Permalink to this return value"></a>
                <div style="font-size: small">
                <span style="color: purple">dict</span>
                </div>
            </td>
            <td>success</td>
            <td>
                <div>The resulting dictionary.</div>
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

