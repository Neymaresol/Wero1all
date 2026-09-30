import os, sqlite3, hmac, json, secrets
from datetime import datetime, timezone
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

VERSION="1.1.2"
DB=os.getenv("DB_PATH","/app/data/wero1.db")
HOTMART_HOTTOK=os.getenv("HOTMART_HOTTOK","")
ADMIN_TOKEN=os.getenv("WERO_ADMIN_TOKEN","")
app=FastAPI(title="Wero1 Operario",version=VERSION)

SALE_EVENTS={"PURCHASE_APPROVED","PURCHASE_COMPLETE"}
REVERSAL_EVENTS={"PURCHASE_REFUNDED","PURCHASE_CHARGEBACK","PURCHASE_CANCELED","PURCHASE_EXPIRED"}
FUNNEL_EVENTS={"PURCHASE_STARTED","PURCHASE_WAITING_PAYMENT","PURCHASE_DELAYED","PURCHASE_BILLET_PRINTED"}
TEST_EVENTS={"PURCHASE_PROTEST"}

def now(): return datetime.now(timezone.utc).isoformat()
def db():
    os.makedirs(os.path.dirname(DB),exist_ok=True)
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,provider TEXT,event_id TEXT UNIQUE,robot_id TEXT,kind TEXT,amount REAL DEFAULT 0,confirmed INTEGER DEFAULT 0,created_at TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS offers(id INTEGER PRIMARY KEY AUTOINCREMENT,provider TEXT DEFAULT 'hotmart',product_id TEXT,product_name TEXT,hotlink TEXT UNIQUE,niche TEXT,price REAL DEFAULT 0,commission REAL DEFAULT 0,currency TEXT DEFAULT 'BRL',active INTEGER DEFAULT 1,created_at TEXT,updated_at TEXT)""")
    # v1.1.2 canonical transaction ledger. Old test/event rows remain for audit but no longer drive financial status.
    c.execute("""CREATE TABLE IF NOT EXISTS transactions(transaction_id TEXT PRIMARY KEY,provider TEXT,robot_id TEXT,product_id TEXT,event_state TEXT,amount REAL DEFAULT 0,currency TEXT DEFAULT 'BRL',is_test INTEGER DEFAULT 0,confirmed INTEGER DEFAULT 0,reversed INTEGER DEFAULT 0,first_seen TEXT,last_seen TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS event_v112(event_id TEXT PRIMARY KEY,transaction_id TEXT,event_type TEXT,is_test INTEGER DEFAULT 0,received_at TEXT)""")
    c.commit(); return c

def admin(auth):
    if not ADMIN_TOKEN: raise HTTPException(503,"admin token not configured")
    token=(auth or "").removeprefix("Bearer ").strip()
    if not secrets.compare_digest(token,ADMIN_TOKEN): raise HTTPException(401,"invalid admin token")

def getv(d,*path,default=None):
    x=d
    for k in path:
        if not isinstance(x,dict): return default
        x=x.get(k)
    return default if x is None else x

def txid(p):
    candidates=[getv(p,"data","purchase","transaction"),getv(p,"data","purchase","order_id"),getv(p,"data","purchase","orderId"),getv(p,"data","purchase","id"),getv(p,"data","transaction"),p.get("transaction")]
    return next((str(x).strip() for x in candidates if x not in (None,"")),"")
def amount(p):
    try:return float(getv(p,"data","purchase","price","value",default=0) or 0)
    except (TypeError,ValueError):return 0.0
def currency(p): return str(getv(p,"data","purchase","price","currency_value",default="BRL") or "BRL")
def product_id(p): return str(getv(p,"data","product","id",default="") or "")
def is_test(p,event):
    return event in TEST_EVENTS or bool(p.get("test")) or str(p.get("environment","")).lower() in {"test","sandbox"}

@app.on_event("startup")
def startup(): db().close()

@app.get("/health")
def health():
    return {"status":"ok","service":"wero1-operario","version":VERSION,"hotmart_hottok_configured":bool(HOTMART_HOTTOK),"admin_token_configured":bool(ADMIN_TOKEN),"time":now()}

@app.get("/api/status")
def status():
    c=db()
    rows=c.execute("""SELECT robot_id,COUNT(*) sales,COALESCE(SUM(amount),0) gross,MAX(last_seen) last_event FROM transactions WHERE confirmed=1 AND reversed=0 AND is_test=0 GROUP BY robot_id""").fetchall()
    offers=c.execute("SELECT COUNT(*) total,COALESCE(SUM(CASE WHEN active=1 THEN 1 ELSE 0 END),0) active FROM offers").fetchone()
    c.close(); robots=[]
    for r in rows: robots.append({"robot_id":r["robot_id"],"sales":r["sales"],"gross":r["gross"],"commission":0,"balance":0,"transferred":0,"last_event":r["last_event"]})
    return {"mode":os.getenv("WERO_MODE","production"),"version":VERSION,"robots":robots,"offers":{"total":offers["total"] or 0,"active":offers["active"] or 0},"totals":{"robots":len(robots),"sales":sum(r["sales"] for r in robots),"gross":sum(r["gross"] for r in robots),"commission":0,"balance":0,"transferred":0}}

@app.get("/api/funnel")
def funnel():
    c=db(); rows=c.execute("SELECT event_type kind,COUNT(*) qty FROM event_v112 GROUP BY event_type ORDER BY qty DESC").fetchall(); c.close()
    return {"events":[dict(r) for r in rows]}

@app.get("/api/offers")
def offers():
    c=db(); rows=c.execute("SELECT id,provider,product_id,product_name,hotlink,niche,price,commission,currency,active,updated_at FROM offers ORDER BY active DESC,id DESC").fetchall(); c.close(); return {"offers":[dict(r) for r in rows]}

@app.post("/api/offers")
async def add_offer(request:Request,authorization:str|None=Header(default=None)):
    admin(authorization); p=await request.json(); hotlink=str(p.get("hotlink","")).strip(); name=str(p.get("product_name","")).strip()
    if not hotlink.startswith("http"): raise HTTPException(400,"valid hotlink required")
    if not name: raise HTTPException(400,"product_name required")
    t=now(); c=db()
    try:
        c.execute("INSERT INTO offers(provider,product_id,product_name,hotlink,niche,price,commission,currency,active,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)",("hotmart",str(p.get("product_id","")),name,hotlink,str(p.get("niche","")),float(p.get("price",0) or 0),float(p.get("commission",0) or 0),str(p.get("currency","BRL")),1,t,t)); c.commit()
    except sqlite3.IntegrityError: c.close(); raise HTTPException(409,"hotlink already registered")
    c.close(); return {"accepted":True,"product_name":name,"active":True}

@app.post("/webhooks/{provider}")
async def webhook(provider:str,request:Request):
    body=await request.body()
    try:p=json.loads(body or b"{}")
    except json.JSONDecodeError: raise HTTPException(400,"invalid json")
    provider=provider.lower(); robot_id=str(p.get("robot_id","WERO1-PAI"))
    if provider!="hotmart": raise HTTPException(400,"provider not supported in v1.1.2")
    if not HOTMART_HOTTOK: raise HTTPException(503,"hotmart hottok not configured")
    if not hmac.compare_digest(request.headers.get("x-hotmart-hottok",""),HOTMART_HOTTOK): raise HTTPException(401,"invalid hotmart hottok")
    event_id=str(p.get("id") or p.get("event_id") or "").strip(); event=str(p.get("event") or "").upper().strip()
    if not event_id or not event: raise HTTPException(400,"id and event required")
    transaction=txid(p); test=is_test(p,event); a=amount(p); cur=currency(p); pid=product_id(p); t=now()
    c=db()
    try:
        c.execute("INSERT INTO event_v112(event_id,transaction_id,event_type,is_test,received_at) VALUES(?,?,?,?,?)",(event_id,transaction,event,1 if test else 0,t))
    except sqlite3.IntegrityError:
        c.close(); return {"accepted":True,"duplicate":True,"event_id":event_id,"transaction_id":transaction,"event":event}
    # Keep audit copy compatible with previous funnel/history.
    kind=("sale" if event in SALE_EVENTS else "reversal_"+event.lower() if event in REVERSAL_EVENTS else "funnel_"+event.lower() if event in FUNNEL_EVENTS else "hotmart_"+event.lower())
    try:c.execute("INSERT OR IGNORE INTO events(provider,event_id,robot_id,kind,amount,confirmed,created_at) VALUES(?,?,?,?,?,?,?)",(provider,event_id,robot_id,kind,a,0,t))
    except Exception:pass
    # Financial events require a real Hotmart transaction identifier. Test events never affect ledger.
    if not test and event in (SALE_EVENTS|REVERSAL_EVENTS):
        if not transaction:
            c.commit(); c.close(); raise HTTPException(422,"transaction id required for financial event")
        old=c.execute("SELECT * FROM transactions WHERE transaction_id=?",(transaction,)).fetchone()
        first=old["first_seen"] if old else t
        confirmed=1 if event in SALE_EVENTS else (old["confirmed"] if old else 0)
        reversed_=1 if event in REVERSAL_EVENTS else (old["reversed"] if old else 0)
        # A later valid sale event can restore only if no reversal has been recorded.
        if event in SALE_EVENTS and not old: reversed_=0
        c.execute("""INSERT INTO transactions(transaction_id,provider,robot_id,product_id,event_state,amount,currency,is_test,confirmed,reversed,first_seen,last_seen) VALUES(?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(transaction_id) DO UPDATE SET robot_id=excluded.robot_id,product_id=CASE WHEN excluded.product_id<>'' THEN excluded.product_id ELSE transactions.product_id END,event_state=excluded.event_state,amount=CASE WHEN excluded.amount>0 THEN excluded.amount ELSE transactions.amount END,currency=excluded.currency,confirmed=MAX(transactions.confirmed,excluded.confirmed),reversed=MAX(transactions.reversed,excluded.reversed),last_seen=excluded.last_seen""",(transaction,provider,robot_id,pid,event,a,cur,0,confirmed,reversed_,first,t))
    c.commit(); c.close()
    return {"accepted":True,"duplicate":False,"event_id":event_id,"transaction_id":transaction or None,"event":event,"test":test,"financial_counted":bool(transaction and not test and event in SALE_EVENTS)}

app.mount("/static",StaticFiles(directory="/app/static"),name="static")
@app.get("/")
def dashboard():return FileResponse("/app/static/index.html")
