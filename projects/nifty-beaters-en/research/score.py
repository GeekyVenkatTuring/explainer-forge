#!/usr/bin/env python3
"""Read all scraped fundamentals, compute a transparent score, print a per-sector
ranked table to reason over. Financials (banks/NBFC/insurers) judged on ROE (ROCE
is not meaningful for lenders); everyone else on ROE+ROCE. Nothing here auto-picks —
it surfaces the real numbers so selection is defensible."""
import json, glob, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# sector map from candidates.tsv
SEC = {}
for line in (ROOT / "candidates.tsv").read_text().splitlines():
    p = line.split("\t")
    if len(p) >= 3: SEC[p[0]] = (p[1], p[2])

FIN_SECT = {"Financial Services"}

def num(x):
    try: return float(x)
    except: return None

rows = []
for f in glob.glob(str(ROOT / "fundamentals" / "*.json")):
    d = json.load(open(f))
    t = d.get("ticker")
    if not d.get("ok") or d.get("pe") is None: continue
    name, sector = SEC.get(t, (t, "?"))
    sg = d.get("sales_growth", {}) or {}; pg = d.get("profit_growth", {}) or {}
    def g(dic, *keys):
        for k in keys:
            if k in dic and dic[k] is not None: return dic[k]
        return None
    sg5, sg3 = g(sg, "5 Years"), g(sg, "3 Years")
    pg5, pg3 = g(pg, "5 Years"), g(pg, "3 Years")
    pe = num(d.get("pe")); roe = num(d.get("roe_pct")); roce = num(d.get("roce_pct"))
    mcap = num(d.get("market_cap_cr"))
    is_fin = sector in FIN_SECT
    # growth: blend, cap each at 60 to avoid outlier dominance
    gvals = [v for v in (sg5, sg3, pg5, pg3) if v is not None]
    gcap = [min(60, max(-20, v)) for v in gvals]
    growth = sum(gcap) / len(gcap) if gcap else None
    # quality
    q_parts = [v for v in ([roe] if is_fin else [roe, roce]) if v is not None]
    quality = sum(q_parts) / len(q_parts) if q_parts else None
    # peg-ish (valuation vs growth); lower better
    peg = (pe / growth) if (pe and growth and growth > 0) else None
    # composite (0..100-ish) — only informative
    score = 0.0; wsum = 0
    if quality is not None: score += min(45, quality) * 1.0; wsum += 1
    if growth is not None: score += min(45, growth) * 1.2; wsum += 1
    if peg is not None: score += max(0, 25 - peg * 8); wsum += 1  # reward cheap-vs-growth
    rows.append({"t": t, "name": name, "sector": sector, "mcap": mcap, "pe": pe,
                 "roe": roe, "roce": roce, "sg5": sg5, "pg5": pg5, "growth": growth,
                 "quality": quality, "peg": peg, "score": round(score, 1), "fin": is_fin})

# per-sector print
from collections import defaultdict
bys = defaultdict(list)
for r in rows: bys[r["sector"]].append(r)
def fmt(v, w=6, d=1):
    return (f"{v:>{w}.{d}f}" if isinstance(v, (int, float)) else f"{'--':>{w}}")
print(f"TOTAL scored: {len(rows)}\n")
for s in sorted(bys):
    rs = sorted(bys[s], key=lambda r: -(r["score"] or 0))
    print(f"### {s}  ({len(rs)})")
    print(f"  {'ticker':<12}{'mcap':>9}{'PE':>7}{'ROE':>7}{'ROCE':>7}{'sg5':>6}{'pg5':>6}{'grw':>6}{'qual':>6}{'peg':>6}{'score':>7}")
    for r in rs:
        print(f"  {r['t']:<12}{fmt(r['mcap'],9,0)}{fmt(r['pe'],7)}{fmt(r['roe'])}{fmt(r['roce'])}"
              f"{fmt(r['sg5'])}{fmt(r['pg5'])}{fmt(r['growth'])}{fmt(r['quality'])}{fmt(r['peg'],6,2)}{fmt(r['score'],7)}")
    print()

# also write a flat csv sorted by score
with open(ROOT / "scored.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["ticker","name","sector","mcap_cr","pe","roe","roce","sg5","pg5","growth","quality","peg","score","fin"])
    for r in sorted(rows, key=lambda r: -(r["score"] or 0)):
        w.writerow([r["t"], r["name"], r["sector"], r["mcap"], r["pe"], r["roe"], r["roce"],
                    r["sg5"], r["pg5"], r["growth"], r["quality"], r["peg"], r["score"], r["fin"]])
