## SMTP HELO

At the time the transmission channel is opened there is an exchange to ensure that the hosts are communicating with the
hosts they think they are.

The following two commands are used in transmission channel opening and closing:

```
HELO <SP> <domain> <CRLF>
QUIT <CRLF>
```

In the HELO command the host sending the command identifies itself; the command may be interpreted as saying "Hello, I
am <domain>".

HELLO (HELO)

This command is used to identify the sender-SMTP to the receiver-SMTP. The argument field contains the host name of the
sender-SMTP.

The receiver-SMTP identifies itself to the sender-SMTP in the connection greeting reply, and in the response to this
command.

This command and an OK reply to it confirm that both the sender-SMTP and the receiver-SMTP are in the initial state,
that is, there is no transaction in progress and all state tables and buffers are cleared.

1. `SMTP helo` 并不是必须的，用于向服务器说明自己的身份，参见[RFC821](https://tools.ietf.org/html/rfc821)；

2. `SMTP helo` 通常与 `SMTP Server` 地址的域名一致。例如 `smtpcloud.sohu.com` SMTP服务器地址对应的 `SMTP helo` 是 `sohu.com`。
