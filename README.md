# Felix's Tools

This collection provides some useful tools.

## Tested with Ansible

Tested with both Ansible 2.9 and the current development version of Ansible.

## External requirements

No requirements.

## Included content

### Dependent Lookup

A plugin which allows to do nested loops where the inner loops depend on the current `item` of the outer loops.

This plugin allows you to write something like:

```yaml
- debug:
    msg: "{{ item.0 }} {{ item.1 }} {{ item.2 }}"
  with_felixfontein.tools.dependent:
  - "[1, 2]"
  - "[item.0 + 3, item.0 + 6]"
  - "[item.0 + item.1 * 10]"
```

in a playbook. This yields the following output:

```
ok: [localhost] => (item={0: 1, 1: 4, 2: 41}) => {
    "item": {
        "0": 1,
        "1": 4,
        "2": 41
    },
    "msg": "1 4 41"
}
ok: [localhost] => (item={0: 1, 1: 7, 2: 71}) => {
    "item": {
        "0": 1,
        "1": 7,
        "2": 71
    },
    "msg": "1 7 71"
}
ok: [localhost] => (item={0: 2, 1: 5, 2: 52}) => {
    "item": {
        "0": 2,
        "1": 5,
        "2": 52
    },
    "msg": "2 5 52"
}
ok: [localhost] => (item={0: 2, 1: 8, 2: 82}) => {
    "item": {
        "0": 2,
        "1": 8,
        "2": 82
    },
    "msg": "2 8 82"
}
```

## Using this collection

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Release notes

See [here](https://github.com/felixfontein/ansible-tools/tree/main/changelogs/CHANGELOG.rst).

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
