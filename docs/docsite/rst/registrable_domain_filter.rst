.. _ansible_collection.felixfontein.tools.docsite.registrable_domain_filter:

felixfontein.tools.registrable_domain -- Return registrable domain name from DNS name
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The *registrable domain name*, also called *registered domain name*, is the label before the public suffix together with the public suffix.

For example, ``"www.ansible.com" | felixfontein.tools.registrable_domain == "ansible.com"`` and ``"some.random.prefixes.ansible.co.uk" | felixfontein.tools.registrable_domain == "ansible.co.uk"``.
For unknown suffixes, or in case there is no label before the pubic suffix, an empty string is returned.
