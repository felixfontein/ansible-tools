.. _ansible_collections.felixfontein.tools.docsite.dict_filter:

felixfontein.tools.dict -- Convert a list of tuples to a dictionary
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This plugin is part of the `felixfontein.tools collection <https://galaxy.ansible.com/felixfontein/tools>`_.

    To install it use: :code:`ansible-galaxy collection install felixfontein.tools`.

    To use it in a playbook, specify: :code:`felixfontein.tools.dict`.

.. version_added

.. versionadded:: 1.4.0 of felixfontein.tools

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Converts a list of tuples to a dictionary. This does the same as the `dict jinja2 function <https://jinja.palletsprojects.com/en/2.11.x/templates/#dict>`_, but has the advantage that it can be used with `map <https://jinja.palletsprojects.com/en/2.11.x/templates/#map>`_.


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
                <div class="ansibleOptionAnchor" id="parameter-sequence"></div>
                    <b>sequence</b>
                    <a class="ansibleOptionLink" href="#parameter-sequence" title="Permalink to this option"></a>
                    <div style="font-size: small">
                    <span style="color: purple">list</span>
                    / <span style="color: purple">elements=list</span>
                    / <span style="color: red">required</span>
                </div>
            </td>
            <td>
            </td>
            <td>
            </td>
            <td>
                <div>A list of two-element lists.</div>
                <div>The list elements are treated as tuples ``(key, value)``, that are used as key and value for the resulting dictionary.</div>
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
          - '[["a", 1], ["b", 2]] | felixfontein.tools.dict == dictionary'
      vars:
        dictionary:
          a: 1
          b: 2


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
                <div>The dictionary created from the input key-value pairs.</div>
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

