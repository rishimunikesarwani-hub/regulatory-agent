"""Wait for the local API before browser integration checks."""
import sys
import time
from urllib.request import urlopen

for attempt in range(30):
    try:
        with urlopen(sys.argv[1], timeout=1) as response:
            if response.status == 200:
                break
    except OSError:
        time.sleep(1)
else:
    raise SystemExit("Local API did not become ready")
