#!/usr/bin/env python
import requests
import time
import sys
import json

BASE_URL = "https://www.muckrock.com/api_v1/foia/"

MAX_TRIES = 5

def get_page(page_num):
    sys.stderr.write("{0}\n".format(page_num))
    res = requests.get(BASE_URL, params={
        "format": "json",
        "page": page_num
    }).json()

    if "results" in res:
        return res["results"]
    else:
        return []

def try_get_page(page_num):
    tries = 0
    while tries < MAX_TRIES:
        try:
            return get_page(page_num)
        except:
            tries += 1
            time.sleep(1)
    raise Exception("TOO MANY FAILS ON PAGE {0}".format(page_num))


def get_all_results(max_page=None):
    results = []
    page_no = 1
    while (page_no == None) == (page_no <= int(max_page or 0)):
        res = try_get_page(page_no)
        if len(res) == 0:
            return results
        results += res
        page_no += 1
    return results

if __name__ == "__main__":
    json.dump(get_all_results(), sys.stdout, indent=2)
