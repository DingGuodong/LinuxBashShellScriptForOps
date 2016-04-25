#!/usr/bin/env bash
# Define some regular expressions for matching addresses.
# The regexp here is far from precise, but good enough.
IP_REGEXP="[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
CIDR_REGEXP="$IP_REGEXP/[0-9]{1,2}"
echo "$1" | grep -E "^$CIDR_REGEXP$" >/dev/null

# TODO validate command ipcalc if exists
# /etc/sysconfig/network-scripts/network-functions-ipv6 (CentOS Linux release 7.2.1511 (Core))
## Test a given IPv6 address for validity
#  $1: <IPv6 address>
# return code: 0=ok 1=not valid
ipv6_test_ipv6_addr_valid() {
        ipcalc -cs6 $1
}

## Test a given IPv4 address for validity
#  $1: <IPv4 address>
# return code: 0=ok 1=not valid
ipv6_test_ipv4_addr_valid() {
        ipcalc -cs4 $1
}

## Test a given IPv4 address for not a private but unicast one
#  $1: <IPv4 address>
# return code: 0=ok 1=argument error 10=private or not unicast
ipv6_test_ipv4_addr_global_usable() {
        local fn="ipv6_test_ipv4_addr_global_usable"

        local testipv4addr_globalusable=$1


        if [ -z "$testipv4addr_globalusable" ]; then
                return 1
        fi

        # Test for a globally usable IPv4 address now
                # test 0.0.0.0/8
                /bin/ipcalc --network $testipv4addr_globalusable 255.0.0.0   | LC_ALL=C grep -q "NETWORK=0\.0\.0\.0"     && return 10
                # test 10.0.0.0/8     (RFC 1918 / private)
                /bin/ipcalc --network $testipv4addr_globalusable 255.0.0.0   | LC_ALL=C grep -q "NETWORK=10\.0\.0\.0"    && return 10
                # test 127.0.0.0/8    (loopback)
                /bin/ipcalc --network $testipv4addr_globalusable 255.0.0.0   | LC_ALL=C grep -q "NETWORK=127\.0\.0\.0"   && return 10
                # test 169.254.0.0/16 (APIPA / DHCP link local)
                /bin/ipcalc --network $testipv4addr_globalusable 255.255.0.0 | LC_ALL=C grep -q "NETWORK=169\.254\.0\.0" && return 10
                # test 172.16.0.0/12  (RFC 1918 / private)
                /bin/ipcalc --network $testipv4addr_globalusable 255.240.0.0 | LC_ALL=C grep -q "NETWORK=172\.16\.0\.0"  && return 10
                # test 192.168.0.0/16 (RFC 1918 / private)
                /bin/ipcalc --network $testipv4addr_globalusable 255.255.0.0 | LC_ALL=C grep -q "NETWORK=192\.168\.0\.0" && return 10
                # test 224.0.0.0/3    (multicast and reserved, broadcast)
                /bin/ipcalc --network $testipv4addr_globalusable 224.0.0.0   | LC_ALL=C grep -q "NETWORK=224\.0\.0\.0"   && return 10

        return 0
}

function is_reserved_ip_address(){
    # Refer to: https://en.wikipedia.org/wiki/Reserved_IP_addresses
    # /etc/sysconfig/network-scripts/network-functions-ipv6 (CentOS Linux release 7.2.1511 (Core))
    test_ipv4_addr_global_usable=$1
    ipcalc -cs4 "$test_ipv4_addr_global_usable"
    ipcalc -cs6 "$test_ipv4_addr_global_usable"
    /bin/ipcalc --network "$test_ipv4_addr_global_usable" 255.0.0.0   | LC_ALL=C grep -q "NETWORK=0\.0\.0\.0"     && return 10
    /bin/ipcalc --network "$test_ipv4_addr_global_usable" 255.0.0.0   | LC_ALL=C grep -q "NETWORK=10\.0\.0\.0"    && return 10
    /bin/ipcalc --network "$test_ipv4_addr_global_usable" 255.0.0.0   | LC_ALL=C grep -q "NETWORK=127\.0\.0\.0"   && return 10
    /bin/ipcalc --network "$test_ipv4_addr_global_usable" 255.255.0.0 | LC_ALL=C grep -q "NETWORK=169\.254\.0\.0" && return 10
    /bin/ipcalc --network "$test_ipv4_addr_global_usable" 255.240.0.0 | LC_ALL=C grep -q "NETWORK=172\.16\.0\.0"  && return 10
    /bin/ipcalc --network "$test_ipv4_addr_global_usable" 255.255.0.0 | LC_ALL=C grep -q "NETWORK=192\.168\.0\.0" && return 10
    /bin/ipcalc --network "$test_ipv4_addr_global_usable" 224.0.0.0   | LC_ALL=C grep -q "NETWORK=224\.0\.0\.0"   && return 10
}
