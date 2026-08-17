#!/usr/bin/env python3
"""
Scrape REAL fundamentals from screener.in for the candidate shortlist.
Nothing invented: every number is parsed from the live page; missing -> null.
Output: research/fundamentals/<TICKER>.json  +  research/fundamentals.csv (rollup)
"""
import json, re, time, sys, csv, urllib.request
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "fundamentals"; OUT.mkdir(exist_ok=True)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"

def fetch(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*",
                                               "Referer": "https://www.screener.in/"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")

def strip(s): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()

def ratio(page, *labels):
    for label in labels:
        m = re.search(r'<span[^>]*class="name"[^>]*>\s*' + re.escape(label) +
                      r'\s*</span>.*?<span[^>]*class="[^"]*value[^"]*"[^>]*>(.*?)</span>',
                      page, re.S | re.I)
        if m:
            raw = strip(m.group(1)).replace(",", "").replace("₹", "").replace("%", "").replace("Cr.", "").strip()
            # handle "high/low" style "688 / 512" -> keep first
            nums = re.findall(r"-?\d+\.?\d*", raw)
            if nums:
                try: return float(nums[0])
                except: return None
    return None

def growth_table(page, section):
    """Compounded Sales/Profit Growth blocks -> {'10Y':..,'5Y':..,'3Y':..,'TTM':..}"""
    m = re.search(re.escape(section) + r".*?<table[^>]*>(.*?)</table>", page, re.S | re.I)
    if not m: return {}
    tbl = m.group(1)
    out = {}
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", tbl, re.S):
        cells = [strip(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)]
        if len(cells) >= 2:
            key = cells[0].replace(":", "").strip()
            val = cells[1].replace("%", "").strip()
            try: out[key] = float(val)
            except: pass
    return out

def quarters(page):
    m = re.search(r'<section[^>]*id="quarters".*?</section>', page, re.S | re.I)
    if not m: return {}
    sec = m.group(0)
    def rowvals(label):
        rm = re.search(r"<td[^>]*class=\"text\"[^>]*>\s*" + re.escape(label) +
                       r"[^<]*</td>(.*?)</tr>", sec, re.S | re.I)
        if not rm: return []
        return [strip(c).replace(",", "") for c in re.findall(r"<td[^>]*>(.*?)</td>", rm.group(1), re.S)]
    heads = []
    hm = re.search(r"<thead.*?</thead>", sec, re.S)
    if hm:
        heads = [strip(c) for c in re.findall(r"<th[^>]*>(.*?)</th>", hm.group(0), re.S) if strip(c)]
    return {"periods": heads, "sales": rowvals("Sales"), "net_profit": rowvals("Net Profit"),
            "opm": rowvals("OPM"), "eps": rowvals("EPS")}

def proscons(page):
    def block(cls):
        m = re.search(r'class="[^"]*' + cls + r'[^"]*".*?<ul[^>]*>(.*?)</ul>', page, re.S | re.I)
        if not m: return []
        return [strip(li) for li in re.findall(r"<li[^>]*>(.*?)</li>", m.group(1), re.S)]
    return block("pros"), block("cons")

def scrape(ticker):
    data = {"ticker": ticker, "scraped_at": datetime.now().isoformat(timespec="seconds"),
            "source": "screener.in", "ok": False}
    page = None
    for suffix in ("consolidated/", ""):
        try:
            page = fetch(f"https://www.screener.in/company/{urllib.parse_ticker(ticker)}/{suffix}")
            if "top-ratios" in page or "Market Cap" in page:
                data["variant"] = "consolidated" if suffix else "standalone"
                break
        except Exception as e:
            data["error"] = repr(e); page = None
    if not page:
        return data
    data["ok"] = True
    data["market_cap_cr"] = ratio(page, "Market Cap")
    data["current_price"] = ratio(page, "Current Price")
    data["pe"] = ratio(page, "Stock P/E", "P/E")
    data["book_value"] = ratio(page, "Book Value")
    data["dividend_yield_pct"] = ratio(page, "Dividend Yield")
    data["roce_pct"] = ratio(page, "ROCE")
    data["roe_pct"] = ratio(page, "ROE")
    data["face_value"] = ratio(page, "Face Value")
    data["high"] = ratio(page, "High / Low")
    data["sales_growth"] = growth_table(page, "Compounded Sales Growth")
    data["profit_growth"] = growth_table(page, "Compounded Profit Growth")
    data["roe_hist"] = growth_table(page, "Return on Equity")
    data["price_cagr"] = growth_table(page, "Stock Price CAGR")
    data["quarters"] = quarters(page)
    pr, co = proscons(page)
    data["pros"], data["cons"] = pr, co
    return data

# screener uses raw ticker incl special chars; encode & and spaces
import urllib.parse as _up
def _ticker_url(t): return _up.quote(t, safe="")
urllib.parse_ticker = _ticker_url  # tiny shim

def main():
    tickers = [l.split("\t")[0].strip() for l in Path(sys.argv[1]).read_text().splitlines()
               if l.strip() and "\t" in l]
    print(f"{len(tickers)} tickers")
    roll = []
    for i, t in enumerate(tickers, 1):
        fp = OUT / f"{t.replace('/', '_')}.json"
        if fp.exists():
            d = json.loads(fp.read_text())
        else:
            try:
                d = scrape(t)
            except Exception as e:
                d = {"ticker": t, "ok": False, "error": repr(e)}
            fp.write_text(json.dumps(d, indent=1))
            time.sleep(0.5)
        flag = "ok" if d.get("ok") else "FAIL"
        print(f"[{i:>3}/{len(tickers)}] {t:<12} {flag}  PE={d.get('pe')} ROE={d.get('roe_pct')} ROCE={d.get('roce_pct')} MCap={d.get('market_cap_cr')}")
        roll.append(d)
    # rollup csv
    with open(ROOT / "fundamentals.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ticker","ok","mcap_cr","price","pe","roe","roce","div_yld","book_value",
                    "sales_g_5y","sales_g_3y","sales_g_ttm","profit_g_5y","profit_g_3y","profit_g_ttm","price_cagr_5y","price_cagr_3y"])
        for d in roll:
            sg=d.get("sales_growth",{}) or {}; pg=d.get("profit_growth",{}) or {}; pc=d.get("price_cagr",{}) or {}
            w.writerow([d.get("ticker"), d.get("ok"), d.get("market_cap_cr"), d.get("current_price"),
                        d.get("pe"), d.get("roe_pct"), d.get("roce_pct"), d.get("dividend_yield_pct"), d.get("book_value"),
                        sg.get("5 Years"), sg.get("3 Years"), sg.get("TTM"),
                        pg.get("5 Years"), pg.get("3 Years"), pg.get("TTM"),
                        pc.get("5 Years"), pc.get("3 Years")])
    print("wrote fundamentals.csv")

if __name__ == "__main__":
    main()
