"""Real, opt-in worker heartbeat. No fake clicks, purchases or social posts.
Run as a separate Render background worker with WERO_BASE_URL and WERO_ADMIN_TOKEN.
"""
import json
import os
import signal
import time
import urllib.request
import urllib.error

BASE=os.environ.get("WERO_BASE_URL","").rstrip("/")
TOKEN=os.environ.get("WERO_ADMIN_TOKEN","")
ROBOT=os.environ.get("WERO_ROBOT_ID","WERO1-PAI")
PARENT=os.environ.get("WERO_PARENT_ROBOT_ID","")
INTERVAL=max(30,int(os.environ.get("WERO_HEARTBEAT_INTERVAL","60")))
RUN=True

def stop(*_):
    global RUN
    RUN=False

def heartbeat():
    data=json.dumps({"robot_id":ROBOT,"parent_robot_id":PARENT or None}).encode()
    req=urllib.request.Request(BASE+"/api/robots/heartbeat",data=data,method="POST",
        headers={"Authorization":"Bearer "+TOKEN,"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=20) as res:
        result=json.load(res)
        if not result.get("accepted"): raise RuntimeError("heartbeat rejected")
    print(json.dumps({"event":"heartbeat_accepted","robot_id":ROBOT}),flush=True)

def main():
    if not BASE.startswith("https://") or not TOKEN:
        raise SystemExit("WERO_BASE_URL must be HTTPS and WERO_ADMIN_TOKEN required")
    if not ROBOT or len(ROBOT)>80: raise SystemExit("Invalid robot ID")
    signal.signal(signal.SIGTERM,stop)
    signal.signal(signal.SIGINT,stop)
    print(json.dumps({"event":"worker_started","robot_id":ROBOT}),flush=True)
    while RUN:
        try: heartbeat()
        except (urllib.error.URLError,TimeoutError,ValueError,RuntimeError) as exc:
            print(json.dumps({"event":"heartbeat_failed","type":type(exc).__name__}),flush=True)
        for _ in range(INTERVAL):
            if not RUN: break
            time.sleep(1)
    print(json.dumps({"event":"worker_stopped","robot_id":ROBOT}),flush=True)

if __name__=="__main__":
    main()
