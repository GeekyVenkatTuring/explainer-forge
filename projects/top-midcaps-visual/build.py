#!/usr/bin/env python3
"""Top Midcaps by Sector — visual edition.

Research cutoff: 2026-08-15. Universe comes from the user-supplied workbook.
Financial statements: public consolidated tables linked by the workbook
(Screener, refreshed 2026-08-15). Business portfolios: official company sites
where machine-readable, otherwise filed business descriptions.

Figures are displayed to two decimals. This is public-source analysis, not
investment advice; prices, index membership and reported values can change.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
import time
from pathlib import Path

VOICE = "en-IN-PrabhatNeural"
RATE = "-2%"
GAP = 0.50
PAUSE = 0.60
PREFIX = "mc"
SLUG = "top-midcaps-visual"

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
COMPOSER = REPO / "composer"
PUBLIC = COMPOSER / "public" / PREFIX
RAW = ROOT / "assets" / "raw"
FIN = ROOT / "assets"
ART = ROOT / "artifacts"
REND = ROOT / "renders"
QA = ROOT / "qa-stills"
DELIVER = Path.home() / "Downloads" / "generated_videos" / SLUG
DATA = Path("/Users/appuram/Developer/canvasforge/midcap_video/research_v3.json")
for directory in (PUBLIC, RAW, FIN, ART, REND, QA, DELIVER):
    directory.mkdir(parents=True, exist_ok=True)

GREEN, CYAN, AMBER, VIOLET, ROSE, BLUE = "#34D399", "#38BDF8", "#FBBF24", "#A78BFA", "#FB7185", "#60A5FA"

PRODUCTS = {
    "HEROMOTOCO": ["Commuter motorcycles", "Premium motorcycles", "Scooters", "VIDA electric vehicles", "Parts and accessories", "Service and ownership plans"],
    "BHARATFORG": ["Automotive forgings", "Industrial forgings", "Aerospace components", "Defence systems", "Power and energy", "Marine and rail components"],
    "UNOMINDA": ["Switching systems", "Automotive lighting", "Acoustic systems", "Alloy wheels", "Seating systems", "EV and electronic systems"],
    "SCHAEFFLER": ["Ball and roller bearings", "Engine systems", "Transmission components", "Chassis applications", "Clutch systems", "Industrial lifecycle services"],
    "MRF": ["Passenger-car tyres", "Two-wheeler tyres", "Truck and bus tyres", "Farm and off-road tyres", "Motorsport products", "Tyre service and retreading"],
    "POWERINDIA": ["Power transformers", "High-voltage products", "Grid automation", "Power quality systems", "Energy storage integration", "Digital and lifecycle services"],
    "BHEL": ["Thermal power equipment", "Hydro and gas systems", "Nuclear equipment", "Rail and transportation", "Defence and aerospace", "Renewables and industrial services"],
    "POLYCAB": ["Wires and cables", "Fans and lighting", "Switches and switchgear", "Conduits and fittings", "Solar products", "EPC and project solutions"],
    "GVT&D": ["Substation solutions", "High-voltage switchgear", "Grid automation", "Protection and control", "Power transformers", "Consulting and lifecycle services"],
    "ASHOKLEY": ["Medium and heavy trucks", "Light commercial vehicles", "Buses and coaches", "Defence mobility", "Power solutions", "Spares, service and digital fleet tools"],
    "RVNL": ["New railway lines", "Track doubling", "Gauge conversion", "Rail electrification", "Metro and urban transport", "Bridges, workshops and project development"],
}

# GE Vernova T&D India's consolidated Screener history is stale. These FY2025
# figures come from the company's FY2024-25 annual report (INR million / 10).
OFFICIAL_OVERRIDES = {
    "GVT&D": {
        "period": "Mar 2025", "sales": 4292.30, "op": 833.98,
        "profit": 608.33, "interest": 14.31, "depreciation": 47.31,
        "opm": 19.40, "reserves": 1721.90, "borrowings": 0.00,
        "fixed": 340.20, "investments": 0.00, "assets": 4661.08,
        "liabilities": 2887.97, "cfo": 903.58, "cfi": -495.75,
        "cff": -69.06, "net": 338.78,
    }
}


def ascii_text(value: object) -> str:
    text = str(value or "").replace("₹", "rupees ").replace("&", "and")
    text = text.replace("—", " - ").replace("–", "-").replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text.encode("ascii", "ignore").decode()).strip()


def number(value: object) -> float | None:
    raw = re.sub(r"[^0-9.\-]", "", str(value or ""))
    try:
        return float(raw)
    except ValueError:
        return None


def row(company: dict, statement: str, *names: str) -> list[tuple[str, float]]:
    table = company["financials"].get(statement, {})
    found = next((vals for key, vals in table.items() if key.lower() in {n.lower() for n in names}), {})
    values = []
    for period, raw in found.items():
        val = number(raw)
        if val is not None and re.search(r"Mar \d{4}|TTM", period):
            values.append((period, val))
    return values


def last(company: dict, statement: str, *names: str, default: float = 0.0) -> tuple[str, float]:
    values = row(company, statement, *names)
    return values[-1] if values else ("not reported", default)


def cagr(values: list[tuple[str, float]]) -> float | None:
    annual = [(p, v) for p, v in values if p != "TTM" and v > 0][-5:]
    if len(annual) < 2:
        return None
    y0 = int(re.search(r"\d{4}", annual[0][0]).group())
    y1 = int(re.search(r"\d{4}", annual[-1][0]).group())
    return (annual[-1][1] / annual[0][1]) ** (1 / max(1, y1 - y0)) - 1


def spoken(value: float) -> str:
    sign = "minus " if value < 0 else ""
    return f"{sign}{abs(value):,.2f} crore rupees"


def clean_about(company: dict, limit: int = 430) -> str:
    about = re.sub(r"\[\d+\]", "", ascii_text(company.get("about")))
    return about[:limit].rsplit(" ", 1)[0] + ("." if about else "")


def company_segments(company: dict, index: int, total: int) -> list[tuple]:
    ticker, name, sector = company["ticker"], ascii_text(company["company"]), ascii_text(company["sector"])
    products = PRODUCTS[ticker]
    sales = row(company, "profit_loss", "Sales", "Revenue")
    op = row(company, "profit_loss", "Operating Profit")
    profit = row(company, "profit_loss", "Net Profit")
    sales_p, sales_v = sales[-1] if sales else ("not reported", 0.0)
    op_p, op_v = op[-1] if op else (sales_p, 0.0)
    profit_p, profit_v = profit[-1] if profit else (sales_p, 0.0)
    expense_v = max(0.0, sales_v - op_v)
    interest_p, interest_v = last(company, "profit_loss", "Interest")
    dep_p, dep_v = last(company, "profit_loss", "Depreciation")
    tax_p, tax_v = last(company, "profit_loss", "Tax %")
    opm_p, opm_v = last(company, "profit_loss", "OPM %")
    sales_cagr = cagr(sales)
    profit_cagr = cagr(profit)
    reserves_p, reserves_v = last(company, "balance_sheet", "Reserves")
    borrow_p, borrow_v = last(company, "balance_sheet", "Borrowings")
    fixed_p, fixed_v = last(company, "balance_sheet", "Fixed Assets")
    invest_p, invest_v = last(company, "balance_sheet", "Investments")
    assets_p, assets_v = last(company, "balance_sheet", "Total Assets")
    liabilities_p, liabilities_v = last(company, "balance_sheet", "Other Liabilities")
    cfo_p, cfo_v = last(company, "cash_flow", "Cash from Operating Activity")
    cfi_p, cfi_v = last(company, "cash_flow", "Cash from Investing Activity")
    cff_p, cff_v = last(company, "cash_flow", "Cash from Financing Activity")
    net_p, net_v = last(company, "cash_flow", "Net Cash Flow")

    if ticker in OFFICIAL_OVERRIDES:
        o = OFFICIAL_OVERRIDES[ticker]
        sales_p = op_p = profit_p = interest_p = dep_p = opm_p = o["period"]
        reserves_p = borrow_p = fixed_p = invest_p = assets_p = liabilities_p = o["period"]
        cfo_p = cfi_p = cff_p = net_p = o["period"]
        sales_v, op_v, profit_v = o["sales"], o["op"], o["profit"]
        expense_v, interest_v, dep_v, opm_v = sales_v - op_v, o["interest"], o["depreciation"], o["opm"]
        reserves_v, borrow_v, fixed_v = o["reserves"], o["borrowings"], o["fixed"]
        invest_v, assets_v, liabilities_v = o["investments"], o["assets"], o["liabilities"]
        cfo_v, cfi_v, cff_v, net_v = o["cfo"], o["cfi"], o["cff"], o["net"]
        sales_cagr = profit_cagr = None

    metric = lambda label, val, suffix="": {"k": label, "v": f"{val:,.2f}{suffix}"}
    metrics = [
        metric("Market cap", float(company.get("workbook_market_cap_cr") or 0), " Cr"),
        metric("P / E", float(company.get("workbook_pe") or 0) if str(company.get("workbook_pe")) != "N/A" else 0, "x"),
        metric("Latest revenue", sales_v, " Cr"),
        metric("Operating margin", opm_v, "%"),
        metric("5Y sales CAGR", sales_cagr * 100, "%") if sales_cagr is not None else {"k": "5Y sales CAGR", "v": "N/A"},
        metric("5Y profit CAGR", profit_cagr * 100, "%") if profit_cagr is not None else {"k": "5Y profit CAGR", "v": "N/A"},
    ]
    if sales_cagr is not None: metrics[4]["hero"] = True
    elif opm_v: metrics[3]["hero"] = True
    thesis = [
        f"Portfolio spans {len(products)} visible product or service groups.",
        f"Latest public revenue table shows {sales_v:,.2f} crore rupees in {sales_p}.",
        "The decision hinges on margins, capital intensity and cash conversion.",
    ]

    parts = [{"n": i + 1, "title": p[:34], "sub": "product / service line", "c": [GREEN, CYAN, AMBER, VIOLET, ROSE, BLUE][i % 6]} for i, p in enumerate(products)]
    business_narr = (f"{name} operates across six visible portfolio groups. [pause] " +
                     ". [pause] ".join(products) + ". [pause] " + clean_about(company) +
                     " These categories show where revenue can come from, but the annual report should still be checked for segment mix and geography.")
    score_narr = (f"Here is the point-in-time scorecard for {name}. [pause] Market capitalization in the workbook is {spoken(float(company.get('workbook_market_cap_cr') or 0))}. "
                  f"The latest public table shows revenue of {spoken(sales_v)} and an operating margin of {opm_v:.2f} percent. [pause] "
                  + (f"Five-year sales growth is {sales_cagr*100:.2f} percent annualized. " if sales_cagr is not None else "A comparable five-year sales series is unavailable. ")
                  + (f"Five-year profit growth is {profit_cagr*100:.2f} percent. " if profit_cagr is not None else "A comparable five-year profit series is unavailable. ")
                  + "Unavailable history is not an economic claim.")
    pnl_narr = (f"Now read the income statement for {name}. [pause] In {sales_p}, revenue was {spoken(sales_v)}. "
                f"Operating costs implied by the table were {spoken(expense_v)}, leaving operating profit of {spoken(op_v)}. [pause] "
                f"Interest was {spoken(interest_v)} and depreciation was {spoken(dep_v)}. Net profit was {spoken(profit_v)}. "
                "Watch whether profit grows faster than sales, and whether the margin survives a weaker cycle.")
    balance_narr = (f"The balance sheet is a snapshot, not a yearly flow. [pause] At {assets_p}, total assets were {spoken(assets_v)}. "
                    f"Fixed assets were {spoken(fixed_v)}, investments were {spoken(invest_v)}, reserves were {spoken(reserves_v)}, borrowings were {spoken(borrow_v)}, and other liabilities were {spoken(liabilities_v)}. [pause] "
                    "The key test is whether incremental debt and retained earnings are producing stronger operating profit and cash generation.")
    cash_narr = (f"Finally, follow the cash for {name}. [pause] Operating cash flow in {cfo_p} was {spoken(cfo_v)}. "
                 f"Investing cash flow was {spoken(cfi_v)}. Financing cash flow was {spoken(cff_v)}. Net cash movement was {spoken(net_v)}. [pause] "
                 "Negative investing cash flow can reflect productive expansion. Persistent weak operating cash flow alongside reported profit deserves much closer investigation.")

    safe = re.sub(r"[^a-z0-9]+", "", ticker.lower())
    return [
        (f"c{index:02d}_{safe}_business", "fa_roadmap", {"kicker": f"{ticker} · BUSINESS AND PORTFOLIO", "parts": parts}, business_narr),
        (f"c{index:02d}_{safe}_score", "nb_stock", {"idx": index, "total": total, "tier": "1", "name": name, "ticker": ticker, "sector": sector[:22], "cap": "Midcap workbook", "metrics": metrics, "thesis": thesis, "growth": (sales_cagr or 0.12) * 100, "take": "Public-source snapshot; verify the latest filing"}, score_narr),
        (f"c{index:02d}_{safe}_pnl", "fa_waterfall", {"kicker": f"{ticker} · INCOME STATEMENT", "title": f"{name}: revenue to net profit", "unit": "rupees Cr", "segs": [
            {"label": "Revenue", "value": sales_v, "c": CYAN, "subtotal": True},
            {"label": "Operating costs", "delta": -expense_v, "c": ROSE},
            {"label": "Operating profit", "value": op_v, "c": GREEN, "subtotal": True},
            {"label": "Interest", "delta": -interest_v, "c": AMBER},
            {"label": "Depreciation", "delta": -dep_v, "c": VIOLET},
            {"label": "Net profit", "value": profit_v, "c": GREEN, "subtotal": True}],
            "note": f"Consolidated public table · {sales_p} · values shown to two decimals", "color": CYAN, "decimals": 2}, pnl_narr),
        (f"c{index:02d}_{safe}_balance", "fa_ledger", {"kicker": f"{ticker} · BALANCE SHEET", "title": f"{name}: what the capital is funding", "rows": [
            {"label": "Total assets", "val": f"{assets_v:,.2f} Cr", "c": CYAN, "bold": True},
            {"label": "Fixed assets", "val": f"{fixed_v:,.2f} Cr"},
            {"label": "Investments", "val": f"{invest_v:,.2f} Cr"},
            {"label": "Reserves", "val": f"{reserves_v:,.2f} Cr", "c": GREEN},
            {"label": "Borrowings", "val": f"{borrow_v:,.2f} Cr", "c": AMBER},
            {"label": "Other liabilities", "val": f"{liabilities_v:,.2f} Cr", "c": ROSE}],
            "caption": f"Consolidated snapshot · {assets_p} · compare leverage with cash generation", "color": VIOLET}, balance_narr),
        (f"c{index:02d}_{safe}_cash", "fa_stack", {"kicker": f"{ticker} · CASH FLOW", "title": f"{name}: operating, investing and financing cash", "unit": "Cr", "segs": [
            {"label": "Operating cash flow", "val": cfo_v, "c": GREEN, "op": "+"},
            {"label": "Investing cash flow", "val": cfi_v, "c": CYAN, "op": "+" if cfi_v >= 0 else "−"},
            {"label": "Financing cash flow", "val": cff_v, "c": AMBER, "op": "+" if cff_v >= 0 else "−"}],
            "result": {"label": "Net cash movement", "val": net_v, "c": GREEN if net_v >= 0 else ROSE},
            "note": f"Consolidated cash-flow table · {net_p} · profit is not the same as cash", "color": GREEN, "decimals": 2}, cash_narr),
    ]


def screenplay(chapter: int) -> list[tuple]:
    data = json.loads(DATA.read_text(encoding="utf-8"))["companies"]
    groups = {
        1: ["Automobile and Auto Components", "Capital Goods", "Construction"],
        2: ["Chemicals", "Construction Materials", "Consumer Durables"],
        3: ["Consumer Services", "Diversified", "Fast Moving Consumer Goods"],
        4: ["Financial Services", "Healthcare", "Information Technology"],
        5: ["Metals & Mining", "Oil Gas & Consumable Fuels", "Power"],
        6: ["Realty", "Services", "Telecommunication", "Textiles"],
    }
    selected = [c for c in data if c["sector"] in groups[chapter]]
    if chapter != 1:
        missing = [c["ticker"] for c in selected if c["ticker"] not in PRODUCTS]
        raise SystemExit(f"Product map for chapter {chapter} is pending: {missing}")
    segs = [
        ("s00_title", "nb_title", {"big": "Top Midcaps", "big2": "by Sector", "sub": "Business portfolios · income statements · balance sheets · cash flows", "kick": "78 INDIAN COMPANIES · VISUAL FUNDAMENTAL DEEP DIVE"},
         "Seventy-eight companies across eighteen sectors. [pause] We map what each business sells, then connect its income statement, balance sheet and cash flow. This is public-source education, not investment advice."),
        ("s01_divider", "fa_divider", {"n": 1, "total": 6, "title": "Mobility and Infrastructure", "sub": "Auto components · capital goods · railway construction", "color": GREEN},
         "Chapter one covers mobility, capital goods and railway construction. [pause] Eleven companies. Each company gets a portfolio map, a scorecard, and three linked financial-statement visuals."),
    ]
    for index, company in enumerate(selected, 1):
        segs.extend(company_segments(company, index, len(selected)))
    segs.append(("s99_recap", "fa_recap", {"kicker": "CHAPTER 01 · RECAP", "title": "Five questions for every company", "items": [
        "What products and services create revenue?",
        "Are sales and operating profit compounding together?",
        "What assets and borrowings fund that growth?",
        "Does accounting profit convert into operating cash?",
        "Which cycle, regulation or execution risk can break the thesis?"],
        "closer": "Read the three statements as one connected system, then verify the notes."},
        "That completes chapter one. [pause] Start with the portfolio. Then test revenue and margins. Follow the funding through the balance sheet. Finally, demand cash conversion. [pause] Every figure here is a dated public snapshot. Recheck the latest filing before making any decision. Thanks for watching."))
    return segs


def ffdur(path: Path) -> float:
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def tts_chunk(path: Path, text: str) -> None:
    mp3 = path.with_suffix(".mp3")
    for attempt in range(6):
        try:
            result = subprocess.run(["edge-tts", "--voice", VOICE, f"--rate={RATE}", "--text", text, "--write-media", str(mp3)], capture_output=True, timeout=60)
        except subprocess.TimeoutExpired:
            result = None
        if result and result.returncode == 0 and mp3.exists() and mp3.stat().st_size:
            break
        if mp3.exists(): mp3.unlink()
        time.sleep(2 + attempt * 2)
    else:
        raise RuntimeError(f"TTS failed: {path.name}")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp3), "-ar", "24000", "-ac", "1", str(path)], check=True)
    mp3.unlink()


def gen_audio(segment_id: str, text: str) -> tuple[Path, float]:
    final = FIN / f"{segment_id}.wav"
    if final.exists(): return final, ffdur(final)
    chunks = [chunk.strip() for chunk in text.split("[pause]") if chunk.strip()]
    paths = []
    for index, chunk in enumerate(chunks):
        raw = RAW / f"{segment_id}_c{index}.wav"
        if not raw.exists(): tts_chunk(raw, chunk)
        paths.append(raw)
    pause = RAW / "_pause.wav"
    if not pause.exists():
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(PAUSE), str(pause)], check=True)
    listing = RAW / f"{segment_id}_concat.txt"
    listing.write_text("".join(f"file '{p}'\n" + (f"file '{pause}'\n" if i < len(paths)-1 else "") for i, p in enumerate(paths)))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(final)], check=True)
    return final, ffdur(final)


def build(chapter: int) -> Path:
    segments = screenplay(chapter)
    manifest = []
    for sid, variant, props, narration in segments:
        path, duration = gen_audio(sid, narration)
        manifest.append((sid, variant, props, narration, path, duration))
        print(f"{sid:28s} {duration:6.2f}s", flush=True)
    gap = FIN / "_gap.wav"
    if not gap.exists():
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(GAP), str(gap)], check=True)
    audio_list = ART / f"ch{chapter:02d}_audio.txt"
    audio_list.write_text("".join(f"file '{m[4]}'\n" + (f"file '{gap}'\n" if i < len(manifest)-1 else "") for i, m in enumerate(manifest)))
    narration = PUBLIC / f"ch{chapter:02d}.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(audio_list), "-c", "copy", str(narration)], check=True)
    cuts, t = [], 0.0
    for sid, variant, props, text, path, duration in manifest:
        cuts.append({"id": sid, "type": variant, "in_seconds": round(t, 3), "out_seconds": round(t + duration, 3), "props": {**props, "dur": round(duration + GAP, 3)}})
        t += duration + GAP
    artifact = ART / f"ch{chapter:02d}.json"
    artifact.write_text(json.dumps({"cuts": cuts, "captions": [], "audio": {"narration": {"src": f"{PREFIX}/ch{chapter:02d}.wav", "volume": 1.0}}}, indent=2))
    print(f"chapter {chapter}: {(t-GAP)/60:.2f} min, {len(cuts)} animated scenes")
    return artifact


def qa(artifact: Path) -> None:
    data = json.loads(artifact.read_text())
    for cut in data["cuts"]:
        frame = round((cut["in_seconds"] + 0.60 * (cut["out_seconds"] - cut["in_seconds"])) * 30)
        output = QA / f"{cut['id']}.png"
        result = subprocess.run(["npx", "remotion", "still", "Explainer", str(output), f"--props={artifact}", f"--frame={frame}"], cwd=COMPOSER, capture_output=True, text=True)
        if result.returncode:
            print((result.stderr or result.stdout)[-1500:]); raise SystemExit(f"QA still failed: {cut['id']}")
        print(f"QA {cut['id']}", flush=True)


def render(artifact: Path, chapter: int) -> Path:
    output = REND / f"chapter-{chapter:02d}.mp4"
    subprocess.run(["npx", "remotion", "render", "Explainer", str(output), f"--props={artifact}", "--concurrency=2", "--timeout=600000"], cwd=COMPOSER, check=True)
    delivered = DELIVER / f"top-midcaps-visual-chapter-{chapter:02d}.mp4"
    subprocess.run(["cp", str(output), str(delivered)], check=True)
    return delivered


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["tts", "qa", "render"])
    parser.add_argument("chapter", type=int, default=1, nargs="?")
    args = parser.parse_args()
    artifact = ART / f"ch{args.chapter:02d}.json"
    if args.mode == "tts": build(args.chapter)
    elif args.mode == "qa": qa(artifact if artifact.exists() else build(args.chapter))
    else: render(artifact if artifact.exists() else build(args.chapter), args.chapter)
