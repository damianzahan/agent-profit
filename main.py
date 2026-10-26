
import os
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

REPORT_EMAIL = os.getenv("REPORT_EMAIL", "damianzahan@yahoo.com")

print(f"✅ Agent Profit pornit! Raport la: {REPORT_EMAIL}")
print("🚀 Ruleaza 24/7...")

# Server mic ca sa ramana LIVE pe Render Free
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(f"Agent Profit LIVE! {datetime.now()} - Raport la {REPORT_EMAIL}".encode())

def run_server():
    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 Server web pe portul {port}")
    HTTPServer(("", port), Handler).serve_forever()

# Porneste serverul in fundal
threading.Thread(target=run_server, daemon=True).start()

# Bucla agentului 24/7
while True:
    try:
        print(f"[{datetime.now()}] 🔍 Agentul analizeaza... LIVE")
        print(f"📧 Urmeaza raport la {REPORT_EMAIL}")
        # Aici o sa adaugam logica de profit real
        time.sleep(60)
    except Exception as e:
        print(f"Eroare: {e}")
        time.sleep(10)
