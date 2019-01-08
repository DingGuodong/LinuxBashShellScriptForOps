# how to install common libraries for data crypt

common libraries for security

* openssl
* libsodium

> current best practice is:  
using RSA to transfer AES keys, then using AES transfer data.  
Exchanging DES or AES data-encrypting keys using an RSA key scheme  
Distributing a DES data-encrypting key using an RSA cryptographic scheme

## [openssl](https://www.openssl.org/)

### install openssl on Microsoft Windows
https://www.openssl.org/source/

https://www.openssl.org/community/binaries.html

https://wiki.openssl.org/index.php/Binaries

https://slproweb.com/products/Win32OpenSSL.html
> this project is best practice

https://slproweb.com/download/Win64OpenSSL-1_1_1a.exe
>  If you installed 64bit Python, you should install 64bit OpenSSL.

> Win64OpenSSL will Copy OpenSSL DLLs to:  
The Windows system directory or The OpenSSL binaries (/bin) directory.  
libcrypto-1_1-x64.dll  
libssl-1_1-x64.dll

### install openssl on Linux
Debian, Ubuntu, RHEL, CentOS
```bash
sudo apt install openssl libssl libssl-dev || sudo yum install openssl openssl-devel
```

## [libsodium](https://github.com/jedisct1/libsodium)
If you want to use salsa20 or chacha20 encryption, 
download libsodium and put dll files (without path) into 
C:\Windows\System32 or C:\Windows\SysWOW64 (32bit Python on 64bit Windows).

### install libsodium on Microsoft Windows
https://github.com/jedisct1/libsodium

https://download.libsodium.org/doc/

https://download.libsodium.org/libsodium/releases/

https://download.libsodium.org/libsodium/releases/libsodium-1.0.17-msvc.zip

Copy next 4 files in libsodium-1.0.17-msvc.zip\x64\Release\v141\dynamic to C:\Windows\System32
1. libsodium.dll
2. libsodium.exp
3. libsodium.lib
4. libsodium.pdb

### install libsodium on Linux

Debian, Ubuntu, RHEL, CentOS
```bash
sudo apt-get install build-essential -y
wget https://github.com/jedisct1/libsodium/releases/download/1.0.17/libsodium-1.0.17.tar.gz
#wget https://download.libsodium.org/libsodium/releases/libsodium-1.0.17.tar.gz
tar xf libsodium-1.0.17.tar.gz && cd libsodium-1.0.17
./configure
make && make check
sudo make install
#ldconfig
```


