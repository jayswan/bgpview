#!/usr/bin/env python3
from argparse import ArgumentParser
import json
import sys
import requests

BASE_URL = 'https://api.bgpview.io'

class BgpView(object):

    def __init__(self):
        self.error = False

    def __repr__(self):
        return self.json

    def query(self, endpoint, query_string):
        self.url = ('{}/{}/{}').format(BASE_URL, endpoint, query_string)
        r = requests.get(self.url)
        r.raise_for_status()
        if r.status_code == 200:
            if r.json()['status'] == 'ok':
                self.response_data = r.json()['data']
            self.error = True

    @property
    def json(self):
        return json.dumps(self.response_data)

    @property
    def verbose(self):
        return self.response_data

    @property
    def summary(self):
        raise NotImplementedError('subclass must implement this')

    @property
    def terse(self):
        raise NotImplementedError('subclass must implement this')

class ASN(BgpView):

    def __init__(self, asn):
        self.endpoint = 'asn'
        self.query(self.endpoint, asn)

    @property
    def asn(self):
        return self.response_data['asn']

    @property
    def name(self):
        return self.response_data['name']

    @property
    def description(self):
        return self.response_data['description_short']

    @property
    def country_code(self):
        return self.response_data['country_code']

    @property
    def cc(self):
        return self.response_data['country_code']

    @property
    def prefixes(self):
        return Prefixes(self.asn).prefixes

    @property
    def summary(self):
        return ','.join(str(i) for i in [self.asn,self.name,self.description,self.cc])

    @property
    def terse(self):
        return self.summary

class Prefixes(BgpView):

    def __init__(self, asn):
        self.endpoint = 'asn'
        self.query(self.endpoint, ('{}/prefixes').format(asn))

    @property
    def prefixes(self):
        return [i['prefix'] for i in self.response_data['ipv4_prefixes']]

    @property
    def verbose(self):
        prefixes = {}
        for i in self.response_data['ipv4_prefixes']:
            prefixes[i['prefix']] = i

        for i in self.response_data['ipv6_prefixes']:
            prefixes[i['prefix']] = i
        return prefixes

    @property
    def summary(self):
        summary = ''
        for i in self.response_data['ipv4_prefixes']:
            line = [i['prefix'],i['ip'],i['name'],i['description'],i['country_code']]
            line_str = ','.join(str(i) for i in line) + '\n'
            summary += line_str
        return summary

    @property
    def terse(self):
        return self.prefixes

class Peers(BgpView):
    def __init__(self, asn):
        self.endpoint = 'asn'
        self.query(self.endpoint, ('{}/peers').format(asn))

    @property
    def peers(self):
        return [i['asn'] for i in self.response_data['ipv4_peers']]

    @property
    def verbose(self):
        peers = {}
        for i in self.response_data['ipv4_peers']:
            peers[i['asn']] = i
        return peers

    @property
    def summary(self):
        summary = ''
        for i in self.response_data['ipv4_peers']:
            line = [i['asn'],i['name'],i['description'],i['country_code']]
            line_str = ','.join(str(i) for i in line) + '\n'
            summary += line_str
        return summary

    @property
    def terse(self):
        return self.peers

class Upstreams(BgpView):
    def __init__(self, asn):
        self.endpoint = 'asn'
        self.query(self.endpoint, ('{}/upstreams').format(asn))

    @property
    def upstreams(self):
        return [i['asn'] for i in self.response_data['ipv4_upstreams']]

    @property
    def verbose(self):
        peers = {}
        for i in self.response_data['ipv4_upstreams']:
            peers[i['asn']] = i
        return peers

    @property
    def summary(self):
        summary = ''
        for i in self.response_data['ipv4_upstreams']:
            line = [i['asn'],i['name'],i['description'],i['country_code']]
            line_str = ','.join(str(i) for i in line) + '\n'
            summary += line_str
        return summary

    @property
    def terse(self):
        return self.upstreams

class Downstreams(BgpView):
    def __init__(self, asn):
        self.endpoint = 'asn'
        self.query(self.endpoint, ('{}/downstreams').format(asn))

    @property
    def downstreams(self):
        return [i['asn'] for i in self.response_data['ipv4_downstreams']]

    @property
    def verbose(self):
        peers = {}
        for i in self.response_data['ipv4_downstreams']:
            peers[i['asn']] = i
        return peers

    @property
    def summary(self):
        summary = ''
        for i in self.response_data['ipv4_downstreams']:
            line = [i['asn'],i['name'],i['description'],i['country_code']]
            line_str = ','.join(str(i) for i in line) + '\n'
            summary += line_str
        return summary

    @property
    def terse(self):
        return self.downstreams

class IX(BgpView):
    def __init__(self, asn):
        self.endpoint = 'asn'
        self.query(self.endpoint, ('{}/ixs').format(asn))

    @property
    def ixs(self):
        return [i['name_full'] for i in self.response_data]

    @property
    def verbose(self):
        ixs = {}
        for i in self.response_data:
            ixs[i['ix_id']] = i
        return ixs

    @property
    def summary(self):
        summary = ''
        for i in self.response_data:
            line = [i['name'],i['name_full'],i['ipv4_address'],i['country_code']]
            line_str = ','.join(str(i) for i in line) + '\n'
            summary += line_str
        return summary

    @property
    def terse(self):
        return self.ixs

class IP(BgpView):
    def __init__(self, ip):
        self.endpoint = 'ip'
        self.query(self.endpoint, ('{}').format(ip))

    @property
    def asn(self):
        return list({i['asn']['asn'] for i in self.response_data['prefixes']})

    @property
    def country_code(self):
        return list({i['country_code'] for i in self.response_data['prefixes']})

    @property
    def cc(self):
        return self.country_code

    @property
    def name(self):
        return list({i['asn']['name'] for i in self.response_data['prefixes']})

    @property
    def description(self):
        return list({i['asn']['description'] for i in self.response_data['prefixes']})

    @property
    def prefixes(self):
        return [i['prefix'] for i in self.response_data['prefixes']]

    @property
    def verbose(self):
        prefixes = {}
        for i in self.response_data['prefixes']:
            prefixes[i['prefix']] = i
        return prefixes

    @property
    def summary(self):
        summary = ''
        for i in self.response_data['prefixes']:
            line = [i['prefix'],i['asn']['asn'],i['name'],i['description'],i['country_code']]
            line_str = ','.join(str(i) for i in line) + '\n'
            summary += line_str
        return summary

    @property
    def terse(self):
        return self.prefixes


def print_output(data,args):
    if args.verbose:
        print(json.dumps(data.verbose,indent=4))
    elif args.terse:
        print(json.dumps(data.terse,indent=4))
    else:
        print(data.summary)
    return

def main():
    parser = ArgumentParser(description="bgpview.io CLI client")
    subs = parser.add_subparsers(dest='cmd')

    asn = subs.add_parser('asn', help="Query basic ASN data")
    asn.add_argument('--query', '-q', required=True,
                      help="ASN number")
    asn.add_argument('--verbose', '-v', action='store_true',
                      help="show all data")
    asn.add_argument('--terse', '-t', action='store_true',
                      help="show terse data")

    asn = subs.add_parser('prefixes', help="Query prefixes for an ASN")
    asn.add_argument('--query', '-q', required=True,
                      help="ASN number")
    asn.add_argument('--verbose', '-v', action='store_true',
                      help="show all data")
    asn.add_argument('--terse', '-t', action='store_true',
                      help="show terse data")

    asn = subs.add_parser('peers', help="Query peers for an ASN")
    asn.add_argument('--query', '-q', required=True,
                      help="ASN number")
    asn.add_argument('--verbose', '-v', action='store_true',
                      help="show all data")
    asn.add_argument('--terse', '-t', action='store_true',
                      help="show terse data")

    asn = subs.add_parser('upstreams', help="Query upstreams for an ASN")
    asn.add_argument('--query', '-q', required=True,
                      help="ASN number")
    asn.add_argument('--verbose', '-v', action='store_true',
                      help="show all data")
    asn.add_argument('--terse', '-t', action='store_true',
                      help="show terse data")

    asn = subs.add_parser('downstreams', help="Query downstreams for an ASN")
    asn.add_argument('--query', '-q', required=True,
                      help="ASN number")
    asn.add_argument('--verbose', '-v', action='store_true',
                      help="show all data")
    asn.add_argument('--terse', '-t', action='store_true',
                      help="show terse data")

    asn = subs.add_parser('ix', help="Query IXs for an ASN")
    asn.add_argument('--query', '-q', required=True,
                      help="ASN number")
    asn.add_argument('--verbose', '-v', action='store_true',
                      help="show all data")
    asn.add_argument('--terse', '-t', action='store_true',
                      help="show terse data")

    asn = subs.add_parser('ip', help="Query ASN/Prefixes for an IP address")
    asn.add_argument('--query', '-q', required=True,
                      help="IP address")
    asn.add_argument('--verbose', '-v', action='store_true',
                      help="show all data")
    asn.add_argument('--terse', '-t', action='store_true',
                      help="show terse data")

    args, unknown = parser.parse_known_args()
    data = None

    # some tools return ASN in formats like `AS1234`; strip it.
    args.query = args.query.lstrip('AaSsNn')

    try:
        if args.cmd == 'asn':
            data = ASN(args.query)
            print_output(data,args)
        elif args.cmd == 'prefixes':
            data = Prefixes(args.query)
            print_output(data,args)
        elif args.cmd == 'peers':
            data = Peers(args.query)
            print_output(data,args)
        elif args.cmd == 'upstreams':
            data = Upstreams(args.query)
            print_output(data,args)
        elif args.cmd == 'downstreams':
            data = Downstreams(args.query)
            print_output(data,args)
        elif args.cmd == 'ix':
            data = IX(args.query)
            print_output(data,args)
        elif args.cmd == 'ip':
            data = IP(args.query)
            print_output(data,args)
        else:
            parser.print_usage()
            sys.exit(1)

    except ValueError as e:
        parser.print_usage()
        sys.stderr.write('{}\n'.format(str(e)))
        sys.exit(1)

if __name__ == '__main__':
    main()
