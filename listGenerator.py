#! /usr/bin/env python3

import requests

SOURCE_FILE = "sources.list"
DST_FILE = "blocklist.txt"

listOfShame = list()

with open(SOURCE_FILE, "r") as src, open(DST_FILE, "w") as dst:
    for line in src:
        line = line.strip()
        if len(line) == 0 or line.startswith("#"):
            continue

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

                    if "]" in url or "@" in url:
                        continue

                    if url.startswith("0.0.0.0"):
                        url = url.split()[-1].strip()

                    dst.write(url + "\n")

        else:
            print("downloading data failed with code:", stCode)
            listOfShame.append( (stCode, line) )

if len(listOfShame) > 0:
    print("following URLs could not be fetched:")
    for item in listOfShame:
        print(item)
