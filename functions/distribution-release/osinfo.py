#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) 2014, Matthew Brennan Jones <matthew.brennan.jones@gmail.com>
# Py-osinfo is a Python module to get the OS type, brand, release, and kernel
# It uses a MIT style license
# It is hosted at: https://github.com/workhorsy/py-osinfo
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import os
import platform


class OSType(object):
    BeOS = ['BeOS']
    BSD = ['BSD']
    Cygwin = ['Cygwin']
    MacOS = ['MacOS']
    Linux = ['Linux']
    Solaris = ['Solaris']
    Windows = ['Windows']

    unknown = ['Unknown']

    withoutRoot = [Cygwin[0], Windows[0], BeOS[0]]
    Unix = [BSD[0], MacOS[0], Solaris[0]]
    Nix = [BSD[0], Linux[0], MacOS[0], Solaris[0]]


class OSBrand(object):
    AndroidAlpha = ['AndroidAlpha']
    AndroidBeta = ['AndroidBeta']
    AndroidCupcake = ['AndroidCupcake']
    AndroidDonut = ['AndroidDonut']
    AndroidEclair = ['AndroidEclair']
    AndroidFroyo = ['AndroidFroyo']
    AndroidGingerbread = ['AndroidGingerbread']
    AndroidHoneycomb = ['AndroidHoneycomb']
    AndroidIceCreamSandwich = ['AndroidIceCreamSandwich']
    AndroidJellyBean = ['AndroidJellyBean']
    AndroidKitKat = ['AndroidKitKat']
    AndroidUnofficial = ['AndroidUnofficial']
    Arch = ['Arch']
    ArchBang = ['ArchBang']
    BeOS = ['BeOS']
    Bodhi = ['Bodhi']
    CentOS = ['CentOS']
    Chakra = ['Chakra']
    Clonezilla = ['Clonezilla']
    CrunchBang = ['CrunchBang']
    Cygwin = ['Cygwin']
    DamnSmallLinux = ['DamnSmallLinux']
    Debian = ['Debian']
    DragonFlyBSD = ['DragonFlyBSD']
    elementary = ['elementary']
    Fedora = ['Fedora']
    FreeBSD = ['FreeBSD']
    Gentoo = ['Gentoo']
    GoboLinux = ['GoboLinux']
    Haiku = ['Haiku']
    Kali = ['Kali']
    KNOPPIX = ['KNOPPIX']
    LinuxMint = ['LinuxMint']
    LXLE = ['LXLE']
    Mageia = ['Mageia']
    Manjaro = ['Manjaro']
    Mandrake = ['Mandrake']
    Mandriva = ['Mandriva']
    MEPIS = ['MEPIS']
    Milax = ['Milax']
    NetBSD = ['NetBSD']
    Nexenta = ['Nexenta']
    OpenBSD = ['OpenBSD']
    OpenIndiana = ['OpenIndiana']
    OpenSolaris = ['OpenSolaris']
    openSUSE = ['openSUSE']
    OpenSXCE = ['OpenSXCE']
    OracleLinux = ['OracleLinux']
    OSX = ['OSX']
    Parsix = ['Parsix']
    PeppermintOS = ['PeppermintOS']
    PCBSD = ['PCBSD']
    PCLinuxOS = ['PCLinuxOS']
    Puppy = ['Puppy']
    RedHat = ['RedHat']
    Sabayon = ['Sabayon']
    Salix = ['Salix']
    Siduction = ['Siduction']
    ScientificLinux = ['ScientificLinux']
    Simplicity = ['Simplicity']
    Slackware = ['Slackware']
    Sparky = ['Sparky']
    Solaris = ['Solaris']
    SteamOS = ['SteamOS']
    Tanglu = ['Tanglu']
    Trisquel = ['Trisquel']
    Ubuntu = ['Ubuntu']
    UltimateEdition = ['UltimateEdition']
    Vector = ['Vector']
    WindowsXP = ['WindowsXP']
    WindowsVista = ['WindowsVista']
    Windows7 = ['Windows7']
    Windows8 = ['Windows8']
    Windows10 = ['Windows10']
    WindowsServer2003 = ['WindowsServer2003']
    WindowsServer2003R2 = ['WindowsServer2003R2']
    WindowsServer2008 = ['WindowsServer2008']
    WindowsServer2008R2 = ['WindowsServer2008R2']
    WindowsServer2012 = ['WindowsServer2012']
    WindowsServer2012R2 = ['WindowsServer2012R2']
    Zorin = ['Zorin']

    unknown = ['Unknown']


def _get_os_type():
    os_type = OSType.unknown[0]

    # Figure out the general OS type
    uname = platform.system().strip().strip('"').strip("'").strip().lower()
    if 'beos' in uname or 'haiku' in uname:
        os_type = OSType.BeOS[0]
    elif 'bsd' in uname or 'gnu/kfreebsd' in uname:
        os_type = OSType.BSD[0]
    elif 'cygwin' in uname:
        os_type = OSType.Cygwin[0]
    elif 'darwin' in uname:
        os_type = OSType.MacOS[0]
    elif 'linux' in uname:
        os_type = OSType.Linux[0]
    elif 'solaris' in uname or 'sunos' in uname:
        os_type = OSType.Solaris[0]
    elif 'windows' in uname:
        os_type = OSType.Windows[0]

    return os_type


def _get_os_brand(os_type):
    dist = platform.dist()

    # Figure out the brand
    if os_type in OSType.BeOS:
        name = platform.system().strip().strip('"').strip("'").strip().lower()

        if 'beos' == name:
            return OSBrand.BeOS[0]
        elif 'haiku' == name:
            return OSBrand.Haiku[0]
    elif os_type in OSType.BSD:
        name = dist[0] or platform.system()
        name = name.strip().strip('"').lower()

        if 'debian' == name:
            return OSBrand.Debian[0]
        elif 'dragonflybsd' == name:
            return OSBrand.DragonFlyBSD[0]
        elif 'freebsd' == name:
            return OSBrand.FreeBSD[0]
        elif 'netbsd' == name:
            return OSBrand.NetBSD[0]
        elif 'openbsd' == name:
            return OSBrand.OpenBSD[0]
        elif 'pcbsd' == name:
            return OSBrand.PCBSD[0]
    elif os_type in OSType.Cygwin:
        return platform.system()
    elif os_type in OSType.MacOS:
        name = platform.mac_ver()[0].strip().strip('"').lower()
        if name.startswith('10'):
            return OSBrand.OSX[0]
    elif os_type in OSType.Linux:
        if os.path.isfile('/etc/lsb-release-crunchbang'):
            return OSBrand.CrunchBang[0]
        elif os.path.isfile('/etc/sabayon-edition'):
            return OSBrand.Sabayon[0]
        elif os.path.isfile('/etc/arch-release'):
            return OSBrand.Arch[0]

        linux_dist = platform.linux_distribution()
        name = linux_dist[0] or dist[0]
        name = name.strip().strip('"').lower()

        if not name:
            if os.path.isfile('/etc/lsb-release'):
                with open('/etc/lsb-release') as f:
                    name = f.read()
                    name = name.split('DISTRIB_ID=')[1].split('\n')[0]
                    name = name.lower()
                    if 'manjaro' in name:
                        return OSBrand.Manjaro[0]
        elif 'centos' == name:
            return OSBrand.CentOS[0]
        elif 'debian' == name:
            return OSBrand.Debian[0]
        elif 'elementary os' == name:
            return OSBrand.elementary[0]
        elif 'fedora' == name:
            return OSBrand.Fedora[0]
        elif 'gentoo' in name:
            return OSBrand.Gentoo[0]
        elif 'linuxmint' == name:
            return OSBrand.LinuxMint[0]
        elif 'mageia' == name:
            return OSBrand.Mageia[0]
        elif 'mandrake' == name:
            return OSBrand.Mandrake[0]
        elif 'mandriva' == name:
            return OSBrand.Mandriva[0]
        elif 'redhat' == name:
            return OSBrand.RedHat[0]
        elif 'scientific linux' == name:
            return OSBrand.ScientificLinux[0]
        elif 'slackware' == name:
            return OSBrand.Slackware[0]
        elif 'suse' == name or 'opensuse' == name:
            return OSBrand.openSUSE[0]
        elif 'ubuntu' == name:
            return OSBrand.Ubuntu[0]
    elif os_type in OSType.Solaris:
        ver = platform.version().strip().strip('"').lower()
        if ver.startswith('milax'):
            return OSBrand.Milax[0]
        elif ver.startswith('oi_'):
            return OSBrand.OpenIndiana[0]
        elif ver.startswith('opensxce'):
            return OSBrand.OpenSXCE[0]
        elif platform.uname()[1].strip().lower() == 'opensolaris':
            return OSBrand.OpenSolaris[0]
        elif ver.startswith('nexenta'):
            return OSBrand.Nexenta[0]
    elif os_type in OSType.Windows:
        name = platform.release().strip().strip('"').lower()

        if 'xp' == name:
            return OSBrand.WindowsXP[0]
        elif 'vista' == name:
            return OSBrand.WindowsVista[0]
        elif '7' == name:
            return OSBrand.Windows7[0]
        elif '8' == name:
            return OSBrand.Windows8[0]
        elif '10' == name:
            return OSBrand.Windows10[0]
        elif '2003server' == name:
            return OSBrand.WindowsServer2003[0]
        elif '2003serverr2' == name:
            return OSBrand.WindowsServer2003R2[0]
        elif '2008server' == name:
            return OSBrand.WindowsServer2008[0]
        elif '2008serverr2' == name:
            return OSBrand.WindowsServer2008R2[0]
        elif '2012server' == name:
            return OSBrand.WindowsServer2012[0]
        elif '2012serverrc' == name:
            return OSBrand.WindowsServer2012R2[0]

    return OSBrand.unknown[0]


def _get_os_release(os_type):
    os_release = 'unknown'
    dist = platform.dist()

    # Figure out the release
    if os_type in OSType.BeOS:
        os_release = platform.release().lower()
    elif os_type in OSType.BSD:
        os_release = platform.release().lower().rstrip('-release')
    elif os_type in OSType.Cygwin:
        os_release = platform.release().split('(')[0]
    elif os_type in OSType.Linux:
        if os.path.isfile('/etc/lsb-release-crunchbang'):
            with open('/etc/lsb-release-crunchbang', 'r') as f:
                lsb = f.read().lower()
                if lsb:
                    os_release = lsb.split('distrib_release=')[1].split("\n")[0]
        elif os.path.isfile('/etc/sabayon-edition'):
            with open('/etc/sabayon-edition', 'r') as f:
                data = f.read().lower().strip().split()
                if data and len(data) > 2:
                    os_release = data[2]
        elif os.path.isfile('/etc/lsb-release'):
            with open('/etc/lsb-release') as f:
                data = f.read()
                data = data.split('DISTRIB_RELEASE=')[1].split('\n')[0]
                data = data.lower()
                os_release = data
        else:
            linux_dist = platform.linux_distribution()
            os_release = linux_dist[1].lower() or dist[1].lower()
    elif os_type in OSType.MacOS:
        os_release = platform.mac_ver()[0].lower()
    elif os_type in OSType.Solaris:
        ver = platform.version().lower()
        os_release = ver.lstrip('oi_')
    elif os_type in OSType.Windows:
        dist = platform.version().lower()
        os_release = dist

    os_release = os_release.strip()
    return os_release


def _get_os_kernel(os_type):
    os_kernel = 'unknown'

    if os_type in OSType.BeOS:
        k = platform.release()
        k = [int(n) for n in k]
        k = tuple(k)
        os_kernel = k
    elif os_type in OSType.BSD:
        k = platform.release().split('-')[0].split('.')
        k = [int(n) for n in k]
        k = tuple(k)
        os_kernel = k
    elif os_type in OSType.Cygwin:
        k = platform.release().split('(')[0].split('.')
        k = [int(n) for n in k]
        k = tuple(k)
        os_kernel = k
    elif os_type in OSType.Linux:
        k = platform.uname()[2].split('-')[0].split('.')
        k = [int(n) for n in k]
        k = tuple(k)
        os_kernel = k
    elif os_type in OSType.MacOS:
        k = platform.release().split('.')
        k = [int(n) for n in k]
        k = tuple(k)
        os_kernel = k
    elif os_type in OSType.Solaris:
        k = platform.release().split('.')
        k = [int(n) for n in k]
        k = tuple(k)
        os_kernel = k
    elif os_type in OSType.Windows:
        k = platform.version().split('.')
        k = [int(n) for n in k]
        k = tuple(k)
        os_kernel = k

    return os_kernel


def get_os_info():
    os_type = _get_os_type()
    os_brand = _get_os_brand(os_type)
    os_release = _get_os_release(os_type)
    os_kernel = _get_os_kernel(os_type)

    return os_type, os_brand, os_release, os_kernel


def main():
    os_type, os_brand, os_release, os_kernel = get_os_info()

    print('type: {0}'.format(os_type))
    print('brand: {0}'.format(os_brand))
    print('release: {0}'.format(os_release))
    print('kernel: {0}'.format(os_kernel))


if __name__ == '__main__':
    main()
