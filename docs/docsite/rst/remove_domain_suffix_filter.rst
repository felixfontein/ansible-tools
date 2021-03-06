.. _ansible_collection.felixfontein.tools.docsite.remove_domain_suffix_filter:

felixfontein.tools.remove_domain_suffix -- Return part before the public suffix from DNS name
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

For example, ``"www.ansible.com" | felixfontein.tools.remove_domain_suffix == "www.ansible"`` and ``"some.random.prefixes.ansible.co.uk" | felixfontein.tools.remove_domain_suffix == "some.random.prefixes.ansible"``.
