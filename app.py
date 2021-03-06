#!/usr/bin/env python3
import random, string, threading, requests
from datetime import datetime, timedelta
from azure.data.tables import TableClient
from azure.core.exceptions import ServiceRequestError

# Azure Data Tables Info
AZURE_ACC_KEY = "..."
AZURE_ENDPOINT_SUFFIX = "..."
AZURE_ACC_NAME = "..."
AZURE_CONN_STR = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix={}".format(
    AZURE_ACC_NAME, AZURE_ACC_KEY, AZURE_ENDPOINT_SUFFIX
)

# Sucuri Info
AZURE_TABLE_NAME = "..."
SUCURI_API_URL = "https://waf.sucuri.net/api?v2"
SUCURI_API_KEY = "..."
SUCURI_SITES = [
    ...
]

CHARS = 'abcdef' + string.digits

# Azure Data Tables
def sucuri_to_azure_table(domain, key, secret, date, mutex):
    mutex.acquire()
    body = requests.post(
        SUCURI_API_URL,
        data={
            "k": key,
            "s": secret,
            "a": "audit_trails",
            "date": date.strftime("%Y-%m-%d"),
            "format": "json",
            "limit": 1000
        }
    ).json()
    if len(body) > 2 and len(body) > 6:
        for o in body:
            ROW_KEY = '-'.join([
                ''.join(random.choices(CHARS, k=8)),
                ''.join(random.choices(CHARS, k=4)),
                ''.join(random.choices(CHARS, k=4)),
                ''.join(random.choices(CHARS, k=4)),
                ''.join(random.choices(CHARS, k=12))
            ])
            ENTITY_TEMPLATE = {
                "PartitionKey": domain,
                "RowKey": ROW_KEY,
            }
            try:
                o["request_date"] = date.strftime("%d-%b-%Y")
                o["request_time"] = datetime.now().strftime("%H:%M:%S")
            except:
                pass
            try:
                del o['geo_location']
            except KeyError:
                ENTITY = ENTITY_TEMPLATE | o
                with TableClient.from_connection_string(AZURE_CONN_STR, AZURE_TABLE_NAME) as table_client:
                    try:
                        resp = table_client.create_entity(entity=ENTITY)
                    except ServiceRequestError:
                        pass
                continue
            except TypeError:
                pass
            else:
                ENTITY = ENTITY_TEMPLATE | o
                with TableClient.from_connection_string(AZURE_CONN_STR, AZURE_TABLE_NAME) as table_client:
                    try:
                        resp = table_client.create_entity(entity=ENTITY)
                    except ServiceRequestError:
                        pass
    mutex.release()
                    
if __name__ == "__main__":
    yesterday = datetime.now() - timedelta(1)
    threads = list()
    mtx = threading.Lock()
    for i in SUCURI_SITES:
        data = requests.post(
            SUCURI_API_URL,
            data={
                "k": SUCURI_API_KEY,
                "s": i['secret'],
                "a": "show_settings"
            }
        ).json()
        i['enabled'] = True if data['output']['proxy_active'] == 1 else False
        i['domain'] = data['output']['domain']
        i['key'] = SUCURI_API_KEY
        if i["enabled"]:
            x = threading.Thread(
                target=sucuri_to_azure_table,
                args=(
                    i["domain"],
                    i["key"],
                    i["secret"],
                    yesterday,
                    mtx
                ), daemon=True
            )
            threads.append(x)
            x.start()
    for index, thread in enumerate(threads):
        thread.join()
        