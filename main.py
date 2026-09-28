import os,sqlite3,hmac,hashlib,json
from datetime import datetime,timezone
from fastapi import FastAPI,Request,HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
DB=os.getenv("DB_PATH","/app/data/wero1.db"); SECRET=os.getenv("WEBHOOK_SECRET","")
app=FastAPI(title="Wero1 Operario",version="1.0.1")
def db():
 os.makedirs(os.path.dirname(DB),exist_ok=True); c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
 c.execute("""CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,provider TEXT,event_id TEXT UNIQUE,robot_id TEXT,kind TEXT,amount REAL DEFAULT 0,confirmed INTEGER DEFAULT 0,created_at TEXT)"""); c.commit(); return c
@app.on_event("startup")
def startup(): db().close()
@app.get("/health")
def health(): return {"status":"ok","service":"wero1-operario","time":datetime.now(timezone.utc).isoformat()}
@app.get("/api/status")
def status():
 c=db(); rows=c.execute("""SELECT robot_id,SUM(CASE WHEN kind='sale' AND confirmed=1 THEN 1 ELSE 0 END) sales,SUM(CASE WHEN kind='sale' AND confirmed=1 THEN amount ELSE 0 END) gross,SUM(CASE WHEN kind='commission' AND confirmed=1 THEN amount ELSE 0 END) commission,SUM(CASE WHEN kind='balance' AND confirmed=1 THEN amount ELSE 0 END) balance,SUM(CASE WHEN kind='transfer' AND confirmed=1 THEN amount ELSE 0 END) transferred,MAX(created_at) last_event FROM events GROUP BY robot_id""").fetchall(); c.close()
 robots=[dict(r) for r in rows]
 return {"mode":os.getenv("WERO_MODE","production"),"robots":robots,"totals":{"robots":len(robots),"sales":sum(r["sales"] or 0 for r in robots),"gross":sum(r["gross"] or 0 for r in robots),"commission":sum(r["commission"] or 0 for r in robots),"balance":sum(r["balance"] or 0 for r in robots),"transferred":sum(r["transferred"] or 0 for r in robots)}}
@app.post("/webhooks/{provider}")
async def webhook(provider:str,request:Request):
 body=await request.body()
 if SECRET:
  sig=request.headers.get("x-wero-signature",""); expected=hmac.new(SECRET.encode(),body,hashlib.sha256).hexdigest()
  if not hmac.compare_digest(sig,expected): raise HTTPException(401,"invalid signature")
 try: p=json.loads(body or b"{}")
 except json.JSONDecodeError: raise HTTPException(400,"invalid json")
 event_id=str(p.get("event_id","")); robot_id=str(p.get("robot_id","WERO1-PAI")); kind=str(p.get("kind","unknown"))
 if not event_id: raise HTTPException(400,"event_id required")
 try: amount=float(p.get("amount",0) or 0)
 except (TypeError,ValueError): raise HTTPException(400,"invalid amount")
 confirmed=bool(p.get("confirmed",False)); c=db()
 try: c.execute("INSERT INTO events(provider,event_id,robot_id,kind,amount,confirmed,created_at) VALUES(?,?,?,?,?,?,?)",(provider,event_id,robot_id,kind,amount,1 if confirmed else 0,datetime.now(timezone.utc).isoformat())); c.commit()
 except sqlite3.IntegrityError: pass
 finally: c.close()
 return {"accepted":True,"confirmed":confirmed}
app.mount("/static",StaticFiles(directory="/app/static"),name="static")
@app.get("/")
def dashboard(): return FileResponse("/app/static/index.html")
