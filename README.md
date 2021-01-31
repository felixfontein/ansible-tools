# Felix's Tools
[![CI](https://github.com/felixfontein/ansible-tools/workflows/CI/badge.svg?event=push)](https://github.com/felixfontein/ansible-tools/actions)
[![Codecov](https://img.shields.io/codecov/c/github/felixfontein/ansible-tools)](https://codecov.io/gh/felixfontein/ansible-tools)

This collection provides some useful tools.

You can find [documentation for this collection on my Ansible docsite](https://ansible.fontein.de/collections/felixfontein/tools/).

## Tested with Ansible

This collection is tested with Ansible 2.9, ansible-base 2.10 and ansible-core's `devel` branch.

## External requirements

No requirements.

## Included content

You can find [documentation for this collection on my Ansible docsite](https://ansible.fontein.de/collections/felixfontein/tools/).

### Compatibilty shims

- `felixfontein.tools.path_join`: shim which redirects to `ansible.builtin.path_join` for ansible-base 2.10 and newer, and provides a basic implementation for Ansible 2.9 and before. It supports joining a list of path fragments.

### Dependent Lookup

A plugin which allows to do nested loops where the inner loops depend on the current `item` of the outer loops.

This plugin allows you to write something like:

```yaml
- ansible.builtin.debug:
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

### Filters for working with domain names

- `felixfontein.tools.dns_zone`: given a domain name, returns the DNS zone, i.e. the label before the public suffix and the public suffix. For example, `"www.ansible.com" | felixfontein.tools.dns_zone == "ansible.com"` and `"some.random.prefixes.ansible.co.uk" | felixfontein.tools.dns_zone == "ansible.co.uk"`.
- `felixfontein.tools.dns_zone_prefix`: given a domain name, returns the part before the DNS zone. For example, `"www.ansible.com" | felixfontein.tools.dns_zone_prefix == "www"` and `"some.random.prefixes.ansible.co.uk" | felixfontein.tools.dns_zone_prefix == "some.random.prefixes"`.
- `felixfontein.tools.get_domain_suffix`: given a domain name, returns the public suffix. For example, `"www.ansible.com" | felixfontein.tools.get_domain_suffix == ".com"` and `"some.random.prefixes.ansible.co.uk" | felixfontein.tools.get_domain_suffix == ".co.uk"`.
- `felixfontein.tools.remove_domain_suffix`: given a domain name, returns the part before the public suffix. For example, `"www.ansible.com" | felixfontein.tools.remove_domain_suffix == "www.ansible"` and `"some.random.prefixes.ansible.co.uk" | felixfontein.tools.remove_domain_suffix == "some.random.prefixes.ansible"`.

## Using this collection

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Release notes

See [here](https://github.com/felixfontein/ansible-tools/tree/main/CHANGELOG.rst).

## Releasing, Deprecation and Versioning

We release new versions once there are new features or bugfixes. Deprecations can happen, and we try to announce them a long time in advance. We currently do not plan breaking changes, so there will be no new major release anytime soon.

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

All files except specifially noted are licensed under the GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

The only exception is `plugins/public_suffix_list.dat`, which is subject to the terms of the Mozilla Public License, v. 2.0. See [MPL](https://mozilla.org/MPL/2.0/) for the full text.
