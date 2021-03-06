.. _ansible_collection.felixfontein.tools.docsite.dns_zone_filter:

felixfontein.tools.dns_zone -- Return registrable domain from DNS name
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Return the label before the public suffix and the public suffix.
For example, ``"www.ansible.com" | felixfontein.tools.dns_zone == "ansible.com"`` and ``"some.random.prefixes.ansible.co.uk" | felixfontein.tools.dns_zone == "ansible.co.uk"``.
This usually equals the *registrable domain* or *registered domain*.
