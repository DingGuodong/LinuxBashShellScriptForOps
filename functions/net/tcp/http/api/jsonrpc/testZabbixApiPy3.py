#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Do not reinventing the wheel
import sys

if sys.version_info[0] != 3:
    print "This py script need python version >= 3"
    exit(sys.version_info)
elif sys.version_info[0] == 3:
    import http.client

    conn = http.client.HTTPSConnection("ops.huntor.cn")

    payload = "{\r\n    \"jsonrpc\": \"2.0\",\r\n    \"method\": \"user.login\",\r\n    \"params\": {\r\n        \"user\": \"Admin\",\r\n        \"password\": \"Pc608qq2Cd\"\r\n    },\r\n    \"id\": 1,\r\n    \"auth\": null\r\n}"

    headers = {
        'content-type': "application/json-rpc",
        'cache-control': "no-cache",
        'postman-token': "b4f440e8-ac7a-ca8a-1c6f-6956ad707da0"
    }

    conn.request("POST", "/api_jsonrpc.php", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
