import os, sqlite3, hmac, json
from datetime import datetime, timezone
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

DB = os.getenv("DB_PATH", "/app/data/wero1.db")
HOTMART_HOTTOK = os.getenv("HOTMART_HOTTOK", "")
app = FastAPI(title="Wero1 Operario", version="1.1.0")

CONFIRMED_SALE_EVENTS = {"PURCHASE_APPROVED", "PURCHASE_COMPLETE"}
REVERSAL_EVENTS = {"PURCHASE_REFUNDED", "PURCHASE_CHARGEBACK", "PURCHASE_CANCELED", "PURCHASE_EXPIRED"}
FUNNEL_EVENTS = {"PURCHASE_STARTED", "PURCHASE_WAITING_PAYMENT", "PURCHASE_DELAYED", "PURCHASE_BILLET_PRINTED"}

def db():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT, provider TEXT, event_id TEXT UNIQUE,
        robot_id TEXT, kind TEXT, amount REAL DEFAULT 0, confirmed INTEGER DEFAULT 0,
        created_at TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS offers(
        id INTEGER PRIMARY KEY AUTOINCREMENT, provider TEXT DEFAULT 'hotmart',
        product_id TEXT, product_name TEXT, hotlink TEXT UNIQUE, niche TEXT,
        price REAL DEFAULT 0, commission REAL DEFAULT 0, currency TEXT DEFAULT 'BRL',
        active INTEGER DEFAULT 1, created_at TEXT, updated_at TEXT)""")
    c.commit()
    return c

@app.on_event("startup")
def startup():
    db().close()

@app.get("/health")
def health():
    return {"status":"ok", "service":"wero1-operario", "version":"1.1.0",
            "hotmart_hottok_configured": bool(HOTMART_HOTTOK),
            "time": datetime.now(timezone.utc).isoformat()}

@app.get("/api/status")
def status():
    c = db()
    rows = c.execute("""SELECT robot_id,
      SUM(CASE WHEN kind='sale' AND confirmed=1 THEN 1 ELSE 0 END) sales,
      SUM(CASE WHEN kind='sale' AND confirmed=1 THEN amount ELSE 0 END) gross,
      SUM(CASE WHEN kind='commission' AND confirmed=1 THEN amount ELSE 0 END) commission,
      SUM(CASE WHEN kind='balance' AND confirmed=1 THEN amount ELSE 0 END) balance,
      SUM(CASE WHEN kind='transfer' AND confirmed=1 THEN amount ELSE 0 END) transferred,
      MAX(created_at) last_event FROM events GROUP BY robot_id""").fetchall()
    offers = c.execute("SELECT COUNT(*) total, SUM(CASE WHEN active=1 THEN 1 ELSE 0 END) active FROM offers").fetchone()
    c.close()
    robots = [dict(r) for r in rows]
    return {"mode": os.getenv("WERO_MODE", "production"), "version":"1.1.0", "robots": robots,
            "offers":{"total": offers["total"] or 0, "active": offers["active"] or 0},
            "totals":{"robots":len(robots), "sales":sum(r["sales"] or 0 for r in robots),
            "gross":sum(r["gross"] or 0 for r in robots), "commission":sum(r["commission"] or 0 for r in robots),
            "balance":sum(r["balance"] or 0 for r in robots), "transferred":sum(r["transferred"] or 0 for r in robots)}}

@app.get("/api/funnel")
def funnel():
    c=db(); rows=c.execute("SELECT kind,COUNT(*) qty,SUM(amount) amount FROM events WHERE provider='hotmart' GROUP BY kind ORDER BY qty DESC").fetchall(); c.close()
    return {"events":[dict(r) for r in rows]}

@app.get("/api/offers")
def offers():
    c=db(); rows=c.execute("SELECT id,provider,product_id,product_name,hotlink,niche,price,commission,currency,active,updated_at FROM offers ORDER BY active DESC,id DESC").fetchall(); c.close()
    return {"offers":[dict(r) for r in rows]}

@app.post("/api/offers")
async def add_offer(request: Request):
    p=await request.json(); hotlink=str(p.get("hotlink","")).strip(); name=str(p.get("product_name","")).strip()
    if not hotlink.startswith("http"): raise HTTPException(400,"valid hotlink required")
    if not name: raise HTTPException(400,"product_name required")
    now=datetime.now(timezone.utc).isoformat(); c=db()
    try:
        c.execute("""INSERT INTO offers(provider,product_id,product_name,hotlink,niche,price,commission,currency,active,created_at,updated_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?)""", ("hotmart",str(p.get("product_id","")),name,hotlink,str(p.get("niche","")),float(p.get("price",0) or 0),float(p.get("commission",0) or 0),str(p.get("currency","BRL")),1,now,now)); c.commit()
    except sqlite3.IntegrityError:
        c.close(); raise HTTPException(409,"hotlink already registered")
    c.close(); return {"accepted":True,"product_name":name,"active":True}

def hotmart_amount(p):
    try: return float((((p.get("data") or {}).get("purchase") or {}).get("price") or {}).get("value",0) or 0)
    except (TypeError,ValueError): return 0.0

@app.post("/webhooks/{provider}")
async def webhook(provider: str, request: Request):
    body=await request.body()
    try: p=json.loads(body or b"{}")
    except json.JSONDecodeError: raise HTTPException(400,"invalid json")
    provider=provider.lower(); robot_id=str(p.get("robot_id","WERO1-PAI"))
    if provider=="hotmart":
        if not HOTMART_HOTTOK: raise HTTPException(503,"hotmart hottok not configured")
        received=request.headers.get("x-hotmart-hottok","")
        if not hmac.compare_digest(received,HOTMART_HOTTOK): raise HTTPException(401,"invalid hotmart hottok")
        event_id=str(p.get("id") or p.get("event_id") or ""); event=str(p.get("event") or "").upper()
        if not event_id: raise HTTPException(400,"id required")
        if not event: raise HTTPException(400,"event required")
        amount=hotmart_amount(p)
        if event in CONFIRMED_SALE_EVENTS: kind="sale"; confirmed=True
        elif event in REVERSAL_EVENTS: kind="reversal_"+event.lower(); confirmed=False
        elif event in FUNNEL_EVENTS: kind="funnel_"+event.lower(); confirmed=False
        else: kind="hotmart_"+event.lower(); confirmed=False
    else:
        event_id=str(p.get("event_id","")); kind=str(p.get("kind","unknown"))
        if not event_id: raise HTTPException(400,"event_id required")
        try: amount=float(p.get("amount",0) or 0)
        except (TypeError,ValueError): raise HTTPException(400,"invalid amount")
        confirmed=bool(p.get("confirmed",False)); event=None
    c=db(); inserted=True
    try:
        c.execute("INSERT INTO events(provider,event_id,robot_id,kind,amount,confirmed,created_at) VALUES(?,?,?,?,?,?,?)",(provider,event_id,robot_id,kind,amount,1 if confirmed else 0,datetime.now(timezone.utc).isoformat())); c.commit()
    except sqlite3.IntegrityError: inserted=False
    finally: c.close()
    return {"accepted":True,"duplicate":not inserted,"event_id":event_id,"event":event,"confirmed":confirmed}

app.mount("/static", StaticFiles(directory="/app/static"), name="static")
@app.get("/")
def dashboard(): return FileResponse("/app/static/index.html")
