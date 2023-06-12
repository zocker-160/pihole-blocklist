#! /usr/bin/env python3

import requests

SOURCE_FILE = "sources.list"
DST_FILE = "blocklist.txt"

resultSet = set()
listOfShame = list()

with open(SOURCE_FILE, "r") as src:
    for line in src:
        line = line.strip()
        if len(line) == 0 or line.startswith("#"):
            continue

        print("---")
        print("downloading:", line)
        data = requests.get(line, allow_redirects=True, timeout=5)

        if retCode := data.status_code != 200:
            print("downloading failed with:", retCode)
            listOfShame.append( (retCode, line) )
            continue            

        print("data downloaded", "| ", end="")

        if respData := data.text:
            print("analyzing...")

            for url in respData.splitlines():
                if not url or url.startswith("#"):
                    continue

                if any([x in url for x in ["]", "@", "/"]]):
                    continue

                if url.startswith("0.0.0.0 "):
                    url = url.split()[-1].strip()

                if url == "0.0.0.0":
                    continue

                resultSet.add(url)

print("---")
print(f"Found {len(resultSet):,} unique entries")
print("writing to file", DST_FILE)

with open(DST_FILE, "w") as dst:
    for e in resultSet:
        dst.write(e + "\n")

print("---")

if len(listOfShame) > 0:
    print("following URLs could not be fetched:")
    for item in listOfShame:
        print(item)

    print("---")

#input("Press any key to exit...")
