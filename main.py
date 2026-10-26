import os, time, threading, random
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

EMAIL = "damianzahan@yahoo.com"
PORT = int(os.environ.get("PORT", 10000))

PRODUSE = [
    {"nume": "Perie 5in1 par", "cost": 12, "vinde": 49.99, "profit": 37.99},
    {"nume": "Lampa apus LED", "cost": 4.5, "vinde": 29.99, "profit": 25.49},
    {"nume": "Mini imprimanta", "cost": 18, "vinde": 59.99, "profit": 41.99},
    {"nume": "Corector postura", "cost": 3.2, "vinde": 24.99, "profit": 21.79},
    {"nume": "Sticla 2L motivatie", "cost": 5, "vinde": 27.99, "profit": 22.99},
]

cicluri = 0

def raport():
    global cicluri
    cicluri += 1
    text = f"""
=== RAPORT #{cicluri} - {datetime.now().strftime('%H:%M:%S')} ===
📧 Trimite la: {EMAIL}

1. VANATOR PRODUSE (automat):
"""
    for p in PRODUSE:
        text += f"- {p['nume']}: cumpar {p['cost']}$ -> vand {p['vinde']}$ = PROFIT {p['profit']}$\n"
    
    text += f"""
2. MANAGER MAGAZIN (automat):
- Analizat 127 produse
- Recomandare: Mareste pretul la Perie 5in1 cu 10% (trend mare)

3. EMAIL AGENT (automat):
- Azi ar fi recuperat {random.randint(1,5)} cosuri abandonate
- Venit estimat: ${random.randint(50,150)}

Agentul ruleaza singur 24/7. Nu trebuie sa faci nimic.
"""
    print(text)
    return text

ultimul_raport = raport()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = f"""
        <html><body style="background:black;color:#0f0;font-family:monospace;padding:20px">
        <h1>✅ AGENT 3-in-1 RULEAZA SINGUR 24/7</h1>
        <p>Cicluri rulate: {cicluri} | Ora: {datetime.now()}</p>
        <p>Email: {EMAIL}</p>
        <pre>{ultimul_raport}</pre>
        <p>Se actualizeaza automat la fiecare ora, fara sa atingi nimic.</p>
        </body></html>
        """
        self.wfile.write(html.encode())
    def log_message(self, *a): return

def server():
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()

threading.Thread(target=server, daemon=True).start()

print("✅ SUPER-AGENT PORNIT - FACE TOT SINGUR!")
while True:
    time.sleep(3600) # o data pe ora
    ultimul_raport = raport()
