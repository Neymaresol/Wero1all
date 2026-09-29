import os,sqlite3,hmac,json
from datetime import datetime,timezone
from fastapi import FastAPI,Request,HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

DB=os.getenv("DB_PATH","/app/data/wero1.db")
SECRET=os.getenv("WEBHOOK_SECRET","")
HOTMART_HOTTOK=os.getenv("HOTMART_HOTTOK","")
app=FastAPI(title="Wero1 Operario",version="1.0.2")

def db():
 os.makedirs(os.path.dirname(DB),exist_ok=True); c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
 c.execute("""CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,provider TEXT,event_id TEXT UNIQUE,robot_id TEXT,kind TEXT,amount REAL DEFAULT 0,confirmed INTEGER DEFAULT 0,created_at TEXT)"""); c.commit(); return c

@app.on_event("startup")
def startup(): db().close()

@app.get("/health")
def health(): return {"status":"ok","service":"wero1-operario","version":"1.0.2","time":datetime.now(timezone.utc).isoformat()}

@app.get("/api/status")
def status():
 c=db(); rows=c.execute("""SELECT robot_id,SUM(CASE WHEN kind='sale' AND confirmed=1 THEN 1 ELSE 0 END) sales,SUM(CASE WHEN kind='sale' AND confirmed=1 THEN amount ELSE 0 END) gross,SUM(CASE WHEN kind='commission' AND confirmed=1 THEN amount ELSE 0 END) commission,SUM(CASE WHEN kind='balance' AND confirmed=1 THEN amount ELSE 0 END) balance,SUM(CASE WHEN kind='transfer' AND confirmed=1 THEN amount ELSE 0 END) transferred,MAX(created_at) last_event FROM events GROUP BY robot_id""").fetchall(); c.close()
 robots=[dict(r) for r in rows]
 return {"mode":os.getenv("WERO_MODE","production"),"robots":robots,"totals":{"robots":len(robots),"sales":sum(r["sales"] or 0 for r in robots),"gross":sum(r["gross"] or 0 for r in robots),"commission":sum(r["commission"] or 0 for r in robots),"balance":sum(r["balance"] or 0 for r in robots),"transferred":sum(r["transferred"] or 0 for r in robots)}}

def hotmart_amount(p):
 try: return float((((p.get("data") or {}).get("purchase") or {}).get("price") or {}).get("value",0) or 0)
 except (TypeError,ValueError): return 0.0

@app.post("/webhooks/{provider}")
async def webhook(provider:str,request:Request):
 body=await request.body()
 try: p=json.loads(body or b"{}")
 except json.JSONDecodeError: raise HTTPException(400,"invalid json")
 provider=provider.lower(); robot_id=str(p.get("robot_id","WERO1-PAI"))
 if provider=="hotmart":
  if HOTMART_HOTTOK:
   received=request.headers.get("x-hotmart-hottok","")
   if not hmac.compare_digest(received,HOTMART_HOTTOK): raise HTTPException(401,"invalid hotmart hottok")
  event_id=str(p.get("id") or p.get("event_id") or ""); event=str(p.get("event") or "").upper()
  if not event_id: raise HTTPException(400,"id required")
  if not event: raise HTTPException(400,"event required")
  amount=hotmart_amount(p)
  if event=="PURCHASE_APPROVED": kind="sale"; confirmed=True
  else: kind="hotmart_"+event.lower(); confirmed=False
 else:
  event_id=str(p.get("event_id","")); kind=str(p.get("kind","unknown"))
  if not event_id: raise HTTPException(400,"event_id required")
  try: amount=float(p.get("amount",0) or 0)
  except (TypeError,ValueError): raise HTTPException(400,"invalid amount")
  confirmed=bool(p.get("confirmed",False))
 c=db(); inserted=True
 try:
  c.execute("INSERT INTO events(provider,event_id,robot_id,kind,amount,confirmed,created_at) VALUES(?,?,?,?,?,?,?)",(provider,event_id,robot_id,kind,amount,1 if confirmed else 0,datetime.now(timezone.utc).isoformat())); c.commit()
 except sqlite3.IntegrityError: inserted=False
 finally: c.close()
 return {"accepted":True,"duplicate":not inserted,"event_id":event_id,"confirmed":confirmed}

app.mount("/static",StaticFiles(directory="/app/static"),name="static")
@app.get("/")
def dashboard(): return FileResponse("/app/static/index.html")
