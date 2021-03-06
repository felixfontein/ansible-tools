.. _ansible_collection.felixfontein.tools.docsite.is_registrable_domain_test:

felixfontein.tools.is_registrable_domain -- Test whether DNS name is a registrable domain name
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The *registrable domain name*, also called *registered domain name*, is the label before the public suffix together with the public suffix.

For example, ``"www.ansible.com" is felixfontein.tools.is_registrable_domain`` evaluates to ``false``, while ``"ansible.co.uk" is felixfontein.tools.is_registrable_domain`` evaluates to ``true``.
