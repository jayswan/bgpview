# bgpview

This is a CLI client for the https://bgpview.io API.

```
usage: bgpview.py [-h] {asn,prefixes,peers,upstreams,downstreams,ix,ip} ...

bgpview.io CLI client

positional arguments:
  {asn,prefixes,peers,upstreams,downstreams,ix,ip}
    asn                 Query basic ASN data
    prefixes            Query prefixes for an ASN
    peers               Query peers for an ASN
    upstreams           Query upstreams for an ASN
    downstreams         Query downstreams for an ASN
    ix                  Query IXs for an ASN
    ip                  Query ASN/Prefixes for an IP address

Each option has a summary, verbose, and terse option. The summary is the default.

```

The `--verbose` option returns the full JSON from the API.

The summary and terse options only return IPv4 data. If you want IPv6 data, use `--verbose`.

Some examples of the default summary output:

```
$ bgpview asn -q 36459
36459,GITHUB,GitHub, Inc.,US

$ bgpview prefixes -q 36459
140.82.112.0/20,140.82.112.0,GITHU,GitHub, Inc.,US
140.82.112.0/24,140.82.112.0,GITHU,GitHub, Inc.,US
140.82.113.0/24,140.82.113.0,GITHU,GitHub, Inc.,US
<etc>

$ bgpview upstreams -q 36459
1299,TELIANET,Telia Carrier,EU
2914,NTT-COMMUNICATIONS-2914,NTT America, Inc.,US
6461,ZAYO-6461,Zayo Bandwidth,US
3257,GTT-BACKBONE,GTT,DE
2828,XO-AS15,MCI Communications Services, Inc. d/b/a Verizon Business,US

$ bgpview ip -q 192.30.252.1
192.30.252.0/24,36459,GITHUB-NET4-1,GitHub, Inc.,US
192.30.252.0/23,36459,GITHUB-NET4-1,GitHub, Inc.,US
192.30.252.0/22,36459,GITHUB-NET4-1,GitHub, Inc.,US
```

Each class in the module is suitable for import in Python apps as well:

```
In [1]: from bgpview import IP,ASN,Prefixes

In [2]: a = IP('192.30.252.1')

In [3]: a.name
Out[3]: ['GITHUB']

In [4]: a.description
Out[4]: ['GitHub, Inc.']

In [5]: a.country_code
Out[5]: ['US']

In [6]: a.prefixes
Out[6]: ['192.30.252.0/24', '192.30.252.0/23', '192.30.252.0/22']

In [7]: a.asn
Out[7]: [36459]

In [8]: b = ASN(a.asn[0])

In [9]: b.prefixes
Out[9]:
['140.82.112.0/20',
 '140.82.112.0/24',
 '140.82.113.0/24',
 '140.82.114.0/24',
 '140.82.115.0/24',
 '140.82.116.0/24',
 '140.82.117.0/24',
 '140.82.118.0/24',
 '140.82.119.0/24',
 '140.82.120.0/24',
 '140.82.121.0/24',
 '140.82.122.0/24',
 '140.82.123.0/24',
 '140.82.124.0/24',
 '140.82.125.0/24',
 '140.82.126.0/24',
 '140.82.127.0/24',
 '192.30.252.0/23',
 '192.30.252.0/24',
 '192.30.252.0/22',
 '192.30.253.0/24',
 '192.30.254.0/23',
 '192.30.254.0/24',
 '192.30.255.0/24']
 ```
