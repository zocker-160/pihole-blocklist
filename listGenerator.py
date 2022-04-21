#! /usr/bin/env python3

import time
import requests

SOURCE_FILE = "sources.list"
DST_FILE = "blocklist.txt"

dst = open(DST_FILE, "w")

with open(SOURCE_FILE, "r") as src:
    for line in src:
        if line.startswith("#"):
            continue

        line = line.strip()

        print("---")
        print("requesting data from:", line)
        data = requests.get(line, allow_redirects=True, timeout=5)
        
        if stCode := data.status_code == 200:
            print("data downloaded ", end="")

            if respData := data.text:
                print("writing data...")

                for url in respData.splitlines():
                    if not url or url.startswith("#"):
                        continue

                    if url.startswith("0.0.0.0"):
                        url = url.split()[-1].strip()

                    dst.write(url + "\n")

        else:
            print("downloading data failed with code:", stCode)
            time.sleep(1)

dst.close()
