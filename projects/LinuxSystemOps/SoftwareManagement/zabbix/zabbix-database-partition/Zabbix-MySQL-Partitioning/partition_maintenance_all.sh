#!/bin/bash

echo "Partitioned table maintenance tasks begin at $(date +%Y%m%d%H%M%S)." >/tmp/partition_maintenance_all_mail.tmp
# shellcheck disable=SC2129
echo '' >>/tmp/partition_maintenance_all_mail.tmp

mysql -D zabbix -e 'CALL partition_maintenance_all("zabbix");' >>/tmp/partition_maintenance_all_mail.tmp 2>&1

echo '' >>/tmp/partition_maintenance_all_mail.tmp
echo "Partitioned table maintenance tasks finish at $(date +%Y%m%d%H%M%S)." >>/tmp/partition_maintenance_all_mail.tmp

#cat /tmp/partition_maintenance_all_mail.tmp | mailx -r 'ITmonitor@didichuxing.com' -s 'Partitioned table maintenance' gaoyuebruce@didiglobal.com

CURL_DATA="{
  \"content\": \"$(sed ":a;N;s/\n/<br \/>/;s/\t/ /g;ta" /tmp/partition_maintenance_all_mail.tmp)\",
  \"sender\": \"erpmonitor@didiglobal.com\",
  \"subject\": \"Partitioned table maintenance\",
  \"tos\": [
    \"gaoyuebruce@didiglobal.com\"
  ]
}
"

curl -X POST --header "Content-Type: application/json" --header "Accept: */*" -d "$CURL_DATA" "http://10.89.139.46:8088/api/v2/notification/email/send?token=【token值】"
