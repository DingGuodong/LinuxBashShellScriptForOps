
## Ad-hoc command

### pipe('|') support
shell module support pipe('|'), but command module does not.

```shell script
ansible -i hosts prod -m comamnd -a 'pgrep ftp'
ansible -i hosts prod -a 'pgrep ftp'  # default module is command
ansible -i hosts prod -m shell -a 'ps -ef|grep ftp'
``` 
