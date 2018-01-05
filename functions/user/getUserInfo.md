# displaying comprehensive user information

**lslogins - display information about known users in the system**

see more information by '```man lslogins```'

### Description:
Examine the wtmp and btmp logs, /etc/shadow (if necessary) and /etc/passwd and output the desired data.

The default action is to list info about all the users in the system.

The lslogins utility is inspired by the logins utility, which first appeared in FreeBSD 4.10.

>The default UID thresholds are read from /etc/login.defs.

### Examples:
The lslogins command is part of the util-linux package and is available from Linux Kernel Archive ftp://ftp.kernel.org/pub/linux/utils/util-linux/.
```bash
lslogins  # general syntax of lslogins, Displaying basic information about all accounts on the system
lslogins username # Displaying detailed information about a single account
lslogins --logins=0,500,jdoe,esmith --output=UID,USER,LAST-LOGIN,LAST-TTY,FAILED-LOGIN,FAILED-TTY # Displaying specific information about a group of users
lslogins --user-accs --supp-groups --acc-expiration # Displaying information about supplementary groups and password expiration for all user accounts
lslogins --logins=jsmith --output=LAST-LOGIN --time-format=iso | tail -1 # Displaying a single piece of information without the heading
```

### Notes:
package name is "util-linux-ng" in CentOS 6, ```yum info util-linux-ng```, note: some old Release not contains ```lslogins```, use ```yum update -y util-linux-ng``` to update it

package name "isutil-linux" in Ubuntu 16, ```dpkg -S lslogins```, note: this is default

### See also:
[3.4.6. DISPLAYING COMPREHENSIVE USER INFORMATION](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/deployment_guide/sec-displaying_comprehensive_user_information)