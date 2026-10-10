"""Read-only HTTP health probe. Exit nonzero on outage; no synthetic sales or writes."""
import argparse
import json
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

def probe(url, timeout=20):
    started = time.monotonic()
    try:
        with urlopen(Request(url, headers={"User-Agent": "PARADIGMA-health-probe/1.0"}), timeout=timeout) as response:
            body = response.read(65536)
            data = json.loads(body)
            healthy = response.status == 200 and data.get("status") == "ok"
            return {"url": url, "http_status": response.status, "healthy": healthy,
                    "latency_ms": round((time.monotonic()-started)*1000), "service": data.get("service")}
    except (HTTPError, URLError, TimeoutError, ValueError, OSError) as exc:
        return {"url": url, "healthy": False, "error": type(exc).__name__,
                "latency_ms": round((time.monotonic()-started)*1000)}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("url", help="Full HTTPS /health URL")
    p.add_argument("--timeout", type=int, default=20)
    args = p.parse_args()
    result = probe(args.url, args.timeout)
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["healthy"] else 1)
