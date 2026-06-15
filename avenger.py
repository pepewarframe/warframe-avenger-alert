import os, requests

WEBHOOK = os.environ["DISCORD_WEBHOOK"]
MAX_PRICE = 65

url = "https://api.warframe.market/v1/items/arcane_avenger/orders"
orders = requests.get(url, timeout=15).json()["payload"]["orders"]

r5 = [
    o for o in orders
    if o["order_type"] == "sell"
    and o.get("mod_rank") == 5
    and o["user"]["status"] in ["online", "ingame"]
]

if not r5:
    print("No hay Avenger R5 online.")
    raise SystemExit

cheap = min(r5, key=lambda o: o["platinum"])
price = cheap["platinum"]
seller = cheap["user"]["ingame_name"]

print(f"Más barato: {price} PL - {seller}")

if price <= MAX_PRICE:
    profit = 84 - price
    msg = (
        f"🚨 Arcane Avenger R5 a {price} PL\n"
        f"Vendedor: {seller}\n"
        f"Ganancia estimada: {profit} PL\n"
        f"https://warframe.market/items/arcane_avenger"
    )
    requests.post(WEBHOOK, json={"content": msg}, timeout=15)
