#!/usr/bin/env python3
"""Chapter 5 — Part 5: Build your own trading bot from scratch (real code)."""
import aitcore as core

SEGMENTS = [
 ("s50_divider", "ait_divider",
  {"n": 5, "title": "Build Your Own", "sub": "From a first strategy to an AI agent", "color": "ai", "parts": 6},
  "Part five. Building your own, from scratch. [pause] We will go one box at a time, "
  "with real code on screen. You do not need to memorise it. You need to see the shape."),

 ("s51_arch", "ait_pipeline",
  {"kicker": "THE BLUEPRINT", "title": "Your bot is the six boxes, in code",
   "stages": [
     {"label": "Data", "sub": "yfinance / broker", "c": "data"},
     {"label": "Features", "sub": "pandas-ta", "c": "data"},
     {"label": "Model", "sub": "a rule, then ML", "c": "ai"},
     {"label": "Signal", "sub": "buy / sell / hold", "c": "edge"},
     {"label": "Risk", "sub": "position sizing", "c": "risk"},
     {"label": "Order", "sub": "broker API", "c": "money"}],
   "caption": "Same six boxes as part one — now each becomes a small, testable function."},
  "Remember the six boxes from part one? We are about to build every one of them in "
  "code. [pause] Data, we will pull with a free library. Features, we will compute with "
  "another. The model starts as a simple rule, and later becomes machine learning. "
  "[pause] The signal is buy, sell, or hold. Risk decides our position size. And the "
  "order goes out through a broker A P I. [pause] The beautiful part. Each box is just "
  "a small function you can test on its own. Build them one at a time, get each one "
  "right, and the whole system falls into place. Let's start with data."),

 ("s52_data", "ait_code",
  {"kicker": "BOX 1 · DATA", "title": "Get clean price data — for free", "file": "data.py", "color": "data",
   "lines": [
     "import yfinance as yf",
     "",
     "def get_data(symbol, period='5y'):",
     "    df = yf.download(symbol, period=period)",
     "    df = df.dropna()                 # remove gaps",
     "    return df",
     "",
     "# Indian stocks use the .NS suffix on NSE",
     "df = get_data('RELIANCE.NS')",
     "print(df.shape, df.index[-1])"],
   "side": {"title": "The rules of data", "points": ["Garbage in, garbage out — clean it first", "Use enough history: 3–5 years minimum", "Watch for splits and survivorship bias", "For live trading, use your broker's feed"]},
   "caption": "yfinance is free and perfect for learning; upgrade to your broker's data later."},
  "Box one. Data. [pause] This tiny function downloads five years of daily prices for a "
  "stock, and drops any missing rows. For Indian stocks, you add dot N S for the "
  "National Stock Exchange. [pause] The library here, yfinance, is free and perfect for "
  "learning. [pause] But respect the data. Garbage in, garbage out. Use at least three "
  "to five years of history so your bot sees more than one kind of market. Watch out "
  "for stock splits, and for survivorship bias, where dead companies quietly vanish "
  "from your data and flatter your results. [pause] When you go live, you will switch "
  "this one function to your broker's real time feed. Everything downstream stays the "
  "same."),

 ("s52b_clean", "ait_code",
  {"kicker": "BOX 1, DONE RIGHT", "title": "Clean data before you trust it", "file": "clean.py", "color": "data",
   "lines": [
     "def clean(df):",
     "    df = df[~df.index.duplicated()]   # drop dupes",
     "    df = df.sort_index()              # time order",
     "    df = df.ffill(limit=2)            # small gaps only",
     "    df = df.dropna()                  # then drop rest",
     "    # sanity: no zero or negative prices",
     "    df = df[df['Close'] > 0]",
     "    return df"],
   "side": {"title": "Cleaning checklist", "points": ["Remove duplicate timestamps", "Sort strictly by time", "Fill only tiny gaps — never invent data", "Reject impossible prices (0 or negative)"]},
   "caption": "Ninety percent of 'my bot is broken' turns out to be dirty data."},
  "Before features, one unglamorous step that separates amateurs from pros. Cleaning "
  "the data. [pause] Real data is messy. Duplicate timestamps, rows out of order, "
  "little gaps, and occasionally an impossible price. [pause] This function fixes the "
  "common problems. It removes duplicates, sorts by time, fills only tiny gaps, and "
  "rejects any price that is zero or negative. [pause] Notice the restraint. We fill "
  "only small gaps. We never invent large stretches of data. Made up data makes a made "
  "up backtest. [pause] I promise you this. Ninety percent of the times you will say my "
  "bot is broken, the real answer will be, my data was dirty. So clean it first, every "
  "time, and look at it with your own eyes."),

 ("s53_features", "ait_code",
  {"kicker": "BOX 2 · FEATURES", "title": "Turn raw prices into signals", "file": "features.py", "color": "data",
   "lines": [
     "import pandas_ta as ta",
     "",
     "def add_features(df):",
     "    df['rsi'] = ta.rsi(df['Close'], length=14)",
     "    df['sma_fast'] = ta.sma(df['Close'], 20)",
     "    df['sma_slow'] = ta.sma(df['Close'], 50)",
     "    df['ret'] = df['Close'].pct_change()",
     "    df['vol'] = df['ret'].rolling(20).std()",
     "    return df.dropna()"],
   "side": {"title": "What a feature is", "points": ["A number that describes the market now", "RSI: is it over-bought or over-sold?", "Two averages: is the trend up or down?", "Volatility: how wild is it right now?"]},
   "caption": "Features are how the market speaks to your model — choose them thoughtfully."},
  "Box two. Features. This is where you turn raw prices into meaningful numbers. [pause] "
  "A feature is just a number that describes the market right now. [pause] Here we add "
  "a few classics with the pandas T A library. The R S I tells us if a stock looks over "
  "bought or over sold. Two moving averages tell us the direction of the trend. And "
  "volatility tells us how wild things are. [pause] Features are how the market speaks "
  "to your model. Choose them with care, and with a reason. [pause] And a warning that "
  "will matter soon. Never build a feature using information from the future. It is the "
  "easiest way to fool yourself into a backtest that can never be repeated."),

 ("s53b_lookahead", "ait_code",
  {"kicker": "THE DEADLIEST BUG", "title": "Look-ahead bias: using the future by accident", "file": "danger.py", "color": "risk",
   "lines": [
     "# WRONG — this peeks at the future:",
     "df['sig'] = (df['Close'] > df['Close'].mean())",
     "#            ^ mean() uses ALL rows, incl. tomorrow",
     "",
     "# RIGHT — only use data available at that moment:",
     "roll = df['Close'].rolling(50).mean()",
     "df['sig'] = df['Close'] > roll   # past 50 days only",
     "",
     "# rule: at row t, touch nothing after row t"],
   "side": {"title": "Why it's deadly", "points": ["It makes any backtest look brilliant", "It passes tests, then fails live", "Rolling/expanding windows fix it", "Suspiciously perfect? Check for this first"]},
   "caption": "If a backtest looks too good, you almost certainly peeked at the future."},
  "Before we go further, meet the deadliest bug in all of trading code. Look ahead "
  "bias. [pause] It means accidentally using information from the future to make a "
  "decision in the past. [pause] Look at the wrong line. It compares today's price to "
  "the average of the whole series. But that average includes tomorrow, and next week. "
  "Your bot cannot know those yet. [pause] The right way uses a rolling window. Only the "
  "past fifty days. Data that truly existed at that moment. [pause] Here is the golden "
  "rule. At any row in time, touch nothing that comes after it. [pause] Why does this "
  "matter so much? Because look ahead bias makes a backtest look brilliant, then fail "
  "instantly live. So if your results ever look too perfect, hunt for this bug first. "
  "It is almost always the culprit."),

 ("s54_signal", "ait_code",
  {"kicker": "BOX 3 & 4 · MODEL → SIGNAL", "title": "The model, as a plain rule first", "file": "strategy.py", "color": "edge",
   "lines": [
     "def signal(df):",
     "    # start transparent: a moving-average crossover",
     "    long = df['sma_fast'] > df['sma_slow']",
     "    # +1 = enter long, -1 = exit, 0 = hold",
     "    return long.astype(int).diff().fillna(0)",
     "",
     "df['signal'] = signal(df)",
     "print(df['signal'].value_counts())"],
   "side": {"title": "Why start with a rule", "points": ["You can read and explain every trade", "It's a fair baseline to beat later", "SEBI calls this a white-box strategy", "Most 'AI bots' still end in a line like this"]},
   "caption": "Get a transparent rule working end-to-end before you add any AI."},
  "Boxes three and four. The model, and the signal it produces. [pause] We start "
  "transparent, with a plain rule. When the fast average crosses above the slow one, we "
  "go long. When it crosses back, we exit. [pause] The output is beautifully simple. "
  "Plus one to enter, minus one to exit, zero to hold. [pause] Why start with a rule "
  "instead of A I? Three reasons. You can read and explain every single trade. It gives "
  "you a fair baseline to beat later. And it is exactly what SEBI calls a white box "
  "strategy. [pause] Here is the secret the hype hides. Even the fanciest A I bot still "
  "ends in a line just like this one. A signal. Get this working end to end before you "
  "add any intelligence."),

 ("s55_backtest", "ait_code",
  {"kicker": "BOX 5 · THE BACKTEST", "title": "Test it on history — honestly", "file": "backtest.py", "color": "money",
   "lines": [
     "from backtesting import Backtest, Strategy",
     "",
     "class Cross(Strategy):",
     "    def next(self):",
     "        if self.data.signal[-1] == 1:",
     "            self.buy()",
     "        elif self.data.signal[-1] == -1:",
     "            self.position.close()",
     "",
     "bt = Backtest(df, Cross, commission=0.002)",
     "print(bt.run())   # returns, Sharpe, drawdown"],
   "side": {"title": "Backtest honestly", "points": ["Always include commission + slippage", "No peeking at future bars — ever", "A perfect equity curve is a red flag", "It's a hypothesis, not a guarantee"]},
   "caption": "Set commission realistically — a costless backtest is a fairy tale."},
  "Box five. The backtest. Now we replay history and see how the strategy would have "
  "done. [pause] The backtesting library steps through each day, and acts on our "
  "signal. Notice one thing. We set a commission. [pause] That is not optional. A "
  "backtest with no costs is a fairy tale, and part two showed you exactly why. [pause] "
  "When you run it, you get real numbers. Total return, the Sharpe ratio, the maximum "
  "drawdown. [pause] But please, hold this thought tightly. If your equity curve is a "
  "perfect, smooth line going up, that is not a triumph. It is a red flag. It almost "
  "always means you peeked at the future somewhere. A backtest is a hypothesis. It is "
  "never a guarantee."),

 ("s55b_read", "ait_code",
  {"kicker": "READING THE REPORT", "title": "What the backtest is actually telling you", "file": "report.py", "color": "money",
   "lines": [
     "stats = bt.run()",
     "print(stats['Return [%]'])        # total return",
     "print(stats['Sharpe Ratio'])      # return per risk",
     "print(stats['Max. Drawdown [%]']) # worst fall",
     "print(stats['# Trades'])          # sample size",
     "print(stats['Win Rate [%]'])      # % winners",
     "",
     "# few trades = luck. Thousands = costs matter."],
   "side": {"title": "Read it like a pro", "points": ["Ignore return; read risk first", "Under ~30 trades? It's noise, not signal", "High win rate can still lose to big losers", "One number never tells the story"]},
   "caption": "A beginner reads the return. A professional reads the drawdown and the trade count."},
  "When the backtest finishes, it hands you a report. Let's read it like a "
  "professional. [pause] The beginner looks straight at the total return. The pro looks "
  "at everything else first. [pause] The Sharpe ratio, return per unit of risk. The "
  "maximum drawdown, the worst fall you would have suffered. [pause] And crucially, the "
  "number of trades. If your strategy only made twenty trades, that is not a signal, it "
  "is luck. You need a healthy sample, ideally hundreds. [pause] Watch the win rate "
  "carefully too. A strategy can win seventy percent of the time and still lose money, "
  "if its rare losses are huge. [pause] No single number tells the story. Read them "
  "together, and be suspicious of anything that looks perfect."),

 ("s56_overfit_trap", "ait_callout",
  {"kicker": "THE TRAP, AGAIN", "color": "risk",
   "text": "Tuning until the backtest looks perfect is how you guarantee it fails live.",
   "sub": "Every knob you twist to fit the past is a promise the future won't keep."},
  "I have to stop you here, because this is where almost everyone destroys their bot. "
  "[pause] You will run that backtest, and you will want to tune it. Change the twenty "
  "to a twenty two. Add a filter. Tweak a threshold. Watch the return climb. It is "
  "intoxicating. [pause] But every knob you twist to fit the past is a promise the "
  "future will not keep. [pause] The more you optimise on one slice of history, the "
  "more you are just memorising its noise. You are not making the bot better. You are "
  "making it more confident and more wrong. [pause] So how do we test a strategy "
  "honestly, without fooling ourselves? There is one technique that saves you. It is "
  "called walk forward."),

 ("s57_walkforward", "ait_loop",
  {"kicker": "THE ANTIDOTE", "title": "Walk-forward: prove it on data it hasn't seen",
   "steps": [
     {"label": "Train window", "sub": "fit on months 1–12", "c": "data"},
     {"label": "Test window", "sub": "check months 13–15", "c": "edge"},
     {"label": "Record result", "sub": "unseen performance", "c": "ai"},
     {"label": "Roll forward", "sub": "shift the window", "c": "money"},
     {"label": "Repeat", "sub": "across all history", "c": "money"},
     {"label": "Judge honestly", "sub": "most ideas die here", "c": "risk"}],
   "caption": "If it survives many unseen windows, you may — may — have something real."},
  "Walk forward is the antidote to overfitting, and it is simple. [pause] You train "
  "your strategy on the first block of time, say twelve months. Then you test it on the "
  "next block it has never seen, say three months, and you record that result. [pause] "
  "Then you roll the whole window forward and do it again. And again, across all your "
  "history. [pause] Now you are judging the strategy only on data it did not train on. "
  "Over and over, in different market conditions. [pause] Here is the emotional part. "
  "Most of your beautiful ideas will die at this step. That is not failure. That is the "
  "system working. It just saved you real money. If a strategy survives many unseen "
  "windows, then, maybe, you have something real."),

 ("s57b_wfcode", "ait_code",
  {"kicker": "WALK-FORWARD IN CODE", "title": "The honesty test, as a loop", "file": "walkforward.py", "color": "ai",
   "lines": [
     "results = []",
     "for start in range(0, len(df) - WIN - TEST, TEST):",
     "    train = df[start : start + WIN]",
     "    test  = df[start + WIN : start + WIN + TEST]",
     "    params = optimise(train)      # fit on train",
     "    r = run(test, params)         # judge on UNSEEN",
     "    results.append(r)",
     "",
     "print('median out-of-sample:', median(results))"],
   "side": {"title": "The one honest number", "points": ["Optimise on train, score on test — never mix", "Roll the window across all history", "The median test result is your reality", "In-sample numbers are for the bin"]},
   "caption": "This tiny loop is the difference between fooling yourself and knowing the truth."},
  "Here is walk forward as actual code, because it is simpler than it sounds. [pause] "
  "You loop across time. In each step, you take a training window, and the test window "
  "right after it. [pause] You optimise your parameters on the training data. Then, "
  "critically, you score them on the test data the strategy has never seen. You record "
  "that result, and roll forward. [pause] At the end, you look at the median of all "
  "those out of sample results. [pause] That one number is your reality. Not the "
  "gorgeous in sample figure. The messy, honest, unseen one. [pause] This tiny loop is "
  "the single most important difference between a hobbyist who fools himself, and "
  "someone who actually knows whether their strategy works. Write it once, and use it "
  "on everything you ever build."),

 ("s58_metrics", "ait_stat",
  {"kicker": "WHAT “GOOD” LOOKS LIKE", "title": "Judge a strategy by these, not by returns", "color": "money",
   "stats": [
     {"value": 1.5, "prefix": "~", "decimals": 1, "label": "a realistic, durable Sharpe ratio", "src": "1 to 2 is genuinely good", "c": "money"},
     {"value": 20, "prefix": "< ", "suffix": "%", "label": "max drawdown you can stomach", "src": "size positions for the worst case", "c": "risk"},
     {"value": 1.5, "prefix": "> ", "decimals": 1, "label": "profit factor: gains over losses", "src": "above 1.5 is meaningful", "c": "edge"}],
   "note": "Anyone quoting a Sharpe of 8 is overfit, lying, or high-frequency — not you."},
  "So how do you know if a strategy is actually good? Not by the total return. That is "
  "the amateur's number. [pause] Professionals look at risk adjusted metrics. The "
  "Sharpe ratio measures return per unit of risk. A realistic, durable Sharpe is "
  "somewhere between one and two. [pause] Maximum drawdown is the worst peak to bottom "
  "fall. Know the number you can actually stomach, and size your bets for the worst "
  "case, not the best. [pause] Profit factor is your gross gains divided by gross "
  "losses. Above one and a half is meaningful. [pause] And a reality check. If anyone "
  "shows you a Sharpe ratio of eight, they are either overfit, lying, or a high "
  "frequency firm. None of which is you."),

 ("s58b_robust", "ait_cards",
  {"kicker": "STRESS-TEST IT", "title": "Four checks before you trust a strategy", "color": "money",
   "cards": [
     {"emoji": "🎚️", "title": "Parameter stability", "body": "Values near your best should work almost as well. A lone spike is luck.", "c": "data"},
     {"emoji": "🎲", "title": "Trade shuffling", "body": "Reorder the trades randomly; if the worst case ruins you, size smaller.", "c": "risk"},
     {"emoji": "📆", "title": "Different periods", "body": "Test bull, bear, and sideways markets separately.", "c": "edge"},
     {"emoji": "💸", "title": "Double the costs", "body": "If it dies when costs rise a little, the edge was never real.", "c": "money"}]},
  "Even after walk forward, run four stress tests before you trust a strategy with real "
  "money. [pause] One, parameter stability. If your best setting is twenty, then "
  "eighteen and twenty two should work almost as well. If only twenty works, you found "
  "luck, not an edge. [pause] Two, trade shuffling. Reorder your trades randomly many "
  "times. If the unluckiest ordering would blow up your account, you must size smaller. "
  "[pause] Three, different periods. Test it separately in bull markets, bear markets, "
  "and boring sideways ones. [pause] Four, double the trading costs and run it again. "
  "If a small rise in costs kills it, the edge was never really there. [pause] A "
  "strategy that survives all four is rare, and worth real attention."),

 ("s59_risk", "ait_code",
  {"kicker": "BOX 6 · RISK", "title": "The box that keeps you alive", "file": "risk.py", "color": "risk",
   "lines": [
     "def position_size(capital, price, stop_pct):",
     "    # risk only 1% of capital per trade",
     "    risk_rupees = capital * 0.01",
     "    risk_per_share = price * stop_pct",
     "    qty = risk_rupees / risk_per_share",
     "    return int(qty)",
     "",
     "# ₹5,00,000 capital, ₹2,500 price, 3% stop",
     "print(position_size(500000, 2500, 0.03))  # -> 66"],
   "side": {"title": "Why this box wins", "points": ["Caps the damage of any single trade", "Turns a stop-loss into a share count", "Survival first — returns are secondary", "This is what pros obsess over"]},
   "caption": "You can be wrong most of the time and still win — if this box is right."},
  "Box six. Risk. This is the box that actually keeps you in the game. [pause] This "
  "function does one job. It decides how many shares to buy so that a single trade can "
  "only lose one percent of your capital. [pause] You give it your capital, the price, "
  "and where your stop loss sits. It hands back a safe quantity. [pause] In the "
  "example, half a million rupees of capital, a stock at twenty five hundred, a three "
  "percent stop, gives you sixty six shares. [pause] This looks boring. It is the most "
  "important code in the whole bot. [pause] Get this right, and you can be wrong on "
  "most of your trades and still come out ahead. Get it wrong, and one bad day ends "
  "your account. Survival first. Returns second."),

 ("s5a_execution", "ait_code",
  {"kicker": "GOING LIVE · CAREFULLY", "title": "The order box — paper first, always", "file": "execute.py", "color": "money",
   "lines": [
     "# same code path for paper AND live —",
     "# only the credentials change",
     "def place(kite, symbol, qty, side):",
     "    return kite.place_order(",
     "        tradingsymbol=symbol,",
     "        transaction_type=side,   # BUY / SELL",
     "        quantity=qty,",
     "        product='CNC', order_type='MARKET')",
     "",
     "# run for WEEKS on paper before this touches money"],
   "side": {"title": "The going-live ladder", "points": ["1 — Backtest passes walk-forward", "2 — Paper trade for weeks", "3 — Go live with tiny size", "4 — Scale only what survives"]},
   "caption": "The jump from paper to live is where discipline, not code, decides your fate."},
  "The final box. The order. This is the code that talks to your broker. [pause] Notice "
  "something important. The exact same code runs for paper trading and for live "
  "trading. Only the credentials change. [pause] That is deliberate. It means what you "
  "tested is exactly what you run. [pause] But do not rush through this door. Follow "
  "the ladder. First, your backtest survives walk forward. Then you paper trade for "
  "weeks. Then you go live with a tiny size, real money but small enough that a total "
  "loss would not hurt. And only then do you scale up what keeps working. [pause] The "
  "jump from paper to live is not a coding problem. It is a discipline problem. That is "
  "where most people quietly break their own rules."),

 ("s5a2_monitor", "ait_code",
  {"kicker": "KEEPING IT ALIVE", "title": "A live bot needs a babysitter", "file": "run_live.py", "color": "data",
   "lines": [
     "import schedule, logging",
     "logging.basicConfig(filename='bot.log', level=20)",
     "",
     "def tick():",
     "    df = get_live_data()",
     "    sig = signal(add_features(df))",
     "    if sig.iloc[-1] != 0:",
     "        place_order(sig.iloc[-1])",
     "    logging.info(f'checked {df.index[-1]}')",
     "",
     "schedule.every().day.at('09:20').do(tick)"],
   "side": {"title": "Non-negotiables for live", "points": ["Log every decision — you'll need the trail", "A kill-switch you can hit instantly", "Alerts when it errors or loses too much", "Handle a dropped connection gracefully"]},
   "caption": "A live strategy that no one is watching is an accident waiting to happen."},
  "Once your bot goes live, it needs a babysitter. Real markets are messy. [pause] This "
  "sketch schedules the bot to wake up each morning, check the market, and act on its "
  "signal. But notice the logging. [pause] Log every single decision. When something "
  "goes wrong at three in the afternoon, that trail is how you find out why. [pause] "
  "Four things are non negotiable for live trading. A log of every decision. A kill "
  "switch you can hit instantly to stop everything. Alerts when the bot errors, or "
  "loses more than expected. And graceful handling of a dropped internet connection, "
  "because it will happen. [pause] A live strategy that nobody is watching is not "
  "passive income. It is an accident waiting to happen. Treat it like a machine on a "
  "factory floor."),

 ("s5b_ml", "ait_code",
  {"kicker": "NOW ADD THE AI", "title": "Swap the rule for a machine-learning model", "file": "ml_model.py", "color": "ai",
   "lines": [
     "from xgboost import XGBClassifier",
     "",
     "feats = ['rsi', 'sma_fast', 'sma_slow', 'vol']",
     "# target: did price rise over the next 5 days?",
     "y = (df['Close'].shift(-5) > df['Close']).astype(int)",
     "",
     "model = XGBClassifier(max_depth=3)   # keep it simple",
     "model.fit(df[feats][:-5], y[:-5])",
     "df['ml_signal'] = model.predict(df[feats])"],
   "side": {"title": "The AI upgrade", "points": ["The model now sets the rule, from data", "Same six boxes — only box 3 changed", "Shallow models beat deep ones here", "More power = more ways to overfit"]},
   "caption": "AI doesn't replace the pipeline — it just makes the model box smarter, and riskier."},
  "Finally, the moment you have been waiting for. Adding the A I. [pause] Instead of "
  "writing the rule ourselves, we let a model learn it from data. Here we use X G "
  "Boost, a powerful and popular model. [pause] We hand it our features, and a target. "
  "In this case, did the price rise over the next five days? The model learns the "
  "patterns that connect them. [pause] And here is the payoff of our whole design. Only "
  "box three changed. The model. Data, features, risk, execution, all untouched. That "
  "is the power of the pipeline. [pause] Two warnings. Keep the model shallow. Simple "
  "models survive live markets far better than deep ones. And remember, more power just "
  "means more ways to overfit. The A I made box three smarter, and riskier."),

 ("s5b2_leakage", "ait_code",
  {"kicker": "THE ML TRAP", "title": "How machine learning fools you", "file": "validate_ml.py", "color": "risk",
   "lines": [
     "# WRONG — shuffling time series leaks the future",
     "# train_test_split(X, y, shuffle=True)   # never!",
     "",
     "# RIGHT — split by TIME, train on the past only",
     "cut = int(len(df) * 0.7)",
     "X_tr, X_te = X[:cut], X[cut:]",
     "y_tr, y_te = y[:cut], y[cut:]",
     "model.fit(X_tr, y_tr)",
     "print('honest accuracy:', model.score(X_te, y_te))"],
   "side": {"title": "ML-specific dangers", "points": ["Never shuffle a time series when splitting", "Scale features using train stats only", "55% accuracy can be great; 99% is a bug", "Predicting price is hard; predicting cost isn't"]},
   "caption": "Most ML trading tutorials leak the future. Split by time, or you're lying to yourself."},
  "Machine learning has its own special way of fooling you, so let's inoculate you. "
  "[pause] Most tutorials split their data randomly. For normal problems that is fine. "
  "For time series, it is a disaster. Random shuffling lets the model peek at the "
  "future. [pause] The right way splits strictly by time. Train on the past, test on "
  "the future. Never the other way around. [pause] Two more traps. When you scale your "
  "features, compute the scaling from the training data only. And keep your "
  "expectations sane. In markets, fifty five percent accuracy can be genuinely "
  "excellent. If you ever see ninety nine percent, that is not genius. That is a bug, "
  "or leakage. [pause] The A I did not break the rules of part two. It just gave you "
  "fancier ways to break them yourself."),

 ("s5b3_sentiment", "ait_code",
  {"kicker": "LLMs, PRACTICALLY", "title": "Use an LLM to read the news", "file": "sentiment.py", "color": "ai",
   "lines": [
     "# ask an LLM to score a headline, -1 to +1",
     "prompt = f'''Rate the market sentiment of this",
     "headline from -1 (very bearish) to +1 (very",
     "bullish). Reply with only a number.",
     "Headline: {headline}'''",
     "",
     "score = float(llm(prompt).strip())",
     "df.loc[date, 'news_score'] = score",
     "# now news_score is just another feature"],
   "side": {"title": "The realistic LLM job", "points": ["Great at reading tone at scale", "Feed the score in as one more feature", "Watch for look-ahead: use the publish time", "It's an analyst, not an oracle"]},
   "caption": "The honest LLM use isn't 'predict the price' — it's 'read 10,000 headlines for me'."},
  "So where does a language model realistically fit? Reading. [pause] Look at this. We "
  "ask the model to score a news headline, from minus one for very bearish, to plus one "
  "for very bullish. It replies with a number. [pause] And now, that sentiment score is "
  "simply another feature. It flows into the exact same pipeline as your R S I and your "
  "moving averages. [pause] This is the honest, practical use of an L L M in trading. "
  "Not predict the price. That it cannot do. But read ten thousand headlines and gauge "
  "the mood, at a scale no human could match. [pause] Two cautions. Mind the timing. "
  "Use the moment the news was actually published, or you reintroduce look ahead bias. "
  "And treat the model as a tireless junior analyst, not an oracle."),

 ("s5c_agents", "ait_orbit",
  {"kicker": "THE FRONTIER · AGENTS", "title": "Where LLM agents fit — honestly", "hub": {"emoji": "🧠", "label": "Agent systems", "c": "ai"},
   "items": [
     {"emoji": "🔬", "label": "FinRL", "sub": "reinforcement learning", "c": "money"},
     {"emoji": "💬", "label": "FinGPT", "sub": "finance-tuned LLM", "c": "data"},
     {"emoji": "🗣️", "label": "TradingAgents", "sub": "a team of LLMs debating", "c": "edge"},
     {"emoji": "📰", "label": "LLM sentiment", "sub": "read news at scale", "c": "ai"},
     {"emoji": "⚠️", "label": "Reality", "sub": "research-grade, not ATMs", "c": "risk"}]},
  "And now the true frontier. A I agents. [pause] These are open source projects worth "
  "knowing by name. FinRL lets you train reinforcement learning agents. FinGPT is a "
  "language model tuned for finance. [pause] The most exciting is a project called "
  "Trading Agents. It runs a whole team of language models that act like a real desk. "
  "One is a researcher, one a risk manager, one a trader. They debate a decision, then "
  "act. [pause] The most practical use today is reading. Point a language model at "
  "thousands of news stories and let it summarise the mood at a scale no human can "
  "match. [pause] But be clear eyed. These are research grade tools, not money "
  "machines. They are brilliant, expensive, and absolutely not guaranteed to profit."),

 ("s5e_portfolio", "ait_cards",
  {"kicker": "DON'T BET ON ONE HORSE", "title": "Run a portfolio of strategies", "color": "money",
   "cards": [
     {"emoji": "🎯", "title": "One bot is fragile", "body": "When its single edge fades, your whole account fades with it.", "c": "risk"},
     {"emoji": "🧺", "title": "Several uncorrelated bots", "body": "When one struggles, another may thrive — smoother overall.", "c": "money"},
     {"emoji": "🔀", "title": "Different ideas, not copies", "body": "Momentum, mean-reversion, and trend behave differently.", "c": "data"},
     {"emoji": "⚖️", "title": "Allocate by conviction", "body": "More capital to the proven ones; keep the rest small.", "c": "edge"}]},
  "Here is how experienced traders think about the whole picture. Do not bet everything "
  "on one bot. [pause] A single strategy is fragile. It has one edge, and when that edge "
  "fades, and it will, your entire account fades with it. [pause] Instead, run a "
  "portfolio of several strategies that behave differently. When one struggles, another "
  "may be thriving, and your overall ride gets much smoother. [pause] The key word is "
  "uncorrelated. Different ideas, not copies of the same idea. A momentum bot, a mean "
  "reversion bot, and a trend bot react to different markets. [pause] Then allocate by "
  "conviction. More capital to the strategies that have proven themselves, and keep the "
  "unproven ones small. [pause] Diversification is the closest thing to a free lunch "
  "that markets offer."),

 ("s5f_retire", "ait_callout",
  {"kicker": "KNOW WHEN TO STOP", "color": "risk",
   "text": "Every strategy dies. The skill is retiring it before it takes your capital with it.",
   "sub": "Decide the shutdown rule in advance, when you're calm — not mid-drawdown."},
  "One last hard truth about building. Every strategy eventually dies. [pause] Edges "
  "decay. Markets change. The bot that printed money last year may quietly stop "
  "working. [pause] So the real skill is not just building a strategy. It is retiring "
  "one before it takes your capital down with it. [pause] Here is the discipline. "
  "Decide your shutdown rule in advance, while you are calm. For example, if the live "
  "results fall far outside what the backtest ever showed, or the drawdown crosses a "
  "line you set, the bot stops. Automatically. No debate. [pause] Deciding this mid "
  "drawdown, in a panic, is how people ride a dying strategy all the way to zero. Write "
  "the exit rule on day one, when your judgement is clear."),

 ("s5c2_project", "ait_list",
  {"kicker": "YOUR FIRST REAL PROJECT", "title": "Build exactly this, this month", "tone": "ok", "color": "money",
   "items": [
     {"h": "Pick 20 large, liquid stocks", "sub": "Nifty names. Liquid enough that slippage stays small."},
     {"h": "Code one white-box rule you understand", "sub": "A moving-average crossover, or the momentum idea from part one."},
     {"h": "Backtest with realistic costs, then walk-forward", "sub": "Judge only the out-of-sample result. Expect to be humbled."},
     {"h": "Add 1% risk sizing and a hard stop-loss", "sub": "Survival first. The risk box is not optional."},
     {"h": "Paper trade it for a month and journal daily", "sub": "Then, and only then, discuss real money with yourself."}],
   "caption": "Finish this one project and you'll be ahead of 95% of people who 'do AI trading'."},
  "Let's turn all of this into one concrete project you can start this month. [pause] "
  "Step one. Pick twenty large, liquid stocks. Nifty names, liquid enough that slippage "
  "stays small. [pause] Step two. Code one white box rule you fully understand. The "
  "moving average crossover, or the momentum idea from part one. [pause] Step three. "
  "Backtest it with realistic costs, then run walk forward, and judge only the out of "
  "sample result. Expect to be humbled. That is normal. [pause] Step four. Add one "
  "percent risk sizing and a hard stop loss. [pause] Step five. Paper trade it for a "
  "month, journaling every day. [pause] Finish just this one project, properly, and you "
  "will already be ahead of ninety five percent of people who claim to do A I trading. "
  "Because you will have actually done it."),

 ("s5c3_pitfalls", "ait_list",
  {"kicker": "THE BUG CHECKLIST", "title": "The mistakes that quietly kill bots", "tone": "bad", "color": "risk",
   "items": [
     {"h": "Look-ahead bias — using future data", "sub": "The number one cause of fake, beautiful backtests."},
     {"h": "Ignoring costs and slippage", "sub": "The number two cause. A costless test is fiction."},
     {"h": "Overfitting by over-tuning", "sub": "Every extra knob is another way to memorise noise."},
     {"h": "Too few trades to mean anything", "sub": "Twenty trades is a story, not statistical evidence."},
     {"h": "Skipping paper trading", "sub": "Going live on faith is how accounts die young."}],
   "caption": "Print this list. Check every strategy against it before it ever sees a rupee."},
  "Before we leave the workshop, here is the checklist of mistakes that quietly kill "
  "bots. Print it. Check every strategy against it. [pause] One. Look ahead bias. Using "
  "future data by accident. The number one cause of fake, beautiful backtests. [pause] "
  "Two. Ignoring costs and slippage. The number two cause. A costless test is fiction. "
  "[pause] Three. Overfitting by over tuning. Every extra knob memorises more noise. "
  "[pause] Four. Too few trades to mean anything. Twenty trades is a story, not "
  "evidence. [pause] Five. Skipping paper trading, and going live on faith. That is how "
  "accounts die young. [pause] Almost every failed bot died of something on this list. "
  "Not of a missing neural network. Master these five, and you have mastered the part "
  "that actually matters."),

 ("s5d_micro", "ait_callout",
  {"kicker": "PART FIVE IN ONE LINE", "color": "ai",
   "text": "Build the boring pipeline first. The AI is the last upgrade, not the plan.",
   "sub": "A working simple bot beats a broken clever one, every single time."},
  "Let's close part five with the line that separates builders from dreamers. [pause] "
  "Build the boring pipeline first. Data, features, a simple rule, an honest backtest, "
  "walk forward, and risk. The A I is the last upgrade, not the plan. [pause] A working "
  "simple bot beats a broken clever one, every single time. [pause] You now know how "
  "the whole thing is built, box by box. So the only question left is, what does a "
  "sane, realistic path actually look like for you? That is part six."),
]

if __name__ == "__main__":
    core.build("ch5", SEGMENTS, target_min=22)
