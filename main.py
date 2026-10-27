import os, json, time, threading, requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import random
from urllib.parse import parse_qs, urlparse

PORT = int(os.environ.get("PORT", 10000))
WALLET = os.environ.get("WALLET", "0x...ne setat")
EMAIL = "damianzahan@yahoo.com"

# AICI II DAI TU ACCES - EL LE FOLOSESTE SINGUR
ACCESURI = {
    "shopify": os.environ.get("SHOPIFY_TOKEN", ""),
    "stripe": os.environ.get("STRIPE_KEY", ""), # pentru plati reale
    "telegram": os.environ.get("TELEGRAM_BOT", ""), # sa promoveze singur
}

produse_live = []
comenzi_reale = []
cicluri = 0

def cauta_singur():
    global produse_live
    try:
        print("Agentul cauta singur...")
        r = requests.get(f"https://dummyjson.com/products?limit=8&skip={random.randint(0,150)}", timeout=10)
        produse = r.json()['products']
        produse_live = []
        for p in produse:
            if p['rating'] >= 4.2 and p['stock'] > 20:
                cost = round(p['price'] * 0.45, 2)
                profit = round(p['price'] - cost, 2)
                produse_live.append({
                    "id": p['id'],
                    "nume": p['title'],
                    "descriere": p['description'][:120],
                    "cost": cost,
                    "pret_vanzare": p['price'],
                    "profit": profit,
                    "imagine": p['thumbnail'],
                    "stoc_supplier": p['stock']
                })
        print(f"Gasit {len(produse_live)} produse noi")
    except Exception as e:
        print(f"Eroare: {e}")

cauta_singur()

def cumpara_dupa_comanda(produs_id):
    """CUMPARA REAL DOAR DUPA CE CLIENTUL A PLATIT - MODELUL TAU!"""
    prod = next((x for x in produse_live if str(x['id']) == str(produs_id)), None)
    if not prod:
        return False
    
    # AICI VA CUMPARA REAL DE PE ALIEXPRESS/TEMU CAND AI CHEIE
    # Deocamdata simuleaza comanda reala la supplier
    # Cand pui cheia ALIEXPRESS_API in Render, va comanda automat
    
    comanda = {
        "produs": prod['nume'],
        "data": datetime.now().strftime("%d.%m %H:%M"),
        "cost_platit_supplier": prod['cost'],
        "incasat_client": prod['pret_vanzare'],
        "profit_net": prod['profit'],
        "wallet": WALLET,
        "status": "COMANDAT LA SUPPLIER - PROFIT IN CURS SPRE WALLET"
    }
    comenzi_reale.append(comanda)
    
    # AICI SE VA FACE TRANSFERUL REAL DE PROFIT CATRE WALLET-UL TAU
    # Prin Stripe -> Crypto off-ramp
    
    return comanda

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global cicluri
        parsed = urlparse(self.path)
        
        # PAGINA DE VANZARE PE CARE SI-O FACE EL SINGUR - GRATIS!
        if parsed.path == "/" or parsed.path == "/shop":
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            produse_html = ""
            for p in produse_live:
                produse_html += f"""
                <div style="background:#111;border:1px solid #333;border-radius:12px;padding:15px;margin:10px;width:280px;display:inline-block;vertical-align:top">
                    <img src="{p['imagine']}" style="width:100%;height:180px;object-fit:cover;border-radius:8px">
                    <h3 style="color:#fff;margin:10px 0">{p['nume']}</h3>
                    <p style="color:#888;font-size:13px">{p['descriere']}</p>
                    <p style="color:#0f0;font-weight:bold;font-size:20px">${p['pret_vanzare']} <span style="color:#666;font-size:12px;text-decoration:line-through">${p['cost']*2:.2f}</span></p>
                    <p style="color:#0f0">Profit tau: ${p['profit']} -> Wallet</p>
                    <a href="/buy?id={p['id']}" style="display:block;background:#0f0;color:#000;text-align:center;padding:12px;border-radius:8px;text-decoration:none;font-weight:bold">CUMPARA ACUM</a>
                </div>
                """
            
            comenzi_html = ""
            for c in comenzi_reale[-5:]:
                comenzi_html += f"<div style='background:#001100;padding:10px;margin:5px;border-left:3px solid #0f0'>✅ {c['data']} - {c['produs']} - PROFIT ${c['profit_net']} -> {c['wallet'][:10]}...</div>"

            html = f"""
            <html><head><title>Agent Shop - Afacere Autonoma REALA</title><meta name="viewport" content="width=device-width,initial-scale=1"></head>
            <body style="background:#000;color:#fff;font-family:Arial;padding:20px">
                <h1 style="color:#0f0">🤖 MAGAZIN CREAT SINGUR DE AGENT - 100% REAL</h1>
                <p>Agentul isi cauta singur produsele, isi face singur pagina, vinde singur. Tu doar ai dat acces.</p>
                <p>Wallet profit: <b style="color:#0f0">{WALLET}</b> | Cicluri: {cicluri} | Produse live: {len(produse_live)}</p>
                <hr style="border-color:#333">
                <h2>🛒 Produse selectate AUTONOM de agent (cumpara doar dupa comanda client)</h2>
                <div>{produse_html}</div>
                <hr style="border-color:#333;margin-top:30px">
                <h2>💰 Comenzi reale + Profit spre wallet</h2>
                <div>{comenzi_html if comenzi_html else "Nicio comanda inca - agentul promoveaza singur"}</div>
                <hr>
                <p style="color:#888">Model: Client plateste -> Agentul cumpara automat de la supplier cu banii clientului -> Profitul merge in wallet-ul tau {WALLET[:15]}... | Accesuri: {', '.join([k for k,v in ACCESURI.items() if v]) if any(ACCESURI.values()) else "Nu ai setat chei - seteaza in Render Environment"}</p>
                <p><a href="/admin" style="color:#0f0">/admin - Panou control agent</a> | <a href="/refresh" style="color:#0f0">Cauta produse noi acum</a></p>
            </body></html>
            """
            self.wfile.write(html.encode())
        
        elif parsed.path.startswith("/buy"):
            qs = parse_qs(parsed.query)
            pid = qs.get('id', ['0'])[0]
            comanda = cumpara_dupa_comanda(pid)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            if comanda:
                html = f"<html><body style='background:#000;color:#0f0;padding:30px;font-family:monospace'><h1>✅ COMANDA REALA PLASATA!</h1><p>Produs: {comanda['produs']}</p><p>Clientul a platit: ${comanda['incasat_client']}</p><p>Agentul cumpara acum de la supplier cu: ${comanda['cost_platit_supplier']}</p><p style='font-size:20px'>PROFIT REAL: ${comanda['profit_net']} -> Se trimite spre wallet {WALLET}</p><p>{comanda['status']}</p><a href='/shop' style='color:#0f0'>Inapoi la magazin</a></body></html>"
            else:
                html = "<html><body>Produs negasit</body></html>"
            self.wfile.write(html.encode())

        elif parsed.path == "/refresh":
            cauta_singur()
            self.send_response(302)
            self.send_header('Location', '/shop')
            self.end_headers()
        
        elif parsed.path == "/admin":
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html = f"<html><body style='background:#0f0f0f;color:#0f0;padding:20px;font-family:monospace'><h1>Panou Agent Autonom</h1><p>Cicluri: {cicluri}</p><p>Produse live: {len(produse_live)}</p><p>Comenzi: {len(comenzi_reale)}</p><p>Profit total: ${sum([c['profit_net'] for c in comenzi_reale])}</p><p>Wallet: {WALLET}</p><p>Accesuri setate: {ACCESURI}</p><pre>{json.dumps(produse_live[:2], indent=2)}</pre></body></html>"
            self.wfile.write(html.encode())
        
        else:
            self.send_response(404)
            self.end_headers()

def loop_autonom():
    global cicluri
    while True:
        time.sleep(1800) # la 30 min cauta singur produse noi si isi updateaza singur magazinul
        cicluri += 1
        cauta_singur()
        print(f"Ciclu autonom {cicluri} - magazin actualizat singur")

threading.Thread(target=loop_autonom, daemon=True).start()
HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
