import os, sqlite3, hmac, json, secrets, urllib.request, urllib.error, time
from datetime import datetime, timezone
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

VERSION="1.9.0"
DB=os.getenv("DB_PATH","/app/data/wero1.db")
HOTMART_HOTTOK=os.getenv("HOTMART_HOTTOK","")
ADMIN_TOKEN=os.getenv("WERO_ADMIN_TOKEN","")
HOTMART_ACCESS_TOKEN=os.getenv("HOTMART_ACCESS_TOKEN","")
AMAZON_PARTNER_TAG=os.getenv("AMAZON_PARTNER_TAG","wero1mercados-20")
AMAZON_CREATOR_CREDENTIAL_ID=os.getenv("AMAZON_CREATOR_CREDENTIAL_ID","")
AMAZON_CREATOR_CREDENTIAL_SECRET=os.getenv("AMAZON_CREATOR_CREDENTIAL_SECRET","")
AMAZON_MARKETPLACE="www.amazon.com.br"
AMAZON_BOOTSTRAP_LINK="https://amzn.to/4rQF28a"
app=FastAPI(title="Wero1 Operario",version=VERSION)
BOOT_MONO=time.monotonic()
PERF_MODE=os.getenv("WERO_PERFORMANCE_MODE","game").lower()
PERF={"requests":0,"errors":0,"latency_ms_ema":0.0}

@app.middleware("http")
async def performance_telemetry(request:Request,call_next):
    start=time.perf_counter(); PERF["requests"]+=1
    try:
        response=await call_next(request); return response
    except Exception:
        PERF["errors"]+=1; raise
    finally:
        ms=(time.perf_counter()-start)*1000
        PERF["latency_ms_ema"]=round(ms if PERF["latency_ms_ema"]==0 else PERF["latency_ms_ema"]*.85+ms*.15,2)

@app.get("/api/performance")
def performance():
    uptime=max(time.monotonic()-BOOT_MONO,0.001)
    return {"service":"wero1-operario","version":VERSION,"mode":PERF_MODE,
      "requests":PERF["requests"],"errors":PERF["errors"],
      "latency_ms_ema":PERF["latency_ms_ema"],"requests_per_second":round(PERF["requests"]/uptime,3),
      "uptime_seconds":round(uptime,1),
      "note":"Telemetria medida no processo atual; performance nao representa vendas."}

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
    c.execute("""CREATE TABLE IF NOT EXISTS catalog_products(product_id TEXT PRIMARY KEY,ucode TEXT,name TEXT,status TEXT,format TEXT,source TEXT,eligible INTEGER DEFAULT 0,last_scan TEXT)""")
    # v1.3.1 commercial funnel: tracks authorized campaign traffic without changing the financial ledger.
    c.execute("""CREATE TABLE IF NOT EXISTS campaign_clicks(click_id TEXT PRIMARY KEY,offer_id INTEGER,channel TEXT,campaign TEXT,robot_id TEXT,creative TEXT DEFAULT '',created_at TEXT)""")
    try:c.execute("ALTER TABLE campaign_clicks ADD COLUMN creative TEXT DEFAULT ''")
    except sqlite3.OperationalError:pass
    c.execute("""CREATE TABLE IF NOT EXISTS robot_heartbeats(
        robot_id TEXT PRIMARY KEY,parent_robot_id TEXT,last_seen TEXT NOT NULL,
        operational_status TEXT NOT NULL DEFAULT 'UNVERIFIED')""")
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

AUTHORIZED_BOOTSTRAP_OFFERS = [
    {"product_id":"42903","product_name":"LeadLovers","hotlink":"https://go.hotmart.com/O107910953Y","niche":"marketing automation","currency":"BRL"},
    {"product_id":"42903","product_name":"LeadLovers","hotlink":"https://go.hotmart.com/O107910953Y?dp=1","niche":"marketing automation","currency":"BRL"},
    {"product_id":"42903","product_name":"LeadLovers","hotlink":"https://go.hotmart.com/O107910953Y?ap=f792","niche":"marketing automation","currency":"BRL"},
    {"provider":"amazon","product_id":"","product_name":"Amazon BR - oferta inicial autorizada","hotlink":AMAZON_BOOTSTRAP_LINK,"niche":"marketplace","currency":"BRL"},
]

def bootstrap_authorized_offers(c):
    """Register only user-confirmed public affiliate HotLinks; safe to run on every startup."""
    t=now()
    for p in AUTHORIZED_BOOTSTRAP_OFFERS:
        hotlink=p["hotlink"]
        row=c.execute("SELECT id FROM offers WHERE hotlink=?",(hotlink,)).fetchone()
        if row:
            # Preserve manual deactivation; startup must not reactivate blocked offers.
            continue
        else:
            c.execute("""INSERT INTO offers(provider,product_id,product_name,hotlink,niche,price,commission,currency,active,created_at,updated_at)
                         VALUES(?,?,?,?,?,0,0,?,1,?,?)""",
                      (p.get("provider","hotmart"),p["product_id"],p["product_name"],hotlink,p["niche"],p["currency"],t,t))
    c.commit()

@app.on_event("startup")
def startup():
    c=db()
    try: bootstrap_authorized_offers(c)
    finally: c.close()

@app.get("/health")
def health():
    return {"status":"ok","service":"wero1-operario","version":VERSION,"hotmart_hottok_configured":bool(HOTMART_HOTTOK),"admin_token_configured":bool(ADMIN_TOKEN),"hotmart_api_configured":bool(HOTMART_ACCESS_TOKEN),"amazon_partner_tag_configured":bool(AMAZON_PARTNER_TAG),"amazon_creators_api_configured":bool(AMAZON_CREATOR_CREDENTIAL_ID and AMAZON_CREATOR_CREDENTIAL_SECRET),"amazon_catalog_mode":"CREATORS_API" if (AMAZON_CREATOR_CREDENTIAL_ID and AMAZON_CREATOR_CREDENTIAL_SECRET) else "WAITING_API","time":now()}

@app.get("/api/status")
def status():
    c=db()
    rows=c.execute("""SELECT robot_id,COUNT(*) sales,COALESCE(SUM(amount),0) gross,MAX(last_seen) last_event FROM transactions WHERE confirmed=1 AND reversed=0 AND is_test=0 GROUP BY robot_id""").fetchall()
    offers=c.execute("SELECT COUNT(*) total,COALESCE(SUM(CASE WHEN active=1 THEN 1 ELSE 0 END),0) active FROM offers").fetchone()
    clicks=c.execute("""SELECT robot_id,COUNT(*) clicks,MAX(created_at) last_click FROM campaign_clicks WHERE robot_id IS NOT NULL AND TRIM(robot_id) != '' GROUP BY robot_id""").fetchall()
    c.close(); robots=[]
    by_id={}
    for r in rows:
        by_id[r["robot_id"]]={"robot_id":r["robot_id"],"sales":r["sales"],"gross":r["gross"],"commission":0,"balance":0,"transferred":0,"last_event":r["last_event"],"tracked_clicks":0,"last_click":None,"operational_status":"UNVERIFIED"}
    for r in clicks:
        robot=by_id.setdefault(r["robot_id"],{"robot_id":r["robot_id"],"sales":0,"gross":0,"commission":0,"balance":0,"transferred":0,"last_event":None,"tracked_clicks":0,"last_click":None,"operational_status":"UNVERIFIED"})
        robot["tracked_clicks"]=r["clicks"]
        robot["last_click"]=r["last_click"]
    robots=list(by_id.values())
    return {"mode":os.getenv("WERO_MODE","production"),"version":VERSION,"robots":robots,"offers":{"total":offers["total"] or 0,"active":offers["active"] or 0},"totals":{"robots":len(robots),"sales":sum(r["sales"] for r in robots),"gross":sum(r["gross"] for r in robots),"commission":0,"balance":0,"transferred":0}}

@app.post("/api/robots/heartbeat")
async def robot_heartbeat(request:Request,authorization:str|None=Header(default=None)):
    """Authenticated worker check-in. A check-in is not evidence of sales."""
    admin(authorization)
    payload=await request.json()
    if not isinstance(payload,dict): raise HTTPException(400,"JSON object required")
    robot_id=str(payload.get("robot_id") or "").strip()
    parent_id=str(payload.get("parent_robot_id") or "").strip() or None
    if not robot_id or len(robot_id)>80 or (parent_id and len(parent_id)>80):
        raise HTTPException(400,"invalid robot identifier")
    if parent_id==robot_id: raise HTTPException(400,"robot cannot be its own parent")
    t=now(); c=db()
    try:
        c.execute("""INSERT INTO robot_heartbeats(robot_id,parent_robot_id,last_seen,operational_status)
            VALUES(?,?,?,'HEARTBEAT_RECEIVED') ON CONFLICT(robot_id)
            DO UPDATE SET parent_robot_id=excluded.parent_robot_id,last_seen=excluded.last_seen,
            operational_status='HEARTBEAT_RECEIVED'""",(robot_id,parent_id,t))
        c.commit()
        return {"accepted":True,"robot_id":robot_id,"last_seen":t,
            "note":"Authenticated heartbeat received; worker tasks and sales not independently verified."}
    finally:
        c.close()

@app.get("/api/robots/heartbeats")
def robot_heartbeats():
    """Read-only freshness: online means recent authenticated check-in only."""
    from datetime import timedelta
    cutoff=(datetime.now(timezone.utc)-timedelta(seconds=180)).isoformat()
    c=db()
    try:
        rows=c.execute("SELECT robot_id,parent_robot_id,last_seen FROM robot_heartbeats ORDER BY robot_id").fetchall()
        robots=[{"robot_id":r["robot_id"],"parent_robot_id":r["parent_robot_id"],
            "last_seen":r["last_seen"],"heartbeat_fresh":r["last_seen"]>=cutoff,
            "task_execution_verified":False} for r in rows]
        return {"version":VERSION,"heartbeat_fresh_count":sum(r["heartbeat_fresh"] for r in robots),
            "robots":robots,"freshness_seconds":180,
            "note":"Heartbeat confirms only a recent authenticated request, not active campaigns or sales."}
    finally:
        c.close()

@app.get("/api/robots/diagnostics")
def robots_diagnostics():
    """Read-only evidence of robot identifiers, not a claim of running workers."""
    c=db()
    try:
        clicks=c.execute("""SELECT robot_id,COUNT(*) AS tracked_clicks,MAX(created_at) AS last_click
            FROM campaign_clicks WHERE robot_id IS NOT NULL AND TRIM(robot_id)!=''
            GROUP BY robot_id ORDER BY tracked_clicks DESC""").fetchall()
        transactions=c.execute("""SELECT robot_id,COUNT(*) AS confirmed_sales,MAX(last_seen) AS last_event
            FROM transactions WHERE confirmed=1 AND reversed=0 AND is_test=0
            AND robot_id IS NOT NULL AND TRIM(robot_id)!=''
            GROUP BY robot_id""").fetchall()
        by_id={}
        for r in clicks:
            by_id[r["robot_id"]]={"robot_id":r["robot_id"],"tracked_clicks":r["tracked_clicks"],
                "last_click":r["last_click"],"confirmed_sales":0,"last_event":None,
                "operational_status":"UNVERIFIED"}
        for r in transactions:
            item=by_id.setdefault(r["robot_id"],{"robot_id":r["robot_id"],
                "tracked_clicks":0,"last_click":None,"confirmed_sales":0,"last_event":None,
                "operational_status":"UNVERIFIED"})
            item["confirmed_sales"]=r["confirmed_sales"]
            item["last_event"]=r["last_event"]
        return {"version":VERSION,"identified_robots":len(by_id),"robots":list(by_id.values()),
            "worker_execution_verified":False,
            "note":"Identificadores provêm apenas de cliques ou vendas reais. Sem heartbeat, não há confirmação de worker ativo."}
    finally:
        c.close()

@app.get("/api/funnel")
def funnel():
    c=db(); rows=c.execute("SELECT event_type kind,COUNT(*) qty FROM event_v112 GROUP BY event_type ORDER BY qty DESC").fetchall(); c.close()
    return {"events":[dict(r) for r in rows]}

@app.get("/api/commercial")
def commercial():
    c=db()
    clicks=c.execute("SELECT COUNT(*) n FROM campaign_clicks").fetchone()["n"]
    active=c.execute("SELECT COUNT(*) n FROM offers WHERE active=1").fetchone()["n"]
    sales=c.execute("SELECT COUNT(*) n FROM transactions WHERE confirmed=1 AND reversed=0 AND is_test=0").fetchone()["n"]
    rows=c.execute("""SELECT o.id,o.product_name,o.product_id,o.hotlink,o.niche,o.price,o.commission,
        COUNT(cc.click_id) clicks
        FROM offers o LEFT JOIN campaign_clicks cc ON cc.offer_id=o.id
        WHERE o.active=1 GROUP BY o.id ORDER BY clicks DESC,o.commission DESC,o.id DESC""").fetchall()
    c.close()
    conversion=(sales/clicks*100) if clicks else 0
    return {"engine":"wero1-commercial","version":VERSION,"active_offers":active,"clicks":clicks,
            "confirmed_sales":sales,"conversion_pct":round(conversion,2),
            "ranking":[dict(x) for x in rows]}

@app.get("/go/{offer_id}")
def go_offer(offer_id:int,channel:str="direct",campaign:str="organic",robot_id:str="wero1-operario",creative:str="default"):
    # Redirect only to an already registered/authorized HotLink; no links are fabricated.
    from fastapi.responses import RedirectResponse
    c=db(); o=c.execute("SELECT id,hotlink,active FROM offers WHERE id=?",(offer_id,)).fetchone()
    if not o or not o["active"]: c.close(); raise HTTPException(404,"active offer not found")
    click_id=secrets.token_urlsafe(16); c.execute("INSERT INTO campaign_clicks(click_id,offer_id,channel,campaign,robot_id,creative,created_at) VALUES(?,?,?,?,?,?,?)",
        (click_id,offer_id,(channel or "direct")[:80],(campaign or "organic")[:120],(robot_id or "wero1-operario")[:80],(creative or "default")[:120],now()))
    c.commit(); url=o["hotlink"]; c.close()
    return RedirectResponse(url=url,status_code=302)

@app.get("/api/ai-sales")
def ai_sales():
    """Evidence-based commercial decision layer. It never fabricates traffic, buyers or sales."""
    c=db()
    rows=c.execute("""SELECT o.id,o.product_name,o.niche,o.price,o.commission,o.currency,
        COUNT(cc.click_id) clicks
        FROM offers o LEFT JOIN campaign_clicks cc ON cc.offer_id=o.id
        WHERE o.active=1 GROUP BY o.id ORDER BY o.id""").fetchall()
    sales=c.execute("SELECT COUNT(*) n FROM transactions WHERE confirmed=1 AND reversed=0 AND is_test=0").fetchone()["n"]
    total_clicks=c.execute("SELECT COUNT(*) n FROM campaign_clicks").fetchone()["n"]
    c.close()
    decisions=[]
    for r in rows:
        clicks=int(r["clicks"] or 0); commission=float(r["commission"] or 0)
        # Exploration protects new authorized offers from being permanently starved of traffic.
        evidence=min(clicks/25.0,1.0)
        commission_signal=min(max(commission,0)/500.0,1.0)
        score=round(35+(evidence*45)+(commission_signal*20),1)
        action="TESTAR DISTRIBUICAO" if clicks<25 else "PRIORIZAR" if score>=70 else "OTIMIZAR CRIATIVO"
        decisions.append({"offer_id":r["id"],"product_name":r["product_name"],"niche":r["niche"],
          "clicks":clicks,"price":r["price"],"commission":commission,"score":score,"action":action,
          "tracked_url":f"/go/{r['id']}?channel=ai&campaign=wero-ai-sales&robot_id=WERO1-PAI"})
    decisions.sort(key=lambda x:(x["score"],-x["offer_id"]),reverse=True)
    conversion=(sales/total_clicks*100) if total_clicks else 0
    return {"engine":"wero-ai-sales","version":VERSION,"mode":"decision-support",
      "active_offers":len(decisions),"tracked_clicks":total_clicks,"confirmed_sales":sales,
      "confirmed_conversion_pct":round(conversion,2),"recommendations":decisions,
      "guardrails":["Somente ofertas autorizadas","Venda somente por evento confirmado do provedor",
                    "Sem trafego, comprador ou receita simulados","Reavaliar ranking com novos dados reais"]}

@app.get("/api/acquisition")
def acquisition():
    """Commercial acquisition control plane: diagnoses the real bottleneck and produces an executable campaign queue."""
    c=db()
    offers=c.execute("""SELECT o.id,o.product_name,o.niche,o.price,o.commission,
        COUNT(cc.click_id) clicks
        FROM offers o LEFT JOIN campaign_clicks cc ON cc.offer_id=o.id
        WHERE o.active=1 GROUP BY o.id ORDER BY clicks DESC,o.commission DESC,o.id""").fetchall()
    clicks=c.execute("SELECT COUNT(*) n FROM campaign_clicks").fetchone()["n"]
    sales=c.execute("SELECT COUNT(*) n FROM transactions WHERE confirmed=1 AND reversed=0 AND is_test=0").fetchone()["n"]
    funnel=c.execute("SELECT event_type,COUNT(*) qty FROM event_v112 GROUP BY event_type").fetchall()
    c.close()
    funnel_map={r["event_type"]:r["qty"] for r in funnel}
    checkout=sum(v for k,v in funnel_map.items() if k in FUNNEL_EVENTS)
    if not offers:
        bottleneck="NO_ACTIVE_OFFERS"; next_action="IMPORT_AUTHORIZED_OFFERS"
    elif clicks==0:
        bottleneck="NO_TRACKED_TRAFFIC"; next_action="DISTRIBUTE_TRACKED_CAMPAIGNS"
    elif checkout==0:
        bottleneck="NO_CHECKOUT_SIGNAL"; next_action="OPTIMIZE_OFFER_AND_LANDING"
    elif sales==0:
        bottleneck="CHECKOUT_WITHOUT_CONFIRMED_SALE"; next_action="OPTIMIZE_CONVERSION_AND_VERIFY_PROVIDER"
    else:
        bottleneck="FUNNEL_CONVERTING"; next_action="SCALE_WINNERS"
    queue=[]
    for i,r in enumerate(offers):
        queue.append({"priority":i+1,"offer_id":r["id"],"product_name":r["product_name"],
          "niche":r["niche"],"tracked_clicks":r["clicks"],
          "tracked_url":f"/go/{r['id']}?channel=campaign&campaign=wero-acquisition&robot_id=WERO1-PAI",
          "objective":"FIRST_CONFIRMED_SALE" if sales==0 else "SCALE_CONFIRMED_SALES"})
    return {"engine":"wero-acquisition","version":VERSION,"bottleneck":bottleneck,
      "next_action":next_action,"active_offers":len(offers),"tracked_clicks":clicks,
      "checkout_signals":checkout,"confirmed_sales":sales,"campaign_queue":queue,
      "rule":"Only real provider-confirmed purchases are counted as sales."}


@app.get("/api/attribution")
def attribution():
    c=db()
    rows=c.execute("""SELECT robot_id,channel,campaign,COALESCE(creative,'') creative,COUNT(*) clicks,MAX(created_at) last_click FROM campaign_clicks GROUP BY robot_id,channel,campaign,COALESCE(creative,'') ORDER BY clicks DESC,last_click DESC""").fetchall()
    sales=c.execute("SELECT COUNT(*) n FROM transactions WHERE confirmed=1 AND reversed=0 AND is_test=0").fetchone()["n"]
    c.close()
    return {"engine":"wero-attribution","version":VERSION,"confirmed_sales":sales,"campaigns":[dict(r) for r in rows],"note":"Clicks attributed by tracked URL; sales remain provider-confirmed."}

@app.get("/api/growth")
def growth():
    c=db()
    clicks=c.execute("SELECT COUNT(*) n FROM campaign_clicks").fetchone()["n"]
    channels=c.execute("SELECT COUNT(DISTINCT channel) n FROM campaign_clicks").fetchone()["n"]
    campaigns=c.execute("SELECT COUNT(DISTINCT campaign) n FROM campaign_clicks").fetchone()["n"]
    checkout=sum(r["qty"] for r in c.execute("SELECT event_type,COUNT(*) qty FROM event_v112 GROUP BY event_type").fetchall() if r["event_type"] in FUNNEL_EVENTS)
    sales=c.execute("SELECT COUNT(*) n FROM transactions WHERE confirmed=1 AND reversed=0 AND is_test=0").fetchone()["n"]
    c.close()
    if clicks==0: stage="TRAFFIC"; action="DISTRIBUTE_TRACKED_LINKS"; reason="Nenhum clique rastreado."
    elif checkout==0: stage="CLICK_TO_CHECKOUT"; action="TEST_CREATIVE_OFFER_LANDING"; reason="Ha cliques, mas nenhum sinal de checkout."
    elif sales==0: stage="CHECKOUT_TO_SALE"; action="VERIFY_CHECKOUT_AND_PROVIDER_EVENTS"; reason="Ha checkout, mas nenhuma venda confirmada."
    else: stage="SCALE"; action="SCALE_CONFIRMED_WINNERS"; reason="O funil possui venda confirmada."
    return {"engine":"wero-growth","version":VERSION,"stage":stage,"next_action":action,"reason":reason,"tracked_clicks":clicks,"checkout_signals":checkout,"confirmed_sales":sales,"channels":channels,"campaigns":campaigns,"rule":"No simulated buyers, clicks, conversions, sales or commissions."}

@app.get("/api/offers")
def offers():
    c=db(); rows=c.execute("SELECT id,provider,product_id,product_name,hotlink,niche,price,commission,currency,active,updated_at FROM offers ORDER BY active DESC,id DESC").fetchall(); c.close(); return {"offers":[dict(r) for r in rows]}

def hotmart_get(url):
    if not HOTMART_ACCESS_TOKEN: raise HTTPException(503,"HOTMART_ACCESS_TOKEN not configured")
    req=urllib.request.Request(url,headers={"Authorization":"Bearer "+HOTMART_ACCESS_TOKEN,"Content-Type":"application/json","User-Agent":"Wero1/1.3.0"})
    try:
        with urllib.request.urlopen(req,timeout=20) as r: return json.loads(r.read().decode())
    except urllib.error.HTTPError as e: raise HTTPException(502,f"Hotmart API HTTP {e.code}")
    except Exception as e: raise HTTPException(502,f"Hotmart API error: {type(e).__name__}")


def amazon_access_token():
    if not (AMAZON_CREATOR_CREDENTIAL_ID and AMAZON_CREATOR_CREDENTIAL_SECRET):
        raise HTTPException(503,"Amazon Creators API credentials not configured; catalog remains WAITING_API")
    body=json.dumps({"grant_type":"client_credentials","client_id":AMAZON_CREATOR_CREDENTIAL_ID,"client_secret":AMAZON_CREATOR_CREDENTIAL_SECRET,"scope":"creatorsapi::default"}).encode()
    req=urllib.request.Request("https://api.amazon.com/auth/o2/token",data=body,headers={"Content-Type":"application/json"},method="POST")
    try:
        with urllib.request.urlopen(req,timeout=20) as r:return json.loads(r.read().decode()).get("access_token","")
    except urllib.error.HTTPError as e: raise HTTPException(502,f"Amazon token HTTP {e.code}")
    except Exception as e: raise HTTPException(502,f"Amazon token error: {type(e).__name__}")

def amazon_search(keywords,item_count=10,search_index="All"):
    token=amazon_access_token()
    payload={"partnerTag":AMAZON_PARTNER_TAG,"keywords":keywords,"itemCount":max(1,min(int(item_count),10)),"searchIndex":search_index,"marketplace":AMAZON_MARKETPLACE,"languagesOfPreference":["pt_BR"],"currencyOfPreference":"BRL","resources":["images.primary.medium","itemInfo.title","offersV2.listings.price"]}
    req=urllib.request.Request("https://creatorsapi.amazon/catalog/v1/searchItems",data=json.dumps(payload).encode(),headers={"Authorization":"Bearer "+token,"Content-Type":"application/json","x-marketplace":AMAZON_MARKETPLACE,"User-Agent":"Wero1/1.9.0"},method="POST")
    try:
        with urllib.request.urlopen(req,timeout=20) as r:return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        detail=e.read().decode(errors="ignore")[:500]
        raise HTTPException(502,f"Amazon Creators API HTTP {e.code}: {detail}")
    except Exception as e: raise HTTPException(502,f"Amazon Creators API error: {type(e).__name__}")

@app.get("/api/amazon/status")
def amazon_status():
    configured=bool(AMAZON_CREATOR_CREDENTIAL_ID and AMAZON_CREATOR_CREDENTIAL_SECRET)
    return {"provider":"amazon","version":VERSION,"partner_tag":AMAZON_PARTNER_TAG,"marketplace":AMAZON_MARKETPLACE,"currency":"BRL","language":"pt_BR","creators_api_configured":configured,"catalog_mode":"CREATORS_API" if configured else "WAITING_API","bootstrap_offer_registered":True,"note":"WAITING_API never fabricates catalog data or confirmed sales."}

@app.get("/api/amazon/catalog/search")
def amazon_catalog_search(q:str,item_count:int=10,search_index:str="All",authorization:str|None=Header(default=None)):
    admin(authorization)
    q=q.strip()
    if not q: raise HTTPException(400,"q required")
    data=amazon_search(q,item_count,search_index)
    items=((data.get("searchResult") or {}).get("items") or [])
    return {"provider":"amazon","query":q,"count":len(items),"items":items}

@app.get("/api/catalog")
def catalog():
    c=db(); rows=c.execute("SELECT * FROM catalog_products ORDER BY name").fetchall(); c.close()
    return {"products":[dict(r) for r in rows]}

@app.post("/api/catalog/scan")
def scan_catalog(authorization:str|None=Header(default=None)):
    admin(authorization)
    data=hotmart_get("https://developers.hotmart.com/products/api/v1/products?max_results=50&status=ACTIVE")
    items=data.get("items") or []; c=db(); t=now(); seen=0
    for x in items:
        pid=str(x.get("id","")); name=str(x.get("name","")).strip()
        if not pid or not name: continue
        seen+=1
        c.execute("""INSERT INTO catalog_products(product_id,ucode,name,status,format,source,eligible,last_scan)
        VALUES(?,?,?,?,?,?,0,?) ON CONFLICT(product_id) DO UPDATE SET ucode=excluded.ucode,name=excluded.name,status=excluded.status,format=excluded.format,last_scan=excluded.last_scan""",
        (pid,str(x.get("ucode","")),name,str(x.get("status","")),str(x.get("format","")),"hotmart_creator_api",t))
    c.commit(); c.close()
    return {"accepted":True,"products_seen":seen,"offers_activated":0,
    "message":"Catalogo oficial consultado. Nenhum HotLink de afiliado foi inventado ou ativado; a API documentada lista produtos do creator."}

def normalize_offer(p):
    hotlink=str(p.get("hotlink","")).strip()
    name=str(p.get("product_name","")).strip()
    if not hotlink.startswith("https://go.hotmart.com/"):
        raise HTTPException(400,"authorized Hotmart hotlink required")
    if not name: raise HTTPException(400,"product_name required")
    try:
        price=float(p.get("price",0) or 0); commission=float(p.get("commission",0) or 0)
    except (TypeError,ValueError):
        raise HTTPException(400,"price and commission must be numeric")
    return {"provider":"hotmart","product_id":str(p.get("product_id","")).strip(),"product_name":name,
            "hotlink":hotlink,"niche":str(p.get("niche","")).strip(),"price":price,
            "commission":commission,"currency":str(p.get("currency","BRL") or "BRL")[:8]}

def upsert_offer(c,p,t):
    x=normalize_offer(p)
    row=c.execute("SELECT id FROM offers WHERE hotlink=?",(x["hotlink"],)).fetchone()
    if row:
        c.execute("""UPDATE offers SET provider=?,product_id=?,product_name=?,niche=?,price=?,commission=?,currency=?,active=1,updated_at=? WHERE id=?""",
                  (x["provider"],x["product_id"],x["product_name"],x["niche"],x["price"],x["commission"],x["currency"],t,row["id"]))
        return row["id"],False
    cur=c.execute("""INSERT INTO offers(provider,product_id,product_name,hotlink,niche,price,commission,currency,active,created_at,updated_at)
                     VALUES(?,?,?,?,?,?,?,?,1,?,?)""",
                  (x["provider"],x["product_id"],x["product_name"],x["hotlink"],x["niche"],x["price"],x["commission"],x["currency"],t,t))
    return cur.lastrowid,True

@app.post("/api/offers/import")
async def import_offers(request:Request,authorization:str|None=Header(default=None)):
    """Universal, authenticated and idempotent import for user-authorized Hotmart HotLinks."""
    admin(authorization)
    p=await request.json(); items=p.get("offers") if isinstance(p,dict) else None
    if not isinstance(items,list) or not items or len(items)>100:
        raise HTTPException(400,"offers must be a non-empty list with at most 100 items")
    c=db(); t=now(); created=0; updated=0; ids=[]
    try:
        for item in items:
            if not isinstance(item,dict): raise HTTPException(400,"each offer must be an object")
            oid,is_new=upsert_offer(c,item,t); ids.append(oid)
            created+=1 if is_new else 0; updated+=0 if is_new else 1
        c.commit()
    except Exception:
        c.rollback(); c.close(); raise
    rows=c.execute("SELECT id,provider,product_id,product_name,hotlink,niche,price,commission,currency,active,updated_at FROM offers WHERE id IN (%s) ORDER BY id" % ",".join("?"*len(ids)),ids).fetchall()
    c.close()
    return {"accepted":True,"created":created,"updated":updated,"offers":[dict(r) for r in rows]}

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
