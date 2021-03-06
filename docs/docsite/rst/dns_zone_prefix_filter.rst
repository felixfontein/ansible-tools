.. _ansible_collection.felixfontein.tools.docsite.dns_zone_prefix_filter:

felixfontein.tools.dns_zone_prefix -- Return part before registrable domain from DNS name
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

For example, ``"www.ansible.com" | felixfontein.tools.dns_zone_prefix == "www"`` and ``"some.random.prefixes.ansible.co.uk" | felixfontein.tools.dns_zone_prefix == "some.random.prefixes"``.
