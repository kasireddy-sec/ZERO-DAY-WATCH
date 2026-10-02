import os, httpx

async def telegram(text):
    token = os.getenv("TELEGRAM_BOT_TOKEN","")
    chat = os.getenv("TELEGRAM_CHAT_ID","")
    if not token or not chat:
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    async with httpx.AsyncClient(timeout=20) as c:
        r = await c.post(url, json={"chat_id":chat,"text":text[:4000]})
        return r.is_success

async def send_alert(record):
    msg = (
        "🚨 ZERO-DAY INTELLIGENCE ALERT\n\n"
        f"Record: {record['Record_ID']}\n"
        f"Title: {record['Title']}\n"
        f"Vendor: {record['Vendor']}\n"
        f"Product: {record['Product']}\n"
        f"CVE: {record['CVE'] or 'Not assigned'}\n"
        f"Exploitation: {record['Exploitation']}\n"
        f"Patch: {record['Patch_Status']}\n"
        f"Confidence: {record['Confidence']}\n\n"
        f"Source: {record['Source_URL']}"
    )
    return await telegram(msg)
