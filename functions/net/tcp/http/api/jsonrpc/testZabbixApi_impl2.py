#!/usr/bin/python
# -*- coding: utf-8 -*-
# Do not reinventing the wheel
import requests

url = "https://ops.huntor.cn/api_jsonrpc.php"

payload = "{\r\n    \"jsonrpc\": \"2.0\",\r\n    \"method\": \"user.login\",\r\n    \"params\": {\r\n        \"user\": \"Admin\",\r\n        \"password\": \"Pc608qq2Cd\"\r\n    },\r\n    \"id\": 1,\r\n    \"auth\": null\r\n}"
headers = {
    'content-type': "application/json-rpc",
    'cache-control': "no-cache",
    'postman-token': "0475d1dd-6e97-a0af-6d12-1d6a3fdbc4e1"
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
