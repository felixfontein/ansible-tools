# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import traceback

from ansible.module_utils.basic import missing_required_lib

try:
    import dns
    import dns.name
    import dns.message
    import dns.query
    import dns.rcode
    import dns.rdatatype
    import dns.resolver
except ImportError:
    DNSPYTHON_IMPORTERROR = traceback.format_exc()
else:
    DNSPYTHON_IMPORTERROR = None


class ResolveDirectlyFromNameServers(object):
    def __init__(self, timeout=20):
        self.cache = {}
        self.timeout = timeout
        self.default_resolver = dns.resolver.get_default_resolver()
        self.default_nameservers = self.default_resolver.nameservers

    def _handle_reponse_errors(self, target, response, accept_not_existing=False):
        rcode = response.rcode()
        if rcode == dns.rcode.NOERROR:
            return True
        if rcode == dns.rcode.NXDOMAIN:
            if accept_not_existing:
                return False
            raise Exception('%s does not exist.' % target)
        else:
            raise Exception('Error %s' % dns.rcode.to_text(rcode))

    def _lookup_ns_names(self, target, nameservers):
        query = dns.message.make_query(target, dns.rdatatype.NS)
        response = dns.query.udp(query, nameservers[0], timeout=self.timeout)
        self._handle_reponse_errors(target, response)

        rrset = None
        if len(response.authority) > 0:
            rrset = response.authority[0]
        else:
            rrset = response.answer[0]

        cname = response.canonical_name()
        if cname == target:
            cname = None

        rr = rrset[0]
        if rr.rdtype != dns.rdatatype.SOA:
            return [str(ns_record.target) for ns_record in rrset], cname
        else:
            return None, cname

    def _lookup_address(self, target):
        result = self.cache.get((target, 'addr'))
        if not result:
            result = [str(res) for res in self.default_resolver.resolve(target, lifetime=self.timeout).rrset]
            self.cache[(target, 'addr')] = result
        return result

    def _do_lookup_ns(self, target):
        nameservers = self.default_nameservers
        for i in range(2, len(target.labels) + 1):
            target_part = target.split(i)[1]
            _nameservers = self.cache.get((str(target_part), 'ns'))
            if _nameservers is None:
                nameserver_names, cname = self._lookup_ns_names(target_part, nameservers)
                if nameserver_names is not None:
                    nameservers = []
                    for nameserver_name in nameserver_names:
                        nameservers.extend(self._lookup_address(nameserver_name))

                self.cache[(str(target_part), 'ns')] = nameservers
                self.cache[(str(target_part), 'cname')] = cname
            else:
                nameservers = _nameservers

        return nameservers

    def _lookup_ns(self, target):
        result = self.cache.get((str(target), 'ns'))
        if not result:
            result = self._do_lookup_ns(target)
            self.cache[(str(target), 'ns')] = result
        return result

    def _get_resolver(self, dnsname, nameservers):
        resolver = self.cache.get((str(dnsname), 'resolver'))
        if resolver is None:
            resolver = dns.resolver.Resolver(configure=False)
            resolver.timeout = self.timeout
            resolver.nameservers = nameservers
            self.cache[(str(dnsname), 'resolver')] = resolver
        return resolver

    def resolve_nameservers(self, target):
        return self._lookup_ns(dns.name.from_unicode(target))

    def resolve(self, target, **kwargs):
        dnsname = dns.name.from_unicode(target)
        loop_catcher = set()
        while True:
            nameservers = self._lookup_ns(dnsname)
            cname = self.cache.get((str(dnsname), 'cname'))
            if cname is None:
                break
            dnsname = cname
            if dnsname in loop_catcher:
                raise Exception('Found CNAME loop starting at {0}'.format(target))
            loop_catcher.add(dnsname)

        resolver = self._get_resolver(dnsname, nameservers)
        try:
            response = resolver.resolve(dnsname, **kwargs)
            if response.rrset:
                return response.rrset
            return None
        except dns.resolver.NoAnswer:
            return None


def assert_requirements_present(module):
    if DNSPYTHON_IMPORTERROR:
        module.fail_json(msg=missing_required_lib('dnspython'))
