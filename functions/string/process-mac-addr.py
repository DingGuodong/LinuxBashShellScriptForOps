#!/usr/bin/python3

def format_mac_to_type_1(addr):
    """
    Transform MAC address to specified format.
    example:
        00-2B-67-59-47-0E --> 002b.6759.470e
        00:2B:67:59:47:0E --> 002b.6759.470e
    """
    mac_without_delimiter = addr.strip().replace("-", "").replace(":", "").lower()

    mac = list()
    for i, x in enumerate(mac_without_delimiter):
        mac.append(x)
        if (i + 1) % 4 == 0 and i != (len(mac_without_delimiter) - 1):
            mac.append('.')

    return "".join(mac)

if __name__ == '__main__':
    print(format_mac_to_type_1("00-2B-67-59-47-0E"))
