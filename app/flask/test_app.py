import sys
import time
import requests

URL = "http://localhost:5000/view"

for i in range(1, 4):
    r = requests.get(URL, timeout=3)

    if r.status_code != 200:
        print(f"FAIL request {i}: {r.status_code}")
        sys.exit(1)

    print(f"OK request {i}")
    time.sleep(1)

print("OK")
sys.exit(0)
