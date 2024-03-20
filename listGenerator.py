#! /usr/bin/env python3

import re
import requests

SOURCE_FILE = "sources.list"
DST_FILE = "blocklist.txt"
DST_FILE_UNF = "blocklistunfiltered.txt"

resultSet = set()
listOfShame = list()

DOMAIN_REG = r"^(\S+\.)*\S+\.[a-zA-Z]{2,}$"

def isLocalhostSplit(line: str) -> bool:
    locIPs = [
        "0.0.0.0 ",
        "127.0.0.1 "
        "::1 "
    ]

    return any([line.startswith(x) for x in locIPs])


with open(SOURCE_FILE, "r") as src, open(DST_FILE_UNF, "w") as dstUnf:
    for line in src:
        line = line.strip()
        if len(line) == 0 or line.startswith("#"):
            continue

        print("---")
        print("downloading:", line)
        data = requests.get(line, allow_redirects=True, timeout=5)

        retCode = data.status_code
        if retCode != 200:
            print("downloading failed with:", retCode)
            listOfShame.append( (retCode, line) )
            continue

        print("data downloaded", "| ", end="")

        if respData := data.text:
            print("analyzing...")

            for url in respData.splitlines():
                if not url:
                    continue

                url = url.strip()

                dstUnf.write(url + "\n")

                # comment
                if url.startswith("#"):
                    continue
                # ABP list comment
                if url.startswith("!"):
                    continue

                # filter entries like "||abandonedclover.com^"
                if url.startswith("||"):
                    url = url[2:]

                if url.endswith("^"):
                    url = url[:-1]

                if any([x in url for x in ["[", "]", "@", "/", "\\"]]):
                    continue

                if isLocalhostSplit(url):
                    url = url.split()[1]

                if " " in url:
                    url = url.split()[0]

                if "\t" in url:
                    url = url.split("\t")[0].strip()

                if not re.match(DOMAIN_REG, url):
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
