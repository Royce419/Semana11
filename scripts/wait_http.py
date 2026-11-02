import sys
import time
from urllib.request import urlopen

url = sys.argv[1]
retries = int(sys.argv[2]) if len(sys.argv) > 2 else 30

for attempt in range(retries):
    try:
        with urlopen(url, timeout=3) as response:
            if 200 <= response.status < 400:
                print(f"Servicio disponible: {url}")
                raise SystemExit(0)
    except Exception:
        time.sleep(2)

print(f"El servicio no respondió a tiempo: {url}", file=sys.stderr)
raise SystemExit(1)
