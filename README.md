# Felix's Tools
[![CI](https://github.com/felixfontein/ansible-tools/workflows/CI/badge.svg?branch=main)](https://github.com/felixfontein/ansible-tools/actions?query=workflow%3A%22CI%22+branch%3Amain)
[![Public Suffix List up-to-date](https://github.com/felixfontein/ansible-tools/workflows/Check%20for%20Public%20Suffix%20List%20updates/badge.svg?branch=main)](https://github.com/felixfontein/ansible-tools/actions?query=workflow%3A%22Check+for+Public+Suffix+List+updates%22+branch%3Amain)
[![Codecov](https://img.shields.io/codecov/c/github/felixfontein/ansible-tools)](https://codecov.io/gh/felixfontein/ansible-tools)

This collection provides some useful tools.

You can find [documentation for this collection on my Ansible docsite](https://ansible.fontein.de/collections/felixfontein/tools/).

## Tested with Ansible

This collection is tested with Ansible 2.9, ansible-base 2.10 and ansible-core's `devel` branch.
This collection requires Ansible 2.9.10 or newer.

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

### Dictionary filters

- `felixfontein.tools.dict`: similar to the `dict` function, converts a list of tuples to a dictionary: `[['a', 1], ['b', 2]] | felixfontein.tools.dict` evaluates to `{'a': 1, 'b': 2}`.
- `felixfontein.tools.list_to_dict`: given a list of values and keys, converts them to a dictionary: `[1, 2] | felixfontein.tools.list_to_dict(['a', 'b'])` evaluates to `{'a': 1, 'b': 2}`.

### Filters for working with domain names

- `felixfontein.tools.dns_zone`: given a domain name, returns the DNS zone, i.e. the label before the public suffix and the public suffix. For example, `"www.ansible.com" | felixfontein.tools.dns_zone == "ansible.com"` and `"some.random.prefixes.ansible.co.uk" | felixfontein.tools.dns_zone == "ansible.co.uk"`. This usually equals the *registrable domain* or *registered domain*.
- `felixfontein.tools.dns_zone_prefix`: given a domain name, returns the part before the DNS zone. For example, `"www.ansible.com" | felixfontein.tools.dns_zone_prefix == "www"` and `"some.random.prefixes.ansible.co.uk" | felixfontein.tools.dns_zone_prefix == "some.random.prefixes"`.
- `felixfontein.tools.get_domain_suffix`: given a domain name, returns the public suffix. For example, `"www.ansible.com" | felixfontein.tools.get_domain_suffix == ".com"` and `"some.random.prefixes.ansible.co.uk" | felixfontein.tools.get_domain_suffix == ".co.uk"`.
- `felixfontein.tools.registrable_domain`: given a domain name, returns the *registrable domain name* (also called *registered domain name*). For example, `"www.ansible.com" | felixfontein.tools.registrable_domain == "ansible.com"` and `"some.random.prefixes.ansible.co.uk" | felixfontein.tools.registrable_domain == "ansible.co.uk"`. For unknown suffixes, or in case there is no label before the pubic suffix, an empty string is returned.
- `felixfontein.tools.remove_domain_suffix`: given a domain name, returns the part before the public suffix. For example, `"www.ansible.com" | felixfontein.tools.remove_domain_suffix == "www.ansible"` and `"some.random.prefixes.ansible.co.uk" | felixfontein.tools.remove_domain_suffix == "some.random.prefixes.ansible"`.

### Tests for working with domain names

- `felixfontein.tools.is_registrable_domain`: given a domain name, tests whether it is a *registrable domain name* (also called *registered domain name*). For example, `"www.ansible.com" is felixfontein.tools.is_registrable_domain` evaluates to `false`, while `"ansible.co.uk" is felixfontein.tools.is_registrable_domain` evaluates to `true`.

## Using this collection

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Release notes

See [here](https://github.com/felixfontein/ansible-tools/tree/main/CHANGELOG.rst).

## Releasing, Deprecation and Versioning

We release new versions once there are new features or bugfixes. Deprecations can happen, and we try to announce them a long time in advance. We currently do not plan breaking changes, so there will be no new major release anytime soon.

Please note that we consider updates to the Public Suffix List as bugfixes. While we update the copy of the Public Suffix List often, we do not create a bugfix release for every change. Please create an issue to request an update if you think the last update was too long ago.

## Contributing

Please create issues to report problems or request new features, and create PRs to fix bugs or add new features. If you want to do a refactoring PR, please create an issue first to discuss the refactoring.

Please follow the general Ansible contributor guidelines; see the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html).

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

All files except specifially noted are licensed under the GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

The only exception is `plugins/public_suffix_list.dat`, which is subject to the terms of the Mozilla Public License, v. 2.0. See [MPL](https://mozilla.org/MPL/2.0/) for the full text.
