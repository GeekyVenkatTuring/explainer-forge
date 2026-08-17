#!/usr/bin/env python3
"""YouTube metadata + thumbnail generator for the Telugu finance video library.

Single source of truth: VIDEOS list below (file, folder, YouTube title/description/tags,
thumbnail props). Emits:
  - <OUT>/_YOUTUBE_METADATA.md   (title/description/tags per video)
  - <OUT>/_thumbnails/<name>.png (1280x720 thumbnail per video, via remotion still)
  - organizes MP4s into subfolders.

Run:  python3 generate.py            (metadata + thumbnails + organize)
      python3 generate.py --meta     (metadata only)
"""
import json, os, subprocess, sys, shutil

OUT = os.path.expanduser("~/Downloads/generated_videos")
COMPOSER = os.path.expanduser("~/Developer/explainer-forge/composer")
THUMBS = os.path.join(OUT, "_thumbnails")
CC = "#22D3EE"; UP = "#34D399"; DOWN = "#FB7185"; MONEY = "#FBBF24"; DERIV = "#A78BFA"; MKT = "#22D3EE"

# Base tags reused across a series (YouTube allows ~500 chars of tags)
CC_TAGS = ["credit card telugu", "credit card in telugu", "క్రెడిట్ కార్డ్", "credit card explained telugu",
           "personal finance telugu", "telugu finance", "CIBIL score telugu", "credit card india"]
SM_TAGS = ["stock market telugu", "stock market for beginners telugu", "స్టాక్ మార్కెట్", "share market telugu",
           "telugu finance", "investing telugu", "mutual funds telugu", "stock market india"]

def V(file, folder, title, desc, tags, thumb):
    return {"file": file, "folder": folder, "title": title, "desc": desc, "tags": tags, "thumb": thumb}

def th(badge, title, sub, accent, hook, hookSmall="", ep=""):
    return {"badge": badge, "title": title, "sub": sub, "accent": accent, "hook": hook, "hookSmall": hookSmall, "ep": ep}

DISC = "⚠️ ఇది విద్య, విశ్లేషణ కోసమే — పెట్టుబడి సలహా కాదు. మీ నిర్ణయాలకు SEBI రిజిస్టర్డ్ సలహాదారును సంప్రదించండి."
DISC_CC = "⚠️ ఇది విద్యా ప్రయోజనం కోసమే — ఆర్థిక సలహా కాదు."
SUBSCRIBE = "👍 నచ్చితే లైక్ చేయండి, ఛానెల్‌ను సబ్‌స్క్రైబ్ చేయండి. 🔔"

def desc(hook, covers, series_line, disc, tags_line):
    return f"{hook}\n\n📌 ఈ వీడియోలో:\n{covers}\n\n{series_line}\n\n{disc}\n{SUBSCRIBE}\n\n{tags_line}"

CCH = "#CreditCard #Telugu #PersonalFinance #CIBIL #తెలుగు"
SMH = "#StockMarket #Telugu #Investing #ShareMarket #MutualFunds #తెలుగు"

CC_SERIES = "📚 క్రెడిట్ కార్డ్ పూర్తి కోర్సు (తెలుగు) — ప్లేలిస్ట్‌లో అన్ని ఛాప్టర్లు చూడండి."
SM_SERIES = "📚 స్టాక్ మార్కెట్ పూర్తి కోర్సు (తెలుగు) — 21 ఛాప్టర్లు, సున్నా నుండి. ప్లేలిస్ట్ చూడండి."

VIDEOS = [
 # ================= CREDIT CARDS =================
 V("credit-cards-telugu-ch01.mp4", "credit-cards-telugu",
   "క్రెడిట్ కార్డ్ అంటే ఏమిటి? | Credit Card Basics in Telugu | Ep 1",
   desc("క్రెడిట్ కార్డ్ అంటే ఏమిటి? ఎలా పనిచేస్తుంది? డెబిట్, UPI కంటే ఎలా భిన్నం?",
        "• క్రెడిట్ కార్డ్ అంటే ఏమిటి\n• క్రెడిట్ vs డెబిట్ vs UPI\n• కార్డ్‌పై ఏముంటుంది\n• స్వైప్ వెనుక ఏం జరుగుతుంది", CC_SERIES, DISC_CC,
        "#CreditCardBasics " + CCH),
   CC_TAGS + ["what is credit card", "credit vs debit", "credit card basics"],
   th("క్రెడిట్ కార్డ్", "క్రెడిట్ కార్డ్\nఅంటే ఏమిటి?", "అర్థం · ఉపయోగం · తేడాలు", CC, "01", "బేసిక్స్", "PART 01")),
 V("credit-cards-telugu-ch02.mp4", "credit-cards-telugu",
   "బిల్లింగ్ సైకిల్, వడ్డీ & గ్రేస్ పీరియడ్ | Credit Card Interest Telugu | Ep 2",
   desc("బిల్లింగ్ సైకిల్, వడ్డీ లేని గ్రేస్ పీరియడ్, మినిమం డ్యూ ఉచ్చు — పూర్తి వివరణ.",
        "• బిల్లింగ్ సైకిల్\n• గ్రేస్ పీరియడ్ (వడ్డీ లేని రోజులు)\n• మినిమం డ్యూ ఉచ్చు\n• 45% వడ్డీ, ఫీజులు", CC_SERIES, DISC_CC,
        "#CreditCardInterest " + CCH),
   CC_TAGS + ["credit card interest telugu", "grace period", "minimum due trap", "billing cycle"],
   th("క్రెడిట్ కార్డ్", "వడ్డీ &\nగ్రేస్ పీరియడ్", "బిల్లింగ్ సైకిల్ · ఫీజులు", MONEY, "45%", "వడ్డీ ఉచ్చు", "PART 02")),
 V("credit-cards-telugu-ch03.mp4", "credit-cards-telugu",
   "CIBIL క్రెడిట్ స్కోర్ ఎలా పెంచాలి? | Credit Score Telugu | Ep 3",
   desc("CIBIL స్కోర్ అంటే ఏమిటి? యుటిలైజేషన్ 30% రూల్, మొదటి కార్డ్ ఎలా పొందాలి?",
        "• CIBIL స్కోర్ (300–900)\n• క్రెడిట్ యుటిలైజేషన్ 30% రూల్\n• స్కోర్ నిర్ణయించే అంశాలు\n• మొదటి కార్డ్", CC_SERIES, DISC_CC,
        "#CIBILScore " + CCH),
   CC_TAGS + ["cibil score telugu", "credit score telugu", "how to increase cibil", "credit utilization"],
   th("క్రెడిట్ కార్డ్", "CIBIL స్కోర్\nపెంచడం", "యుటిలైజేషన్ · మొదటి కార్డ్", DERIV, "750+", "మంచి స్కోర్", "PART 03")),
 V("credit-cards-telugu-ch04.mp4", "credit-cards-telugu",
   "క్రెడిట్ కార్డ్ రివార్డ్స్ & నో-కాస్ట్ EMI నిజం | Credit Card Rewards Telugu | Ep 4",
   desc("రివార్డ్స్, క్యాష్‌బ్యాక్, నో-కాస్ట్ EMI అసలు నిజం, మంచి అలవాట్లు.",
        "• రివార్డ్స్ & క్యాష్‌బ్యాక్\n• నో-కాస్ట్ EMI నిజం\n• పెర్క్‌లు (లాంజ్, బీమా)\n• మంచి అలవాట్లు", CC_SERIES, DISC_CC,
        "#CreditCardRewards " + CCH),
   CC_TAGS + ["credit card rewards telugu", "no cost emi", "cashback", "credit card benefits"],
   th("క్రెడిట్ కార్డ్", "రివార్డ్స్ &\nEMI నిజం", "క్యాష్‌బ్యాక్ · పెర్క్‌లు", UP, "💳", "లాభాలు", "PART 04")),
 V("credit-cards-telugu-ch05.mp4", "credit-cards-telugu",
   "అప్పు ఉచ్చు నుండి బయటపడటం | Credit Card Debt Trap Telugu | Ep 5",
   desc("మినిమం డ్యూ ఉచ్చు, డెట్ స్పైరల్, తప్పులు — వాటి నుండి ఎలా బయటపడాలి.",
        "• డెట్ స్పైరల్ ఎలా మొదలవుతుంది\n• మినిమం డ్యూ ఉచ్చు\n• సాధారణ తప్పులు\n• బయటపడే మార్గం", CC_SERIES, DISC_CC,
        "#DebtTrap " + CCH),
   CC_TAGS + ["credit card debt telugu", "debt trap", "minimum due trap", "escape debt"],
   th("క్రెడిట్ కార్డ్", "అప్పు ఉచ్చు\nనుండి బయట", "డెట్ స్పైరల్ · పరిష్కారం", DOWN, "⚠️", "జాగ్రత్త", "PART 05")),
 V("credit-cards-telugu-ch06.mp4", "credit-cards-telugu",
   "సరైన క్రెడిట్ కార్డ్ ఎలా ఎంచుకోవాలి? | Choose Best Credit Card Telugu | Ep 6",
   desc("బ్యాంక్ vs ఫిన్‌టెక్ కార్డులు, మీకు సరైన కార్డ్ ఎలా ఎంచుకోవాలి.",
        "• బ్యాంక్ కార్డులు\n• ఫిన్‌టెక్ కార్డులు\n• ఎంపిక చెక్‌లిస్ట్\n• పూర్తి రీక్యాప్", CC_SERIES, DISC_CC,
        "#ChooseCreditCard " + CCH),
   CC_TAGS + ["best credit card telugu", "choose credit card", "bank vs fintech card"],
   th("క్రెడిట్ కార్డ్", "సరైన కార్డ్\nఎంపిక", "బ్యాంక్ vs ఫిన్‌టెక్", CC, "✓", "ఎంపిక", "PART 06")),
 V("credit-cards-telugu-ch07-card-reviews.mp4", "credit-cards-telugu",
   "టాప్ క్రెడిట్ కార్డుల రివ్యూ | Best Credit Cards India Telugu | Bonus",
   desc("భారత్‌లో టాప్ క్రెడిట్ కార్డుల పోలిక, ఎవరికి ఏది సరిపోతుంది.",
        "• టాప్ కార్డుల రివ్యూ\n• ఫీచర్లు, ఫీజుల పోలిక\n• ఎవరికి ఏ కార్డ్", CC_SERIES, DISC_CC,
        "#CreditCardReview " + CCH),
   CC_TAGS + ["best credit cards india", "credit card review telugu", "credit card comparison"],
   th("బోనస్", "టాప్ కార్డుల\nరివ్యూ", "పోలిక · ఎవరికి ఏది", MONEY, "⭐", "రివ్యూ", "BONUS")),
 V("credit-cards-telugu-ch08-cibil-masterclass.mp4", "credit-cards-telugu",
   "CIBIL స్కోర్ మాస్టర్‌క్లాస్ | CIBIL Score Full Guide Telugu | Bonus",
   desc("CIBIL స్కోర్ బ్యాండ్‌లు, పెంచే మార్గాలు, తప్పులు — పూర్తి మాస్టర్‌క్లాస్.",
        "• స్కోర్ బ్యాండ్‌లు\n• స్కోర్ పెంచే 5 మార్గాలు\n• తప్పులు సరిదిద్దడం", CC_SERIES, DISC_CC,
        "#CIBILMasterclass " + CCH),
   CC_TAGS + ["cibil masterclass", "cibil score bands", "improve credit score telugu"],
   th("బోనస్", "CIBIL\nమాస్టర్‌క్లాస్", "బ్యాండ్‌లు · పెంచే మార్గాలు", DERIV, "900", "గరిష్ఠం", "BONUS")),
 V("credit-cards-telugu-ch09-escape-debt.mp4", "credit-cards-telugu",
   "క్రెడిట్ కార్డ్ అప్పు ఎలా తీర్చాలి? | Escape Credit Card Debt Telugu | Bonus",
   desc("అప్పు తీర్చే వ్యూహాలు — స్నోబాల్, అవలాంచ్, బ్యాలెన్స్ ట్రాన్స్‌ఫర్.",
        "• అప్పు తీర్చే వ్యూహాలు\n• స్నోబాల్ vs అవలాంచ్\n• ఆచరణ ప్రణాళిక", CC_SERIES, DISC_CC,
        "#EscapeDebt " + CCH),
   CC_TAGS + ["escape credit card debt", "pay off debt telugu", "debt free"],
   th("బోనస్", "అప్పు ఎలా\nతీర్చాలి?", "స్నోబాల్ · అవలాంచ్", UP, "0", "అప్పు లేని", "BONUS")),
 V("credit-cards-telugu-ch10-rewards-masterclass.mp4", "credit-cards-telugu",
   "రివార్డ్స్ మాస్టర్‌క్లాస్ | Maximize Credit Card Rewards Telugu | Bonus",
   desc("రివార్డ్స్‌ను గరిష్ఠంగా పొందడం, పాయింట్ల విలువ, రిడీమ్ చేయడం.",
        "• రివార్డ్స్ గరిష్ఠీకరణ\n• పాయింట్ల విలువ\n• కేటగిరీ మ్యాచింగ్", CC_SERIES, DISC_CC,
        "#RewardsMasterclass " + CCH),
   CC_TAGS + ["credit card rewards maximize", "reward points telugu"],
   th("బోనస్", "రివార్డ్స్\nమాస్టర్‌క్లాస్", "గరిష్ఠ లాభం", UP, "₹", "క్యాష్‌బ్యాక్", "BONUS")),
 V("credit-cards-telugu-ch11-cc-vs-loan-vs-bnpl.mp4", "credit-cards-telugu",
   "క్రెడిట్ కార్డ్ vs పర్సనల్ లోన్ vs BNPL | Telugu | Bonus",
   desc("క్రెడిట్ కార్డ్, పర్సనల్ లోన్, BNPL — ఏది ఎప్పుడు మంచిది?",
        "• మూడింటి పోలిక\n• వడ్డీ, రిస్క్\n• ఏది ఎప్పుడు", CC_SERIES, DISC_CC,
        "#BNPL " + CCH),
   CC_TAGS + ["credit card vs personal loan", "bnpl telugu", "buy now pay later"],
   th("బోనస్", "కార్డ్ vs లోన్\nvs BNPL", "ఏది ఎప్పుడు?", CC, "VS", "పోలిక", "BONUS")),
 V("credit-cards-telugu-ch12-safety-fraud.mp4", "credit-cards-telugu",
   "క్రెడిట్ కార్డ్ ఫ్రాడ్ & భద్రత | Credit Card Safety Telugu | Bonus",
   desc("కార్డ్ మోసాలు, OTP స్కామ్‌లు, భద్రత నియమాలు, ఫిర్యాదు ఎలా చేయాలి.",
        "• కార్డ్ మోసాల రకాలు\n• 5 భద్రత నియమాలు\n• ఫిర్యాదు (1930)", CC_SERIES, DISC_CC,
        "#CreditCardSafety " + CCH),
   CC_TAGS + ["credit card fraud telugu", "card safety", "otp scam"],
   th("బోనస్", "ఫ్రాడ్ &\nభద్రత", "స్కామ్‌లు · రక్షణ", DOWN, "🛡️", "జాగ్రత్త", "BONUS")),
 V("credit-cards-telugu-ch13-festival-balance-transfer.mp4", "credit-cards-telugu",
   "పండుగ షాపింగ్ & బ్యాలెన్స్ ట్రాన్స్‌ఫర్ | Telugu | Bonus",
   desc("పండుగ సీజన్ స్మార్ట్ షాపింగ్, బ్యాలెన్స్ ట్రాన్స్‌ఫర్ ఎలా వాడాలి.",
        "• పండుగ షాపింగ్ 5 నియమాలు\n• బ్యాలెన్స్ ట్రాన్స్‌ఫర్\n• స్మార్ట్ ఖర్చు", CC_SERIES, DISC_CC,
        "#BalanceTransfer " + CCH),
   CC_TAGS + ["balance transfer telugu", "festival shopping", "no cost emi festival"],
   th("బోనస్", "పండుగ &\nబ్యాలెన్స్ ట్రాన్స్‌ఫర్", "స్మార్ట్ ఖర్చు", MONEY, "🎁", "ఆఫర్‌లు", "BONUS")),
 V("credit-cards-telugu-FULL.mp4", "credit-cards-telugu",
   "క్రెడిట్ కార్డ్ పూర్తి కోర్సు (తెలుగు) | Complete Credit Card Course Telugu",
   desc("క్రెడిట్ కార్డ్ — అర్థం నుండి మాస్టరీ వరకు. పూర్తి కోర్సు ఒకే వీడియోలో.",
        "• అన్ని ఛాప్టర్లు ఒకే చోట\n• బేసిక్స్ నుండి అడ్వాన్స్‌డ్\n• CIBIL, రివార్డ్స్, భద్రత", CC_SERIES, DISC_CC,
        "#CreditCardCourse " + CCH),
   CC_TAGS + ["credit card full course telugu", "credit card complete guide"],
   th("పూర్తి కోర్సు", "క్రెడిట్ కార్డ్\nA to Z", "అర్థం · ఉపయోగం · భద్రత", CC, "13", "ఛాప్టర్లు", "FULL")),

 # ================= STOCK MARKET — COURSE =================
 V("stock-market-telugu-ch01-basics.mp4", "stock-market-telugu/course",
   "స్టాక్ మార్కెట్ బేసిక్స్ | Stock Market for Beginners Telugu | Ep 1",
   desc("షేర్ అంటే ఏమిటి? IPO, NSE, BSE, SEBI, సెన్సెక్స్, నిఫ్టీ — సున్నా నుండి.",
        "• షేర్ అంటే ఏమిటి\n• IPO, NSE, BSE, SEBI\n• ధర ఎందుకు మారుతుంది\n• సెన్సెక్స్, నిఫ్టీ", SM_SERIES, DISC,
        "#StockMarketBasics " + SMH),
   SM_TAGS + ["what is share market telugu", "stock market basics", "sensex nifty telugu"],
   th("స్టాక్ మార్కెట్", "షేర్ అంటే\nఏమిటి?", "IPO · NSE · SEBI · Nifty", UP, "01", "బేసిక్స్", "PART 01")),
 V("stock-market-telugu-ch02-first-steps.mp4", "stock-market-telugu/course",
   "డీమ్యాట్ ఖాతా & మొదటి ఆర్డర్ | Open Demat Account Telugu | Ep 2",
   desc("డీమ్యాట్, ట్రేడింగ్ ఖాతా, KYC, బ్రోకర్ ఎంపిక, మొదటి ఆర్డర్ ఎలా పెట్టాలి.",
        "• 3 ఖాతాలు (బ్యాంక్/ట్రేడింగ్/డీమ్యాట్)\n• KYC\n• బ్రోకర్ ఎంపిక\n• మొదటి ఆర్డర్, T+1", SM_SERIES, DISC,
        "#DematAccount " + SMH),
   SM_TAGS + ["demat account telugu", "how to buy shares telugu", "zerodha groww telugu"],
   th("స్టాక్ మార్కెట్", "మొదటి\nఅడుగు", "డీమ్యాట్ · బ్రోకర్ · ఆర్డర్", MKT, "02", "ఖాతా", "PART 02")),
 V("stock-market-telugu-ch03-equity-investing.mp4", "stock-market-telugu/course",
   "ఈక్విటీ పెట్టుబడి & కాంపౌండింగ్ | Equity Investing Telugu | Ep 3",
   desc("కాంపౌండింగ్ మహిమ, కంపెనీని కొలిచే కొలతలు, డైవర్సిఫికేషన్.",
        "• కాంపౌండింగ్\n• మార్కెట్ క్యాప్, PE\n• లార్జ్/మిడ్/స్మాల్ క్యాప్\n• డైవర్సిఫికేషన్", SM_SERIES, DISC,
        "#EquityInvesting " + SMH),
   SM_TAGS + ["equity investing telugu", "compounding telugu", "how to pick stocks telugu"],
   th("స్టాక్ మార్కెట్", "ఈక్విటీ\nపెట్టుబడి", "కాంపౌండింగ్ · ఎంపిక", UP, "03", "సంపద", "PART 03")),
 V("stock-market-telugu-ch04-mutual-funds.mp4", "stock-market-telugu/course",
   "మ్యూచువల్ ఫండ్స్ & SIP | Mutual Funds SIP Telugu | Ep 4",
   desc("మ్యూచువల్ ఫండ్ అంటే ఏమిటి? NAV, ఫండ్ రకాలు, SIP రూపీ-కాస్ట్ యావరేజింగ్.",
        "• మ్యూచువల్ ఫండ్\n• NAV\n• ఈక్విటీ/డెట్/హైబ్రిడ్\n• SIP మ్యాజిక్", SM_SERIES, DISC,
        "#MutualFunds " + SMH),
   SM_TAGS + ["mutual funds telugu", "sip telugu", "best mutual funds telugu"],
   th("స్టాక్ మార్కెట్", "మ్యూచువల్\nఫండ్స్ & SIP", "NAV · రకాలు · SIP", UP, "SIP", "₹500+", "PART 04")),
 V("stock-market-telugu-ch05-funds-deep-dive.mp4", "stock-market-telugu/course",
   "ఎక్స్‌పెన్స్ రేషియో, డైరెక్ట్ ప్లాన్, ELSS | Mutual Funds Deep Dive Telugu | Ep 5",
   desc("ఎక్స్‌పెన్స్ రేషియో, డైరెక్ట్ vs రెగ్యులర్, ELSS పన్ను ఆదా, ఫండ్ ఎంపిక.",
        "• ఎక్స్‌పెన్స్ రేషియో\n• డైరెక్ట్ vs రెగ్యులర్\n• ELSS 80C\n• ఫండ్ ఎంపిక", SM_SERIES, DISC,
        "#DirectMutualFund " + SMH),
   SM_TAGS + ["direct mutual fund telugu", "elss telugu", "expense ratio"],
   th("స్టాక్ మార్కెట్", "ఫండ్స్\nలోతుగా", "డైరెక్ట్ · ELSS · ఖర్చు", MONEY, "05", "పన్ను ఆదా", "PART 05")),
 V("stock-market-telugu-ch06-index-etf.mp4", "stock-market-telugu/course",
   "ఇండెక్స్ ఫండ్స్ & ETF | Index Funds ETF Telugu | Ep 6",
   desc("ఇండెక్స్ ఫండ్, ETF అంటే ఏమిటి? యాక్టివ్ vs పాసివ్, ఏది ఎప్పుడు.",
        "• ఇండెక్స్ ఫండ్\n• ETF\n• యాక్టివ్ vs పాసివ్\n• ఎంపిక చెక్‌లిస్ట్", SM_SERIES, DISC,
        "#IndexFunds " + SMH),
   SM_TAGS + ["index fund telugu", "etf telugu", "nifty 50 index fund"],
   th("స్టాక్ మార్కెట్", "ఇండెక్స్\n& ETF", "పాసివ్ · చౌక · సింపుల్", MKT, "06", "0.2% ఖర్చు", "PART 06")),
 V("stock-market-telugu-ch07-intraday.mp4", "stock-market-telugu/course",
   "ఇంట్రాడే ట్రేడింగ్ నిజాలు | Intraday Trading Truth Telugu | Ep 7",
   desc("ఇంట్రాడే అంటే ఏమిటి? క్యాండిల్ చార్ట్, మార్జిన్, SEBI 71% నష్టం నిజం.",
        "• ఇంట్రాడే అంటే\n• క్యాండిల్ చార్ట్\n• లివరేజ్ రిస్క్\n• SEBI: 71% నష్టం", SM_SERIES, DISC,
        "#IntradayTrading " + SMH),
   SM_TAGS + ["intraday trading telugu", "candlestick telugu", "day trading telugu"],
   th("స్టాక్ మార్కెట్", "ఇంట్రాడే\nనిజాలు", "చార్ట్ · రిస్క్ · నిజం", DERIV, "71%", "నష్టం (SEBI)", "PART 07")),
 V("stock-market-telugu-ch08-futures.mp4", "stock-market-telugu/course",
   "ఫ్యూచర్స్ ట్రేడింగ్ | Futures Trading Telugu | Ep 8",
   desc("ఫ్యూచర్స్ అంటే ఏమిటి? లాట్ సైజు, మార్జిన్, లివరేజ్, హెడ్జింగ్.",
        "• ఫార్వర్డ్ → ఫ్యూచర్స్\n• లాట్, ఎక్స్పైరీ\n• మార్జిన్, లివరేజ్\n• హెడ్జర్ vs స్పెక్యులేటర్", SM_SERIES, DISC,
        "#FuturesTrading " + SMH),
   SM_TAGS + ["futures trading telugu", "f&o telugu", "leverage telugu"],
   th("స్టాక్ మార్కెట్", "ఫ్యూచర్స్", "లాట్ · మార్జిన్ · లివరేజ్", DERIV, "10x", "లివరేజ్", "PART 08")),
 V("stock-market-telugu-ch09-options-basics.mp4", "stock-market-telugu/course",
   "ఆప్షన్స్ బేసిక్స్ — కాల్ & పుట్ | Options Basics Telugu | Ep 9",
   desc("ఆప్షన్స్ అంటే ఏమిటి? కాల్, పుట్, స్ట్రైక్, ప్రీమియం, పేఆఫ్ చిత్రం.",
        "• ఆప్షన్ = బీమా\n• కాల్ & పుట్\n• స్ట్రైక్, ప్రీమియం\n• పేఆఫ్ డయాగ్రామ్", SM_SERIES, DISC,
        "#OptionsTrading " + SMH),
   SM_TAGS + ["options trading telugu", "call put telugu", "options for beginners telugu"],
   th("స్టాక్ మార్కెట్", "ఆప్షన్స్\nబేసిక్స్", "కాల్ · పుట్ · ప్రీమియం", DERIV, "09", "కాల్/పుట్", "PART 09")),
 V("stock-market-telugu-ch10-options-reality.mp4", "stock-market-telugu/course",
   "ఆప్షన్స్ నిజాలు & SEBI 91% నష్టం | Options Reality Telugu | Ep 10",
   desc("టైమ్ డికే, SEBI F&O 91% నష్టం అధ్యయనం, నియంత్రణలు — అసలు నిజం.",
        "• టైమ్ డికే (థీటా)\n• SEBI: 91% F&O నష్టం\n• SEBI కళ్లాలు\n• F&O ఎవరికి", SM_SERIES, DISC,
        "#FnOLoss " + SMH),
   SM_TAGS + ["options reality telugu", "f&o loss sebi", "time decay telugu"],
   th("స్టాక్ మార్కెట్", "ఆప్షన్స్\nనిజాలు", "టైమ్ డికే · SEBI డేటా", DOWN, "91%", "F&O నష్టం", "PART 10")),
 V("stock-market-telugu-ch11-tax-charges.mp4", "stock-market-telugu/course",
   "స్టాక్ మార్కెట్ పన్నులు & ఛార్జీలు | Capital Gains Tax Telugu | Ep 11",
   desc("STCG 20%, LTCG 12.5%, ₹1.25L మినహాయింపు, STT, అన్ని ఛార్జీలు — 2026.",
        "• STCG 20% / LTCG 12.5%\n• ₹1.25L మినహాయింపు\n• STT 2026\n• ఛార్జీల గోపురం", SM_SERIES, DISC,
        "#CapitalGainsTax " + SMH),
   SM_TAGS + ["capital gains tax telugu", "ltcg stcg telugu", "stock market tax india"],
   th("స్టాక్ మార్కెట్", "పన్నులు &\nఛార్జీలు", "STCG · LTCG · STT", MONEY, "12.5%", "LTCG 2026", "PART 11")),
 V("stock-market-telugu-ch12-portfolio-roadmap.mp4", "stock-market-telugu/course",
   "పోర్ట్‌ఫోలియో & పెట్టుబడి రోడ్‌మ్యాప్ | Portfolio Telugu | Ep 12",
   desc("పునాది (అత్యవసర నిధి, బీమా), అసెట్ కేటాయింపు, మోసాల రక్షణ, రోడ్‌మ్యాప్.",
        "• పునాది మెట్లు\n• అసెట్ కేటాయింపు\n• మోసాల రక్షణ\n• 5-అడుగుల రోడ్‌మ్యాప్", SM_SERIES, DISC,
        "#Portfolio " + SMH),
   SM_TAGS + ["portfolio telugu", "asset allocation telugu", "investment roadmap"],
   th("స్టాక్ మార్కెట్", "పోర్ట్‌ఫోలియో\nరోడ్‌మ్యాప్", "పునాది · కేటాయింపు", UP, "🧭", "ప్రణాళిక", "PART 12")),
 V("stock-market-telugu-ch13-ipo-masterclass.mp4", "stock-market-telugu/course",
   "IPO మాస్టర్‌క్లాస్ | IPO Guide Telugu | Ep 13",
   desc("IPO అంటే ఏమిటి? దరఖాస్తు, అలాట్‌మెంట్, ఉచ్చుల నుండి తప్పించుకోవడం.",
        "• IPO ప్రక్రియ\n• దరఖాస్తు చెక్‌లిస్ట్\n• అపోహలు\n• లిస్టింగ్", SM_SERIES, DISC,
        "#IPO " + SMH),
   SM_TAGS + ["ipo telugu", "how to apply ipo telugu", "ipo allotment"],
   th("స్టాక్ మార్కెట్", "IPO\nమాస్టర్‌క్లాస్", "దరఖాస్తు · అలాట్‌మెంట్", MKT, "IPO", "పూర్తి గైడ్", "PART 13")),
 V("stock-market-telugu-ch14-psychology.mp4", "stock-market-telugu/course",
   "పెట్టుబడి మనస్తత్వం | Investor Psychology Telugu | Ep 14",
   desc("మెదడు ఆడే 4 ట్రిక్కులు, భయం-దురాశ చక్రం, క్రమశిక్షణ అలవాట్లు.",
        "• 4 బయాస్‌లు (FOMO...)\n• భయం-దురాశ చక్రం\n• 5 క్రమశిక్షణ అలవాట్లు", SM_SERIES, DISC,
        "#InvestorPsychology " + SMH),
   SM_TAGS + ["investor psychology telugu", "trading psychology telugu", "fomo investing"],
   th("స్టాక్ మార్కెట్", "పెట్టుబడి\nమనస్తత్వం", "బయాస్ · భయం · దురాశ", DERIV, "🧠", "EQ ఆట", "PART 14")),
 V("stock-market-telugu-ch15-fundamental-analysis.mp4", "stock-market-telugu/course",
   "కంపెనీని ఎలా చదవాలి? | Fundamental Analysis Telugu | Ep 15",
   desc("బాలెన్స్ షీట్, P&L, క్యాష్ ఫ్లో, ROE, PE, మోట్ — సింపుల్‌గా.",
        "• 3 ఫైనాన్షియల్ స్టేట్‌మెంట్లు\n• ROE, Debt/Equity, PE\n• గొప్ప కంపెనీ 5 లక్షణాలు", SM_SERIES, DISC,
        "#FundamentalAnalysis " + SMH),
   SM_TAGS + ["fundamental analysis telugu", "how to read balance sheet telugu", "roe pe ratio"],
   th("స్టాక్ మార్కెట్", "కంపెనీని\nచదవడం", "బాలెన్స్ షీట్ · ROE · PE", MKT, "15", "అనాలిసిస్", "PART 15")),
 V("stock-market-telugu-ch16-gold-reits-bonds.mp4", "stock-market-telugu/course",
   "గోల్డ్ ETF, REITs, బాండ్లు | Gold REITs Bonds Telugu | Ep 16",
   desc("బంగారం (గోల్డ్ ETF), REIT, ప్రభుత్వ/కార్పొరేట్ బాండ్లు — పూర్తి చిత్రం.",
        "• గోల్డ్ ETF vs నగలు\n• REIT (రియల్ ఎస్టేట్)\n• బాండ్లు\n• పూర్తి పోర్ట్‌ఫోలియో", SM_SERIES, DISC,
        "#GoldETF " + SMH),
   SM_TAGS + ["gold etf telugu", "reit telugu", "bonds telugu"],
   th("స్టాక్ మార్కెట్", "గోల్డ్ · REIT\n· బాండ్లు", "ఈక్విటీకి ఆవల", MONEY, "16", "వైవిధ్యం", "PART 16")),
 V("stock-market-telugu-ch17-technical-analysis.mp4", "stock-market-telugu/course",
   "టెక్నికల్ అనాలిసిస్ బేసిక్స్ | Technical Analysis Telugu | Ep 17",
   desc("ట్రెండ్, సపోర్ట్-రెసిస్టెన్స్, వాల్యూమ్, మూవింగ్ యావరేజ్ — ప్రాథమికాలు.",
        "• ట్రెండ్\n• సపోర్ట్ & రెసిస్టెన్స్\n• వాల్యూమ్\n• మూవింగ్ యావరేజ్", SM_SERIES, DISC,
        "#TechnicalAnalysis " + SMH),
   SM_TAGS + ["technical analysis telugu", "chart analysis telugu", "support resistance"],
   th("స్టాక్ మార్కెట్", "టెక్నికల్\nఅనాలిసిస్", "ట్రెండ్ · సపోర్ట్ · MA", UP, "17", "చార్ట్‌లు", "PART 17")),
 V("stock-market-telugu-ch18-goal-planning.mp4", "stock-market-telugu/course",
   "లక్ష్యాల ఆధారిత ప్రణాళిక | Goal Based Planning Telugu | Ep 18",
   desc("లక్ష్యాలను కాలం వారీగా, రిటైర్మెంట్ లెక్క, ఆలస్యానికి ధర.",
        "• 0–3 / 3–7 / 7+ ఏళ్ల బకెట్లు\n• రిటైర్మెంట్ లెక్క\n• ప్రణాళిక 5 నియమాలు", SM_SERIES, DISC,
        "#GoalPlanning " + SMH),
   SM_TAGS + ["goal based investing telugu", "retirement planning telugu", "financial planning"],
   th("స్టాక్ మార్కెట్", "లక్ష్యాల\nప్రణాళిక", "బకెట్లు · రిటైర్మెంట్", UP, "18", "ప్లానింగ్", "PART 18")),
 V("stock-market-telugu-ch19-retirement.mp4", "stock-market-telugu/course",
   "EPF, PPF, NPS vs ఈక్విటీ | Retirement Planning Telugu | Ep 19",
   desc("EPF, PPF, NPS ఎలా పనిచేస్తాయి? స్థిర వడ్డీ vs ఈక్విటీ, రిటైర్మెంట్ మిక్స్.",
        "• EPF · PPF · NPS\n• స్థిర వడ్డీ ఎందుకు సరిపోదు\n• రిటైర్మెంట్ కేటాయింపు", SM_SERIES, DISC,
        "#Retirement " + SMH),
   SM_TAGS + ["epf ppf nps telugu", "retirement planning telugu", "nps telugu"],
   th("స్టాక్ మార్కెట్", "రిటైర్మెంట్\nసాధనాలు", "EPF · PPF · NPS", MONEY, "19", "పెన్షన్", "PART 19")),
 V("stock-market-telugu-ch20-results-dividends.mp4", "stock-market-telugu/course",
   "క్వార్టర్లీ రిజల్ట్స్ & డివిడెండ్లు | Results Dividends Telugu | Ep 20",
   desc("Q1 ఫలితాలు ఎలా చదవాలి? రెవెన్యూ, మార్జిన్, గైడెన్స్, డివిడెండ్ ఈల్డ్.",
        "• 4 కీలక అంకెలు\n• మంచి ఫలితం ≠ షేర్ పెరుగుదల\n• డివిడెండ్ ఈల్డ్", SM_SERIES, DISC,
        "#QuarterlyResults " + SMH),
   SM_TAGS + ["quarterly results telugu", "dividend telugu", "how to read results"],
   th("స్టాక్ మార్కెట్", "రిజల్ట్స్ &\nడివిడెండ్లు", "రెవెన్యూ · మార్జిన్ · ఈల్డ్", UP, "20", "ఫలితాలు", "PART 20")),
 V("stock-market-telugu-ch21-faq.mp4", "stock-market-telugu/course",
   "కొత్తవారి 15 ప్రశ్నలు | Stock Market FAQ Telugu | Ep 21",
   desc("కొత్త పెట్టుబడిదారుల టాప్ ప్రశ్నలకు సూటి జవాబులు + మొదటి ఏడాది సిలబస్.",
        "• డబ్బు, ప్రాసెస్ ప్రశ్నలు\n• బ్రోకర్ మునిగితే?\n• మొదటి ఏడాది ప్లాన్", SM_SERIES, DISC,
        "#StockMarketFAQ " + SMH),
   SM_TAGS + ["stock market faq telugu", "beginner questions telugu"],
   th("స్టాక్ మార్కెట్", "కొత్తవారి\nప్రశ్నలు", "15 FAQ · మొదటి ఏడాది", MKT, "FAQ", "సందేహాలు", "PART 21")),
 V("stock-market-telugu-FULL.mp4", "stock-market-telugu/course",
   "స్టాక్ మార్కెట్ పూర్తి కోర్సు (తెలుగు) | Complete Stock Market Course Telugu",
   desc("స్టాక్ మార్కెట్ — సున్నా నుండి పూర్తిగా. 21 ఛాప్టర్లు ఒకే వీడియోలో (~82 నిమి).",
        "• షేర్లు, MF, ETF, F&O\n• పన్నులు, పోర్ట్‌ఫోలియో\n• బోనస్ మాస్టర్‌క్లాస్‌లు", SM_SERIES, DISC,
        "#StockMarketCourse " + SMH),
   SM_TAGS + ["stock market full course telugu", "share market complete course telugu"],
   th("పూర్తి కోర్సు", "స్టాక్ మార్కెట్\nA to Z", "షేర్లు · MF · F&O · ETF", UP, "21", "ఛాప్టర్లు", "FULL")),

 # ================= STOCK MARKET — UPDATES / TOPICAL =================
 V("stock-market-telugu-strategies-2026-part1.mp4", "stock-market-telugu/updates",
   "2026 కొత్త పెట్టుబడి వ్యూహాలు | New Investing Strategies Telugu | Part 1",
   desc("SEBI 2026 కొత్త ఫండ్ రూల్స్, కోర్-శాటిలైట్, మొమెంటమ్, ₹1.25L పన్ను ఆదా.",
        "• SEBI true-to-label రూల్స్\n• కోర్-శాటిలైట్ 70/30\n• మొమెంటమ్ ఫండ్స్\n• టాక్స్ హార్వెస్టింగ్", SM_SERIES, DISC,
        "#InvestingStrategy #SEBI " + SMH),
   SM_TAGS + ["investing strategy 2026 telugu", "sebi new rules 2026", "momentum investing telugu"],
   th("2026 వ్యూహాలు", "కొత్త\nవ్యూహాలు", "SEBI రూల్స్ · మొమెంటమ్", UP, "2026", "అప్‌డేట్", "PART 1")),
 V("stock-market-telugu-strategies-2026-part2.mp4", "stock-market-telugu/updates",
   "Zerodha, Groww, Upstox లో వ్యూహాలు అమలు | Implement Strategies Telugu | Part 2",
   desc("SIP సెటప్, బ్రోకర్ పోలిక, smallcase మొమెంటమ్, టాక్స్ హార్వెస్టింగ్, SIF.",
        "• 4-అడుగుల SIP\n• Zerodha/Groww/Upstox పోలిక\n• smallcase\n• టాక్స్ హార్వెస్టింగ్, SIF", SM_SERIES, DISC,
        "#Zerodha #Groww " + SMH),
   SM_TAGS + ["zerodha groww upstox telugu", "smallcase telugu", "how to invest telugu"],
   th("2026 వ్యూహాలు", "ఎలా అమలు\nచేయాలి", "Zerodha · Groww · Upstox", MKT, "SIP", "స్టెప్-బై-స్టెప్", "PART 2")),
 V("stock-market-telugu-ipo-guide-2026.mp4", "stock-market-telugu/updates",
   "2026 IPO గైడ్ — Jio & అలాట్‌మెంట్ లాటరీ | IPO Guide Telugu",
   desc("2026 IPO క్యాలెండర్, Reliance Jio, దరఖాస్తు, అలాట్‌మెంట్ లాటరీ నిజం.",
        "• IPO క్యాలెండర్ + మెగా పైప్‌లైన్\n• Reliance Jio\n• దరఖాస్తు 4 అడుగులు\n• లాటరీ ఎలా పనిచేస్తుంది", SM_SERIES, DISC,
        "#IPO #RelianceJio " + SMH),
   SM_TAGS + ["ipo 2026 telugu", "reliance jio ipo telugu", "ipo allotment telugu"],
   th("IPO స్పెషల్", "2026 IPO\nగైడ్", "Jio · లాటరీ · అలాట్‌మెంట్", DERIV, "Jio", "మెగా IPO", "2026")),
 V("stock-market-telugu-expert-strategies-2026.mp4", "stock-market-telugu/updates",
   "నిపుణులు ఏం చెబుతున్నారు? | Top Investors Strategy Telugu 2026",
   desc("Samir Arora, Saurabh Mukherjea, Nilesh Shah, Deepak Shenoy — వారి వ్యూహాలు.",
        "• Arora: ఎలిమినేషన్\n• Mukherjea: క్వాలిటీ లార్జ్ క్యాప్\n• Nilesh Shah: అసెట్ అలొకేషన్\n• Shenoy: రూల్స్", SM_SERIES, DISC,
        "#Investing #SaurabhMukherjea " + SMH),
   SM_TAGS + ["saurabh mukherjea telugu", "samir arora telugu", "expert strategy telugu"],
   th("నిపుణుల వ్యూహాలు", "నిపుణులు ఏం\nచెబుతున్నారు?", "Arora · Mukherjea · Shah", DERIV, "4", "టాప్ వాయిస్‌లు", "2026")),
 V("stock-market-telugu-market-wrap-20jul2026.mp4", "stock-market-telugu/updates",
   "మార్కెట్ ఎందుకు పడింది? | Market Wrap 20 July 2026 Telugu",
   desc("సెన్సెక్స్ −443, నిఫ్టీ −96 — HDFC/Axis మార్జిన్ మిస్, క్రూడ్ $90, 10 షేర్లు.",
        "• సెన్సెక్స్/నిఫ్టీ ముగింపు\n• పతనానికి 3 కారణాలు\n• పడిన/పెరిగిన 10 షేర్లు\n• NIM పాఠం", "📊 రోజువారీ మార్కెట్ అప్‌డేట్ కోసం సబ్‌స్క్రైబ్ చేయండి.", DISC,
        "#MarketWrap #Nifty #Sensex " + SMH),
   SM_TAGS + ["market wrap telugu", "why nifty fell today", "sensex today telugu"],
   th("మార్కెట్ అప్‌డేట్", "మార్కెట్ ఎందుకు\nపడింది?", "20 జూలై · బ్యాంక్ మార్జిన్", DOWN, "−443", "సెన్సెక్స్", "20 JUL")),
 V("stock-market-telugu-premarket-21jul2026.mp4", "stock-market-telugu/updates",
   "రేపటి ప్రీ-మార్కెట్ వాచ్‌లిస్ట్ | Pre-Market 21 July 2026 Telugu",
   desc("రేపటి ఓపెనింగ్ సెటప్, లార్జ్/మిడ్/స్మాల్ క్యాప్ ఫోకస్ షేర్లు, గోల్డ్ థీమ్.",
        "• GIFT Nifty, క్రూడ్, ఎక్స్పైరీ\n• లార్జ్ క్యాప్ ఫోకస్\n• గోల్డ్/జ్యువెలరీ థీమ్\n• ఇది వాచ్‌లిస్ట్, జోస్యం కాదు", "📊 రోజువారీ ప్రీ-మార్కెట్ కోసం సబ్‌స్క్రైబ్ చేయండి.", DISC,
        "#PreMarket #StocksToWatch " + SMH),
   SM_TAGS + ["pre market telugu", "stocks to watch tomorrow telugu", "gift nifty telugu"],
   th("ప్రీ-మార్కెట్", "రేపటి\nవాచ్‌లిస్ట్", "లార్జ్ · మిడ్ · స్మాల్ క్యాప్", MONEY, "21", "జూలై", "WATCH")),
 V("stock-market-telugu-ipo-listing-21jul2026.mp4", "stock-market-telugu/updates",
   "SBI MF & Millworks IPO లిస్టింగ్ | IPO Listing 21 July 2026 Telugu",
   desc("SBI మ్యూచువల్ ఫండ్ & Millworks SME లిస్టింగ్ సెంటిమెంట్, GMP, ఎగ్జిట్ స్ట్రాటజీ.",
        "• SBI MF: 41.66x · GMP ~18%\n• Millworks SME: 219x · GMP ~90%\n• GMP నిజం\n• ఎగ్జిట్ స్ట్రాటజీ", "📊 IPO అప్‌డేట్ల కోసం సబ్‌స్క్రైబ్ చేయండి.", DISC,
        "#IPOListing #SBIMutualFund " + SMH),
   SM_TAGS + ["sbi mutual fund ipo telugu", "ipo listing telugu", "ipo gmp telugu"],
   th("IPO లిస్టింగ్", "SBI MF &\nMillworks", "సెంటిమెంట్ · GMP · ఎగ్జిట్", DERIV, "GMP", "18% / 90%", "21 JUL")),
]

def emit_metadata():
    lines = ["# 📺 YouTube Metadata — Telugu Finance Video Library",
             "", f"Total: {len(VIDEOS)} videos. Generated for upload. Copy-paste per video.",
             "", "> For finance videos, keep the disclaimer in the description (YouTube + compliance).", ""]
    by_folder = {}
    for v in VIDEOS:
        by_folder.setdefault(v["folder"], []).append(v)
    for folder in ["credit-cards-telugu", "stock-market-telugu/course", "stock-market-telugu/updates"]:
        vs = by_folder.get(folder, [])
        lines.append(f"\n---\n## 📁 {folder}  ({len(vs)} videos)\n")
        for v in vs:
            tags = ", ".join(dict.fromkeys(v["tags"]))  # dedupe, keep order
            lines += [f"### 🎬 `{v['file']}`", "",
                      f"**Title:**  {v['title']}", "",
                      "**Description:**", "```", v["desc"], "```",
                      f"**Tags:** `{tags}`", "",
                      f"**Thumbnail:** `_thumbnails/{v['file'].replace('.mp4','.png')}`", ""]
    open(os.path.join(OUT, "_YOUTUBE_METADATA.md"), "w").write("\n".join(lines))
    print(f"Wrote _YOUTUBE_METADATA.md ({len(VIDEOS)} videos)")

def render_thumbs():
    os.makedirs(THUMBS, exist_ok=True)
    for v in VIDEOS:
        pj = os.path.join("/tmp", "thmb_" + v["file"].replace(".mp4", ".json"))
        json.dump(v["thumb"], open(pj, "w"), ensure_ascii=False)
        out = os.path.join(THUMBS, v["file"].replace(".mp4", ".png"))
        r = subprocess.run(["npx", "remotion", "still", "Thumbnail", out, f"--props={pj}", "--frame=0"],
                           cwd=COMPOSER, capture_output=True, text=True)
        print(f"  {'OK ' if os.path.exists(out) else 'ERR'} {os.path.basename(out)}")

def organize():
    for v in VIDEOS:
        dest = os.path.join(OUT, v["folder"])
        os.makedirs(dest, exist_ok=True)
        src = os.path.join(OUT, v["file"])
        if os.path.exists(src):
            shutil.move(src, os.path.join(dest, v["file"]))
    print("Organized MP4s into subfolders.")

if __name__ == "__main__":
    emit_metadata()
    if "--meta" not in sys.argv:
        render_thumbs()
        organize()
