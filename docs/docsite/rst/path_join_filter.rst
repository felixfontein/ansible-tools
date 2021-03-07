.. _ansible_collection.felixfontein.tools.docsite.path_join_filter:

felixfontein.tools.path_join -- Join path components (compatibility shim)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This plugin is part of the `felixfontein.tools collection <https://galaxy.ansible.com/felixfontein/tools>`_.

    To install it use: :code:`ansible-galaxy collection install felixfontein.tools`.

    To use it in a playbook, specify: :code:`felixfontein.tools.path_join`.

.. version_added

.. versionadded:: 1.1.0 of felixfontein.tools

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Compatiblity shim which redirects to ``ansible.builtin.path_join`` for ansible-base 2.10 and newer, and provides a basic implementation for Ansible 2.9 and before. It supports joining a list of path fragments.


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
                <div class="ansibleOptionAnchor" id="parameter-path_fragments"></div>
                    <b>path_fragments</b>
                    <a class="ansibleOptionLink" href="#parameter-path_fragments" title="Permalink to this option"></a>
                    <div style="font-size: small">
                    <span style="color: purple">list</span>
                    / <span style="color: purple">elements=str</span>
                    / <span style="color: red">required</span>
                </div>
            </td>
            <td>
            </td>
            <td>
            </td>
            <td>
                <div>A list of path fragments to be joined.</div>
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
          - '["/home", "user", "file"] | felixfontein.tools.path_join == "/home/user/felix"'
          - '["/home", "/var", "temp"] | felixfontein.tools.path_join == "/var/temp"'


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
                <div class="ansibleOptionAnchor" id="return-path"></div>
                <b>path</b>
                <a class="ansibleOptionLink" href="#return-path" title="Permalink to this return value"></a>
                <div style="font-size: small">
                <span style="color: purple">str</span>
                </div>
            </td>
            <td>success</td>
            <td>
                <div>The combined path.</div>
                <br/>
                <div style="font-size: smaller"><b>Sample:</b></div>
                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/tmp/asdf</div>
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

