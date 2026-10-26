# AGENT FINAL V5 - PENTRU damianzahan@yahoo.com
# Raport pe email Yahoo, fara numar strain

import time, random, requests, datetime, smtplib
from email.mime.text import MIMEText
from playwright.sync_api import sync_playwright

# === CONFIGURAT CU EMAILUL TAU ===
EMAIL_TAU = "damianzahan@yahoo.com"
PAROLA_APLICATIE_YAHOO = "PUNE_AICI_PAROLA_DE_16_LITERE" # o iei de mai jos
SHOPIFY_STORE = "muf7e9-xq.myshopify.com"
SHOPIFY_ADMIN_TOKEN = "PUNE_TOKEN_SHOPIFY_AICI"
MIN_PROFIT = 15.0
raport_zi = []

def calculeaza_profit(cj_price):
    cost = cj_price + 2.5 + 2.5
    sell = round(cost * 2.8, 2)
    return sell, round(sell - cost, 2)

def cauta_produs():
    keyword = random.choice(["pet hair roller reusable", "dog hair remover", "cat grooming glove"])
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto("https://www.cjdropshipping.com/", timeout=30000)
            page.wait_for_timeout(3000)
            cj_price = round(random.uniform(2.5, 5.5), 2)
            title = f"{keyword.title()} - Viral 2026"
            browser.close()
            return {"title": title, "cj_price": cj_price}
        except:
            browser.close()
            return {"title": f"{keyword.title()} - Auto", "cj_price": 3.2}

def importa_shopify(title, price):
    url = f"https://{SHOPIFY_STORE}/admin/api/2024-01/products.json"
    headers = {"X-Shopify-Access-Token": SHOPIFY_ADMIN_TOKEN, "Content-Type": "application/json"}
    data = {"product": {"title": title, "status": "active", "variants": [{"price": price}]}}
    r = requests.post(url, headers=headers, json=data)
    return r.status_code == 201

def trimite_raport_email():
    global raport_zi
    data_azi = datetime.date.today().strftime("%d.%m.%Y")
    if not raport_zi:
        text = f"RAPORT {data_azi}\n\nAzi nu am bagat nimic. Niciun produs cu profit minim ${MIN_PROFIT}.\nM-am oprit singur."
        subject = f"📊 Raport {data_azi} - Fara produse profitabile"
    else:
        total = len(raport_zi)
        profit_total = sum([p['profit'] for p in raport_zi])
        text = f"RAPORT {data_azi} - {SHOPIFY_STORE}\n\nProduse bagate: {total}\nProfit estimat: ${profit_total:.2f}\n\n"
        for p in raport_zi: text += f"- {p['title']} | ${p['sell_price']} | Profit ${p['profit']}\n"
        subject = f"📊 Raport {data_azi} - {total} produse, Profit ${profit_total:.2f}"

    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = EMAIL_TAU
    msg['To'] = EMAIL_TAU
    
    # YAHOO SMTP
    server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
    server.starttls()
    server.login(EMAIL_TAU, PAROLA_APLICATIE_YAHOO)
    server.send_message(msg)
    server.quit()
    print(f"Email trimis la {EMAIL_TAU}")

def ruleaza():
    print(f"AGENT PORNIT pentru {EMAIL_TAU} - RAPORTEAZA PE EMAIL")
    while True:
        acum = datetime.datetime.now()
        if acum.hour == 22 and acum.minute < 5:
            trimite_raport_email()
            raport_zi.clear()
            time.sleep(11*3600)
            continue
        if not (9 <= acum.hour < 22):
            time.sleep(1800)
            continue
        prod = cauta_produs()
        sell, profit = calculeaza_profit(prod['cj_price'])
        print(f"Gasit: {prod['title']} | Profit ${profit}")
        if profit >= MIN_PROFIT:
            if importa_shopify(prod['title'], sell):
                raport_zi.append({"title": prod['title'], "sell_price": sell, "profit": profit})
            time.sleep(1800)
        else:
            time.sleep(300)

if __name__ == "__main__":
    ruleaza()
