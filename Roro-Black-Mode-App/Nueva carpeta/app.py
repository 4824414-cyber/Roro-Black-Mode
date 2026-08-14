from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
import base64

app = FastAPI(title="Roro Black Mode")
CAPTURES = Path("captures")
CAPTURES.mkdir(exist_ok=True)

browser = None
page = None

class Action(BaseModel):
    type: str
    value: str = ""

async def ensure_browser():
    global browser, page
    if browser is None:
        from playwright.async_api import async_playwright
        app.state.pw = await async_playwright().start()
        browser = await app.state.pw.chromium.launch(headless=False)
        page = await browser.new_page(viewport={"width": 1400, "height": 900})
    return page

@app.get("/", response_class=HTMLResponse)
def home():
    return Path("index.html").read_text(encoding="utf-8")

@app.post("/action")
async def action(a: Action):
    global browser, page
    if a.type == "open":
        p = await ensure_browser()
        await p.goto(a.value, wait_until="domcontentloaded")
        return {"ok": True, "url": p.url, "title": await p.title()}

    if a.type == "screenshot":
        p = await ensure_browser()
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = CAPTURES / f"roro_{stamp}.png"
        await p.screenshot(path=str(filename), full_page=True)
        return {"ok": True, "file": str(filename), "url": p.url}

    if a.type == "close":
        if browser:
            await browser.close()
            browser = None
            page = None
        return {"ok": True}

    if a.type == "url":
        p = await ensure_browser()
        return {"ok": True, "url": p.url, "title": await p.title()}

    raise HTTPException(400, "Acción no permitida")

@app.get("/captures")
def captures():
    files = sorted(CAPTURES.glob("*.png"), reverse=True)
    return {"count": len(files), "files": [str(x) for x in files]}

@app.get("/health")
def health():
    return {"status": "online", "captures": len(list(CAPTURES.glob("*.png")))}

