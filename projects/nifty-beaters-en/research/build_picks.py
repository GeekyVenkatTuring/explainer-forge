#!/usr/bin/env python3
"""Assemble the final 50 -> picks.json. Metrics are pulled from the scraped JSONs
(exact, no transcription); editorial fields (tier, thesis, hero metric) are curated.
Sector-aware: banks/NBFC/insurers show ROE (ROCE not meaningful for lenders)."""
import json, os
from pathlib import Path
ROOT = Path(__file__).resolve().parent
F = ROOT / "fundamentals"

def load(t): return json.load(open(F / f"{t}.json"))
def g(dic, *ks):
    for k in ks:
        if dic and dic.get(k) is not None: return dic[k]
    return None
def cap_class(mc):
    if mc is None: return "—"
    if mc >= 50000: return "Large-cap"
    if mc >= 15000: return "Mid-cap"
    return "Small-cap"
def cap_fmt(mc):
    if mc is None: return "—"
    return f"₹{mc/100000:.2f}L Cr" if mc >= 100000 else f"₹{mc:,.0f} Cr"
def pct(v): return f"{v:.1f}%" if isinstance(v, (int, float)) else "—"

# true lenders / leveraged financials — ROCE is not meaningful, show ROE only.
# (CAMS/CDSL/BSE are asset-light market infra — ROCE IS their standout metric.)
FIN = {"NUVAMA","MOTILALOFS","POLICYBZR","ICICIBANK","HDFCBANK",
       "SBIN","BAJFINANCE","SHRIRAMFIN","CHOLAFIN"}

# ---- editorial: (tier, name, sector, hero, thesis[3], take) ----
E = {
 # ================= TIER 1 — CORE COMPOUNDERS =================
 "ICICIBANK": (1,"ICICI Bank","Private Bank","roe",
    ["Best-run large private bank: clean book, sector-leading return on equity.",
     "Retail + business banking engine still compounding loans in the mid-teens.",
     "Digital-first franchise wins deposits cheaply — the core banking moat."],
    "Quality large-cap compounding, priced sensibly"),
 "HDFCBANK": (1,"HDFC Bank","Private Bank","pe",
    ["India's largest private bank, now digesting the HDFC merger.",
     "Deposit re-acceleration + margin recovery set up an earnings re-rating.",
     "Cheapest it has looked in a decade versus its own history."],
    "The re-rating candidate hiding in plain sight"),
 "SBIN": (1,"State Bank of India","PSU Bank","pe",
    ["The PSU banking giant at a single-digit P/E — cheap for its franchise.",
     "Cleaned-up book + credit growth riding India's capex cycle.",
     "Unmatched deposit base and reach no private bank can copy."],
    "Value + scale: a bank you buy cheap"),
 "BAJFINANCE": (1,"Bajaj Finance","NBFC","roe",
    ["Premier consumer-lending NBFC with a data + distribution flywheel.",
     "AUM compounding ~25–30% as it cross-sells to 90M+ customers.",
     "Building its own payments + app stack to defend the moat."],
    "The compounding machine of Indian lending"),
 "LT": (1,"Larsen & Toubro","Capex / Infra","pe",
    ["The purest proxy for India's infrastructure and capex super-cycle.",
     "Record order book across roads, power, defence and Gulf projects.",
     "Asset-light services (IT, tech) add a high-margin second engine."],
    "You buy India's build-out in one stock"),
 "M&M": (1,"Mahindra & Mahindra","Auto","grw",
    ["SUV market-share leader with the strongest new-launch pipeline.",
     "Tractors ride the rural recovery; EV + tech add optionality.",
     "Trades cheaper than peers despite the fastest earnings growth."],
    "Cheapest quality in Indian autos"),
 "BEL": (1,"Bharat Electronics","Defence","roce",
    ["Defence indigenisation tailwind with a multi-year order backlog.",
     "Elite return on capital and near-zero debt — a rare combination.",
     "Radars, missiles, electronic warfare: high-moat, high-margin lines."],
    "A structural defence compounder"),
 "TITAN": (1,"Titan Company","Consumption","roe",
    ["Formalisation of India's ₹5-lakh-crore jewellery market flows to Tanishq.",
     "Watches, eyewear, and a fast-scaling wearables and care business.",
     "Premium brand power lets it grow volumes and pricing together."],
    "The premiumisation-of-India compounder"),
 "SUNPHARMA": (1,"Sun Pharma","Pharma","pe",
    ["India's largest drug-maker pivoting to high-margin global specialty.",
     "Ilumya, Winlevi and the specialty book de-risk US generic pricing.",
     "Strong cash generation funds R&D without stressing the balance sheet."],
    "Pharma quality with a specialty kicker"),
 "TCS": (1,"Tata Consultancy Services","IT Services","roe",
    ["Best-in-class margins and cash returns in Indian IT.",
     "AI is a services opportunity, not just a threat, at this scale.",
     "Defensive ballast: pays out most of its cash as dividends/buybacks."],
    "The steady, cheap quality anchor"),
 "POLYCAB": (1,"Polycab India","Electrification","roce",
    ["Market-leading wires & cables riding electrification and housing.",
     "Fast-growing FMEG + exports diversify beyond the core.",
     "Strong balance sheet and ROCE fund the 'Leap' capex plan."],
    "Electrifying India, profitably"),
 "ULTRACEMCO": (1,"UltraTech Cement","Cement / Infra","grw",
    ["The consolidating leader of Indian cement, adding capacity fast.",
     "Volume + pricing leverage as the housing/infra cycle turns up.",
     "Scale advantage on cost that smaller peers cannot match."],
    "The infrastructure cycle's toll-booth"),
 "ZYDUSLIFE": (1,"Zydus Lifesciences","Pharma","peg",
    ["Quality pharma at a value-stock P/E — a rare mispricing.",
     "Strong US pipeline plus a resilient India branded business.",
     "Consistent 20%+ return on capital with a light balance sheet."],
    "Growth you're barely paying for"),
 "BAJAJ-AUTO": (1,"Bajaj Auto","Auto","roce",
    ["Premium 2-wheelers + a dominant, high-margin export franchise.",
     "Electric Chetak scaling as it defends the premium ICE base.",
     "Fortress balance sheet and elite returns on capital."],
    "Export-powered 2-wheeler quality"),
 "SOLARINDS": (1,"Solar Industries","Defence / Explosives","grw",
    ["World-scale explosives maker now a fast-rising defence supplier.",
     "Defence (ammo, drones, propellants) is the high-growth new leg.",
     "Elite ROE/ROCE with 40%+ earnings growth — a rare pairing."],
    "Explosive growth, literally"),
 "APLAPOLLO": (1,"APL Apollo Tubes","Building Materials","roce",
    ["The category-creating leader in structural steel tubes.",
     "Innovation + distribution keep it ahead as construction booms.",
     "High return on capital with a light, working-capital-lean model."],
    "A branded moat in a commodity"),

 # ================= TIER 2 — GROWTH ACCELERATORS =================
 "DIXON": (2,"Dixon Technologies","EMS / China+1","grw",
    ["India's electronics-manufacturing champion under the PLI + China+1 wave.",
     "Mobiles, then components and displays — climbing the value chain.",
     "Backward integration is the next margin and moat expansion."],
    "The China+1 manufacturing bet"),
 "KALYANKJIL": (2,"Kalyan Jewellers","Jewellery","grw",
    ["Asset-light franchise model powering rapid, funded store expansion.",
     "Formalisation shifts share from unorganised players to brands.",
     "Candere + South-to-North expansion widen the runway."],
    "Formalisation on fast-forward"),
 "TRENT": (2,"Trent (Westside · Zudio)","Retail","grw",
    ["Zudio is one of India's fastest-scaling value-fashion formats.",
     "Tata-backed retail with best-in-class store economics.",
     "Adding grocery and beauty to extend the growth runway."],
    "Hyper-growth retail execution"),
 "VBL": (2,"Varun Beverages","Beverages","grw",
    ["PepsiCo's key bottler, expanding into Africa and new categories.",
     "Distribution + cold-chain build-out drives volume compounding.",
     "Energy drinks and snacks add fresh growth vectors."],
    "Compounding one bottle at a time"),
 "APARINDS": (2,"Apar Industries","T&D / Cables","grw",
    ["Conductors + cables leader riding global grid and renewables capex.",
     "Exports to the US/Europe grid upgrade cycle are surging.",
     "Specialty oils round out a diversified, order-rich book."],
    "Wired into the global energy grid"),
 "BLUESTARCO": (2,"Blue Star","Cooling","grw",
    ["Room-AC share gains as Indian cooling penetration is still tiny.",
     "Strong commercial refrigeration + MEP projects business.",
     "Rising incomes + heat make air-conditioning a secular story."],
    "Structural cooling demand"),
 "KPITTECH": (2,"KPIT Technologies","Auto Tech / ER&D","roce",
    ["Pure-play software partner to global automakers going electric.",
     "Software-defined vehicles = a multi-year outsourcing tailwind.",
     "High return on capital with sticky, deep OEM relationships."],
    "Selling picks in the EV gold-rush"),
 "COFORGE": (2,"Coforge","IT Services","grw",
    ["Mid-cap IT growing well above the large-cap pack.",
     "Large deal wins give multi-year revenue visibility.",
     "Focused verticals (BFSI, travel) deepen domain moats."],
    "Where IT growth actually is"),
 "SHRIRAMFIN": (2,"Shriram Finance","NBFC","peg",
    ["Vehicle-finance leader to India's used-truck and MSME economy.",
     "Merged entity cross-sells across a huge, underbanked base.",
     "Cheap valuation for a 30%+ profit-growth lender."],
    "Deep-value lending growth"),
 "CHOLAFIN": (2,"Cholamandalam Finance","NBFC","grw",
    ["Murugappa-group NBFC compounding AUM across vehicle + home + SME.",
     "Consistent underwriting through cycles builds trust and scale.",
     "New businesses (CSEL, SBPL) extend the growth runway."],
    "A serial NBFC compounder"),
 "MAXHEALTH": (2,"Max Healthcare","Hospitals","grw",
    ["Premium hospital network doubling bed capacity by decade-end.",
     "Best-in-class occupancy and revenue-per-bed economics.",
     "Health-insurance penetration expands the paying pool."],
    "Beds = a multi-year growth pipeline"),
 "APOLLOHOSP": (2,"Apollo Hospitals","Hospitals + Digital","grw",
    ["India's hospital brand plus a fast-growing pharmacy + digital arm.",
     "24|7 digital platform is a scaling, separately-valued option.",
     "Aging demographics + insurance = durable demand."],
    "Healthcare, offline and online"),
 "PHOENIXLTD": (2,"Phoenix Mills","Retail Realty","grw",
    ["India's premier mall developer riding consumption + premiumisation.",
     "New malls across cities add rental income year after year.",
     "Annuity rental model + retail recovery = compounding cash."],
    "Owning the premium high-street"),
 "BRIGADE": (2,"Brigade Enterprises","Realty","peg",
    ["South-India developer with strong pre-sales momentum.",
     "Residential upcycle + annuity offices/hotels diversify income.",
     "Reasonable valuation for the pre-sales growth on offer."],
    "The real-estate upcycle, cheaply"),
 "CAMS": (2,"CAMS","Capital-Market Infra","roce",
    ["Duopoly registrar to India's booming mutual-fund industry.",
     "SIP + financialisation of savings drive recurring, asset-linked fees.",
     "Elite ROCE, asset-light — a toll-booth on rising AUM."],
    "A toll-booth on India's SIP boom"),
 "CDSL": (2,"CDSL","Depository","roce",
    ["Duopoly depository earning fees on every demat account + trade.",
     "Retail-investor explosion keeps adding accounts structurally.",
     "Asset-light, high-margin, near-monopoly economics."],
    "The demat monopoly of a rising market"),
 "BSE": (2,"BSE Ltd","Exchange","grw",
    ["Derivatives revival + Star MF + colocation drive a profit surge.",
     "Operating leverage: volumes grow far faster than costs.",
     "A structural play on India's financialisation."],
    "The exchange in the right cycle"),
 "LUPIN": (2,"Lupin","Pharma","peg",
    ["A genuine turnaround: US complex generics + inhalation pipeline.",
     "India branded business + margin recovery drive the re-rating.",
     "Cheap on growth (low PEG) if the recovery holds."],
    "Turnaround at a turnaround price"),

 # ================= TIER 3 — HIGH RISK / HIGH REWARD =================
 "ZENTEC": (3,"Zen Technologies","Defence (Small-cap)","grw",
    ["Defence-training simulators + anti-drone systems in a hot niche.",
     "Order book visibility high, but lumpy government contracts add risk.",
     "Small-cap volatility — position sizing matters."],
    "High-torque defence small-cap"),
 "ASTRAMICRO": (3,"Astra Microwave","Defence Electronics","grw",
    ["RF/microwave sub-systems for radars and missiles.",
     "Rides indigenisation, but is exposed to defence order timing.",
     "50%+ growth with the risk profile of a lumpy order book."],
    "A leveraged defence-electronics bet"),
 "KAYNES": (3,"Kaynes Technology","Semiconductors / EMS","grw",
    ["EMS + a bet on India's OSAT semiconductor assembly build-out.",
     "Hyper-growth, but the valuation prices in flawless execution.",
     "Semiconductor capex is long-gestation and capital-hungry."],
    "The semiconductor moonshot"),
 "COCHINSHIP": (3,"Cochin Shipyard","Defence Shipbuilding","grw",
    ["Warship + submarine build and repair for the navy's expansion.",
     "Multi-decade naval capex, but revenue is milestone-lumpy.",
     "PSU shipbuilder — execution and margin swings are the risk."],
    "Naval capex, in bursts"),
 "TITAGARH": (3,"Titagarh Rail Systems","Railways","grw",
    ["Wagons + metro/Vande Bharat trainsets in a railway capex boom.",
     "Order pipeline strong; execution ramp is the swing factor.",
     "Cyclical exposure to government ordering."],
    "Riding the railway capex wave"),
 "VEDL": (3,"Vedanta","Metals / Resources","roe",
    ["Diversified metals + energy cash-cow at a low P/E, high yield.",
     "Demerger could unlock value across the commodity verticals.",
     "Commodity cyclicality + parent leverage are real risks."],
    "Deep-cyclical value with a catalyst"),
 "HINDZINC": (3,"Hindustan Zinc","Zinc + Silver","roe",
    ["Near-monopoly zinc producer with elite margins and dividends.",
     "The world's largest silver play as the metal's demand tightens.",
     "Commodity-price and promoter-overhang risk cap the multiple."],
    "A silver/zinc cash machine"),
 "NUVAMA": (3,"Nuvama Wealth","Wealth Management","peg",
    ["Wealth + capital-markets play on India's rising affluence.",
     "Fast AUM growth at a low valuation — but market-cycle sensitive.",
     "Earnings swing with capital-market activity."],
    "Financialisation, geared to the cycle"),
 "POLICYBZR": (3,"PB Fintech (Policybazaar)","Fintech","grw",
    ["India's largest online insurance + credit marketplace.",
     "Newly profitable, with insurance penetration still very low.",
     "Valuation rich; profitability path must keep delivering."],
    "Newly-profitable fintech optionality"),
 "COROMANDEL": (3,"Coromandel International","Agri-Inputs","roce",
    ["Fertiliser + crop-protection leader with a strong distribution moat.",
     "Backward integration and a Nano-DAP/specialty pivot add growth.",
     "Subsidy policy + monsoon swings are the cyclical risks."],
    "Agri-inputs with a quality tilt"),
 "FORTIS": (3,"Fortis Healthcare","Hospitals (Turnaround)","grw",
    ["Turnaround hospital chain plus a growing diagnostics arm.",
     "Occupancy + margin recovery still has a long way to run.",
     "Execution and governance-legacy risks temper the upside."],
    "A hospital recovery story"),
 "MEDANTA": (3,"Global Health (Medanta)","Hospitals","grw",
    ["High-acuity quaternary-care network in North/East India.",
     "New hospitals ramp occupancy — strong incremental economics.",
     "Capacity build-out means near-term margin lumpiness."],
    "Premium care, scaling up"),
 "NTPC": (3,"NTPC","Power / Energy","pe",
    ["Cheap power giant adding thermal, renewables and nuclear capacity.",
     "NTPC Green listing highlights a large clean-energy option.",
     "Regulated returns = stability; energy-transition = the upside."],
    "Old-economy value, new-energy call"),
 "TATAPOWER": (3,"Tata Power","Energy Transition","grw",
    ["Integrated play: generation, distribution, solar + EV charging.",
     "Rooftop solar and manufacturing ride the clean-energy shift.",
     "Capex-heavy transition carries execution and funding risk."],
    "A one-stop energy-transition bet"),
 "RADICO": (3,"Radico Khaitan","Premium Spirits","grw",
    ["Premiumisation of Indian spirits lifts mix and margins.",
     "Own brands (Magic Moments, Rampur) scale the P&L up-market.",
     "Input-cost and state-excise swings add volatility."],
    "Premiumisation in a glass"),
 "MOTILALOFS": (3,"Motilal Oswal","Broking + AMC","grw",
    ["Broking + asset + wealth + PE — geared to buoyant markets.",
     "Rising treasury and AMC book compound in an up-cycle.",
     "Earnings are highly sensitive to market direction."],
    "A high-beta financialisation play"),
}

order = list(E.keys())
picks = []
missing = []
for t in order:
    fp = F / f"{t}.json"
    if not fp.exists():
        missing.append(t); continue
    d = load(t)
    if d.get("pe") is None:
        missing.append(t); continue
    tier, name, sector, hero, thesis, take = E[t]
    sg = d.get("sales_growth", {}); pg = d.get("profit_growth", {})
    sg5 = g(sg, "5 Years", "3 Years"); pg5 = g(pg, "5 Years", "3 Years")
    is_fin = t in FIN
    pe, roe, roce, mc = d.get("pe"), d.get("roe_pct"), d.get("roce_pct"), d.get("market_cap_cr")
    # metric rows (label, value, key)
    rows = [("P / E", f"{pe:.1f}" if pe else "—", "pe"),
            ("ROE", pct(roe), "roe")]
    if not is_fin:
        rows.append(("ROCE", pct(roce), "roce"))
    rows.append(("5Y sales CAGR", pct(sg5), "sg"))
    rows.append(("5Y profit CAGR", pct(pg5), "pg"))
    rows.append(("Market cap", cap_fmt(mc), "mc"))
    def is_hero(k, kk):
        if hero == "peg": return k == "P / E"
        if hero == "grw": return kk == "pg"
        return kk == hero
    metrics = [{"k": k, "v": v, "hero": is_hero(k, kk)} for (k, v, kk) in rows]
    # growth number for the alpha chart (blended, clamped)
    gv = [x for x in (sg5, pg5) if isinstance(x, (int, float))]
    growth = max(6, min(45, sum(gv) / len(gv))) if gv else 16
    picks.append({"ticker": t, "name": name, "sector": sector, "tier": str(tier),
                  "cap": cap_class(mc), "metrics": metrics, "thesis": thesis,
                  "take": take, "growth": round(growth, 1)})

json.dump(picks, open(ROOT / "picks.json", "w"), indent=1)
n1 = sum(1 for p in picks if p["tier"] == "1"); n2 = sum(1 for p in picks if p["tier"] == "2"); n3 = sum(1 for p in picks if p["tier"] == "3")
print(f"picks.json: {len(picks)} total  (T1={n1} T2={n2} T3={n3})")
if missing: print("MISSING DATA (excluded):", missing)
