# -*- coding: utf-8 -*-
"""Design Patterns, Java — screenplay (one video PER pattern, 23 GoF total).

Each pattern is ONE self-contained video that follows the identical 10-section arc:
  title(hook) → scenario → naive code → PAIN → insight(varies/fixed) → analogy →
  refactor(moves) → try(pause) → payoff → REVEAL(name+UML) → map(participants) →
  tradeoffs → recap(+challenge).
The pattern's NAME and UML are never shown until the reveal scene — the viewer must
FEEL the need first. Scenes are the shared archetypes in composer/src/scenes/DPScenes.tsx.

Narration is SPOKEN language (numbers as words), with [pause] markers (0.6s) after new
terms / big ideas / rhetorical questions. Every on-screen element is mentioned in its
beat, phased to when it is said (skills/02). Code line lists use ln(): a plain str is a
normal line; ("text","hi"|"dim"|"add"|"del"|"ghost") sets per-line emphasis.
"""


def ln(*rows):
    """Build a code-line list. Each row: "text"  or  ("text", state)."""
    out = []
    for r in rows:
        if isinstance(r, tuple):
            out.append({"t": r[0], "s": r[1]})
        else:
            out.append({"t": r})
    return out


# =====================================================================================
# dp01 — STRATEGY   (behavioral; the canonical if/else → open-closed story)
# =====================================================================================
STRATEGY = {
    "id": "dp01-strategy",
    "title": "Strategy",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 01",
            "line1": "One switch statement", "line2": "that keeps growing",
            "sub": "a checkout bug story — and the fix that never touches old code"},
         "narration":
            "Here is a piece of code that works perfectly today. [pause] And every single "
            "week, it forces you to open it up and change it. [pause] Same file. Same method. "
            "Over and over. [pause] By the end of this video, you will see exactly why that "
            "happens — and a way to add new behavior without ever touching the working code "
            "again. Let's start at the checkout page."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "You run an online store",
            "situation": "A customer reaches checkout and picks how they want the order "
                         "shipped. Your job: given the order, return the shipping cost. Each "
                         "method prices it differently.",
            "actors": [
                {"emoji": "📦", "label": "Standard"},
                {"emoji": "🚚", "label": "Express"},
                {"emoji": "✈️", "label": "Overnight"}],
            "ask": "Three ways to price one order. How would you write that?"},
         "narration":
            "You run an online store. [pause] A customer reaches the checkout, and picks how "
            "they want their order shipped. [pause] Standard is cheap and slow. Express costs "
            "more. Overnight costs the most. [pause] Your job is simple to state. Given the "
            "order, return the shipping cost — and each method prices it with a different "
            "formula. [pause] Three ways to price one order. [pause] Take a second. How would "
            "you actually write that?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "It works. Ship it.",
            "file": "ShippingCalculator.java",
            "lines": ln(
                "class ShippingCalculator {",
                "  double cost(Order order, String method) {",
                "    double w = order.weight();",
                ('    if (method.equals("STANDARD"))  return 5.00 + w * 0.50;', "hi"),
                ('    if (method.equals("EXPRESS"))   return 15.00 + w * 0.75;', "hi"),
                ('    if (method.equals("OVERNIGHT")) return 30.00 + w * 1.20;', "hi"),
                '    throw new IllegalArgumentException("method: " + method);',
                "  }",
                "}"),
            "note": "One method, one branch per shipping type. Clear, direct, correct."},
         "narration":
            "And here is what most of us reach for. [pause] One method. It takes the order and "
            "the chosen method, as a string. [pause] Then a branch for each type. If it is "
            "standard, five dollars plus fifty cents a kilo. Express, a bit more. Overnight, "
            "more still. [pause] Anything unknown throws. [pause] And honestly? This is fine. "
            "It is clear. It is direct. It compiles, it passes the tests, it ships. [pause] "
            "If the story ended here, there would be no video. But it doesn't."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Add international shipping.\"",
            "file": "ShippingCalculator.java",
            "lines": ln(
                "  double cost(Order order, String method) {",
                "    double w = order.weight();",
                ('    if (method.equals("STANDARD"))  return 5.00 + w*0.50;', "dim"),
                ('    if (method.equals("EXPRESS"))   return 15.00 + w*0.75;', "dim"),
                ('    if (method.equals("OVERNIGHT")) return 30.00 + w*1.20;', "dim"),
                ('    if (method.equals("INTERNATIONAL"))            // NEW', "hi"),
                ("      return 20.00 + w*0.90 + customs(order.zone());  // NEW", "hi"),
                '    throw new IllegalArgumentException(method);',
                "  }"),
            "smell": "Open–Closed violated + shotgun surgery",
            "touched": ["cost() — add a branch", "estimateDelivery() — same switch",
                        "printLabel() — same switch again"]},
         "narration":
            "Two weeks later, the request comes in. Add international shipping. [pause] So you "
            "open the file — the working, tested file — and you add another branch. Twenty "
            "dollars, plus weight, plus a customs fee. [pause] Easy enough. But now look at "
            "what you just did. [pause] You edited code that already worked, and put every "
            "existing shipping type at risk of your typo. [pause] There is a name for that. "
            "Code should be open to new behavior, but closed to modification — you keep "
            "reopening it. [pause] And it gets worse. That exact same switch is copied inside "
            "the method that estimates delivery dates, and again in the one that prints the "
            "label. [pause] One new shipping type. Three files to touch, in perfect sync. "
            "[pause] Change one place, forget another — that is a bug that reaches customers. "
            "This is the pain. Sit with it for a second."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["\"Take an order, return a cost\"",
                      "The checkout flow that asks for it",
                      "The type of the answer — a double"],
            "varies": ["The formula for each method",
                       "How many methods exist",
                       "New ones you cannot predict yet"],
            "principle": "Isolate what varies behind a stable interface — so new behavior "
                         "is added, never edited in."},
         "narration":
            "So let's step back and ask the question that unlocks every pattern. [pause] What "
            "is actually changing, and what is staying the same? [pause] Look carefully. The "
            "shape never changes. Take an order, return a cost, as a number. The checkout "
            "always asks the same question. [pause] What changes is only the formula inside — "
            "and how many formulas there are. Standard, express, overnight, international, and "
            "whatever marketing dreams up next quarter. [pause] So here is the principle, and "
            "it is the whole game. [pause] Find the thing that varies, and wall it off behind "
            "something that stays fixed. [pause] Do that, and adding a new behavior becomes "
            "adding something new — instead of editing something old."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "Think of a camera",
            "emoji": "📷", "analogy": "One camera body. Many lenses. Same mount.",
            "map": [
                {"from": "The camera body", "to": "the fixed method signature"},
                {"from": "The lens mount", "to": "a shared interface"},
                {"from": "A specific lens", "to": "one pricing formula"},
                {"from": "Swapping lenses", "to": "choosing a strategy"}],
            "breaks": "a camera holds one lens at a time and you swap by hand — in code the "
                      "caller can pass a different behavior on every single call, even pick "
                      "it automatically."},
         "narration":
            "Here is a picture for it. Think of a camera. [pause] The body stays the same. But "
            "you can twist off one lens and click on another — wide, zoom, macro — because "
            "they all share the same mount. [pause] The body doesn't care which lens is on it. "
            "It just knows the mount will fit. [pause] That is exactly what we want. The camera "
            "body is our fixed method. The mount is a shared interface. Each lens is one "
            "pricing formula, and swapping lenses is choosing which one to use. [pause] But "
            "let me flag where the picture lies, so it doesn't mislead you. [pause] A camera "
            "holds one lens at a time, and you swap it by hand. In code, the caller can hand "
            "in a different behavior on every call — and can even pick it automatically. Keep "
            "that difference in your pocket."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "Name the thing that varies",
            "file": "ShippingStrategy.java",
            "lines": ln(
                "// the one thing that varies: a cost formula.",
                "// give it a name and a shape.",
                ("interface ShippingStrategy {", "add"),
                ("  double cost(Order order);", "add"),
                ("}", "add")),
            "note": "That's the mount. Anything that can price an order will fit it."},
         "narration":
            "Alright. Let's fix it, one move at a time. [pause] Move one. We take the thing "
            "that varies — a cost formula — and we give it a name and a shape. [pause] An "
            "interface. Shipping strategy. One method: given an order, return a cost. [pause] "
            "That is it. That is our lens mount. [pause] Notice we have not written a single "
            "formula yet. We have only declared the shape that every formula will fit into."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "One class per formula",
            "file": "strategies/*.java",
            "lines": ln(
                ("class StandardShipping implements ShippingStrategy {", "add"),
                ("  public double cost(Order o) {", "add"),
                ("    return 5.00 + o.weight() * 0.50;", "add"),
                ("  }", "add"),
                ("}", "add"),
                ("class ExpressShipping implements ShippingStrategy {", "add"),
                ("  public double cost(Order o) {", "add"),
                ("    return 15.00 + o.weight() * 0.75;", "add"),
                ("  }", "add"),
                ("}", "add")),
            "note": "Each old branch becomes its own small, testable class — the lenses."},
         "narration":
            "Move two. Every branch from that switch becomes its own little class. [pause] "
            "Standard shipping implements the interface, and its cost method holds exactly the "
            "old standard formula. [pause] Express shipping — another class, the express "
            "formula. [pause] Each one is tiny. Each one does exactly one thing. And each one "
            "can be tested completely on its own, with no giant switch around it. [pause] These "
            "are our lenses. Same mount, different glass."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Write the overnight lens",
            "file": "OvernightShipping.java",
            "lines": ln(
                "class OvernightShipping implements ShippingStrategy {",
                "  public double cost(Order o) {",
                ("    // ▯ your line: base 30.00, plus 1.20 per kilo", "ghost"),
                "  }",
                "}"),
            "prompt": "Fill in the one line of overnight's cost formula.",
            "hint": "return 30.00 + o.weight() * 1.20;"},
         "narration":
            "Now your turn. [pause] Here is the overnight class, with the mount already in "
            "place. The only thing missing is the one line inside cost. [pause] Overnight is "
            "thirty dollars flat, plus one dollar twenty per kilo. [pause] Pause the video, and "
            "write that line yourself. [pause] Got it? It follows the exact same shape as the "
            "other two — return thirty, plus the weight times one twenty. If you wrote that, "
            "you now understand the pattern better than any diagram could teach you."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "The calculator just delegates",
            "file": "ShippingCalculator.java",
            "lines": ln(
                "class ShippingCalculator {",
                ("  private final ShippingStrategy strategy;", "add"),
                ("  ShippingCalculator(ShippingStrategy strategy) {", "add"),
                ("    this.strategy = strategy;", "add"),
                "  }",
                "  double cost(Order order) {",
                ("    return strategy.cost(order);   // no switch, ever", "add"),
                "  }",
                "}"),
            "note": "The switch is gone. Which lens to use is now chosen at the edge."},
         "narration":
            "Move three, and this is where it clicks. [pause] The calculator no longer knows "
            "any formulas. It just holds a strategy — whichever lens you clicked on — and it "
            "delegates. [pause] Its cost method is now one line. Ask the strategy. [pause] The "
            "entire switch statement is gone. Deleted. [pause] And that duplicated switch in "
            "delivery estimates and label printing? They delegate too. The knowledge lives in "
            "one place now — the class itself. [pause] Which lens to use gets decided once, at "
            "the edge of the system, where the customer's choice comes in."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Add international shipping\" — the exact same request",
            "naiveLabel": "Before", "naiveCost": "Reopen a working file. Edit three switches.",
            "naiveSteps": ["edit the switch in 3 methods", "recompile the core",
                           "risk breaking A, B, C"],
            "patLabel": "Now", "patCost": "Add one new class. Touch nothing else.",
            "patFile": "InternationalShipping.java",
            "patLines": ln(
                ("class InternationalShipping", "add"),
                ("    implements ShippingStrategy {", "add"),
                ("  public double cost(Order o) {", "add"),
                ("    return 20.00 + o.weight()*0.90", "add"),
                ("         + customs(o.zone());", "add"),
                ("  }", "add"),
                ("}", "add"))},
         "narration":
            "Now let's rewind to the request that caused all the pain. Add international "
            "shipping. [pause] The same request. Watch how different it feels. [pause] Before, "
            "you reopened working code and edited three separate switches, hoping you did not "
            "miss one. [pause] Now? You write one new class. International shipping, implements "
            "the interface, holds its own formula. [pause] You register it, and you are done. "
            "[pause] The calculator — untouched. Standard, express, overnight — untouched, "
            "unretested, unbroken. [pause] New behavior was added, not edited in. That is the "
            "whole promise, delivered."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Strategy Pattern",
            "plain": "A family of interchangeable algorithms, each in its own class, swapped "
                     "behind one shared interface.",
            "nodes": [
                {"id": "strat", "title": "ShippingStrategy", "stereo": "interface",
                 "members": ["+ cost(order): double"], "x": 760, "y": 220, "w": 400, "color": "#22D3EE"},
                {"id": "ctx", "title": "ShippingCalculator",
                 "members": ["- strategy: ShippingStrategy", "+ cost(order): double"],
                 "x": 150, "y": 235, "w": 430, "color": "#A78BFA"},
                {"id": "std", "title": "StandardShipping", "members": ["+ cost(o): double"],
                 "x": 150, "y": 630, "w": 370, "color": "#8B93B0"},
                {"id": "exp", "title": "ExpressShipping", "members": ["+ cost(o): double"],
                 "x": 555, "y": 630, "w": 370, "color": "#8B93B0"},
                {"id": "ovn", "title": "OvernightShipping", "members": ["+ cost(o): double"],
                 "x": 960, "y": 630, "w": 370, "color": "#8B93B0"},
                {"id": "intl", "title": "InternationalShipping", "members": ["+ cost(o): double"],
                 "x": 1365, "y": 630, "w": 370, "color": "#34D399"}],
            "edges": [
                {"from": "ctx", "to": "strat", "kind": "has"},
                {"from": "std", "to": "strat", "kind": "impl"},
                {"from": "exp", "to": "strat", "kind": "impl"},
                {"from": "ovn", "to": "strat", "kind": "impl"},
                {"from": "intl", "to": "strat", "kind": "impl"}]},
         "narration":
            "And now — only now — we name it. [pause] What you just built is the Strategy "
            "pattern. [pause] Look at the shape you created without being told to. [pause] In "
            "the middle, the interface — shipping strategy. The mount. [pause] On the left, the "
            "calculator. It holds a strategy and points to that interface. It never knows which "
            "concrete one it has. [pause] And underneath, your four classes — standard, "
            "express, overnight, international — all implementing that one interface. [pause] "
            "The green one, international, is the one you added last. Notice it just slots into "
            "the row. Nothing above it had to move."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Strategy", "your": "interface ShippingStrategy"},
                {"role": "ConcreteStrategy", "your": "StandardShipping, ExpressShipping, …"},
                {"role": "Context", "your": "ShippingCalculator"},
                {"role": "Client", "your": "checkout — picks the strategy"}],
            "plain": "Put each algorithm in its own class behind a shared interface, and let "
                     "the caller pick which one to use.",
            "gof": "Define a family of algorithms, encapsulate each one, and make them "
                   "interchangeable. Strategy lets the algorithm vary independently from the "
                   "clients that use it."},
         "narration":
            "The textbooks give these four roles names, so let's map each one to a class you "
            "already wrote. [pause] The Strategy is your interface. [pause] The concrete "
            "strategies are your four shipping classes. [pause] The Context is the calculator "
            "that holds one and delegates to it. [pause] And the Client is the checkout code "
            "that decides which strategy to hand in. [pause] In plain English — put each "
            "algorithm in its own class behind a shared interface, and let the caller choose. "
            "[pause] The Gang of Four said it more formally: define a family of algorithms, "
            "encapsulate each one, and make them interchangeable, so the algorithm can vary "
            "independently from the code that uses it."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "Don't reach for it out of habit",
            "costs": ["More classes and files to navigate",
                      "The client must know which strategy to pick",
                      "Selection logic moves — it does not vanish"],
            "dont": ["There are only two cases, forever",
                     "The behavior never varies at runtime",
                     "A simple if is genuinely clearer"],
            "signal": "a switch on a 'type' keeps growing, and each case is an interchangeable "
                      "behavior you keep adding to."},
         "narration":
            "Now the honest part, because no pattern is free. [pause] Strategy costs you "
            "classes. Four formulas that used to be four lines are now four files. [pause] And "
            "the choice of which strategy to use does not disappear — it moves out to the "
            "caller. Someone still has to pick. [pause] So do not reach for this out of habit. "
            "[pause] If you have exactly two cases and you are certain there will only ever be "
            "two — a plain if statement is clearer, and you should just write the if. [pause] "
            "If the behavior never changes at runtime, you may not need it either. [pause] "
            "Here is the one signal that means yes, use it. [pause] You have a switch on some "
            "type field, it keeps growing, and every case is an interchangeable behavior you "
            "keep adding. The moment you feel that, reach for Strategy."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Strategy, in one breath",
            "items": [
                "A growing switch on shipping type forced edits to working code, in three "
                "places, every time.",
                "The formula varies; 'take an order, return a cost' stays fixed — so wall the "
                "formula off behind an interface.",
                "Strategy: one class per algorithm, swapped behind a shared interface. New "
                "behavior is a new class."],
            "challenge": "Your app exports reports, and a switch on format handles PDF and "
                         "CSV today. Marketing wants HTML now, and XLSX next quarter.",
            "question": "Does Strategy fit? What's the interface — and what are the classes?"},
         "narration":
            "So, the whole journey in three beats. [pause] The problem: a switch on shipping "
            "type forced you to edit working code, in three places, every single time it grew. "
            "[pause] The insight: the formula varies, but take an order return a cost stays "
            "fixed — so wall the formula off behind an interface. [pause] The pattern: "
            "Strategy. One class per algorithm, swapped behind a shared interface, so new "
            "behavior is a new class instead of an edit. [pause] Now, before the next episode, "
            "here is one for you. [pause] Your app exports reports. A switch on format handles "
            "P D F and C S V today. Marketing now wants H T M L, and next quarter, spreadsheets. "
            "[pause] Does Strategy fit here? What would the interface be — and what are the "
            "concrete classes? [pause] Pause, and sketch it, before you press play on the next one."},
    ],
}


# =====================================================================================
# dp02 — OBSERVER   (behavioral; one change must fan out to many reactions)
# =====================================================================================
OBSERVER = {
    "id": "dp02-observer",
    "title": "Observer",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 02",
            "line1": "One method that keeps", "line2": "sprouting new calls",
            "sub": "when an order ships, five things must happen — and tomorrow, six"},
         "narration":
            "There is a method in almost every codebase that has a disease. [pause] Every time "
            "the business wants one more thing to happen, this method grows another line. "
            "Another dependency. Another reason to break. [pause] Today we are going to cure "
            "it. Watch what happens the moment an order changes status."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "An order changes status",
            "situation": "The moment an order is marked 'shipped', several parts of your system "
                         "must react — and none of them are optional.",
            "actors": [
                {"emoji": "📧", "label": "Email the buyer"},
                {"emoji": "📦", "label": "Update inventory"},
                {"emoji": "📊", "label": "Track analytics"}],
            "ask": "One event. Many reactions. Where does that code live?"},
         "narration":
            "Here is the situation. [pause] An order gets marked as shipped. [pause] And the "
            "instant that happens, a whole crowd of things need to react. [pause] Email the "
            "buyer their tracking number. Decrement the warehouse inventory. Send the event to "
            "analytics. [pause] None of these are optional, and there will only be more of them "
            "over time. [pause] So here is the question. One event, many reactions — where does "
            "all that code actually live?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "Just call them, right there.",
            "file": "Order.java",
            "lines": ln(
                "class Order {",
                "  private Status status;",
                "  void setStatus(Status s) {",
                "    this.status = s;",
                ("    email.send(this);", "hi"),
                ("    inventory.update(this);", "hi"),
                ("    analytics.track(this);", "hi"),
                "  }",
                "}"),
            "note": "setStatus does the one thing it should — and then four favors."},
         "narration":
            "And the obvious answer is: just call them. Right there in the order. [pause] When "
            "we set the status, we set the field — and then we email the buyer, update "
            "inventory, and track the event. [pause] It reads top to bottom. It works. Anyone "
            "can follow it. [pause] But look closely at what the order has quietly become. It "
            "sets a status — and then it does four unrelated favors for four other systems."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Also award loyalty points.\"",
            "file": "Order.java",
            "lines": ln(
                "  void setStatus(Status s) {",
                "    this.status = s;",
                ("    email.send(this);", "dim"),
                ("    inventory.update(this);", "dim"),
                ("    analytics.track(this);", "dim"),
                ("    loyalty.award(this);        // NEW today", "hi"),
                ("    // sms? push? fraud check? ...", "hi"),
                "  }"),
            "smell": "A domain object drowning in dependencies",
            "touched": ["Order now imports 5 services", "setStatus() edited yet again",
                        "can't test Order without all 5"]},
         "narration":
            "Now marketing asks for one small thing. Award loyalty points when an order ships. "
            "[pause] So you open the order — your core domain class — and add a line. [pause] "
            "And it is never just one. Tomorrow it is text messages. Then push notifications. "
            "Then a fraud check. [pause] Every single one reopens this method. [pause] Step "
            "back and see the damage. Your order — a thing that should just model an order — now "
            "depends on email, inventory, analytics, loyalty, and more. [pause] It cannot even "
            "be tested without dragging all five of them along. [pause] The order knows far too "
            "much about a crowd it should not care about."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["The fact that the status changed",
                      "The order's job: announce it happened",
                      "There is exactly one order"],
            "varies": ["Who wants to hear about it",
                       "How many listeners there are",
                       "What each listener does in response"],
            "principle": "Let the one that changed announce it once — and let whoever cares "
                         "listen in."},
         "narration":
            "Same question as always. What actually changes here, and what stays fixed? [pause] "
            "The fixed part is small. The status changed — that is a fact. And the order's job "
            "is simply to announce that fact. There is one order. [pause] Everything else "
            "varies. Who wants to know. How many of them there are. And what each one does "
            "about it. [pause] So here is the shift. [pause] Instead of the order reaching out "
            "and calling each system by name, let the order just announce, once, that something "
            "happened — and let anyone who cares listen in. [pause] Crucially, the order should "
            "not know who is listening."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "Think of a newsletter",
            "emoji": "📰", "analogy": "The publisher sends one issue. Every subscriber gets it.",
            "map": [
                {"from": "The publisher", "to": "the Order (the subject)"},
                {"from": "A subscriber", "to": "a listener object"},
                {"from": "Subscribing", "to": "registering to be notified"},
                {"from": "The issue going out", "to": "one notify() call"}],
            "breaks": "a newsletter is one-way and delayed — here the notification is immediate, "
                      "in-process, and a listener can even react before the next one runs."},
         "narration":
            "Picture a newsletter. [pause] The publisher writes one issue and sends it. Every "
            "subscriber receives it. [pause] And here is the key: the publisher does not phone "
            "each reader by name. It does not even keep a mental list of who you are. People "
            "subscribe, people unsubscribe, and the publisher just broadcasts. [pause] That is "
            "exactly our fix. The order is the publisher. Each system that reacts is a "
            "subscriber. Subscribing means asking to be told, and sending the issue is a single "
            "notify. [pause] Where does the picture break? A newsletter is slow and one "
            "directional. Our notification is immediate and in the same process — a listener "
            "can even finish its work before the next one starts."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "Name the listener",
            "file": "OrderObserver.java",
            "lines": ln(
                "// anyone who wants to react to an order change",
                "// only has to promise one thing:",
                ("interface OrderObserver {", "add"),
                ("  void onStatusChanged(Order order);", "add"),
                ("}", "add")),
            "note": "One tiny promise. Email, SMS, loyalty — all can make it."},
         "narration":
            "Let's fix it, one move at a time. [pause] Move one. We name the listener. [pause] "
            "Anyone who wants to react to an order only has to promise one thing — a method "
            "called on status changed, that takes the order. [pause] That is the whole "
            "contract. Email can promise it. Inventory can promise it. Loyalty, a class that "
            "does not even exist yet, can promise it too."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "The order keeps a guest list",
            "file": "Order.java",
            "lines": ln(
                "class Order {",
                ("  private final List<OrderObserver> observers", "add"),
                ("      = new ArrayList<>();", "add"),
                ("  void subscribe(OrderObserver o) { observers.add(o); }", "add"),
                "  void setStatus(Status s) {",
                "    this.status = s;",
                ("    notifyObservers();   // that's all it does now", "add"),
                "  }",
                "}"),
            "note": "The order holds a list of listeners and one way to add to it."},
         "narration":
            "Move two. The order stops calling services, and instead keeps a guest list. "
            "[pause] A plain list of observers, and a subscribe method to add one. [pause] And "
            "now look at set status. It sets the field, and then it does one single thing — it "
            "notifies. [pause] It no longer mentions email, or inventory, or analytics. It has "
            "no idea who is even on the list. It just announces."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Write notifyObservers()",
            "file": "Order.java",
            "lines": ln(
                "private void notifyObservers() {",
                ("  // ▯ your lines: tell every observer, in turn", "ghost"),
                "}"),
            "prompt": "Loop the guest list and call each observer with this order.",
            "hint": "for (OrderObserver o : observers) o.onStatusChanged(this);"},
         "narration":
            "Your turn. [pause] The notify method is empty. Its whole job is to walk the guest "
            "list and tell every observer, in turn, that this order changed. [pause] Pause, and "
            "write it. [pause] It is a single for-each loop. For each observer on the list, call "
            "on status changed, passing this order. [pause] That one loop is the beating heart "
            "of the entire pattern."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "Services become listeners, wired at startup",
            "file": "AppStartup.java",
            "lines": ln(
                ("class EmailObserver implements OrderObserver {", "add"),
                ("  public void onStatusChanged(Order o) { email.send(o); }", "add"),
                ("}", "add"),
                "// wiring, once, at the edge — not inside Order:",
                ("order.subscribe(new EmailObserver());", "add"),
                ("order.subscribe(new InventoryObserver());", "add"),
                ("order.subscribe(new AnalyticsObserver());", "add")),
            "note": "Each service implements the interface; subscriptions live at the edge."},
         "narration":
            "Move three. Each old service becomes a listener. [pause] The email observer "
            "implements the interface, and its react method does the exact thing that used to "
            "sit inside the order. [pause] And the wiring — deciding who subscribes — moves out "
            "to the startup of the app, at the edge of the system. [pause] The order does not "
            "assemble this list. Something on the outside hands it its audience."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Also award loyalty points\" — the exact same request",
            "naiveLabel": "Before", "naiveCost": "Reopen the core Order. Add another dependency.",
            "naiveSteps": ["reopen the core Order", "add another dependency",
                           "recompile + retest it all"],
            "patLabel": "Now", "patCost": "Add one observer. Subscribe it. Order untouched.",
            "patFile": "LoyaltyObserver.java",
            "patLines": ln(
                ("class LoyaltyObserver", "add"),
                ("    implements OrderObserver {", "add"),
                ("  public void onStatusChanged(Order o) {", "add"),
                ("    points.award(o.buyer());", "add"),
                ("  }", "add"),
                ("}", "add"),
                ("order.subscribe(new LoyaltyObserver());", "add"))},
         "narration":
            "Now rewind to the request that started the pain. Also award loyalty points. "
            "[pause] Before, that meant reopening the core order and bolting on another "
            "dependency. [pause] Now? You write one new observer. It reacts by awarding points. "
            "[pause] Then, at startup, one line subscribes it. [pause] The order class — never "
            "opened. Email, inventory, analytics — never touched, never retested. [pause] A new "
            "reaction became a new class. The core stayed frozen."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Observer Pattern",
            "plain": "One subject holds many listeners; when it changes, it notifies every one "
                     "of them — without knowing who they are.",
            "nodes": [
                {"id": "obs", "title": "OrderObserver", "stereo": "interface",
                 "members": ["+ onStatusChanged(o)"], "x": 760, "y": 220, "w": 400, "color": "#22D3EE"},
                {"id": "subj", "title": "Order", "members": ["- observers: List", "+ subscribe(o)", "+ notify()"],
                 "x": 150, "y": 225, "w": 430, "color": "#A78BFA"},
                {"id": "em", "title": "EmailObserver", "members": ["+ onStatusChanged(o)"],
                 "x": 150, "y": 640, "w": 370, "color": "#8B93B0"},
                {"id": "iv", "title": "InventoryObserver", "members": ["+ onStatusChanged(o)"],
                 "x": 555, "y": 640, "w": 370, "color": "#8B93B0"},
                {"id": "an", "title": "AnalyticsObserver", "members": ["+ onStatusChanged(o)"],
                 "x": 960, "y": 640, "w": 370, "color": "#8B93B0"},
                {"id": "lo", "title": "LoyaltyObserver", "members": ["+ onStatusChanged(o)"],
                 "x": 1365, "y": 640, "w": 370, "color": "#34D399"}],
            "edges": [
                {"from": "subj", "to": "obs", "kind": "has"},
                {"from": "em", "to": "obs", "kind": "impl"},
                {"from": "iv", "to": "obs", "kind": "impl"},
                {"from": "an", "to": "obs", "kind": "impl"},
                {"from": "lo", "to": "obs", "kind": "impl"}]},
         "narration":
            "Now we name it. [pause] What you built is the Observer pattern. [pause] Look at the "
            "shape. In the middle, the observer interface — the one-line promise. [pause] On the "
            "left, the order. It holds a list of observers and a way to subscribe. It points "
            "only at the interface. It has no idea what an email observer even is. [pause] And "
            "underneath, your listeners, each implementing that promise. [pause] The green one, "
            "loyalty, is the one you added last — it just joins the row. Nothing above it moved."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Subject", "your": "Order (holds + notifies)"},
                {"role": "Observer", "your": "interface OrderObserver"},
                {"role": "ConcreteObserver", "your": "EmailObserver, LoyaltyObserver, …"},
                {"role": "Client", "your": "startup — wires subscriptions"}],
            "plain": "Objects subscribe to a subject; when it changes, it notifies them all — "
                     "each reacting on its own.",
            "gof": "Define a one-to-many dependency between objects so that when one object "
                   "changes state, all its dependents are notified and updated automatically."},
         "narration":
            "Four roles, mapped to what you wrote. [pause] The Subject is the order — the thing "
            "that holds listeners and notifies them. [pause] The Observer is your interface. "
            "[pause] The concrete observers are your email, inventory, and loyalty classes. "
            "[pause] And the Client is the startup code that decides who subscribes. [pause] In "
            "plain terms — objects subscribe to a subject, and when it changes, it tells them "
            "all. [pause] The Gang of Four called it a one to many dependency, where a change "
            "in one object notifies all its dependents automatically."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "The costs nobody warns you about",
            "costs": ["Notification order is not guaranteed",
                      "Forget to unsubscribe → memory leak",
                      "Cascades get hard to trace and debug"],
            "dont": ["There is one fixed reaction, forever",
                     "The listeners never change",
                     "A direct call is clearer and safer"],
            "signal": "one event must trigger many independent reactions, and that set of "
                      "reactions keeps growing."},
         "narration":
            "Now the honest costs, and Observer has some sharp ones. [pause] The order that "
            "listeners run in is not guaranteed, so never rely on email firing before "
            "analytics. [pause] If a listener subscribes and forgets to unsubscribe, it lives "
            "forever — a classic memory leak. [pause] And when one notification triggers "
            "another, tracing the cascade at three in the morning is genuinely painful. [pause] "
            "So skip it when there is exactly one reaction that will never change — just call "
            "it directly, it is clearer. [pause] The signal to use it is unmistakable. One "
            "event must fan out to many independent reactions, and that set keeps growing. When "
            "you feel that, reach for Observer."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Observer, in one breath",
            "items": [
                "One method kept sprouting calls — every new reaction reopened the core Order "
                "and coupled it tighter.",
                "The order's job is just to announce a change; who listens, and how many, "
                "varies — so let them subscribe.",
                "Observer: a subject notifies a list of listeners it does not know. New "
                "reaction, new observer."],
            "challenge": "In your chat app, a new message updates the unread badge and plays a "
                         "sound. Now product wants desktop notifications and a typing indicator.",
            "question": "Does Observer fit? What's the subject, and what are the observers?"},
         "narration":
            "The whole journey in three beats. [pause] The problem: one method kept sprouting "
            "calls, and every new reaction reopened the core order and coupled it tighter. "
            "[pause] The insight: the order's only job is to announce that something changed — "
            "who listens, and how many, is not its business. [pause] The pattern: Observer. A "
            "subject notifies a list of listeners it does not even know, so a new reaction is "
            "just a new observer. [pause] Now one for you, before the next episode. [pause] In "
            "a chat app, a new message updates the unread badge and plays a sound. Now product "
            "wants desktop notifications, and a typing indicator too. [pause] Does Observer fit? "
            "What is the subject — and what are the observers? [pause] Pause, and sketch it, "
            "before you press play."},
    ],
}


# =====================================================================================
# dp03 — DECORATOR   (structural; boolean flags / subclass explosion → wrap & stack)
# =====================================================================================
DECORATOR = {
    "id": "dp03-decorator",
    "title": "Decorator",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 03",
            "line1": "One class, a dozen", "line2": "booleans, and a mess",
            "sub": "a coffee menu that doubles in size every time the barista learns a trick"},
         "narration":
            "This is a class that starts clean, with one job. [pause] Then the feature requests "
            "arrive — and it grows a new boolean flag for every single one, until nobody can "
            "read it anymore. [pause] There is a beautiful fix, and it comes from thinking about "
            "wrapping paper. Let's start at a coffee shop."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "Pricing a customized coffee",
            "situation": "A customer orders an espresso, then customizes it — add milk, add "
                         "caramel, add whip. You need the final price and a description.",
            "actors": [
                {"emoji": "☕", "label": "Espresso"},
                {"emoji": "🥛", "label": "+ Milk"},
                {"emoji": "🍯", "label": "+ Caramel"}],
            "ask": "Any add-on, any combination, even twice. What's the price?"},
         "narration":
            "You are building the till for a coffee shop. [pause] A customer orders an espresso. "
            "Then they start customizing. Add milk. Add caramel. A double shot of whip. [pause] "
            "You need two things out of any order: the final price, and a description to print "
            "on the cup. [pause] And here is the catch. Any add-on can combine with any other — "
            "and someone will absolutely ask for double caramel. [pause] So, how do you price "
            "that?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "A flag for each extra.",
            "file": "Coffee.java",
            "lines": ln(
                "class Coffee {",
                "  boolean milk, caramel, whip;",
                "  double cost() {",
                "    double c = 2.00;              // base espresso",
                ("    if (milk)    c += 0.50;", "hi"),
                ("    if (caramel) c += 0.60;", "hi"),
                ("    if (whip)    c += 0.70;", "hi"),
                "    return c;",
                "  }",
                "}"),
            "note": "A boolean per add-on, an if per boolean. Feels tidy enough."},
         "narration":
            "The natural first move: one boolean per add-on. [pause] Milk, caramel, whip — flip "
            "the ones the customer wants. [pause] Then cost starts at two dollars for the "
            "espresso, and adds a little for each flag that is on. [pause] Honestly, it looks "
            "tidy. It reads fine. For three add-ons, this is completely reasonable. [pause] But "
            "watch what the fourth, fifth, and sixth add-on do to it."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Add oat milk, hazelnut, extra shot…\"",
            "file": "Coffee.java",
            "lines": ln(
                "  boolean milk, caramel, whip,",
                ("      oat, hazelnut, extraShot;   // and counting", "hi"),
                "  double cost() {",
                ("    if (milk)     c += 0.50;", "dim"),
                ("    if (caramel)  c += 0.60;", "dim"),
                ("    if (oat)      c += 0.55;", "hi"),
                ("    if (hazelnut) c += 0.60;", "hi"),
                "    // ...and the same list again in desc()",
                "  }"),
            "smell": "Class explosion + you can't order it twice",
            "touched": ["cost() — new if", "desc() — same list", "calories() — same list",
                        "double caramel? impossible"]},
         "narration":
            "The menu grows, the way menus do. Oat milk. Hazelnut. An extra shot. [pause] Each "
            "one adds a boolean field, and an if in cost. And another if in the description "
            "method. And another in the calorie counter. [pause] The same growing list, copied "
            "in three places, forever. [pause] But here is the killer, the thing a boolean can "
            "never do. [pause] A customer asks for double caramel. [pause] Your flag is true or "
            "false. It cannot be true twice. [pause] The whole model is wrong — you are trying "
            "to describe stackable layers with a row of on-off switches."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["A drink has a cost and a description",
                      "Every add-on wraps a drink",
                      "The result is still just a drink"],
            "varies": ["Which extras are on the drink",
                       "How they stack — any order, any count",
                       "New extras invented all the time"],
            "principle": "Make each extra a wrapper around a drink that adds a little — and is "
                         "itself a drink."},
         "narration":
            "The question that unlocks it. What changes, what stays fixed? [pause] Fixed: a "
            "drink always has a cost and a description. That never changes. [pause] What varies "
            "is which extras are on it, how they stack, and how many new ones exist. [pause] "
            "Now here is the leap. [pause] What if each add-on were not a flag, but a wrapper — "
            "something you put around a drink that takes its price and adds a little? [pause] "
            "And crucially — the wrapper is itself a drink. So you can wrap a wrapper. That one "
            "idea makes double caramel trivial."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "Think of gift wrapping",
            "emoji": "🎁", "analogy": "A gift, in a box, in wrapping paper, with a bow.",
            "map": [
                {"from": "The gift inside", "to": "the base Espresso"},
                {"from": "Each layer of wrap", "to": "one add-on wrapper"},
                {"from": "Still one parcel", "to": "still implements Beverage"},
                {"from": "Add another layer", "to": "wrap it once more"}],
            "breaks": "with a real gift the outer layer hides the inside — here each wrapper "
                      "asks the layer within for its price, then adds its own."},
         "narration":
            "Picture wrapping a gift. [pause] There is the present, then a box around it, then "
            "paper around the box, then a bow. [pause] Each layer goes around everything so far "
            "— and the whole thing is still just one parcel you can hand over. [pause] That is "
            "our fix exactly. The gift is the espresso. Each add-on is a layer wrapped around "
            "it. And wrapped or not, it is still a drink you can ask for a price. [pause] Where "
            "does the picture break? Real wrapping hides what is inside. Our wrapper does the "
            "opposite — it asks the layer within for its price, and then adds its own on top."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "A drink is a drink",
            "file": "Beverage.java",
            "lines": ln(
                "// the fixed shape: anything drinkable",
                ("interface Beverage {", "add"),
                ("  double cost();", "add"),
                ("  String desc();", "add"),
                ("}", "add"),
                "",
                ("class Espresso implements Beverage {", "add"),
                ('  public double cost() { return 2.00; }', "add"),
                ('  public String desc() { return "espresso"; }', "add"),
                ("}", "add")),
            "note": "The base drink, with no add-ons, knows only itself."},
         "narration":
            "Move one. We pin down what a drink is. [pause] An interface, beverage, with a cost "
            "and a description. [pause] Then the plain espresso implements it. Two dollars, and "
            "the word espresso. [pause] No flags. No add-ons. It knows only itself. This is the "
            "gift, before any wrapping."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "A wrapper that is also a drink",
            "file": "AddOn.java",
            "lines": ln(
                "// wraps a Beverage, and IS a Beverage",
                ("abstract class AddOn implements Beverage {", "add"),
                ("  protected final Beverage inner;", "add"),
                ("  AddOn(Beverage inner) { this.inner = inner; }", "add"),
                "}",
                ("class Milk extends AddOn {", "add"),
                ("  Milk(Beverage b) { super(b); }", "add"),
                ('  public double cost() { return inner.cost() + 0.50; }', "add"),
                ('  public String desc() { return inner.desc() + ", milk"; }', "add"),
                "}"),
            "note": "The wrapper holds the layer inside, and adds to whatever it returns."},
         "narration":
            "Move two, and this is the whole trick. [pause] An add-on is an abstract class that "
            "implements beverage — so it is a drink — and also holds a beverage inside it: the "
            "layer it wraps. [pause] Then milk extends it. Its cost asks the inner drink for its "
            "price, and adds fifty cents. Its description takes the inner description, and "
            "appends the word milk. [pause] It does not care what is inside. Espresso, or "
            "another wrapper — it just adds its own bit on top."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Write the Whip wrapper",
            "file": "Whip.java",
            "lines": ln(
                "class Whip extends AddOn {",
                "  Whip(Beverage b) { super(b); }",
                ("  // ▯ your line: cost is inner + 0.70", "ghost"),
                "}"),
            "prompt": "Write Whip's cost() — the inner drink's price, plus seventy cents.",
            "hint": "public double cost() { return inner.cost() + 0.70; }"},
         "narration":
            "Your turn. [pause] Here is the whip wrapper, already holding its inner drink. All "
            "it needs is a cost method. [pause] Whip adds seventy cents on top of whatever it "
            "wraps. Pause, and write that one line. [pause] It mirrors milk exactly — return the "
            "inner cost, plus seventy cents. If you wrote that, you have the pattern in your "
            "hands."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "Stack them like layers",
            "file": "Order.java",
            "lines": ln(
                "// espresso, then milk around it, then whip around that:",
                ("Beverage drink =", "add"),
                ("    new Whip(new Milk(new Espresso()));", "add"),
                "",
                ("drink.cost();   // 2.00 + 0.50 + 0.70 = 3.20", "hi"),
                'drink.desc();   // "espresso, milk, whip"',
                "",
                "// double caramel? just wrap twice:",
                ("new Caramel(new Caramel(new Espresso()));", "add")),
            "note": "Each call unwraps one layer inward, summing as it goes."},
         "narration":
            "Move three. Now we stack them, just like layers of wrapping. [pause] Espresso, with "
            "milk wrapped around it, with whip wrapped around that. [pause] Ask the outer drink "
            "for its cost, and watch it cascade. Whip asks milk, milk asks espresso — two "
            "dollars, plus fifty, plus seventy — three twenty. The description assembles the "
            "same way. [pause] And that impossible request from before? Double caramel? [pause] "
            "You just wrap caramel around caramel. Two layers. Done."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Add caramel drizzle\" — the newest add-on",
            "naiveLabel": "Before", "naiveCost": "A new boolean, and a new if in three methods.",
            "naiveSteps": ["add a boolean field", "edit cost, desc, calories",
                           "still can't stack it twice"],
            "patLabel": "Now", "patCost": "One wrapper class. Stack it any way you like.",
            "patFile": "Caramel.java",
            "patLines": ln(
                ("class Caramel extends AddOn {", "add"),
                ("  Caramel(Beverage b) {", "add"),
                ("    super(b);", "add"),
                ("  }", "add"),
                ("  public double cost() {", "add"),
                ("    return inner.cost() + 0.60;", "add"),
                ("  }", "add"),
                ("}", "add"))},
         "narration":
            "Now the newest request. Add a caramel drizzle. [pause] Before, that meant another "
            "boolean, and another if in cost, and in description, and in calories — and it still "
            "could not be ordered twice. [pause] Now? One small wrapper class. Caramel, adding "
            "sixty cents to whatever it wraps. [pause] Espresso — untouched. Milk and whip — "
            "untouched. [pause] And because caramel is just a drink, you can stack it, combine "
            "it, wrap it twice. A new extra became a new wrapper, and every old combination "
            "still works."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Decorator Pattern",
            "plain": "Wrap an object in another object of the same type that adds behavior — "
                     "and stack the wrappers freely.",
            "nodes": [
                {"id": "bev", "title": "Beverage", "stereo": "interface",
                 "members": ["+ cost(): double", "+ desc(): String"],
                 "x": 760, "y": 205, "w": 400, "color": "#22D3EE"},
                {"id": "esp", "title": "Espresso", "members": ["+ cost()", "+ desc()"],
                 "x": 150, "y": 250, "w": 360, "color": "#8B93B0"},
                {"id": "dec", "title": "AddOn", "stereo": "abstract",
                 "members": ["- inner: Beverage", "+ cost() / desc()"],
                 "x": 1410, "y": 250, "w": 380, "color": "#A78BFA"},
                {"id": "mk", "title": "Milk", "members": ["+ cost() / desc()"],
                 "x": 430, "y": 650, "w": 360, "color": "#8B93B0"},
                {"id": "wh", "title": "Whip", "members": ["+ cost() / desc()"],
                 "x": 830, "y": 650, "w": 360, "color": "#8B93B0"},
                {"id": "ca", "title": "Caramel", "members": ["+ cost() / desc()"],
                 "x": 1230, "y": 650, "w": 360, "color": "#34D399"}],
            "edges": [
                {"from": "esp", "to": "bev", "kind": "impl"},
                {"from": "dec", "to": "bev", "kind": "impl"},
                {"from": "dec", "to": "bev", "kind": "has"},
                {"from": "mk", "to": "dec", "kind": "impl"},
                {"from": "wh", "to": "dec", "kind": "impl"},
                {"from": "ca", "to": "dec", "kind": "impl"}]},
         "narration":
            "Now we name it. [pause] This is the Decorator pattern. [pause] In the middle, the "
            "beverage interface — the fixed shape. [pause] On the left, the plain espresso, "
            "implementing it. [pause] On the right, the add-on. Look closely at it — it "
            "implements beverage, and it holds a beverage. That double arrow, both is-a and "
            "has-a, is the whole signature of the pattern. [pause] Underneath, your wrappers — "
            "milk, whip, and the green caramel you just added — each one a decorator you can "
            "stack as deep as you like."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Component", "your": "interface Beverage"},
                {"role": "ConcreteComponent", "your": "Espresso"},
                {"role": "Decorator (abstract)", "your": "AddOn (wraps a Beverage)"},
                {"role": "ConcreteDecorator", "your": "Milk, Whip, Caramel"}],
            "plain": "A decorator wraps a component, forwards to it, and adds a little before "
                     "or after — and is a component itself.",
            "gof": "Attach additional responsibilities to an object dynamically. Decorators "
                   "provide a flexible alternative to subclassing for extending functionality."},
         "narration":
            "The roles, mapped to your code. [pause] The Component is the beverage interface. "
            "[pause] The concrete component is the plain espresso. [pause] The Decorator is your "
            "abstract add-on, the one that wraps a beverage. [pause] And the concrete decorators "
            "are milk, whip, and caramel. [pause] In plain terms — a decorator wraps a "
            "component, forwards to it, and adds a little of its own, while being a component "
            "itself. [pause] The Gang of Four put it this way: attach extra responsibilities to "
            "an object dynamically — a flexible alternative to subclassing."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "It is not free",
            "costs": ["Many small classes and tiny objects",
                      "A deep stack is hard to debug",
                      "Order of wrapping can matter"],
            "dont": ["There is one fixed set of extras",
                     "Behavior never combines or repeats",
                     "A field or subclass truly suffices"],
            "signal": "responsibilities need to be added and combined at runtime, in "
                      "combinations you can't enumerate ahead of time."},
         "narration":
            "The honest costs. [pause] Decorator multiplies objects. A single latte can be four "
            "or five wrapped instances deep, and stepping through that stack in a debugger is "
            "not fun. [pause] And order can matter — tax around a discount is not the same as a "
            "discount around tax — so you have to think about it. [pause] Skip it when there is "
            "one fixed set of options that never combines or repeats. A plain field is simpler. "
            "[pause] The signal to reach for it: you need to add and combine responsibilities at "
            "runtime, in combinations you cannot list in advance. That is Decorator's home turf."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Decorator, in one breath",
            "items": [
                "Boolean flags for add-ons exploded across three methods — and could never "
                "model 'double caramel'.",
                "Each extra is really a layer that wraps a drink and adds a little — and is "
                "itself a drink.",
                "Decorator: wrap an object in another of the same type; stack wrappers freely. "
                "New extra, new wrapper."],
            "challenge": "You have an InputStream. You need it buffered, then gzip-compressed, "
                         "then encrypted — in different combinations per file.",
            "question": "Does Decorator fit? What's the component, and what are the wrappers?"},
         "narration":
            "The journey in three beats. [pause] The problem: boolean flags for add-ons "
            "exploded across three methods, and still could not express double caramel. [pause] "
            "The insight: each extra is really a layer that wraps a drink and adds a little — "
            "while being a drink itself. [pause] The pattern: Decorator. Wrap an object in "
            "another of the same type, and stack the wrappers as deep as you like. [pause] Now, "
            "for you, before the next episode. [pause] You have an input stream. For some files "
            "you need it buffered. For others, buffered then compressed. For others still, "
            "compressed then encrypted. [pause] Does Decorator fit? What is the component here — "
            "and what are the wrappers? [pause] Pause, and sketch it. And notice — Java's own "
            "streams already work exactly this way."},
    ],
}


# =====================================================================================
# dp04 — FACTORY METHOD   (creational; hardcoded `new Truck()` scattered everywhere)
# =====================================================================================
FACTORY_METHOD = {
    "id": "dp04-factory-method",
    "title": "Factory Method",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 04",
            "line1": "The word 'new' that", "line2": "leaks everywhere",
            "sub": "your delivery app only knows trucks — until the day it needs ships"},
         "narration":
            "There is one keyword that quietly welds your code to a single concrete class. "
            "[pause] The word new. [pause] Sprinkle it through your logic, and the day you need "
            "a second kind of thing, you will be hunting it down in a dozen places. [pause] "
            "Let's watch that happen to a delivery app."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "A logistics app plans deliveries",
            "situation": "Your app plans deliveries. Today, everything moves by road, so every "
                         "delivery creates a truck and tells it to go.",
            "actors": [
                {"emoji": "🚚", "label": "Truck (today)"},
                {"emoji": "🚢", "label": "Ship (soon)"},
                {"emoji": "🛩️", "label": "Drone (later)"}],
            "ask": "The planning logic is the same. Only the vehicle changes. Where's the seam?"},
         "narration":
            "You are building a logistics app that plans deliveries. [pause] Right now, "
            "everything goes by road. So every time you plan a delivery, you create a truck, "
            "and you tell it to deliver. [pause] Soon the company expands to sea freight. Then, "
            "eventually, drones. [pause] But notice — the planning steps barely change. Book it, "
            "route it, dispatch it. The only thing that really differs is which vehicle you "
            "create. [pause] So where is the seam between the two?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "Just new it up.",
            "file": "Logistics.java",
            "lines": ln(
                "class Logistics {",
                "  void planDelivery(Order order) {",
                "    route(order);",
                ("    Truck t = new Truck();     // hardcoded", "hi"),
                "    t.deliver(order);",
                "  }",
                "  // ...and new Truck() again in scheduleFleet(),",
                "  //    and again in estimateCost(). Everywhere.",
                "}"),
            "note": "Road-only, so 'new Truck()' feels harmless. It isn't."},
         "narration":
            "The obvious code just news up a truck, right where it is needed. [pause] Plan the "
            "route, create a truck, tell it to deliver. Done. [pause] And because everything is "
            "road today, that hardcoded new truck feels completely harmless. [pause] But that "
            "same line — new truck — is also sitting inside the method that schedules the "
            "fleet, and the one that estimates cost. [pause] The decision of which class to "
            "build is scattered across your whole codebase."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"We now ship by sea too.\"",
            "file": "Logistics.java",
            "lines": ln(
                "  void planDelivery(Order order) {",
                "    route(order);",
                ("    Transport t;", "hi"),
                ("    if (order.bySea())  t = new Ship();", "hi"),
                ("    else                t = new Truck();", "hi"),
                "    t.deliver(order);",
                "    // same if/else pasted into 3 other methods...",
                "  }"),
            "smell": "Creation logic tangled into business logic",
            "touched": ["planDelivery() — add if/else", "scheduleFleet() — same if/else",
                        "estimateCost() — same if/else", "add air? touch them all again"]},
         "narration":
            "Then the email arrives. We now ship by sea too. [pause] So you crack open plan "
            "delivery and add a branch. If it goes by sea, new ship, otherwise new truck. "
            "[pause] Fine — except that exact same if-else has to be pasted into schedule fleet, "
            "and estimate cost, and everywhere else you were creating a vehicle. [pause] Your "
            "business logic — planning, scheduling, costing — is now tangled up with the "
            "question of which class to construct. [pause] And when drones arrive next year? You "
            "reopen every single one of those methods again. [pause] The decision refuses to "
            "live in one place."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["The steps of planning a delivery",
                      "That a transport can deliver()",
                      "The workflow around it"],
            "varies": ["Which concrete vehicle is built",
                       "How many vehicle types exist",
                       "The rule for choosing one"],
            "principle": "Pull the 'which class to build' decision out of the workflow and "
                         "give it one overridable home."},
         "narration":
            "What changes, what stays fixed? [pause] The workflow is fixed. Plan, route, "
            "dispatch — those steps are identical no matter what moves the package. And every "
            "vehicle can deliver. [pause] What varies is only which concrete vehicle gets "
            "built, how many kinds there are, and the rule for picking one. [pause] So the fix "
            "is to take that one decision — which class to construct — and lift it out of the "
            "workflow entirely. [pause] Give it a single home that can be overridden, instead "
            "of a new keyword hiding in every method."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "Think of a franchise",
            "emoji": "🍔", "analogy": "Head office writes the recipe. Each branch sources locally.",
            "map": [
                {"from": "The head-office recipe", "to": "the fixed workflow"},
                {"from": "\"Get today's protein\"", "to": "an overridable create step"},
                {"from": "A branch's local supplier", "to": "a subclass's choice"},
                {"from": "Opening a new branch", "to": "a new subclass"}],
            "breaks": "a franchise recipe fixes many steps — here we hand exactly one step, "
                      "'make the product', to the subclass, and keep the rest shared."},
         "narration":
            "Think of a restaurant franchise. [pause] Head office writes the recipe — the exact "
            "steps every branch follows. But one step just says, get today's protein. [pause] "
            "The Tokyo branch sources fish. The Texas branch sources beef. Same recipe, "
            "different supplier, decided locally. [pause] That is our fix. The recipe is the "
            "fixed workflow. Get the protein is an overridable step. Each branch is a subclass "
            "that chooses its own vehicle. And opening a new branch is just writing a new "
            "subclass. [pause] Where it breaks: a real recipe fixes lots of steps. Here we hand "
            "exactly one step to the subclass — make the product — and keep everything else "
            "shared."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "A common product type",
            "file": "Transport.java",
            "lines": ln(
                ("interface Transport {", "add"),
                ("  void deliver(Order order);", "add"),
                ("}", "add"),
                "",
                ("class Truck implements Transport { /* ... */ }", "add"),
                ("class Ship  implements Transport { /* ... */ }", "add")),
            "note": "The workflow will only ever touch Transport, never Truck or Ship."},
         "narration":
            "Move one. We give every vehicle a common type. [pause] An interface, transport, "
            "with a deliver method. [pause] Truck implements it. Ship implements it. [pause] "
            "From now on, the planning code will only ever mention transport — never the "
            "concrete truck or ship. It just needs something that can deliver."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "One overridable creation step",
            "file": "Logistics.java",
            "lines": ln(
                ("abstract class Logistics {", "add"),
                ("  abstract Transport createTransport();  // the seam", "add"),
                "",
                "  void planDelivery(Order order) {",
                "    route(order);",
                ("    Transport t = createTransport();   // no 'new'", "add"),
                "    t.deliver(order);",
                "  }",
                "}"),
            "note": "planDelivery no longer says 'new'. It asks for a transport."},
         "narration":
            "Move two, and here is the heart of it. [pause] Logistics becomes abstract, and it "
            "declares one abstract method — create transport. That is the seam. [pause] Look at "
            "plan delivery now. It routes the order, then asks create transport for a vehicle, "
            "and tells it to deliver. [pause] The word new is gone. The workflow no longer knows "
            "or cares which vehicle it gets. It just trusts that some subclass will hand it "
            "one."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Write RoadLogistics",
            "file": "RoadLogistics.java",
            "lines": ln(
                "class RoadLogistics extends Logistics {",
                ("  // ▯ override createTransport() to build a Truck", "ghost"),
                "}"),
            "prompt": "Override createTransport() so road logistics builds a Truck.",
            "hint": "Transport createTransport() { return new Truck(); }"},
         "narration":
            "Your turn. [pause] Road logistics extends the abstract logistics. All it has to do "
            "is answer one question — what vehicle do I build? [pause] For road, the answer is a "
            "truck. Pause, and override create transport to return a new truck. [pause] That is "
            "the only place the word new for a truck now lives — inside the road subclass, and "
            "nowhere else."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "Each branch picks its vehicle",
            "file": "*Logistics.java",
            "lines": ln(
                ("class RoadLogistics extends Logistics {", "add"),
                ("  Transport createTransport() { return new Truck(); }", "add"),
                ("}", "add"),
                ("class SeaLogistics extends Logistics {", "add"),
                ("  Transport createTransport() { return new Ship(); }", "add"),
                ("}", "add"),
                "// planDelivery() is inherited, unchanged, by both."),
            "note": "Two subclasses, two choices. The workflow is written once."},
         "narration":
            "Move three. Each kind of logistics becomes a subclass with a single decision. "
            "[pause] Road logistics builds a truck. Sea logistics builds a ship. [pause] And "
            "plan delivery? Neither one rewrites it. They both inherit the exact same workflow, "
            "unchanged. [pause] The steps are written once, in the parent. The choice of vehicle "
            "is answered once, in each child."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Add drone delivery\" — the newest vehicle",
            "naiveLabel": "Before", "naiveCost": "A third branch in every creation site.",
            "naiveSteps": ["edit planDelivery's if/else", "edit scheduleFleet, estimateCost",
                           "hope you found them all"],
            "patLabel": "Now", "patCost": "One subclass. The workflow never moves.",
            "patFile": "AirLogistics.java",
            "patLines": ln(
                ("class AirLogistics", "add"),
                ("    extends Logistics {", "add"),
                ("  Transport createTransport() {", "add"),
                ("    return new Drone();", "add"),
                ("  }", "add"),
                ("}", "add"))},
         "narration":
            "Now the newest request. Add drone delivery. [pause] Before, that meant hunting down "
            "every if-else that chose a vehicle and adding a third branch — and praying you "
            "found them all. [pause] Now? One subclass. Air logistics, whose only job is to "
            "build a drone. [pause] Plan delivery, schedule fleet, estimate cost — none of them "
            "move. They inherit the workflow and simply receive a drone instead of a truck. "
            "[pause] A new vehicle became a new subclass. The business logic never even "
            "noticed."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Factory Method Pattern",
            "plain": "A parent defines the workflow and an overridable create step; each "
                     "subclass decides which concrete product that step builds.",
            "nodes": [
                {"id": "prod", "title": "Transport", "stereo": "interface",
                 "members": ["+ deliver(order)"], "x": 150, "y": 250, "w": 360, "color": "#22D3EE"},
                {"id": "creator", "title": "Logistics", "stereo": "abstract",
                 "members": ["+ createTransport()", "+ planDelivery()"],
                 "x": 760, "y": 220, "w": 430, "color": "#A78BFA"},
                {"id": "road", "title": "RoadLogistics", "members": ["+ createTransport()"],
                 "x": 430, "y": 640, "w": 360, "color": "#8B93B0"},
                {"id": "sea", "title": "SeaLogistics", "members": ["+ createTransport()"],
                 "x": 830, "y": 640, "w": 360, "color": "#8B93B0"},
                {"id": "air", "title": "AirLogistics", "members": ["+ createTransport()"],
                 "x": 1230, "y": 640, "w": 360, "color": "#34D399"}],
            "edges": [
                {"from": "creator", "to": "prod", "kind": "has"},
                {"from": "road", "to": "creator", "kind": "impl"},
                {"from": "sea", "to": "creator", "kind": "impl"},
                {"from": "air", "to": "creator", "kind": "impl"}]},
         "narration":
            "Now we name it. [pause] This is the Factory Method pattern. [pause] On the left, the "
            "product — the transport interface every vehicle shares. [pause] In the center, the "
            "creator — abstract logistics. It owns the workflow, plan delivery, and it declares "
            "the create transport step, pointing at the product it will build. [pause] "
            "Underneath, the concrete creators — road, sea, and the green air logistics you just "
            "added. Each overrides that one create step. [pause] The factory method is that "
            "single overridable line where a subclass chooses the concrete product."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Product", "your": "interface Transport"},
                {"role": "ConcreteProduct", "your": "Truck, Ship, Drone"},
                {"role": "Creator", "your": "abstract Logistics"},
                {"role": "ConcreteCreator", "your": "RoadLogistics, SeaLogistics, …"}],
            "plain": "The parent calls its own create step inside a fixed workflow; subclasses "
                     "override just that step to pick the product.",
            "gof": "Define an interface for creating an object, but let subclasses decide which "
                   "class to instantiate. Factory Method lets a class defer instantiation to "
                   "subclasses."},
         "narration":
            "The roles, mapped to your code. [pause] The Product is the transport interface. "
            "[pause] The concrete products are truck, ship, and drone. [pause] The Creator is "
            "your abstract logistics — it owns the workflow and the create step. [pause] And the "
            "concrete creators are road and sea logistics, each choosing a product. [pause] In "
            "plain terms — the parent calls its own create step inside a fixed workflow, and "
            "subclasses override only that step. [pause] The Gang of Four: define an interface "
            "for creating an object, but let subclasses decide which class to instantiate."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "Don't factory everything",
            "costs": ["A subclass for every product variant",
                      "More indirection to trace a 'new'",
                      "Parallel creator + product hierarchies"],
            "dont": ["There is only ever one product",
                     "A simple 'new' will never change",
                     "A static helper method is enough"],
            "signal": "a workflow is identical except for which object it constructs, and that "
                      "set of objects will grow."},
         "narration":
            "The honest costs. [pause] Factory Method needs a subclass for each product variant, "
            "so you can end up with two parallel family trees — creators on one side, products "
            "on the other. [pause] And it adds indirection: to find out what actually gets "
            "built, you have to follow the override. [pause] So do not factory everything. If "
            "there is only ever one product, and that new will never change, just write new — "
            "it is honest and clear. Sometimes a simple static helper is all you need. [pause] "
            "The signal to use it: a workflow that is identical every time, except for which "
            "object it constructs — and that set of objects keeps growing."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Factory Method, in one breath",
            "items": [
                "Hardcoded 'new Truck()' spread across the code; adding a vehicle meant editing "
                "every creation site.",
                "The workflow is fixed; only which class to build varies — so give that one "
                "decision an overridable home.",
                "Factory Method: the parent runs the workflow and calls a create step; each "
                "subclass picks the product."],
            "challenge": "A cross-platform UI toolkit runs the same 'render dialog' steps, but "
                         "must build Windows buttons on Windows and web buttons on the web.",
            "question": "Does Factory Method fit? What's the product, and who are the creators?"},
         "narration":
            "The journey in three beats. [pause] The problem: hardcoded new truck spread across "
            "the codebase, so adding a vehicle meant editing every place that built one. "
            "[pause] The insight: the workflow is fixed, and only the class you construct "
            "varies — so give that one decision a single, overridable home. [pause] The "
            "pattern: Factory Method. The parent runs the workflow and calls a create step, and "
            "each subclass decides which product that step builds. [pause] Now, for you, before "
            "the next episode. [pause] A cross-platform toolkit runs the very same steps to "
            "render a dialog — but it must build Windows buttons on Windows, and web buttons on "
            "the web. [pause] Does Factory Method fit? What is the product here, and who are the "
            "creators? [pause] Pause, and sketch it before you press play."},
    ],
}


# =====================================================================================
# dp05 — COMMAND   (behavioral; button handlers that can't be undone, queued, or logged)
# =====================================================================================
COMMAND = {
    "id": "dp05-command",
    "title": "Command",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 05",
            "line1": "You clicked the button.", "line2": "Now try to undo it.",
            "sub": "an editor where every action happens — but nothing can be taken back"},
         "narration":
            "Doing something is easy. Your button handler calls the code, and it happens. "
            "[pause] But the moment someone asks for undo — or redo, or a macro, or a queue — "
            "that simple handler falls apart. [pause] Because you threw away the one thing you "
            "needed: the action itself, as a thing you can hold. Let's build a text editor."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "A text editor's toolbar",
            "situation": "Your editor has toolbar buttons — bold, cut, paste. Each one changes "
                         "the document. Then the boss asks for Ctrl-Z: undo, and redo.",
            "actors": [
                {"emoji": "🔤", "label": "Bold"},
                {"emoji": "✂️", "label": "Cut"},
                {"emoji": "📋", "label": "Paste"}],
            "ask": "Every button works. Now make all of them undoable. From where?"},
         "narration":
            "You are writing a text editor. [pause] The toolbar has buttons — bold, cut, paste "
            "— and each one changes the document. [pause] They all work. Ship it. [pause] Then "
            "the request comes: control-Z. Undo. And of course, redo. And, while you are at it, "
            "let power users record a macro. [pause] Every button works today. Now make all of "
            "them undoable. [pause] Where does that even live?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "Handlers just do the work.",
            "file": "Editor.java",
            "lines": ln(
                "class Editor {",
                "  Document doc;",
                ("  void onBold()  { doc.applyBold(selection); }", "hi"),
                ("  void onCut()   { doc.cut(selection); }", "hi"),
                ("  void onPaste() { doc.paste(clipboard); }", "hi"),
                "  // click → change the document. Simple.",
                "}"),
            "note": "Each handler reaches straight into the document. Clean and direct."},
         "narration":
            "The obvious code wires each button straight to the work. [pause] On bold, apply "
            "bold. On cut, cut the selection. On paste, paste the clipboard. [pause] Click, and "
            "the document changes. It could not be more direct, and for just doing things, it "
            "is perfect. [pause] But look at what is missing. After on bold runs, there is no "
            "record that it ever happened. The action did its work and vanished."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Add undo and redo.\"",
            "file": "Editor.java",
            "lines": ln(
                "  enum Action { BOLD, CUT, PASTE }",
                ("  Deque<Action> history;", "hi"),
                "  void undo() {",
                ("    switch (history.pop()) {", "hi"),
                ('      case BOLD:  doc.removeBold(lastSel); break;', "hi"),
                ('      case CUT:   doc.restore(lastCut);    break;', "hi"),
                "      // ...and how do I know lastSel? lastCut?",
                "    }",
                "  }"),
            "smell": "No object holds 'what was done' + its data",
            "touched": ["a do-switch on every action", "an undo-switch, mirrored",
                        "store each action's data by hand", "redo? a third switch"]},
         "narration":
            "So you try to bolt on undo. [pause] You add an enum of actions, and a history stack "
            "to remember them. Then undo pops the last action and switches on it — if it was "
            "bold, remove bold; if it was cut, restore the cut text. [pause] But immediately it "
            "unravels. [pause] To undo bold, you need which selection it was applied to. To undo "
            "cut, you need the exact text you removed. [pause] None of that was saved — the "
            "action is long gone. [pause] So you start hoarding loose variables, last selection, "
            "last cut text, and a giant switch that must mirror every button perfectly. [pause] "
            "Add redo, and it is a third switch. This will rot."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["A request is made; do it",
                      "It may need to be reversed",
                      "The invoker just triggers it"],
            "varies": ["Which action it is",
                       "The data it needs to run and reverse",
                       "How you store or replay it"],
            "principle": "Turn the request itself into an object that carries how to do it — and "
                         "how to undo it."},
         "narration":
            "What changes, and what stays fixed? [pause] Fixed: a request gets made, and you do "
            "it. Sometimes you reverse it. And whatever triggers it — a button, a shortcut, a "
            "menu — just fires it, without knowing the details. [pause] What varies is which "
            "action it is, the data it needs to run and to reverse, and how you might store or "
            "replay it. [pause] So here is the move. [pause] Stop treating the action as a "
            "method call that evaporates. Make the request itself an object — one that carries "
            "both how to do it, and how to undo it, together in one place."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "Think of an order ticket",
            "emoji": "🧾", "analogy": "The waiter writes a ticket. The ticket can be re-fired or voided.",
            "map": [
                {"from": "Writing the ticket", "to": "creating a Command"},
                {"from": "The waiter", "to": "the invoker (a button)"},
                {"from": "The kitchen", "to": "the receiver (the Document)"},
                {"from": "The spike of tickets", "to": "the undo history"}],
            "breaks": "a paper ticket can't un-cook a meal — our command also carries the "
                      "recipe for reversing itself."},
         "narration":
            "Picture a diner. [pause] The waiter does not cook. They write your order on a "
            "ticket, and the ticket goes to the kitchen. [pause] And because the order is now a "
            "physical thing, you can do things with it — stack it, re-fire it, void it, keep it "
            "on a spike as a record. [pause] That is our fix. Writing the ticket is creating a "
            "command object. The waiter is the button that fires it. The kitchen is the "
            "document that actually does the work. And the spike of old tickets is your undo "
            "history. [pause] Where it breaks: a paper ticket cannot un-cook a steak. Our "
            "command is smarter — it also carries the recipe for reversing itself."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "A request becomes an object",
            "file": "Command.java",
            "lines": ln(
                "// the request itself, with both directions:",
                ("interface Command {", "add"),
                ("  void execute();", "add"),
                ("  void undo();", "add"),
                ("}", "add")),
            "note": "Do and undo, bound together — that pairing is the whole idea."},
         "narration":
            "Move one. We turn the request into an object. [pause] An interface, command, with "
            "two methods — execute, and undo. [pause] That pairing is everything. Do and undo, "
            "bound together in one type. [pause] From now on, an action is not something that "
            "happens and disappears. It is a thing you can hold, store, and reverse."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "Each command captures its own data",
            "file": "BoldCommand.java",
            "lines": ln(
                ("class BoldCommand implements Command {", "add"),
                ("  private final Document doc;", "add"),
                ("  private final Range selection;   // captured!", "add"),
                ("  public void execute() { doc.applyBold(selection); }", "add"),
                ("  public void undo()    { doc.removeBold(selection); }", "add"),
                "}"),
            "note": "The selection it needs to undo is stored inside the command itself."},
         "narration":
            "Move two, and this is what fixes the undo mess. [pause] A bold command holds the "
            "document, and the exact selection it was told to bold. [pause] Its execute applies "
            "bold to that selection. Its undo removes bold from that same selection. [pause] The "
            "data you were scrambling to remember by hand? It lives inside the command, captured "
            "the moment it was created. Every command carries everything it needs to reverse "
            "itself."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Write PasteCommand.undo()",
            "file": "PasteCommand.java",
            "lines": ln(
                "class PasteCommand implements Command {",
                "  Document doc; String pasted; int at;",
                "  public void execute() { doc.insert(pasted, at); }",
                ("  // ▯ undo(): remove what you inserted", "ghost"),
                "}"),
            "prompt": "Write undo() — delete the text this command pasted, at its position.",
            "hint": "public void undo() { doc.delete(at, pasted.length()); }"},
         "narration":
            "Your turn. [pause] Here is a paste command. Its execute inserts the pasted text at "
            "a position — and it remembers both the text and the spot. [pause] Write its undo. "
            "[pause] To reverse a paste, you delete exactly what you inserted, right where you "
            "put it. Pause, and write it. [pause] Because the command captured the text and the "
            "position, undo is trivial — delete that length, at that spot. That is the power of "
            "making the request an object."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "The invoker just runs and stacks them",
            "file": "Editor.java",
            "lines": ln(
                "class Editor {",
                ("  private final Deque<Command> history = new ArrayDeque<>();", "add"),
                ("  void run(Command c) {", "add"),
                ("    c.execute();", "add"),
                ("    history.push(c);          // remember it", "add"),
                ("  }", "add"),
                ("  void undo() { history.pop().undo(); }   // that's it", "add"),
                "}"),
            "note": "One run(), one undo() — and they work for every command, forever."},
         "narration":
            "Move three. Now the editor gets beautifully dumb. [pause] It keeps a history stack "
            "of commands. To run one, it calls execute, then pushes it onto the stack. [pause] "
            "And undo? Pop the last command, and call its undo. One line. [pause] Look at what "
            "is gone — no enum, no switch, no mirrored reverse logic. [pause] And here is the "
            "magic: this run and undo work for every command that exists, and every command you "
            "will ever add, without changing a character."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Add a Cut button\" — and it must undo, redo, and record",
            "naiveLabel": "Before", "naiveCost": "A new case in the do-, undo-, and redo-switch.",
            "naiveSteps": ["add to the do-switch", "mirror it in undo + redo",
                           "stash its data by hand"],
            "patLabel": "Now", "patCost": "One CutCommand. Undo, redo, macros — all free.",
            "patFile": "CutCommand.java",
            "patLines": ln(
                ("class CutCommand", "add"),
                ("    implements Command {", "add"),
                ("  Document doc; Range sel; String cut;", "add"),
                ("  public void execute() {", "add"),
                ("    cut = doc.cut(sel);", "add"),
                ("  }", "add"),
                ("  public void undo() { doc.insert(cut, sel.start); }", "add"),
                ("}", "add"))},
         "narration":
            "Now the newest request. Add a cut button — and naturally, it must undo, redo, and "
            "work in macros. [pause] Before, that was a new case in three different switches, "
            "plus more loose variables to stash the cut text. [pause] Now? One cut command. Its "
            "execute cuts and remembers the text. Its undo puts it back. [pause] And that is the "
            "whole job. [pause] Undo already works, because the editor just calls undo. Redo, "
            "macros, a command queue — all of them work the instant the command exists, with "
            "zero changes to the editor. You added one class, and got four features."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Command Pattern",
            "plain": "Wrap a request in an object with execute() and undo(); an invoker runs and "
                     "stores it, a receiver does the real work.",
            "nodes": [
                {"id": "cmd", "title": "Command", "stereo": "interface",
                 "members": ["+ execute()", "+ undo()"], "x": 760, "y": 215, "w": 400, "color": "#22D3EE"},
                {"id": "inv", "title": "Editor", "stereo": "invoker",
                 "members": ["- history: Deque", "+ run(c) / undo()"],
                 "x": 150, "y": 230, "w": 430, "color": "#A78BFA"},
                {"id": "bold", "title": "BoldCommand", "members": ["+ execute() / undo()"],
                 "x": 430, "y": 650, "w": 360, "color": "#8B93B0"},
                {"id": "paste", "title": "PasteCommand", "members": ["+ execute() / undo()"],
                 "x": 830, "y": 650, "w": 360, "color": "#8B93B0"},
                {"id": "cut", "title": "CutCommand", "members": ["+ execute() / undo()"],
                 "x": 1230, "y": 650, "w": 360, "color": "#34D399"}],
            "edges": [
                {"from": "inv", "to": "cmd", "kind": "has"},
                {"from": "bold", "to": "cmd", "kind": "impl"},
                {"from": "paste", "to": "cmd", "kind": "impl"},
                {"from": "cut", "to": "cmd", "kind": "impl"}]},
         "narration":
            "Now we name it. [pause] This is the Command pattern. [pause] In the middle, the "
            "command interface — execute, and undo. [pause] On the left, the editor, the "
            "invoker. It holds a history and just runs commands; it points only at the "
            "interface. [pause] Underneath, the concrete commands — bold, paste, and the green "
            "cut you just added — each one bundling an action with the data to reverse it. "
            "[pause] Not shown here, but named in each command, is the receiver — the document "
            "that does the actual work."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Command", "your": "interface Command"},
                {"role": "ConcreteCommand", "your": "BoldCommand, CutCommand, …"},
                {"role": "Invoker", "your": "Editor (runs + stores)"},
                {"role": "Receiver", "your": "Document (does the work)"}],
            "plain": "The invoker triggers a command object; the command tells the receiver what "
                     "to do, and remembers how to undo it.",
            "gof": "Encapsulate a request as an object, thereby letting you parameterize clients "
                   "with different requests, queue or log requests, and support undoable "
                   "operations."},
         "narration":
            "The roles, mapped to your code. [pause] The Command is your interface. [pause] The "
            "concrete commands are bold, cut, and paste. [pause] The Invoker is the editor — it "
            "triggers commands and keeps the history, but never knows what they do. [pause] And "
            "the Receiver is the document, which does the actual work when a command tells it "
            "to. [pause] In plain terms — the invoker fires a command, the command directs the "
            "receiver, and remembers how to undo. [pause] The Gang of Four: encapsulate a "
            "request as an object — which lets you queue it, log it, and undo it."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "The price of the ticket",
            "costs": ["A class for every kind of request",
                      "Undo state can grow large in memory",
                      "Indirection between click and effect"],
            "dont": ["The action never needs undo or replay",
                     "A direct method call is plenty",
                     "There's exactly one, simple handler"],
            "signal": "you need undo/redo, queuing, logging, or macros — anything that treats "
                      "'an action' as a value you store."},
         "narration":
            "The honest costs. [pause] Command means a class for every kind of request, so a "
            "big app grows a lot of little command classes. [pause] And keeping undo history "
            "means keeping state — a long editing session can hold a lot of it in memory. "
            "[pause] Plus there is a hop between the click and the effect, which is one more "
            "thing to trace. [pause] So skip it when an action never needs to be undone, "
            "queued, or replayed — a direct call is simpler and honest. [pause] But the signal "
            "is crystal clear. The moment you need undo, redo, queuing, logging, or macros — "
            "anything that treats an action as a value you can store — reach for Command."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Command, in one breath",
            "items": [
                "Button handlers did the work and vanished, so undo needed mirrored switches "
                "and hand-stashed data.",
                "A request should be an object that carries how to do AND undo it, with the "
                "data it needs inside.",
                "Command: invoker runs and stores command objects; each reverses itself. New "
                "action, new command."],
            "challenge": "A design tool needs multi-level undo, plus the ability to record a "
                         "sequence of edits and replay it as a one-click macro.",
            "question": "Does Command fit? What's the command, and who is the invoker?"},
         "narration":
            "The journey in three beats. [pause] The problem: button handlers did the work and "
            "vanished, so adding undo meant mirrored switches and a pile of hand-stashed data. "
            "[pause] The insight: a request should be an object that carries how to do it and "
            "how to undo it, with all its data inside. [pause] The pattern: Command. An invoker "
            "runs and stores command objects, and each one knows how to reverse itself — so a "
            "new action is just a new command. [pause] Now, for you, before the next episode. "
            "[pause] A design tool needs multi-level undo, and it wants to record a sequence of "
            "edits and replay them as a one-click macro. [pause] Does Command fit? What is the "
            "command here, and who is the invoker? [pause] Pause, and sketch it before you press "
            "play."},
    ],
}


# =====================================================================================
# dp06 — ADAPTER   (structural; a third-party SDK whose shape you can't change)
# =====================================================================================
ADAPTER = {
    "id": "dp06-adapter",
    "title": "Adapter",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 06",
            "line1": "Two interfaces that", "line2": "refuse to fit",
            "sub": "your checkout speaks one language; the new payment SDK speaks another"},
         "narration":
            "Sometimes the problem is not your code at all. [pause] It is a library you did not "
            "write, cannot change, and absolutely must use — and its shape is all wrong for "
            "yours. [pause] Force them together directly, and the mismatch bleeds into every "
            "corner of your app. There is a clean seam for exactly this. Let's take a payment."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "Adding a new payment provider",
            "situation": "Your checkout already charges cards through a clean PaymentGateway "
                         "interface. Now the business wants PayPal — whose SDK looks nothing "
                         "like yours, and you can't edit it.",
            "actors": [
                {"emoji": "💳", "label": "Your interface"},
                {"emoji": "🅿️", "label": "PayPal SDK"},
                {"emoji": "🔌", "label": "?"}],
            "ask": "Same goal — take a payment. Totally different shapes. Now what?"},
         "narration":
            "Your checkout already takes card payments. [pause] It does it through a clean "
            "interface you designed — a payment gateway, with a charge method that takes an "
            "amount and returns a receipt. Lovely. [pause] Now the business wants PayPal. "
            "[pause] So you pull in PayPal's official SDK — and its class looks nothing like "
            "yours. Different method name. Money in cents, not dollars. Its own response type. "
            "[pause] And you cannot change a line of it. It is a library. [pause] Same goal, "
            "take a payment. Completely different shapes. Now what?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "Just translate it inline.",
            "file": "Checkout.java",
            "lines": ln(
                "void pay(Order order) {",
                "  if (order.usesPayPal()) {",
                ('    long cents = (long)(order.total() * 100);', "hi"),
                ('    PayPalResponse r =', "hi"),
                ('        paypal.sendPayment("USD", cents);', "hi"),
                ('    if (!r.ok()) throw new PaymentError(r.msg());', "hi"),
                "  } else {",
                "    stripe.charge(order.total());",
                "  }",
                "}"),
            "note": "It works — PayPal's quirks translated right where you need them."},
         "narration":
            "The quickest fix: just translate it, right here in checkout. [pause] If the order "
            "uses PayPal, convert the dollars to cents, call send payment with a currency "
            "string, then unpack PayPal's response and turn a failure into your own error. "
            "Otherwise, use the normal charge. [pause] And it works. [pause] But look at what "
            "you have done. PayPal's cents, its currency codes, its response type — all of "
            "PayPal's quirks are now sitting inside your checkout logic."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Add PayPal to refunds too. And receipts.\"",
            "file": "everywhere.java",
            "lines": ln(
                "// refund flow:",
                ('if (order.usesPayPal()) {', "dim"),
                ('  paypal.reverse(txId, (long)(amt*100));  // again', "hi"),
                "} else { stripe.refund(txId, amt); }",
                "// receipt flow, reporting flow, webhook flow...",
                ('if (order.usesPayPal()) { /* translate AGAIN */ }', "hi")),
            "smell": "A foreign shape leaking into every flow",
            "touched": ["pay() — translate cents/currency", "refund() — translate again",
                        "receipts, webhooks, reports…", "add Razorpay? every flow again"]},
         "narration":
            "Then it spreads, the way these things do. [pause] Refunds need PayPal too — so the "
            "same dollars-to-cents dance, the same response unpacking, copied into the refund "
            "flow. [pause] Then receipts. Then reporting. Then webhooks. [pause] Every single "
            "flow that touches money now has an if-PayPal branch, translating the same quirks "
            "over and over. [pause] The foreign shape has leaked into your entire codebase. "
            "[pause] And when the company adds Razorpay next quarter — a third shape — you get "
            "to do all of it a third time. This is untenable."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["Your interface: charge, get a receipt",
                      "Everything that calls it",
                      "The idea of 'take a payment'"],
            "varies": ["Each SDK's method names and types",
                       "Dollars vs cents, response shapes",
                       "How many providers you support"],
            "principle": "Translate the foreign shape in ONE place — an object that speaks your "
                         "interface on the outside."},
         "narration":
            "What changes, and what stays fixed? [pause] Your side is fixed. You have a payment "
            "gateway interface — charge an amount, get a receipt — and a whole app that speaks "
            "it. [pause] What varies is each provider's shape. Its method names, its cents, its "
            "response types, and how many of them there are. [pause] So the fix is almost "
            "obvious once you see it. [pause] Do the translation exactly once, hidden inside one "
            "object — a thing that looks like PayPal on the inside, but speaks your interface on "
            "the outside."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "Think of a travel plug adapter",
            "emoji": "🔌", "analogy": "Your plug on one side, the foreign socket on the other.",
            "map": [
                {"from": "Your appliance's plug", "to": "your PaymentGateway interface"},
                {"from": "The foreign wall socket", "to": "the PayPal SDK"},
                {"from": "The little adapter", "to": "a PayPalAdapter class"},
                {"from": "Plug in, it just works", "to": "checkout stays unchanged"}],
            "breaks": "a plug adapter only reshapes the pins — a code adapter often converts the "
                      "signal too, like dollars into cents and back."},
         "narration":
            "You already own the perfect picture for this. A travel plug adapter. [pause] Your "
            "laptop has one kind of plug. The hotel wall has a different socket. The little "
            "adapter fits your plug on one side and the foreign socket on the other — and your "
            "laptop neither knows nor cares. [pause] That is the fix exactly. Your plug is your "
            "payment interface. The foreign socket is PayPal's SDK. And the adapter is a small "
            "class that bridges them. [pause] Where does the picture break? A plug adapter only "
            "reshapes the pins. A software adapter usually converts the signal too — turning "
            "your dollars into their cents, and their response back into your receipt."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "Your side already has a shape",
            "file": "PaymentGateway.java",
            "lines": ln(
                "// the shape your whole app speaks:",
                ("interface PaymentGateway {", "add"),
                ("  Receipt charge(double amount);", "add"),
                ("}", "add"),
                "",
                ("class StripeGateway implements PaymentGateway { /*ok*/ }", "add")),
            "note": "Stripe already fits. The target interface is the plug shape."},
         "narration":
            "Move one. Notice you already have the target shape. [pause] Your payment gateway "
            "interface — charge an amount, return a receipt. [pause] Stripe already implements "
            "it cleanly, because it happened to fit. [pause] This interface is the plug. "
            "Everything downstream expects this shape and nothing else. Our job is to make "
            "PayPal fit it too — without touching PayPal, and without touching checkout."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "An adapter that speaks both",
            "file": "PayPalAdapter.java",
            "lines": ln(
                ("class PayPalAdapter implements PaymentGateway {", "add"),
                ("  private final PayPalClient paypal;   // the foreign SDK", "add"),
                ("  public Receipt charge(double amount) {", "add"),
                ("    long cents = (long)(amount * 100);        // convert", "add"),
                ('    PayPalResponse r = paypal.sendPayment("USD", cents);', "add"),
                ("    return Receipt.from(r);                   // convert back", "add"),
                ("  }", "add"),
                "}"),
            "note": "Your interface on the outside; PayPal's mess sealed on the inside."},
         "narration":
            "Move two — the whole pattern in one class. [pause] The PayPal adapter implements "
            "your payment gateway, so from the outside it looks exactly like Stripe. [pause] "
            "Inside, it holds a PayPal client — the foreign SDK. [pause] Its charge method does "
            "the translation you were scattering everywhere: dollars to cents, call send "
            "payment, then turn PayPal's response back into your receipt. [pause] All of "
            "PayPal's quirks are now sealed inside this one class. Your interface faces out; "
            "the mess faces in."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Adapt the refund",
            "file": "PayPalAdapter.java",
            "lines": ln(
                "public Receipt refund(String txId, double amount) {",
                ("  // ▯ convert to cents, call paypal.reverse(...)", "ghost"),
                "}"),
            "prompt": "Write refund(): convert dollars to cents, call PayPal's reverse.",
            "hint": "long c = (long)(amount*100); return Receipt.from(paypal.reverse(txId, c));"},
         "narration":
            "Your turn. [pause] The adapter should handle refunds too. Here is the refund "
            "method, empty. [pause] It is the same idea as charge — convert the dollars to "
            "cents, then call PayPal's reverse with the transaction id, and wrap the result in "
            "a receipt. [pause] Pause, and write it. [pause] Notice you are doing the "
            "translation here, once — so that no refund flow anywhere else ever has to know "
            "PayPal uses cents."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "Checkout goes back to being simple",
            "file": "Checkout.java",
            "lines": ln(
                ("void pay(Order order, PaymentGateway gateway) {", "add"),
                ("  Receipt r = gateway.charge(order.total());   // that's all", "add"),
                "}",
                "",
                "// wiring, at the edge — checkout never sees PayPal:",
                ("PaymentGateway g = order.usesPayPal()", "add"),
                ("    ? new PayPalAdapter(paypal)", "add"),
                ("    : new StripeGateway();", "add")),
            "note": "Every 'if PayPal' branch across the app collapses to one line at the edge."},
         "narration":
            "Move three. Now watch checkout heal. [pause] Pay just takes a payment gateway and "
            "calls charge. One line. No cents, no currency codes, no response unpacking. It has "
            "no idea PayPal exists. [pause] The only place that chooses PayPal is the wiring, "
            "once, at the edge of the system. [pause] And every one of those if-PayPal branches "
            "— in refunds, receipts, reports, webhooks — collapses. They all just call charge, "
            "or refund, on the gateway."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Add Razorpay\" — a third provider, third shape",
            "naiveLabel": "Before", "naiveCost": "A third translate-branch in every money flow.",
            "naiveSteps": ["add if-Razorpay to pay()", "and refund, receipts, webhooks",
                           "translate its shape each time"],
            "patLabel": "Now", "patCost": "One adapter class. Every flow already works.",
            "patFile": "RazorpayAdapter.java",
            "patLines": ln(
                ("class RazorpayAdapter", "add"),
                ("    implements PaymentGateway {", "add"),
                ("  private final RazorpaySdk rz;", "add"),
                ("  public Receipt charge(double amt) {", "add"),
                ("    return Receipt.from(", "add"),
                ("        rz.pay(amt, Currency.USD));", "add"),
                ("  }", "add"),
                ("}", "add"))},
         "narration":
            "Now the third provider. Add Razorpay — yet another shape. [pause] Before, that "
            "meant a third branch in pay, and refund, and receipts, and webhooks, translating "
            "Razorpay's quirks in every one. [pause] Now? One adapter class. It implements your "
            "gateway, wraps Razorpay's SDK, and translates inside. [pause] And that is the "
            "entire change. [pause] Checkout, refunds, reporting — none of them move. They "
            "already speak to a payment gateway, and Razorpay is now just another one. A new "
            "provider became a single new class."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Adapter Pattern",
            "plain": "Wrap an incompatible class in one that implements the interface your code "
                     "expects, translating between the two.",
            "nodes": [
                {"id": "target", "title": "PaymentGateway", "stereo": "interface",
                 "members": ["+ charge(amount): Receipt"], "x": 720, "y": 210, "w": 440, "color": "#22D3EE"},
                {"id": "adaptee", "title": "PayPalClient", "stereo": "external SDK",
                 "members": ["+ sendPayment(cur, cents)"], "x": 1420, "y": 250, "w": 380, "color": "#FBBF24"},
                {"id": "stripe", "title": "StripeGateway", "members": ["+ charge()"],
                 "x": 200, "y": 650, "w": 340, "color": "#8B93B0"},
                {"id": "ppa", "title": "PayPalAdapter", "members": ["+ charge()  → translates"],
                 "x": 720, "y": 650, "w": 440, "color": "#A78BFA"},
                {"id": "rza", "title": "RazorpayAdapter", "members": ["+ charge()"],
                 "x": 1340, "y": 650, "w": 380, "color": "#34D399"}],
            "edges": [
                {"from": "stripe", "to": "target", "kind": "impl"},
                {"from": "ppa", "to": "target", "kind": "impl"},
                {"from": "rza", "to": "target", "kind": "impl"},
                {"from": "ppa", "to": "adaptee", "kind": "has"}]},
         "narration":
            "Now we name it. [pause] This is the Adapter pattern. [pause] At the top, your "
            "target — the payment gateway your app speaks. [pause] On the right, the adaptee — "
            "PayPal's external SDK, in amber, the shape you cannot change. [pause] And in the "
            "middle-bottom, the adapter. Look at its two arrows. It implements your interface, "
            "and it holds the foreign SDK. [pause] That is the signature — it faces your code "
            "with your shape, and faces PayPal with PayPal's. Stripe fits natively; the green "
            "Razorpay adapter is the one you just added."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Target", "your": "interface PaymentGateway"},
                {"role": "Adaptee", "your": "PayPalClient (external SDK)"},
                {"role": "Adapter", "your": "PayPalAdapter"},
                {"role": "Client", "your": "checkout — speaks Target only"}],
            "plain": "The adapter implements the target and delegates to the adaptee, converting "
                     "calls and data between the two shapes.",
            "gof": "Convert the interface of a class into another interface clients expect. "
                   "Adapter lets classes work together that couldn't otherwise because of "
                   "incompatible interfaces."},
         "narration":
            "The roles, mapped to your code. [pause] The Target is your payment gateway "
            "interface — the shape you want. [pause] The Adaptee is PayPal's SDK — the shape "
            "you have. [pause] The Adapter is the class that bridges them. [pause] And the "
            "Client is your checkout, which only ever speaks the target. [pause] In plain "
            "terms — the adapter implements your interface and delegates to the foreign class, "
            "converting between the two. [pause] The Gang of Four: convert the interface of a "
            "class into another interface clients expect, so incompatible classes can work "
            "together."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "It's glue, not magic",
            "costs": ["One more layer of indirection",
                      "Leaky abstractions if shapes differ deeply",
                      "A class per external provider"],
            "dont": ["You own both sides — just change one",
                     "The interfaces already match",
                     "It's a one-off, throwaway call"],
            "signal": "you must use a class you can't change, and its interface doesn't match "
                      "the one your code already speaks."},
         "narration":
            "The honest costs. [pause] An adapter is a layer of glue, and glue is still code to "
            "maintain — a class for every external provider. [pause] And if the two shapes "
            "differ deeply — say one is asynchronous and one is not — the abstraction can leak, "
            "and the adapter gets complicated. [pause] So skip it when you own both sides. If "
            "you can just change one interface to match, do that — an adapter would be "
            "ceremony. And do not build one for a single throwaway call. [pause] The signal is "
            "specific. You must use a class you cannot change, and its interface does not match "
            "the one your code already speaks. That gap is exactly what Adapter fills."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Adapter, in one breath",
            "items": [
                "A third-party SDK's shape — cents, odd methods, its own responses — leaked its "
                "quirks into every money flow.",
                "Your interface is fixed; only the foreign shapes vary — so translate them in "
                "one place, behind your interface.",
                "Adapter: a class that implements your target and wraps the foreign one, "
                "converting between them. New SDK, new adapter."],
            "challenge": "Your app logs through a clean Logger interface. Ops wants everything "
                         "sent to a third-party service whose client is a totally different "
                         "shape you can't modify.",
            "question": "Does Adapter fit? What's the target, and what's the adaptee?"},
         "narration":
            "The journey in three beats. [pause] The problem: a third-party SDK's shape — its "
            "cents, its odd method names, its own response type — leaked into every flow that "
            "touched money. [pause] The insight: your interface is fixed, and only the foreign "
            "shapes vary, so translate them once, behind your interface. [pause] The pattern: "
            "Adapter. A class that implements your target and wraps the foreign one, converting "
            "between them — so a new SDK is just a new adapter. [pause] Now, for you, before the "
            "next episode. [pause] Your app logs through a clean logger interface. Ops wants "
            "every log shipped to a third-party service whose client is a completely different "
            "shape you cannot modify. [pause] Does Adapter fit? What is the target here, and "
            "what is the adaptee? [pause] Pause, and sketch it before you press play."},
    ],
}


# =====================================================================================
# dp07 — STATE   (behavioral; the same switch(status) copied into every method)
# =====================================================================================
STATE = {
    "id": "dp07-state",
    "title": "State",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 07",
            "line1": "The same switch,", "line2": "in every method",
            "sub": "an order that behaves differently depending on where it is in its life"},
         "narration":
            "Here is a class where one field — a status string — secretly controls everything. "
            "[pause] And because it does, the exact same switch on that field ends up copied "
            "into every method, each with slightly different rules. [pause] Change the "
            "lifecycle, and you are editing all of them at once. There is a way to make the "
            "states themselves do the work. Let's follow an order."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "An order moves through its life",
            "situation": "An order is placed, paid, shipped, delivered — or cancelled. The same "
                         "actions (pay, ship, cancel) mean different things depending on where "
                         "the order currently is.",
            "actors": [
                {"emoji": "🆕", "label": "New"},
                {"emoji": "💰", "label": "Paid"},
                {"emoji": "📦", "label": "Shipped"}],
            "ask": "You can't ship an unpaid order, or cancel a delivered one. Who enforces that?"},
         "narration":
            "Every order lives a little life. [pause] It is placed, then paid, then shipped, "
            "then delivered. Or, somewhere along the way, cancelled. [pause] And the same three "
            "actions — pay, ship, cancel — mean completely different things depending on where "
            "the order currently is. [pause] You cannot ship an order that is not paid. You "
            "cannot cancel one that already arrived. [pause] So the real question is: who "
            "enforces all those rules about what is allowed, and when?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "A status field and some checks.",
            "file": "Order.java",
            "lines": ln(
                "class Order {",
                '  String status = "NEW";',
                "  void ship() {",
                ('    if (status.equals("PAID")) status = "SHIPPED";', "hi"),
                ('    else throw new IllegalState("can\'t ship: " + status);', "hi"),
                "  }",
                "  void pay()    { /* its own switch on status */ }",
                "  void cancel() { /* its own switch on status */ }",
                "}"),
            "note": "Each action checks the status, acts, and sets the next one. Reasonable."},
         "narration":
            "The obvious approach: a status string, and a check in each method. [pause] To ship, "
            "make sure the order is paid, then move it to shipped — otherwise, refuse. [pause] "
            "Pay has its own version of that check. So does cancel. [pause] Each action looks at "
            "the status, decides if it is legal, does the work, and sets the next status. "
            "[pause] For four states and three actions, this is perfectly reasonable. Until the "
            "lifecycle grows."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Add an 'awaiting stock' state.\"",
            "file": "Order.java",
            "lines": ln(
                '  void pay() {    // must handle AWAITING_STOCK now',
                ('    if (status.equals("NEW")) status = inStock()', "dim"),
                ('        ? "PAID" : "AWAITING_STOCK";', "hi"),
                "  }",
                '  void ship()   { /* + AWAITING_STOCK case */ }',
                ('  void cancel() { /* + AWAITING_STOCK case */ }', "hi"),
                '  void restock(){ /* a whole new action, everywhere */ }'),
            "smell": "The state machine is invisible + smeared",
            "touched": ["pay() — new branch", "ship() — new branch",
                        "cancel() — new branch", "miss one → illegal transition ships"]},
         "narration":
            "Then a new requirement. Some paid orders are out of stock, so we need an awaiting "
            "stock state. [pause] Now pay has to decide between paid and awaiting stock. Ship "
            "has to handle the new state. So does cancel. And you add a whole new action, "
            "restock, which needs its own switch too. [pause] The transition rules are "
            "scattered across every method, and nowhere can you see the state machine as a "
            "whole. [pause] Worst of all — miss a single case, and an order slips into an "
            "illegal state, and ships when it never should have. [pause] The status field looks "
            "innocent, but it is quietly running a state machine that no one can see."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["An order responds to pay, ship, cancel",
                      "It is always in exactly one state",
                      "The context just forwards the action"],
            "varies": ["What each action DOES right now",
                       "Which transition is allowed",
                       "The set of states itself"],
            "principle": "Give each state its own class that knows its own actions and its own "
                         "next state."},
         "narration":
            "What changes, and what stays fixed? [pause] Fixed: an order always responds to the "
            "same three actions, and it is always in exactly one state. And whatever calls it "
            "just says, pay, or ship — it forwards the action. [pause] What varies is what each "
            "action actually does right now, which transitions are legal, and the set of states "
            "itself. [pause] All of that depends entirely on the current state. [pause] So here "
            "is the move. Stop scattering the rules by action. [pause] Instead, give each state "
            "its own class — one that knows its own behavior, and knows which state comes next."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "Think of a traffic light",
            "emoji": "🚦", "analogy": "Each colour knows what it allows, and what turns next.",
            "map": [
                {"from": "The pole and housing", "to": "the Order (the context)"},
                {"from": "Red / amber / green", "to": "each State class"},
                {"from": "\"What comes after me\"", "to": "the state returns the next state"},
                {"from": "Only the colour changes", "to": "swap the current state object"}],
            "breaks": "a traffic light changes itself on a timer — here an external action, like "
                      "'pay', triggers the transition."},
         "narration":
            "Picture a traffic light. [pause] The pole does not contain a giant rulebook. Each "
            "colour carries its own rules. Red means stop, and red knows that green comes next. "
            "Green knows amber follows. [pause] The light itself just holds whichever colour is "
            "active, and swaps it. [pause] That is the fix. The order is the pole. Each state — "
            "new, paid, shipped — is a colour that knows its own behavior and its own next "
            "state. And a transition is just swapping which state object is current. [pause] "
            "Where it breaks: a real light changes itself on a timer. Our order changes when an "
            "outside action, like pay, triggers it."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "Each state is a type",
            "file": "OrderState.java",
            "lines": ln(
                "// each action returns the state to move to:",
                ("interface OrderState {", "add"),
                ("  OrderState pay();", "add"),
                ("  OrderState ship();", "add"),
                ("  OrderState cancel();", "add"),
                ("}", "add")),
            "note": "Return-type is the trick: an action hands back the NEXT state."},
         "narration":
            "Move one. Every state becomes a type. [pause] An interface, order state, with the "
            "three actions — pay, ship, cancel. [pause] But notice the return type. Each action "
            "returns an order state. [pause] That is the whole trick. Performing an action does "
            "not just do work — it hands back the state you should move to next. The transition "
            "is baked right into the return value."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "Each state owns its rules",
            "file": "states.java",
            "lines": ln(
                ("class NewState implements OrderState {", "add"),
                ("  public OrderState pay()    { return new PaidState(); }", "add"),
                ('  public OrderState ship()   { throw new IllegalState("unpaid"); }', "add"),
                ("  public OrderState cancel() { return new CancelledState(); }", "add"),
                "}",
                ("class PaidState implements OrderState {", "add"),
                ("  public OrderState ship() { return new ShippedState(); }", "add"),
                "}"),
            "note": "From New: paying → Paid; shipping is illegal. The rules live in one place."},
         "narration":
            "Move two. Each state owns its own rules, completely. [pause] Look at the new state. "
            "Paying it returns a paid state. Cancelling returns a cancelled state. And "
            "shipping? Shipping throws — you cannot ship an unpaid order, and that rule lives "
            "right here, where it belongs. [pause] The paid state is different. From paid, "
            "shipping is now legal, and returns a shipped state. [pause] Every transition rule "
            "sits inside the one state it applies to. No more hunting across methods."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Write ShippedState",
            "file": "ShippedState.java",
            "lines": ln(
                "class ShippedState implements OrderState {",
                ("  // ▯ from here: deliver? yes. cancel? no.", "ghost"),
                "  public OrderState cancel() {",
                ("    // ▯ what should this do?", "ghost"),
                "  }",
                "}"),
            "prompt": "In ShippedState, what should cancel() do? (A shipped order is on its way.)",
            "hint": "throw new IllegalState(\"already shipped — can't cancel\");"},
         "narration":
            "Your turn. [pause] Here is the shipped state. Think about what cancel should do from "
            "here. [pause] The order is already on a truck. You cannot cancel it anymore. "
            "[pause] Pause, and write that cancel method. [pause] It should refuse — throw, "
            "because a shipped order cannot be cancelled. And notice: you did not have to touch "
            "any other state to add that rule. It belongs to shipped, and only shipped."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "The order just delegates and swaps",
            "file": "Order.java",
            "lines": ln(
                "class Order {",
                ("  private OrderState state = new NewState();", "add"),
                ("  void pay()    { state = state.pay(); }", "add"),
                ("  void ship()   { state = state.ship(); }", "add"),
                ("  void cancel() { state = state.cancel(); }", "add"),
                "  // no status string, no switches, anywhere",
                "}"),
            "note": "Each action asks the current state, then becomes whatever it returns."},
         "narration":
            "Move three. Now the order becomes wonderfully thin. [pause] It holds a current "
            "state — starting as new. [pause] To pay, it asks the current state to pay, and "
            "then becomes whatever state that returns. Ship and cancel do the same. [pause] "
            "There is no status string left. No switch statements anywhere. [pause] The order "
            "just delegates to its current state, and swaps itself for the one that comes back. "
            "The whole state machine now lives in the states."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Add the 'awaiting stock' state\" — the same request",
            "naiveLabel": "Before", "naiveCost": "A new branch in pay, ship, cancel, restock.",
            "naiveSteps": ["edit every method's switch", "add the new action everywhere",
                           "miss one → illegal transition"],
            "patLabel": "Now", "patCost": "One new state class. Others barely notice.",
            "patFile": "AwaitingStockState.java",
            "patLines": ln(
                ("class AwaitingStockState", "add"),
                ("    implements OrderState {", "add"),
                ("  public OrderState restock() {", "add"),
                ("    return new PaidState();", "add"),
                ("  }", "add"),
                ("  public OrderState cancel() {", "add"),
                ("    return new CancelledState();", "add"),
                ("  }", "add"),
                ("}", "add"))},
         "narration":
            "Now the request that caused the pain. Add the awaiting stock state. [pause] Before, "
            "that meant a new branch in pay, in ship, in cancel, and in restock — with the "
            "ever-present risk of missing one and letting an order do something illegal. "
            "[pause] Now? One new state class. Awaiting stock. It says restock leads to paid, "
            "and cancel leads to cancelled — its own rules, all in one place. [pause] The order "
            "class does not change. The states that do not transition into it do not change. "
            "[pause] A new stage of life became a new class."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The State Pattern",
            "plain": "Put each state in its own class that handles the actions and returns the "
                     "next state; the context just delegates to the current one.",
            "nodes": [
                {"id": "st", "title": "OrderState", "stereo": "interface",
                 "members": ["+ pay() / ship() / cancel()"], "x": 740, "y": 215, "w": 440, "color": "#22D3EE"},
                {"id": "ctx", "title": "Order", "members": ["- state: OrderState", "+ pay() / ship() / cancel()"],
                 "x": 150, "y": 230, "w": 430, "color": "#A78BFA"},
                {"id": "new", "title": "NewState", "members": ["+ pay() / ship() / …"],
                 "x": 250, "y": 650, "w": 340, "color": "#8B93B0"},
                {"id": "paid", "title": "PaidState", "members": ["+ pay() / ship() / …"],
                 "x": 720, "y": 650, "w": 340, "color": "#8B93B0"},
                {"id": "shp", "title": "ShippedState", "members": ["+ pay() / ship() / …"],
                 "x": 1190, "y": 650, "w": 340, "color": "#8B93B0"},
                {"id": "awa", "title": "AwaitingStock", "members": ["+ restock() / …"],
                 "x": 1560, "y": 430, "w": 300, "color": "#34D399"}],
            "edges": [
                {"from": "ctx", "to": "st", "kind": "has"},
                {"from": "new", "to": "st", "kind": "impl"},
                {"from": "paid", "to": "st", "kind": "impl"},
                {"from": "shp", "to": "st", "kind": "impl"},
                {"from": "awa", "to": "st", "kind": "impl"}]},
         "narration":
            "Now we name it. [pause] This is the State pattern. [pause] And notice — it looks "
            "almost exactly like a pattern you have seen. In the middle, the state interface. "
            "On the left, the order, holding one current state and delegating to it. [pause] "
            "Underneath, a class per state — new, paid, shipped, and the green awaiting stock "
            "you just added. [pause] The difference from strategy is intent. These states are "
            "not interchangeable algorithms a caller picks. They know about each other, and "
            "they hand control from one to the next. This is a state machine."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Context", "your": "Order (holds current state)"},
                {"role": "State", "your": "interface OrderState"},
                {"role": "ConcreteState", "your": "NewState, PaidState, …"},
                {"role": "Transition", "your": "a state returns the next state"}],
            "plain": "The context delegates every action to its current state object, which "
                     "does the work and returns the state to become next.",
            "gof": "Allow an object to alter its behavior when its internal state changes. The "
                   "object will appear to change its class."},
         "narration":
            "The roles, mapped to your code. [pause] The Context is the order, holding the "
            "current state. [pause] The State is your interface. [pause] The concrete states "
            "are new, paid, shipped, and the rest. [pause] And the transitions are not a "
            "separate table — they are simply the state each action returns. [pause] In plain "
            "terms — the context delegates to its current state, which does the work and hands "
            "back the next state. [pause] The Gang of Four: allow an object to alter its "
            "behavior when its internal state changes — it will appear to change its class."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "Same shape as Strategy — different job",
            "costs": ["A class for every state",
                      "Transitions spread across the states",
                      "States must know some siblings"],
            "dont": ["Two or three states, stable forever",
                     "No real per-state behavior, just a label",
                     "A tiny enum switch is clearer"],
            "signal": "behavior AND the allowed actions depend on a mode, and that same switch "
                      "on the mode appears in many methods."},
         "narration":
            "The honest costs. [pause] State means a class for every state, and the transition "
            "logic is now spread across those classes rather than sitting in one table you can "
            "read top to bottom. And states end up knowing about a few of their neighbors. "
            "[pause] So skip it when you have two or three states that will never change, or "
            "when the status is really just a label with no behavior behind it. A small enum "
            "switch is clearer then. [pause] The signal to reach for it: both the behavior and "
            "the allowed actions depend on a mode, and you notice that same switch on the mode "
            "showing up in method after method. That is a state machine asking to be born."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "State, in one breath",
            "items": [
                "A status field ran a hidden state machine, so the same switch was copied "
                "into every method — and easy to get wrong.",
                "Behavior and transitions depend on the current state — so give each state a "
                "class that owns its own rules.",
                "State: the context delegates to its current state object, which acts and "
                "returns the next. New state, new class."],
            "challenge": "A media player's Play, Pause, and Stop buttons each behave "
                         "differently when it's playing, paused, or stopped.",
            "question": "Does State fit? What's the context, and what are the states?"},
         "narration":
            "The journey in three beats. [pause] The problem: a status field was secretly "
            "running a state machine, so the same switch got copied into every method, and was "
            "dangerously easy to get wrong. [pause] The insight: behavior and transitions both "
            "depend on the current state, so give each state its own class that owns its rules. "
            "[pause] The pattern: State. The context delegates to its current state object, "
            "which acts and returns the next one — so a new state is just a new class. [pause] "
            "Now, for you, before the next episode. [pause] A media player has play, pause, and "
            "stop buttons — and each one behaves differently depending on whether it is "
            "playing, paused, or stopped. [pause] Does State fit? What is the context here, and "
            "what are the states? [pause] Pause, and sketch it before you press play."},
    ],
}


# =====================================================================================
# dp08 — TEMPLATE METHOD   (behavioral; the same algorithm skeleton copy-pasted)
# =====================================================================================
TEMPLATE_METHOD = {
    "id": "dp08-template-method",
    "title": "Template Method",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 08",
            "line1": "Two classes, eighty", "line2": "percent identical",
            "sub": "every importer repeats the same steps — and every fix must be made twice"},
         "narration":
            "Here are two classes that are almost the same. [pause] Same steps, same order, "
            "same nearly-identical code — differing in just one place. [pause] So every bug you "
            "fix, you fix twice. Every step you add, you add twice. [pause] There is a clean way "
            "to write the shared skeleton exactly once, and leave only the holes. Let's import "
            "some data."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "Nightly data imports",
            "situation": "Every night you import vendor data. One vendor sends CSV, another "
                         "sends JSON. Both follow the same flow — open, parse, validate, save "
                         "— and only the parsing differs.",
            "actors": [
                {"emoji": "📄", "label": "CSV feed"},
                {"emoji": "🔧", "label": "JSON feed"},
                {"emoji": "🗄️", "label": "Database"}],
            "ask": "Same five steps, one different line. Why does each importer repeat them all?"},
         "narration":
            "Every night, your app imports data from vendors. [pause] One sends a CSV file. "
            "Another sends JSON. [pause] And both importers do the exact same things, in the "
            "exact same order. Open the file. Parse it. Validate the rows. Remove duplicates. "
            "Save to the database. [pause] The only real difference is the parsing step — CSV "
            "versus JSON. [pause] So why does each importer spell out all five steps from "
            "scratch?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "One importer per format.",
            "file": "CsvImporter.java",
            "lines": ln(
                "class CsvImporter {",
                "  void run(File f) {",
                "    var raw = open(f);",
                ('    var rows = parseCsv(raw);   // the only real difference', "hi"),
                "    validate(rows);",
                "    dedupe(rows);",
                "    save(rows);",
                "  }",
                "}  // JsonImporter is a copy — only parseCsv → parseJson",
            ),
            "note": "Clean and obvious. And JsonImporter is this, pasted."},
         "narration":
            "The obvious approach: one importer per format. [pause] The CSV importer opens the "
            "file, parses the CSV, validates, dedupes, and saves. Five clear steps. [pause] And "
            "the JSON importer? It is this exact class, copied — with one line changed. Parse "
            "CSV becomes parse JSON. Everything else is identical. [pause] Two importers today. "
            "It feels harmless. It is a trap."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Skip rows we already imported.\"",
            "file": "both importers",
            "lines": ln(
                "// CsvImporter.run():",
                ("  validate(rows);", "dim"),
                ("  rows = skipAlreadyImported(rows);  // NEW", "hi"),
                "  dedupe(rows);",
                "// JsonImporter.run():   ← paste the SAME new line",
                ("  rows = skipAlreadyImported(rows);  // AGAIN", "hi"),
                "// XmlImporter next quarter → a third copy"),
            "smell": "Duplicated skeleton — every fix, made N times",
            "touched": ["CsvImporter.run() — add step", "JsonImporter.run() — same step",
                        "a validation bug → fix in both", "add XML → copy all five steps"]},
         "narration":
            "Then the request: skip rows we have already imported. [pause] So you add a step to "
            "the CSV importer. Then you paste the very same line into the JSON importer. [pause] "
            "And that is the whole disease. [pause] The skeleton — the sequence of steps — is "
            "duplicated. So every change happens twice. [pause] Find a bug in validation? Fix "
            "it in both. Reorder the steps? In both. [pause] And when the XML vendor arrives "
            "next quarter, you copy all five steps a third time. [pause] The shared algorithm "
            "has no single home."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["The sequence of steps",
                      "Four of the five steps exactly",
                      "The order they must run in"],
            "varies": ["Only the parse step",
                       "Maybe one optional extra step",
                       "The formats you support"],
            "principle": "Write the skeleton once in a parent; leave holes for the one or two "
                         "steps that differ."},
         "narration":
            "What changes, and what stays fixed? [pause] Almost everything is fixed. The "
            "sequence of steps. Four of the five steps, exactly. And the order they must run "
            "in. [pause] What actually varies is tiny — just the parse step, and maybe one "
            "optional extra. [pause] So the fix writes itself. [pause] Put the skeleton — the "
            "fixed sequence — in one place, a parent class. And leave holes, exactly where the "
            "steps differ, for the children to fill."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "Think of a form letter",
            "emoji": "📝", "analogy": "The letter is printed. Only the blanks get filled in.",
            "map": [
                {"from": "The printed letter", "to": "the fixed run() skeleton"},
                {"from": "The fill-in blanks", "to": "the abstract steps"},
                {"from": "Each person's answers", "to": "a subclass's overrides"},
                {"from": "You can't reorder it", "to": "the parent locks the sequence"}],
            "breaks": "on a form YOU choose when to fill each blank — here the parent decides "
                      "when each step runs, and calls you. Don't call it; it calls you."},
         "narration":
            "Think of a printed form letter. [pause] The body is already written — the "
            "greeting, the structure, the closing. All you do is fill in a few blanks. Your "
            "name here. The date there. [pause] You cannot rearrange the letter. The template "
            "fixes the order; you only supply the missing pieces. [pause] That is our fix "
            "exactly. The printed letter is the fixed sequence of steps. The blanks are the "
            "steps that differ. Each subclass fills them in. [pause] Where it breaks — and this "
            "is the subtle, important part. With a form, you decide when to fill each blank. "
            "Here, the parent decides when each step runs, and calls down to you. Don't call "
            "it. It calls you."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "The skeleton, written once",
            "file": "Importer.java",
            "lines": ln(
                ("abstract class Importer {", "add"),
                ("  public final void run(File f) {   // the template — final!", "add"),
                ("    var raw = open(f);", "add"),
                ("    var rows = parse(raw);          // a hole", "add"),
                ("    validate(rows); dedupe(rows); save(rows);", "add"),
                ("  }", "add"),
                ("  protected abstract List<Row> parse(String raw);  // fill me", "add"),
                "}"),
            "note": "run() is final — the sequence is locked. parse() is the hole."},
         "narration":
            "Move one. We write the skeleton once, in an abstract importer. [pause] There is a "
            "run method — and notice it is final. That is deliberate. The sequence of steps is "
            "locked; no subclass can reorder it. [pause] Inside, it opens, parses, validates, "
            "dedupes, and saves — the shared flow, in one place. [pause] But parse is not "
            "written here. It is declared abstract — a hole. The parent says, at this exact "
            "point I will parse, but a child must tell me how."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "A subclass fills only the hole",
            "file": "CsvImporter.java",
            "lines": ln(
                ("class CsvImporter extends Importer {", "add"),
                ("  protected List<Row> parse(String raw) {", "add"),
                ("    return Csv.split(raw);   // the ONE thing CSV does", "add"),
                ("  }", "add"),
                "}",
                "// no run(), no open(), no validate() — all inherited"),
            "note": "The whole class is one method. Everything else is inherited."},
         "narration":
            "Move two. The CSV importer shrinks to almost nothing. [pause] It extends the "
            "importer, and it overrides exactly one method — parse — to split CSV. [pause] "
            "That is the entire class. No run. No open. No validate, dedupe, or save. All of "
            "that is inherited from the parent, written once. [pause] The subclass fills the "
            "hole, and nothing more."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Write JsonImporter",
            "file": "JsonImporter.java",
            "lines": ln(
                "class JsonImporter extends Importer {",
                ("  // ▯ override just parse() to read JSON", "ghost"),
                "}"),
            "prompt": "Write JsonImporter — override only parse() to parse JSON.",
            "hint": "protected List<Row> parse(String raw) { return Json.rows(raw); }"},
         "narration":
            "Your turn. [pause] The JSON importer needs nothing but its own parse. [pause] "
            "Everything else — the whole flow — it inherits. Pause, and write it. Just override "
            "parse to read JSON, and stop. [pause] If you wrote a single method, you got it "
            "exactly right. That is the entire class — because everything the two importers "
            "share now lives in one place."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "One skeleton fix helps everyone",
            "file": "Importer.java",
            "lines": ln(
                "  public final void run(File f) {",
                "    var rows = parse(open(f));",
                "    validate(rows);",
                ("    rows = skipAlreadyImported(rows);  // added ONCE", "add"),
                "    dedupe(rows); save(rows);",
                "  }",
                ("  protected boolean useCache() { return true; }  // a hook", "add")),
            "note": "That new step now applies to CSV, JSON, XML — automatically."},
         "narration":
            "Move three, and here is the payoff of a single skeleton. [pause] Remember that "
            "skip already imported step you had to paste everywhere? Add it once, in the "
            "parent's run. [pause] And instantly, every importer — CSV, JSON, and every future "
            "one — gets it. For free. [pause] You can even leave optional holes, called hooks — "
            "a method with a sensible default that a subclass may override if it wants, but "
            "does not have to. The skeleton stays in charge."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Add an XML importer\" — a third format",
            "naiveLabel": "Before", "naiveCost": "Copy all five steps into a third class.",
            "naiveSteps": ["paste the whole run() flow", "keep all three in sync forever",
                           "fix every bug three times"],
            "patLabel": "Now", "patCost": "One method. The skeleton is already yours.",
            "patFile": "XmlImporter.java",
            "patLines": ln(
                ("class XmlImporter", "add"),
                ("    extends Importer {", "add"),
                ("  protected List<Row> parse(", "add"),
                ("      String raw) {", "add"),
                ("    return Xml.rows(raw);", "add"),
                ("  }", "add"),
                ("}", "add"))},
         "narration":
            "Now the third format. Add an XML importer. [pause] Before, that meant pasting all "
            "five steps into a third class, then keeping three copies in sync forever, and "
            "fixing every bug three times. [pause] Now? One method. Parse the XML. [pause] The "
            "open, the validate, the dedupe, the save, the skip-already-imported — all "
            "inherited, all shared, all correct. [pause] A new format became a single new "
            "method. The algorithm was written exactly once."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Template Method Pattern",
            "plain": "A parent defines the algorithm's skeleton in one method and leaves certain "
                     "steps abstract for subclasses to fill.",
            "nodes": [
                {"id": "base", "title": "Importer", "stereo": "abstract",
                 "members": ["+ run()   «template, final»", "# parse()   «abstract»", "# validate() / save()"],
                 "x": 660, "y": 210, "w": 600, "color": "#A78BFA"},
                {"id": "csv", "title": "CsvImporter", "members": ["# parse()"],
                 "x": 250, "y": 640, "w": 380, "color": "#8B93B0"},
                {"id": "json", "title": "JsonImporter", "members": ["# parse()"],
                 "x": 770, "y": 640, "w": 380, "color": "#8B93B0"},
                {"id": "xml", "title": "XmlImporter", "members": ["# parse()"],
                 "x": 1290, "y": 640, "w": 380, "color": "#34D399"}],
            "edges": [
                {"from": "csv", "to": "base", "kind": "impl"},
                {"from": "json", "to": "base", "kind": "impl"},
                {"from": "xml", "to": "base", "kind": "impl"}]},
         "narration":
            "Now we name it. [pause] This is the Template Method pattern. [pause] At the top, "
            "the abstract importer. It owns the template method, run — final, so the sequence "
            "cannot change — and it declares the abstract step, parse. [pause] Underneath, the "
            "concrete importers — CSV, JSON, and the green XML you just added. Each one fills "
            "the single hole, and inherits everything else. [pause] There is just one hierarchy "
            "here. The parent holds the algorithm; the children hold the details."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "AbstractClass", "your": "abstract Importer"},
                {"role": "Template Method", "your": "run() — final, fixed order"},
                {"role": "Primitive / hook", "your": "parse() (abstract), useCache() (hook)"},
                {"role": "ConcreteClass", "your": "CsvImporter, JsonImporter, …"}],
            "plain": "The parent's template method calls the fixed steps in order, calling down "
                     "to abstract steps the subclass provides.",
            "gof": "Define the skeleton of an algorithm in an operation, deferring some steps to "
                   "subclasses. Template Method lets subclasses redefine certain steps without "
                   "changing the algorithm's structure."},
         "narration":
            "The roles, mapped to your code. [pause] The abstract class is your importer. "
            "[pause] The template method is run — final, holding the fixed order. [pause] The "
            "primitive operations are the holes, like parse, that subclasses must fill; and "
            "hooks are the optional ones with defaults. [pause] The concrete classes are your "
            "CSV, JSON, and XML importers. [pause] In plain terms — the parent's one method "
            "runs the fixed steps, calling down to the pieces a subclass supplies. [pause] The "
            "Gang of Four: define the skeleton of an algorithm, deferring some steps to "
            "subclasses, so they can redefine steps without changing the structure."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "Inheritance is the catch",
            "costs": ["It's inheritance — one rigid superclass",
                      "Flow jumps between parent and child",
                      "Subclasses can't change the order"],
            "dont": ["The steps vary more than they share",
                     "You'd rather compose than inherit",
                     "There's really only one version"],
            "signal": "several methods share an identical skeleton and differ in just a step "
                      "or two — and you keep copy-pasting the skeleton."},
         "narration":
            "The honest costs. [pause] Template Method is built on inheritance, so each concrete "
            "class is locked to one rigid superclass — and the flow jumps between parent and "
            "child, which can be hard to follow. [pause] And subclasses genuinely cannot change "
            "the order of steps; that is the point, but it is also a constraint. [pause] So "
            "skip it when the steps vary more than they share — at that point you want "
            "composition, and Strategy, which we have already met, is often the better tool. "
            "[pause] The signal to use it: several methods share an identical skeleton and "
            "differ in only a step or two, and you keep copy-pasting that skeleton. Write it "
            "once, and leave the holes."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Template Method, in one breath",
            "items": [
                "Each importer copy-pasted the same five steps, so every fix and every new "
                "step had to be made in every copy.",
                "The skeleton and most steps are fixed; only one step varies — so write the "
                "skeleton once and leave holes.",
                "Template Method: a final parent method runs the fixed steps and calls down to "
                "abstract ones. New variant, one method."],
            "challenge": "A game's enemy types all take a turn the same way — sense, decide, "
                         "act — but each decides differently. A boss adds one extra step.",
            "question": "Does Template Method fit? What's the template, and what are the holes?"},
         "narration":
            "The journey in three beats. [pause] The problem: each importer copy-pasted the "
            "same five steps, so every fix and every new step had to be made in every copy. "
            "[pause] The insight: the skeleton and most steps are fixed, and only one step "
            "varies, so write the skeleton once and leave holes. [pause] The pattern: Template "
            "Method. A final parent method runs the fixed steps and calls down to abstract "
            "ones, so a new variant is just one method. [pause] Now, for you, before the next "
            "episode. [pause] A game's enemies all take a turn the same way — sense, decide, "
            "act — but each one decides differently, and a boss adds one extra step at the end. "
            "[pause] Does Template Method fit? What is the template here, and what are the "
            "holes? [pause] Pause, and sketch it before you press play."},
    ],
}


# =====================================================================================
# dp09 — COMPOSITE   (structural; client special-cases leaf-vs-group everywhere)
# =====================================================================================
COMPOSITE = {
    "id": "dp09-composite",
    "title": "Composite",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 09",
            "line1": "Is it one thing,", "line2": "or a bag of things?",
            "sub": "a folder holds files and folders — and your code keeps asking which"},
         "narration":
            "Some structures are trees. [pause] A folder holds files — and other folders, which "
            "hold more files, and more folders, all the way down. [pause] And when your code has "
            "to keep asking, at every step, is this a single thing or a group of things — it "
            "drowns in that question. [pause] There is a way to stop asking entirely. Let's "
            "measure a folder."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "Total the size of a folder",
            "situation": "You need the total size of a folder. But a folder contains files — "
                         "and sub-folders, which contain more files and more sub-folders, "
                         "nested as deep as you like.",
            "actors": [
                {"emoji": "📄", "label": "A file"},
                {"emoji": "📁", "label": "A folder"},
                {"emoji": "🌲", "label": "…a whole tree"}],
            "ask": "A leaf has a size. A group's size is its parts. How do you total the tree?"},
         "narration":
            "The task sounds trivial. Get the total size of a folder. [pause] But a folder is "
            "not flat. It holds files, which have a size — and sub-folders, which hold more "
            "files and more sub-folders, nested however deep. [pause] A single file has a size "
            "you can just read. A folder's size is the sum of everything inside it. [pause] So "
            "how do you total up a whole tree like that?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "Ask what kind it is.",
            "file": "SizeCalculator.java",
            "lines": ln(
                "long totalSize(Node node) {",
                ('  if (node.isFolder()) {              // which kind?', "hi"),
                "    long sum = 0;",
                ("    for (Node child : node.children())", "hi"),
                ("      sum += totalSize(child);        // recurse by hand", "hi"),
                "    return sum;",
                "  }",
                "  return node.bytes();                 // it's a file",
                "}"),
            "note": "Check the type, branch, recurse yourself. It works."},
         "narration":
            "The obvious approach: ask what kind of thing you are looking at. [pause] If it is a "
            "folder, loop its children and add up each one — calling yourself, recursively, to "
            "handle the nesting. [pause] If it is a file, just return its bytes. [pause] And it "
            "works. It correctly totals the tree. [pause] But look at the shape of it. The "
            "client — your code — is doing all the structural work. Checking the type. Doing "
            "the recursion. Holding the whole tree in its head."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Now count files. And print the tree.\"",
            "file": "everywhere.java",
            "lines": ln(
                ("long count(Node n)  { if (n.isFolder()) {...recurse...} }", "hi"),
                ("void print(Node n)  { if (n.isFolder()) {...recurse...} }", "hi"),
                ("Node find(Node n..) { if (n.isFolder()) {...recurse...} }", "hi"),
                "// the SAME isFolder + recurse dance, every time",
                ("if (n.isSymlink()) { /* now handle a THIRD kind */ }", "hi")),
            "smell": "Type checks + manual recursion, copied per operation",
            "touched": ["size() — isFolder branch", "count() — isFolder branch",
                        "print(), find() — same branch", "add Symlink → every method"]},
         "narration":
            "Then more operations arrive. Count the files. Print the tree. Find a file by name. "
            "[pause] And every one of them repeats the exact same dance — check if it is a "
            "folder, loop the children, recurse by hand. [pause] The structural logic is copied "
            "into operation after operation. [pause] Then someone adds a third kind of node — a "
            "symlink. [pause] Now every one of those methods needs a new branch to handle it. "
            "[pause] The client is buried in bookkeeping about the shape of the tree, when all "
            "it ever wanted was a total."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["Every node has a size",
                      "A file and a folder are both 'nodes'",
                      "The operation you want: a total"],
            "varies": ["Whether it's a leaf or a group",
                       "How each one computes its size",
                       "How deep the nesting goes"],
            "principle": "Give leaf and group the SAME interface, and let each compute its own "
                         "size — a group by asking its children."},
         "narration":
            "What changes, and what stays fixed? [pause] Fixed: every node — file or folder — "
            "has a size. Both are, at heart, just nodes. And the thing you want is always the "
            "same: a total. [pause] What varies is only whether a node is a single leaf or a "
            "group, how it computes its size, and how deep it all nests. [pause] So here is the "
            "move. [pause] Give a file and a folder the exact same interface. Let each one "
            "compute its own size. A file knows its bytes. A folder just asks its children — "
            "and they ask theirs. The recursion becomes the tree's job, not yours."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "Think of a box of boxes",
            "emoji": "📦", "analogy": "To weigh a box, weigh everything inside — boxes included.",
            "map": [
                {"from": "A single item", "to": "a leaf node (a file)"},
                {"from": "A box of items", "to": "a composite (a folder)"},
                {"from": "\"What do you weigh?\"", "to": "the shared size() method"},
                {"from": "A box asks its contents", "to": "a folder asks its children"}],
            "breaks": "you can lift a real box to weigh it whole — code has to walk the contents; "
                      "the uniformity is in the interface, not the physics."},
         "narration":
            "Picture a box that can contain other boxes. [pause] You want to know what the "
            "whole thing weighs. [pause] You ask the outer box. If it holds a single item, it "
            "just tells you that item's weight. If it holds more boxes, it asks each of them — "
            "and they ask their contents. [pause] The beautiful part: you ask every box the "
            "same question. What do you weigh? You never care whether it is a single item or a "
            "nested stack. [pause] That is the fix. A file is a single item. A folder is a box. "
            "Both answer the same question — size. [pause] Where it breaks: you can lift a real "
            "box to weigh it in one go. Code still has to walk the contents. The uniformity "
            "lives in the interface, not the physics."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "One interface for both",
            "file": "FileNode.java",
            "lines": ln(
                "// a file AND a folder are both just this:",
                ("interface FileNode {", "add"),
                ("  long size();", "add"),
                ("}", "add"),
                "",
                ("class FileLeaf implements FileNode {", "add"),
                ("  public long size() { return bytes; }   // a leaf", "add"),
                ("}", "add")),
            "note": "The leaf is trivial — it already knows its own size."},
         "narration":
            "Move one. We give a file and a folder one shared interface. [pause] A file node, "
            "with a single method — size. [pause] Then the file leaf implements it. Its size? "
            "Just its bytes. It already knows. [pause] This is the simple half. A leaf is a "
            "node that has no children, and answers the size question directly."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "The group is a node too",
            "file": "Folder.java",
            "lines": ln(
                ("class Folder implements FileNode {   // also a FileNode!", "add"),
                ("  private final List<FileNode> children = new ArrayList<>();", "add"),
                ("  void add(FileNode n) { children.add(n); }", "add"),
                ("  public long size() {", "add"),
                ("    return children.stream()", "add"),
                ("        .mapToLong(FileNode::size).sum();   // ask each child", "add"),
                "  }",
                "}"),
            "note": "A folder holds FileNodes — and IS a FileNode. That's the whole trick."},
         "narration":
            "Move two — the heart of it. [pause] A folder also implements file node. So a folder "
            "is a file node, and it holds a list of file nodes. [pause] Read that twice. It is "
            "a node, and it contains nodes. That self-reference is the entire pattern. [pause] "
            "And its size? It simply asks each child for its size, and sums them. [pause] It "
            "does not know or care whether a child is a plain file or another folder full of "
            "folders. It just asks size — and the tree answers itself."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Add count() to Folder",
            "file": "Folder.java",
            "lines": ln(
                "// FileLeaf.count() returns 1. And a folder?",
                "public long count() {",
                ("  // ▯ sum count() over the children", "ghost"),
                "}"),
            "prompt": "A leaf counts as 1. Write a Folder's count() — sum of its children.",
            "hint": "return children.stream().mapToLong(FileNode::count).sum();"},
         "narration":
            "Your turn. [pause] Say we add a count operation — how many files are in here? A "
            "single file counts as one. [pause] Write the folder's version. [pause] It is the "
            "same shape as size — ask each child to count, and sum the results. Pause, and "
            "write it. [pause] Notice how mechanical it has become. Any whole-tree question "
            "follows the same pattern: a leaf answers directly, a folder asks its children and "
            "combines."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "The client stops asking",
            "file": "Client.java",
            "lines": ln(
                "// build a tree of files and folders:",
                ("Folder root = new Folder();", "add"),
                ("root.add(new FileLeaf(2_000));", "add"),
                ("Folder sub = new Folder();", "add"),
                ("sub.add(new FileLeaf(500));", "add"),
                ("root.add(sub);", "add"),
                "",
                ('long total = root.size();   // no isFolder, no recursion', "hi")),
            "note": "One call on the root. The recursion is inside the objects now."},
         "narration":
            "Move three. Now watch the client. [pause] You build a tree — a root folder, a file "
            "in it, a sub-folder with its own file, nested however you like. [pause] And to get "
            "the total? You call size, once, on the root. [pause] That is it. No is-folder "
            "check. No manual loop. No recursion in your code at all. [pause] The root asks its "
            "children, they ask theirs, and the answer bubbles back up. The client finally gets "
            "to just ask its question."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Add symlink nodes\" — a third kind of node",
            "naiveLabel": "Before", "naiveCost": "An isSymlink branch in every operation.",
            "naiveSteps": ["add a branch to size()", "and count, print, find…",
                           "one miss → wrong total"],
            "patLabel": "Now", "patCost": "One class. It just works in any tree.",
            "patFile": "SymlinkNode.java",
            "patLines": ln(
                ("class SymlinkNode", "add"),
                ("    implements FileNode {", "add"),
                ("  private final FileNode target;", "add"),
                ("  public long size() {", "add"),
                ("    return 0;   // a link adds nothing", "add"),
                ("  }", "add"),
                ("}", "add"))},
         "narration":
            "Now a third kind of node. Add symlinks. [pause] Before, that meant a new branch in "
            "size, and in count, and in print, and in find — with a wrong total waiting for the "
            "one you forgot. [pause] Now? One class. Symlink node implements file node, and "
            "decides its size is zero. [pause] And that is all. [pause] Because it is a file "
            "node, it drops straight into any tree, and every operation — size, count, print — "
            "handles it automatically. Nothing that walks the tree had to change. A new node "
            "type became a single new class."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Composite Pattern",
            "plain": "Give leaves and groups one interface; a group holds children of that same "
                     "interface and delegates the work down the tree.",
            "nodes": [
                {"id": "comp", "title": "FileNode", "stereo": "interface",
                 "members": ["+ size(): long"], "x": 760, "y": 210, "w": 400, "color": "#22D3EE"},
                {"id": "leaf", "title": "FileLeaf", "stereo": "leaf", "members": ["+ size()"],
                 "x": 150, "y": 430, "w": 360, "color": "#8B93B0"},
                {"id": "folder", "title": "Folder", "stereo": "composite",
                 "members": ["- children: List", "+ add(n) / size()"],
                 "x": 1410, "y": 430, "w": 380, "color": "#A78BFA"},
                {"id": "sym", "title": "SymlinkNode", "members": ["+ size()"],
                 "x": 760, "y": 660, "w": 400, "color": "#34D399"}],
            "edges": [
                {"from": "leaf", "to": "comp", "kind": "impl"},
                {"from": "folder", "to": "comp", "kind": "impl"},
                {"from": "sym", "to": "comp", "kind": "impl"},
                {"from": "folder", "to": "comp", "kind": "has"}]},
         "narration":
            "Now we name it. [pause] This is the Composite pattern. [pause] At the top, the "
            "shared interface — file node. [pause] On the left, the leaf — a single file. "
            "[pause] On the right, the folder, the composite. Look at its two arrows. It "
            "implements file node, and it holds a list of file nodes. [pause] That loop — a "
            "node that contains nodes — is the signature. It lets a folder hold files, or other "
            "folders, forever. [pause] And the green symlink you just added is simply one more "
            "node the whole tree treats like any other."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Component", "your": "interface FileNode"},
                {"role": "Leaf", "your": "FileLeaf, SymlinkNode"},
                {"role": "Composite", "your": "Folder (holds FileNodes)"},
                {"role": "Client", "your": "just calls size() on the root"}],
            "plain": "A composite holds children of the component type and forwards each "
                     "operation to them; a leaf just answers directly.",
            "gof": "Compose objects into tree structures to represent part-whole hierarchies. "
                   "Composite lets clients treat individual objects and compositions "
                   "uniformly."},
         "narration":
            "The roles, mapped to your code. [pause] The Component is your file node interface. "
            "[pause] The Leaf is the plain file — and the symlink. [pause] The Composite is the "
            "folder, which holds children of the component type. [pause] And the Client just "
            "calls size on the root, treating one file and a huge tree exactly the same. [pause] "
            "In plain terms — a composite forwards each operation to its children, while a leaf "
            "answers directly. [pause] The Gang of Four: compose objects into tree structures, "
            "and let clients treat individual objects and compositions uniformly."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "Uniformity has a price",
            "costs": ["Leaf must answer methods that fit groups",
                      "The type system gets more permissive",
                      "Deep trees can recurse expensively"],
            "dont": ["The data isn't really a tree",
                     "Leaves and groups behave very differently",
                     "A flat list is all you have"],
            "signal": "you have a part-whole hierarchy, and you keep writing 'if it's a group, "
                      "recurse; else, handle the leaf.'"},
         "narration":
            "The honest costs. [pause] For true uniformity, the leaf has to offer methods that "
            "only make sense for groups — a file with an add-child method it must reject. So "
            "the interface gets a little permissive, and the type system stops protecting you "
            "there. [pause] And a very deep tree means deep recursion, which can be slow or "
            "even overflow. [pause] So skip it when your data is not really a tree, or when "
            "leaves and groups behave so differently that forcing one interface hurts. [pause] "
            "The signal is unmistakable. You have a part-whole hierarchy, and you keep writing: "
            "if it is a group, recurse; otherwise, handle the leaf. That if is Composite, "
            "waiting to be born."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Composite, in one breath",
            "items": [
                "Every operation on the tree repeated the same 'is it a folder? then recurse' "
                "dance — copied, and fragile.",
                "A file and a folder are both nodes with a size — so give them one interface "
                "and let each compute its own.",
                "Composite: a group holds children of the same type and forwards work down; a "
                "leaf answers directly. New node, new class."],
            "challenge": "A drawing app has shapes — circles, rectangles — and groups of "
                         "shapes, which can hold other groups. You must move, and draw, any "
                         "selection.",
            "question": "Does Composite fit? What's the component, the leaf, and the composite?"},
         "narration":
            "The journey in three beats. [pause] The problem: every operation on the tree "
            "repeated the same is-it-a-folder-then-recurse dance, copied everywhere and easy to "
            "break. [pause] The insight: a file and a folder are both nodes with a size, so give "
            "them one interface and let each compute its own. [pause] The pattern: Composite. A "
            "group holds children of the same type and forwards the work down; a leaf answers "
            "directly — so a new node type is just a new class. [pause] Now, for you, before the "
            "next episode. [pause] A drawing app has shapes — circles, rectangles — and groups "
            "of shapes, and a group can hold other groups. You need to move, and to draw, any "
            "selection at all. [pause] Does Composite fit? What is the component, what is the "
            "leaf, and what is the composite? [pause] Pause, and sketch it before you press "
            "play."},
    ],
}


BUILDER = {
    "id": "dp10-builder",
    "title": "Builder",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 10",
            "line1": "Ten arguments,", "line2": "half of them null",
            "sub": "and nobody remembers which position the timeout goes in"},
         "narration":
            "Some objects are trivial to build. [pause] Others carry a dozen settings — a few "
            "required, most optional — and every one has to be decided before the object can "
            "even exist. [pause] So you reach for a constructor. And the constructor grows. Ten "
            "parameters long, half of them null at every call, and no one can remember which "
            "position the timeout goes in. [pause] There is a cleaner way to assemble a "
            "complicated object. Let's build an HTTP request."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "Build an HTTP request",
            "situation": "An HTTP request needs a URL — and optionally a method, headers, a "
                         "body, a timeout, a retry count, redirect handling. One field is "
                         "required; the rest are all optional.",
            "actors": [
                {"emoji": "🔗", "label": "The URL — required"},
                {"emoji": "⚙️", "label": "Method, timeout…"},
                {"emoji": "📮", "label": "…a finished request"}],
            "ask": "How do you let a caller set any subset of these, and still end up with one "
                   "valid, immutable request?"},
         "narration":
            "Here is the object we want to build: an HTTP request. [pause] It has exactly one "
            "thing it cannot do without — a URL. [pause] Everything else is optional. The "
            "method, a set of headers, a body, a timeout, how many times to retry, whether to "
            "follow redirects. [pause] One caller might set two of those; another might set ten. "
            "[pause] So the question is this — how do you let each caller configure any subset "
            "they like, and still hand back a single, valid, immutable request at the end?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "One constructor for everything.",
            "file": "HttpRequest.java",
            "lines": ln(
                "new HttpRequest(",
                "    url,                 // required",
                '    "GET",               // method',
                ("    headers,             // or null", "hi"),
                ("    null,                // no body", "hi"),
                "    30,                  // timeout",
                ("    3,                   // retries", "hi"),
                ("    true, false);        // redirects? http2?", "hi")),
            "note": "Positional, null-padded. Which boolean is which?"},
         "narration":
            "The direct approach: one big constructor that takes everything. [pause] So a call "
            "looks like this. A URL, a method, a headers map — then null for the body just to "
            "skip it, a timeout, a retry count, and a pair of booleans on the end. [pause] It "
            "compiles. It even works. [pause] But read it back. Half the arguments are null only "
            "to be skipped. And those two booleans — which one is redirects, which one is HTTP "
            "two? You cannot tell without opening the class. [pause] Every caller has to pass all "
            "of it, in exactly the right order, every time."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Now make some of them optional.\"",
            "file": "constructors.java",
            "lines": ln(
                ("HttpRequest(String url) { ... }", "hi"),
                ("HttpRequest(String url, String method) { ... }", "hi"),
                ("HttpRequest(String url, String m, Map h) { ... }", "hi"),
                "// a new overload for every combination you allow",
                ("HttpRequest(String url, ..., boolean http2) { ... }", "hi")),
            "smell": "Telescoping constructors — one per field combination",
            "touched": ["2 optional fields → 4 overloads",
                        "add a field → double them all again",
                        "callers still count argument positions",
                        "every skipped field is a null trap"]},
         "narration":
            "The moment you try to make fields optional, it gets worse. [pause] You add a "
            "constructor for just the URL. Then one for URL and method. Then URL, method, and "
            "headers. [pause] This is the telescoping constructor — a new overload for every "
            "combination of fields you're willing to support. [pause] Two optional fields "
            "already means four of them. Add one more field, and you double the whole set again. "
            "[pause] And the caller is still counting positions, still passing nulls, still one "
            "slip away from putting the timeout where the retry count should go."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["You always end with ONE HttpRequest",
                      "It should be immutable once built",
                      "The URL is always required"],
            "varies": ["Which optional fields get set",
                       "The order the caller sets them",
                       "How many callers set what"],
            "principle": "Separate building from the built: collect fields on a helper, then "
                         "construct once at the end."},
         "narration":
            "So what is fixed, and what varies? [pause] Fixed: you always end up with exactly one "
            "HttpRequest, it should be immutable the instant it exists, and it always needs a "
            "URL. [pause] What varies is only which optional fields a given caller sets, in what "
            "order, and how many of them. [pause] Here is the move. [pause] Separate the act of "
            "building from the finished thing. Let the caller set fields one at a time on a "
            "small, mutable helper — and then, in a single step at the end, hand back one "
            "finished, immutable request."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "Ordering at the sandwich counter", "emoji": "🥪",
            "analogy": "You call out fillings one at a time; only at the end do they wrap the "
                       "finished sandwich.",
            "map": [
                {"from": "The empty order", "to": "a fresh builder"},
                {"from": "Each thing you add", "to": "one fluent setter, e.g. .header()"},
                {"from": "\"That's everything\"", "to": "the build() call"},
                {"from": "The wrapped sandwich", "to": "the immutable HttpRequest"}],
            "breaks": "a real sandwich keeps changing as you build it; the finished request is "
                      "frozen — all the mutation stays behind on the builder."},
         "narration":
            "Think about ordering at a sandwich counter. [pause] You don't hand over every choice "
            "in one breath, in a fixed order. You call them out one at a time — bread, then a "
            "filling, then a sauce — in whatever order you like. [pause] The empty order is a "
            "fresh builder. Each thing you add is one fluent setter call. Saying that's "
            "everything is the build step. And the wrapped sandwich they hand back is your "
            "immutable request. [pause] The only difference: the finished request is frozen. All "
            "the changing happened on the builder, and it stays behind there."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "A builder that collects the fields",
            "file": "HttpRequest.java",
            "lines": ln(
                "public final class HttpRequest {",
                "  private final String url, method;   // immutable",
                ("  public static class Builder {", "add"),
                ("    private final String url;         // required", "add"),
                ('    private String method = "GET";    // default', "add"),
                ("    Builder(String url) { this.url = url; }", "add"),
                "  }",
                "}"),
            "note": "The Builder mirrors the fields — but it's mutable while you configure."},
         "narration":
            "The refactor, step one. [pause] Inside HttpRequest, we add a static nested class — "
            "the Builder. [pause] It holds the same fields the request will have. The required "
            "URL comes in through its constructor, so you cannot even start without one. The "
            "optional fields get sensible defaults — method starts as GET. [pause] And here is "
            "the key difference. The request itself is final and immutable, but the builder is "
            "mutable while you are still configuring it. That is the whole trick — the mutation "
            "lives on the builder, never on the product."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "Fluent setters that return this",
            "file": "HttpRequest.Builder.java",
            "lines": ln(
                ("public Builder method(String m) {", "hi"),
                "  this.method = m;",
                ("  return this;              // ← enables chaining", "hi"),
                "}",
                "public Builder timeout(int s) {",
                "  this.timeout = s; return this;",
                "}"),
            "note": "Each setter mutates one field and returns the builder — so calls chain."},
         "narration":
            "Step two: the setters. [pause] Each one does two things. It sets its single field — "
            "and then it returns the builder itself. [pause] That one line, return this, is what "
            "lets the calls chain together, one after another, in any order the caller likes. "
            "[pause] One method for the HTTP method, one for the timeout, one for every optional "
            "field. Small, boring, and every single one of them ends with return this."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Add header(key, value)",
            "file": "HttpRequest.Builder.java",
            "lines": ln(
                "private final Map<String,String> headers = new HashMap<>();",
                "// headers accumulate — a caller may add several",
                "public Builder header(String k, String v) {",
                ("  // ▯ store it, and keep the chain going", "ghost"),
                "}"),
            "prompt": "Write header() so it accumulates into the map — and still allows chaining.",
            "hint": "headers.put(k, v); return this;"},
         "narration":
            "Your turn. Pause here. [pause] Most setters replace a single value. But headers are "
            "different — a caller might add several, so this one should accumulate into a map "
            "rather than overwrite. [pause] Write a header method that takes a key and a value, "
            "stores it, and — like every other setter — keeps the chain alive. [pause] Think "
            "about what its very last line has to be."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "build() constructs the finished request",
            "file": "HttpRequest.java  +  the call site",
            "lines": ln(
                ("public HttpRequest build() {", "hi"),
                "  if (url == null) throw new IllegalStateException();",
                ("  return new HttpRequest(this);   // private ctor", "hi"),
                "}",
                "// the call site now reads like a sentence:",
                ("HttpRequest r = new HttpRequest.Builder(url)", "add"),
                ('    .method("POST").timeout(30)', "add"),
                ('    .header("Accept", "json").build();', "add")),
            "note": "Validate once, then copy the builder into an immutable request."},
         "narration":
            "Step three, and it all comes together. [pause] The builder gets a build method. It "
            "validates once — no URL, no request — and then constructs the real HttpRequest "
            "through a private constructor that just copies the builder's fields in. [pause] Now "
            "look at the call site. You start a builder with the required URL, then chain only "
            "the options you actually want — a method, a timeout, a header — and finish with "
            "build. [pause] No nulls. No positions to count. It reads like a sentence, and what "
            "you get back is fully immutable."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Support HTTP/2\" — one more optional flag",
            "naiveLabel": "Before", "naiveCost": "Another param, or another row of overloads.",
            "naiveSteps": ["widen the giant constructor", "or add more overloads",
                           "every existing caller must change"],
            "patLabel": "Now", "patCost": "One setter. Old call sites don't change.",
            "patFile": "HttpRequest.Builder.java",
            "patLines": ln(
                ("public Builder http2(boolean on) {", "add"),
                ("  this.http2 = on;", "add"),
                ("  return this;", "add"),
                ("}", "add"),
                ("// existing chains keep working, untouched", "add"))},
         "narration":
            "Now the requirement that used to hurt. Support HTTP two — one more optional flag. "
            "[pause] Before, that meant widening the giant constructor again, or adding yet "
            "another row of overloads — and every existing caller would have to change just to "
            "match. [pause] With the builder, you add one setter. That is all. [pause] Callers "
            "who want HTTP two chain one more call. And every caller who doesn't — every line of "
            "code already written — keeps working, completely untouched."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Builder Pattern",
            "plain": "Move an object's construction onto a separate builder that collects the "
                     "parts, then hands back one finished, immutable product.",
            "nodes": [
                {"id": "client", "title": "Client", "stereo": "client",
                 "members": ["configures the builder,", "then calls build()"],
                 "x": 130, "y": 410, "w": 360, "color": "#8B93B0"},
                {"id": "builder", "title": "HttpRequest.Builder", "stereo": "builder",
                 "members": ["+ method() / header()", "+ timeout() / build()"],
                 "x": 690, "y": 410, "w": 540, "color": "#A78BFA"},
                {"id": "product", "title": "HttpRequest", "stereo": "product",
                 "members": ["- url, headers, body", "(final, immutable)"],
                 "x": 1430, "y": 410, "w": 400, "color": "#22D3EE"}],
            "edges": [
                {"from": "client", "to": "builder", "kind": "assoc"},
                {"from": "builder", "to": "product", "kind": "assoc"}]},
         "narration":
            "This is the Builder pattern. [pause] Three roles, reading left to right. [pause] The "
            "Client — that is your calling code — configures a builder, and then asks it to "
            "build. [pause] The Builder holds one setter per field, plus the build method that "
            "produces the result. [pause] And the Product — HttpRequest — is the finished, "
            "immutable object that falls out the end. [pause] Construction moved out of the "
            "product and onto a builder whose only job is to collect the parts and assemble them "
            "once."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Product", "your": "HttpRequest (immutable)"},
                {"role": "Builder", "your": "HttpRequest.Builder"},
                {"role": "Fluent setters", "your": "method(), header(), timeout()"},
                {"role": "Client", "your": "chains setters, calls build()"}],
            "plain": "The builder accumulates state through chained setters; build() validates "
                     "it and returns one finished product.",
            "gof": "Separate the construction of a complex object from its representation so "
                   "that the same construction process can create different representations."},
         "narration":
            "The names, against the code you just wrote. [pause] The Product is HttpRequest — the "
            "immutable thing you actually wanted. [pause] The Builder is HttpRequest.Builder, and "
            "its fluent setters — method, header, timeout — are how you feed it. [pause] The "
            "Client is whatever chains those calls and finishes with build. [pause] And the Gang "
            "of Four definition: separate the construction of a complex object from its "
            "representation, so that the same construction process can create different "
            "representations."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "Fluency isn't free",
            "costs": ["A whole second class to write and maintain",
                      "Two objects made where one used to be",
                      "Overkill when there are only two or three fields"],
            "dont": ["The object has one or two simple fields",
                     "Everything is required — no optional soup",
                     "The object is already tiny and immutable"],
            "signal": "a constructor with four-plus parameters, several optional, and callers "
                      "passing nulls just to skip them."},
         "narration":
            "Builder is not free either. [pause] You are writing and maintaining an entire second "
            "class alongside the real one. You create two objects where a constructor made one. "
            "And for an object with two or three fields, it is plainly overkill — a plain "
            "constructor is clearer. [pause] So do not reach for it when the object is small, or "
            "when every field is required and there is no optional soup to tame. [pause] The "
            "signal to reach for it is specific — a constructor with four or more parameters, "
            "several of them optional, and callers passing null just to skip the ones they don't "
            "care about."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Builder, in one breath",
            "items": [
                "One giant constructor — or a telescoping stack of overloads — buried the caller "
                "in positional arguments and nulls.",
                "You always end with one immutable object; only which fields get set varies — so "
                "collect them on a mutable builder first.",
                "Builder: fluent setters each return this, and build() validates once and "
                "produces the product. New field, one new setter."],
            "challenge": "You're building a database Query: a required table, plus optional "
                         "where-clauses, ordering, a limit, and joins — set in any combination.",
            "question": "Does Builder fit? What's the product, the builder, and where does "
                        "build() validate?"},
         "narration":
            "Builder, in one breath. [pause] A single giant constructor, or a telescoping stack "
            "of overloads, buried every caller in positional arguments and nulls. [pause] But "
            "you always end with one immutable object — only the set of chosen fields varies — "
            "so you collect them on a mutable builder first. [pause] Builder: fluent setters "
            "that each return this, and a build method that validates once and hands back the "
            "finished product. A new field costs one new setter, nothing more. [pause] Now, one "
            "to carry out. [pause] You're building a database query — a required table, plus "
            "optional where-clauses, ordering, a limit, and joins, in any combination. [pause] "
            "Does Builder fit? What is the product, what is the builder, and where should build "
            "do its validating? [pause] Pause, and sketch it before you press play."},
    ],
}


SINGLETON = {
    "id": "dp11-singleton",
    "title": "Singleton",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 11",
            "line1": "Everyone wants", "line2": "the same one",
            "sub": "and every stray 'new' quietly hands them a different one"},
         "narration":
            "Some objects you want many of. [pause] But a few — a connection pool, a "
            "configuration, a cache — are different. There should be exactly one, shared by the "
            "whole program, and a second copy is not a convenience. It is a bug. [pause] Yet the "
            "default tool we reach for, the new keyword, is a copy machine. Call it twice, get "
            "two. [pause] So how do you guarantee there is only ever one? Let's build a "
            "connection pool."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "One database connection pool",
            "situation": "A connection pool holds a fixed set of live database connections — "
                         "expensive to open, strictly limited by the database. Every part of "
                         "the app must share the very same pool.",
            "actors": [
                {"emoji": "🗄️", "label": "The database"},
                {"emoji": "🔌", "label": "A pool of connections"},
                {"emoji": "🧩", "label": "…every module needs it"}],
            "ask": "How do you make sure the whole program shares one pool — never accidentally "
                   "two?"},
         "narration":
            "Here is the object: a database connection pool. [pause] It is expensive. Opening a "
            "connection takes real time, and the database itself allows only so many at once. So "
            "the pool opens a fixed set of them up front and lends them out. [pause] And every "
            "part of your app — the web layer, the background jobs, the health check — has to "
            "draw from the exact same pool. [pause] Because if two pools exist, each opens its "
            "own connections, and together they can blow straight past the database's limit. "
            "[pause] So how do you guarantee the whole program shares one pool, and never, ever "
            "creates a second?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "Everyone just news one up.",
            "file": "across the app.java",
            "lines": ln(
                "class WebHandler {",
                ("  ConnectionPool pool = new ConnectionPool();  // #1", "hi"),
                "}",
                "class JobRunner {",
                ("  ConnectionPool pool = new ConnectionPool();  // #2", "hi"),
                "}",
                "// the health check makes a third. and a fourth…"),
            "note": "Each 'new' opens its own connections. The DB cap is now fiction."},
         "narration":
            "The obvious thing: wherever you need the pool, you make one. [pause] The web handler "
            "news up a pool. The job runner news up its own. The health check makes a third. "
            "[pause] And each of those pools, dutifully, opens its own full set of connections. "
            "[pause] Four pools, four times the connections — and the database's limit, the one "
            "hard number this was all supposed to respect, is now pure fiction. [pause] Nothing "
            "is wrong with any single line. The bug is that there are four of them."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Just pass the one pool everywhere.\"",
            "file": "threading.java",
            "lines": ln(
                ("new WebHandler(pool);", "hi"),
                ("new JobRunner(pool, cache);", "hi"),
                ("new Health(pool, cache, clock);   // and on…", "hi"),
                "// every constructor grows another parameter",
                ("static ConnectionPool POOL = new ConnectionPool();", "hi")),
            "smell": "Thread the instance by hand, or expose a mutable global",
            "touched": ["pool passed through every constructor",
                        "new module → thread it again",
                        "or a public static, created eagerly",
                        "tests can't stop it opening real connections"]},
         "narration":
            "So you try to fix it by discipline. Create exactly one pool at startup, and pass it "
            "in everywhere. [pause] But now that pool has to be threaded through every "
            "constructor — web handler, job runner, health check — and each new class means "
            "passing it one more level down. [pause] The tempting shortcut is a public static "
            "field: one global pool everyone can reach. [pause] But nothing stops someone newing "
            "up another. It is created eagerly whether you use it or not. And in a test, you "
            "cannot stop it from opening real database connections. [pause] The guarantee you "
            "wanted — exactly one — still is not enforced anywhere. It is just a convention you "
            "are hoping everyone follows."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["There must be exactly one pool",
                      "It has to be reachable everywhere",
                      "Opening it is expensive"],
            "varies": ["When it's first actually needed",
                       "Which module happens to ask first"],
            "principle": "Let the class own its single instance: hide the constructor, expose "
                         "one access point."},
         "narration":
            "What is fixed here, and what varies? [pause] Fixed: there must be exactly one pool, "
            "it has to be reachable from anywhere in the program, and creating it is expensive. "
            "[pause] What varies is only when it is first genuinely needed, and which module "
            "happens to ask for it first. [pause] So here is the move. [pause] Stop trusting "
            "every caller to cooperate. Make the class itself responsible for its own "
            "uniqueness. Hide the constructor, so no one outside can call new — and expose a "
            "single access point that always returns the same instance."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "A country's official clock", "emoji": "🕰️",
            "analogy": "You don't run your own national time — you ask the one authority, and so "
                       "does everyone else.",
            "map": [
                {"from": "The single official time", "to": "the one instance"},
                {"from": "You can't mint your own", "to": "the private constructor"},
                {"from": "\"What time is it?\"", "to": "getInstance()"},
                {"from": "Every clock in sync", "to": "one shared pool, everywhere"}],
            "breaks": "a country enforces its single clock by law; in code, nothing enforces it "
                      "until you remove the public constructor."},
         "narration":
            "Think of a country's official time. [pause] There is exactly one authoritative "
            "source, and every clock, every train schedule, every phone syncs to it. [pause] You "
            "do not get to declare your own national time — that authority is not yours to "
            "create. You simply ask what time it is, and so does everyone else, and everyone "
            "stays in agreement. [pause] The single official time is the one instance. The fact "
            "that you cannot mint your own is the private constructor. Asking the time is "
            "getInstance. [pause] Where the analogy strains: a country enforces its one clock by "
            "law — in code, nothing enforces it until you actually take the public constructor "
            "away."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "Hide the constructor, own the instance",
            "file": "ConnectionPool.java",
            "lines": ln(
                "public final class ConnectionPool {",
                ("  private static ConnectionPool instance;   // the one", "add"),
                ("  private ConnectionPool() { /* open pool */ }  // ← private!", "add"),
                "  // no one outside can call new ConnectionPool()",
                "}"),
            "note": "A private constructor makes 'new ConnectionPool()' a compile error elsewhere."},
         "narration":
            "The refactor, step one. [pause] The class keeps a single static field to hold the "
            "one instance. [pause] And then the crucial line — the constructor is made private. "
            "[pause] That one word changes everything. Now no code anywhere else in the program "
            "can call new ConnectionPool. The compiler forbids it. [pause] The class has taken "
            "ownership of its own creation. The only code allowed to make a pool is the pool "
            "class itself."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "One access point — but mind the race",
            "file": "ConnectionPool.java",
            "lines": ln(
                "public static ConnectionPool getInstance() {",
                ("  if (instance == null)          // two threads can BOTH", "hi"),
                ("    instance = new ConnectionPool();  // see null here", "hi"),
                "  return instance;",
                "}"),
            "note": "Lazy: built on first call. But unsynchronized, two threads can make two."},
         "narration":
            "Step two: the single access point. [pause] A static getInstance method. The first "
            "time anyone asks, the instance is null, so it builds the pool. Every call after "
            "that returns the same one. [pause] This is lazy — the expensive pool is not created "
            "until something actually needs it. [pause] But look closely, because there is a bug "
            "hiding here. [pause] If two threads call getInstance at the very same moment, both "
            "can see instance as null, and both can create a pool. The one guarantee we built "
            "this whole class to provide — quietly broken by concurrency."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Make getInstance() thread-safe",
            "file": "ConnectionPool.java",
            "lines": ln(
                "private static volatile ConnectionPool instance;",
                "public static ConnectionPool getInstance() {",
                ("  // ▯ ensure only ONE is ever created, even under threads", "ghost"),
                "}"),
            "prompt": "Two threads must never both build a pool. How do you close the race?",
            "hint": "double-checked lock: if(null){ synchronized(...){ if(null) create } }"},
         "narration":
            "Your turn — pause here. [pause] The field is marked volatile, which will matter for "
            "what comes next. [pause] Your job: rewrite getInstance so that even if a hundred "
            "threads call it at the same instant, exactly one pool is ever created. [pause] The "
            "classic answer is double-checked locking — check for null, and only if it is null "
            "enter a synchronized block, then check once more inside before creating. [pause] "
            "Try to write it. Then let me show you an idiom that sidesteps the whole problem."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "The holder idiom — lazy, thread-safe, no locks",
            "file": "ConnectionPool.java",
            "lines": ln(
                ("private static class Holder {", "add"),
                ("  static final ConnectionPool INSTANCE = new ConnectionPool();", "add"),
                ("}", "add"),
                ("public static ConnectionPool getInstance() {", "add"),
                ("  return Holder.INSTANCE;   // JVM inits it exactly once", "add"),
                ("}", "add")),
            "note": "The class loader initializes Holder once, lazily, thread-safe — for free."},
         "narration":
            "Step three — the idiom most Java code actually uses. [pause] Put the instance inside "
            "a private static nested class, a holder. [pause] The trick is in how the Java class "
            "loader works. That holder class is not loaded until the first time getInstance "
            "touches it — so it stays lazy. And the language already guarantees a class is "
            "initialized exactly once, safely, even across threads. [pause] So you get lazy "
            "creation and rock-solid thread safety, with no synchronized block, no volatile, no "
            "double-checked anything. [pause] The concurrency problem does not get solved. It "
            "gets handed to the JVM, which solved it long ago."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Never exceed the DB's 20-connection cap\"",
            "naiveLabel": "Before", "naiveCost": "Every stray pool opened its own 20.",
            "naiveSteps": ["4 pools → up to 80 connections", "DB starts rejecting at peak",
                           "fails only under load — the worst kind"],
            "patLabel": "Now", "patCost": "One pool exists. The cap holds by construction.",
            "patFile": "anywhere.java",
            "patLines": ln(
                ("ConnectionPool.getInstance().borrow();", "add"),
                ("// same pool, same 20 connections, everywhere", "add"),
                ("// a second pool is now a COMPILE error", "add"))},
         "narration":
            "Now the requirement this all existed for — never exceed the database's cap of "
            "twenty connections. [pause] Before, with pools breeding freely, four of them meant "
            "up to eighty open connections. The database starts rejecting them at peak traffic — "
            "a failure that only shows up under load, which is the worst kind to debug. [pause] "
            "Now there is exactly one pool, holding exactly its twenty connections, and every "
            "borrow across the whole app draws from that same set. [pause] The cap is not a hope "
            "anymore. It holds by construction — because a second pool is now a compile error."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Singleton Pattern",
            "plain": "A class that permits only one instance of itself and gives the whole "
                     "program a single point of access to it.",
            "nodes": [
                {"id": "client", "title": "Client", "members": ["ConnectionPool", ".getInstance()"],
                 "x": 210, "y": 440, "w": 380, "color": "#8B93B0"},
                {"id": "single", "title": "ConnectionPool", "stereo": "singleton",
                 "members": ["- static instance", "- ConnectionPool() «private»",
                             "+ static getInstance()"],
                 "x": 900, "y": 420, "w": 640, "color": "#A78BFA"}],
            "edges": [
                {"from": "client", "to": "single", "kind": "assoc"}]},
         "narration":
            "This is the Singleton pattern. [pause] It is really a single class carrying three "
            "moving parts. [pause] A private static field that holds the one and only instance. "
            "[pause] A private constructor, so nothing outside can ever create another. [pause] "
            "And a public static getInstance — the one door everyone in the program walks "
            "through to reach it. [pause] The client on the left never says new. It only ever "
            "asks, getInstance, and always receives the very same object."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Singleton", "your": "final class ConnectionPool"},
                {"role": "The instance", "your": "private static Holder.INSTANCE"},
                {"role": "Access point", "your": "static getInstance()"},
                {"role": "Client", "your": "calls getInstance(), never new"}],
            "plain": "The class hides its constructor and exposes one static accessor that "
                     "always returns the same instance.",
            "gof": "Ensure a class has only one instance, and provide a global point of access "
                   "to it."},
         "narration":
            "The names, against your code. [pause] The Singleton is the ConnectionPool class "
            "itself. [pause] The single instance lives in that static holder field. [pause] The "
            "access point is the static getInstance method — the one global door. [pause] And "
            "the Client is any code that calls getInstance and never, ever calls new. [pause] "
            "The Gang of Four, in one sentence: ensure a class has only one instance, and "
            "provide a global point of access to it. [pause] Read that second half carefully — a "
            "global point of access — because that is also where the trouble starts."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "The pattern with the most caveats",
            "costs": ["It's global state, dressed as an object",
                      "Dependencies get hidden inside methods",
                      "Hard to swap or reset — tests bleed state"],
            "dont": ["You want 'usually one' — inject it instead",
                     "You need to substitute it in tests",
                     "'One' is really a scope or lifetime concern"],
            "signal": "a resource that is genuinely unique AND expensive AND must be shared "
                      "process-wide — like a real connection pool."},
         "narration":
            "And now the honesty, because Singleton has more caveats than any pattern we have "
            "covered. [pause] What you have built is global state, wearing the costume of an "
            "object. [pause] Any class that calls getInstance carries a dependency that is "
            "invisible from its constructor — you cannot tell what it needs just by looking at "
            "it. [pause] And because one instance lives for the whole life of the program, tests "
            "bleed state into each other, and you cannot easily swap in a fake. [pause] So here "
            "is the real guidance. If you only want usually one of something, do not use this — "
            "create one instance and inject it where it is needed. That gives you the sharing "
            "without the global. [pause] Reach for Singleton only when a resource is genuinely "
            "unique, genuinely expensive, and genuinely must be shared across the whole process "
            "— like a real connection pool. [pause] It is the pattern most worth knowing, and "
            "most worth resisting."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Singleton, in one breath",
            "items": [
                "Every 'new' made another copy of a resource meant to be shared — so the "
                "database's limit became a fiction.",
                "There must be exactly one, reachable everywhere — so let the class own its "
                "instance: private constructor, one accessor.",
                "Use the holder idiom for lazy, thread-safe creation with no locks — and reach "
                "for Singleton sparingly; it's global state."],
            "challenge": "An app needs one in-memory metrics registry — counters and timers "
                         "every module updates, and a reporter reads once a minute.",
            "question": "Does Singleton truly fit — or would injecting one shared instance serve "
                        "you better?"},
         "narration":
            "Singleton, in one breath. [pause] Every new made another copy of something meant to "
            "be shared, and the database's limit became fiction. [pause] There must be exactly "
            "one, reachable everywhere — so the class owns its single instance behind a private "
            "constructor and one access point. [pause] Use the holder idiom for lazy, "
            "thread-safe creation with no locks — and reach for the pattern sparingly, because "
            "what you are really creating is global state. [pause] Here is one to sit with. "
            "[pause] An app needs a single in-memory metrics registry — counters and timers that "
            "every module updates, and a reporter that reads it once a minute. [pause] Does "
            "Singleton truly fit here? Or, having heard the caveats, would simply creating one "
            "registry and injecting it serve you better? [pause] That question, not the "
            "mechanics, is the real lesson of this pattern."},
    ],
}


PROXY = {
    "id": "dp12-proxy",
    "title": "Proxy",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 12",
            "line1": "Don't load it", "line2": "until someone looks",
            "sub": "a stand-in that fronts an expensive object and summons it only on demand"},
         "narration":
            "Some objects are expensive to create. [pause] A high-resolution image, a remote "
            "connection, a large file — the cost is real, and often you pay it for objects no "
            "one ever actually uses. [pause] What if something could stand in for the real "
            "object — look exactly like it, sit exactly where it sits — and conjure the real, "
            "expensive thing only at the moment it is first needed? [pause] That stand-in has a "
            "name. Let's build a document full of images."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "A document full of high-res images",
            "situation": "A document embeds hundreds of high-resolution images. Each is slow to "
                         "load and heavy in memory — but on open, the reader only ever sees the "
                         "first page.",
            "actors": [
                {"emoji": "📄", "label": "A long document"},
                {"emoji": "🖼️", "label": "200 heavy images"},
                {"emoji": "👁️", "label": "…one page in view"}],
            "ask": "How do you open instantly and load only the images actually shown?"},
         "narration":
            "Here is the situation: a document with hundreds of embedded high-resolution images. "
            "[pause] Each image is expensive — slow to decode, heavy in memory. [pause] But when "
            "a reader opens the document, they see one page. Maybe they scroll a little. Most of "
            "those images are never looked at in a given session. [pause] So the question is: "
            "how do you open the document instantly, and pay to load an image only when it is "
            "actually put on screen?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "Load them all, up front.",
            "file": "Document.java",
            "lines": ln(
                "class Document {",
                "  List<RealImage> images = new ArrayList<>();",
                "  Document(List<String> files) {",
                ("    for (String f : files)", "hi"),
                ("      images.add(new RealImage(f));  // decodes NOW", "hi"),
                "  }",
                "}"),
            "note": "Opening decodes all 200 images — before a single one is shown."},
         "narration":
            "The direct approach: when the document loads, load its images. [pause] The "
            "constructor walks the list of filenames and, for each one, creates a RealImage — "
            "which immediately reads the file and decodes the pixels. [pause] It is simple, and "
            "it is correct. [pause] But opening a two-hundred-image document now decodes all two "
            "hundred, up front, before the reader has seen a single page. [pause] Seconds of "
            "delay, and gigabytes of memory, spent almost entirely on images no one will look "
            "at."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Fine — load them lazily, then.\"",
            "file": "leaked.java",
            "lines": ln(
                "void drawPage(int p) {",
                "  for (Image img : pageImages(p)) {",
                ("    if (!img.isLoaded()) img.load();  // lazy check…", "hi"),
                "    img.draw();",
                "  }",
                ("// the same guard in getWidth(), export(), print()…", "hi")),
            "smell": "Lazy-loading logic smeared across every caller",
            "touched": ["every draw() guarded by isLoaded()",
                        "getWidth/getHeight need the same guard",
                        "forget one → a blank or a crash",
                        "Document now knows about loading"]},
         "narration":
            "So you make it lazy by hand. Don't load in the constructor; load on first use. "
            "[pause] But now every place that touches an image has to ask the same question "
            "first — is it loaded yet? If not, load it, then use it. [pause] That guard shows up "
            "in draw. And in getWidth. And in export, and print. [pause] Forget it in one place "
            "and you get a blank image, or a crash. [pause] The lazy-loading logic — which has "
            "nothing to do with what a document is — is now smeared across every method that "
            "touches an image. The client is doing the object's job for it."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["The client just wants an Image to draw",
                      "Every image has width, height, draw()",
                      "The real image is expensive to load"],
            "varies": ["Whether the pixels are loaded yet",
                       "Whether this image is ever shown"],
            "principle": "Put a stand-in with the SAME interface in front of the real object; "
                         "it loads on demand."},
         "narration":
            "What is fixed, and what varies? [pause] Fixed: the client just wants something it "
            "can treat as an image — draw it, ask its size. Every image has that same interface. "
            "And the real, pixel-loaded image is expensive. [pause] What varies is only whether "
            "the pixels are loaded yet, and whether this particular image is ever shown at all. "
            "[pause] Here is the move. [pause] Put a lightweight stand-in in front of the real "
            "image — one that implements the exact same interface. The client holds the "
            "stand-in, treats it as an image, and the stand-in quietly loads the real one the "
            "first moment it is genuinely needed."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "A valet ticket", "emoji": "🎟️",
            "analogy": "The ticket stands in for your car; the valet fetches the real one only "
                       "when you present it.",
            "map": [
                {"from": "The valet ticket", "to": "the proxy object"},
                {"from": "Your actual car", "to": "the real, heavy object"},
                {"from": "\"Bring the car\"", "to": "a method call, e.g. draw()"},
                {"from": "Fetched only on request", "to": "loaded lazily, on first use"}],
            "breaks": "a ticket obviously isn't a car; a good proxy is indistinguishable from "
                      "the real object through the interface."},
         "narration":
            "Think of a valet ticket. [pause] You hand over your car, and you get back a small "
            "paper ticket. [pause] For all practical purposes, that ticket is your car — it is "
            "what you hold, what you present to leave. But the real car is parked somewhere "
            "expensive to reach, and the valet fetches it only when you hand over the ticket. "
            "[pause] The ticket is the proxy. Your actual car is the real, heavy object. Asking "
            "for the car is a method call. And the car is fetched only on request. [pause] Where "
            "it breaks: a ticket obviously is not a car. A good software proxy is built so that, "
            "through the interface, you truly cannot tell the difference."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "One interface; the real image is heavy",
            "file": "Image.java",
            "lines": ln(
                ("interface Image {", "add"),
                ("  void draw();  int width();", "add"),
                ("}", "add"),
                "class RealImage implements Image {",
                ("  RealImage(String f) { load(f); }   // heavy!", "hi"),
                "  public void draw() { /* blit pixels */ }",
                "}"),
            "note": "Both the real image and its stand-in will implement this one interface."},
         "narration":
            "The refactor, step one. [pause] First, pin down the shared interface. An image is "
            "something you can draw and ask the size of — that is all the client ever needs. "
            "[pause] The RealImage implements it the honest, expensive way: its constructor "
            "loads and decodes the file immediately, and draw blits the pixels. [pause] Nothing "
            "about RealImage changes. It stays exactly as costly as it always was. [pause] The "
            "point is only this — it now sits behind an interface that something else can also "
            "implement."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "The proxy: same interface, no pixels yet",
            "file": "ImageProxy.java",
            "lines": ln(
                ("class ImageProxy implements Image {", "hi"),
                "  private final String file;",
                ("  private RealImage real;      // null until needed", "hi"),
                "  ImageProxy(String f) { this.file = f; }  // cheap!",
                "  public int width() { return readMeta(file).w; }  // no decode",
                "}"),
            "note": "Constructing a proxy costs nothing — it just remembers the filename."},
         "narration":
            "Step two: the proxy itself. [pause] ImageProxy implements the very same Image "
            "interface. But its constructor does almost nothing — it just remembers the "
            "filename. No file read, no decode. Creating one is free. [pause] It holds a "
            "reference to a RealImage that starts out null, and stays null until someone "
            "genuinely needs the pixels. [pause] And notice — some questions it can answer "
            "without ever loading. Width and height often live in a tiny metadata header, so the "
            "proxy can read just that, and skip decoding the whole image."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Write the proxy's draw()",
            "file": "ImageProxy.java",
            "lines": ln(
                "private RealImage real;   // starts null",
                "public void draw() {",
                ("  // ▯ load the RealImage on first draw, then delegate", "ghost"),
                "}"),
            "prompt": "First draw() must create the RealImage; every draw after reuses it.",
            "hint": "if (real == null) real = new RealImage(file);  real.draw();"},
         "narration":
            "Your turn — pause here. [pause] The proxy has answered the cheap questions. Now the "
            "expensive one: draw. [pause] The first time draw is called, there are no pixels yet "
            "— so the proxy must create the RealImage, paying the load cost exactly once, right "
            "then. [pause] Every draw after that should reuse the one it already made. [pause] "
            "Write it. Two lines: create if missing, then hand the call to the real image."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "The client holds proxies, unaware",
            "file": "Document.java",
            "lines": ln(
                ("for (String f : files)", "add"),
                ("  images.add(new ImageProxy(f));   // instant", "add"),
                "// ...opening the document is now free...",
                "void drawPage(int p) {",
                "  for (Image img : pageImages(p))",
                ("    img.draw();     // THIS is where loading happens", "hi"),
                "}"),
            "note": "Same Image type, same draw() call — loading moved inside, out of sight."},
         "narration":
            "Step three, and watch the client. [pause] The document now fills its list with "
            "ImageProxy objects instead of RealImages. Constructing them is instant, so opening "
            "a two-hundred-image document is effectively free. [pause] And drawing a page? The "
            "client just calls draw on each image on that page — the exact same call as before. "
            "[pause] It has no idea some of those images are proxies. It never checks isLoaded. "
            "It never sees the loading. [pause] The lazy loading happens inside the draw call, "
            "precisely for the images that page actually shows — and nowhere else."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Open a 200-image report; user reads page 1\"",
            "naiveLabel": "Eager", "naiveCost": "All 200 decoded on open.",
            "naiveSteps": ["≈ 8 s to open", "≈ 2 GB resident",
                           "199 images never viewed"],
            "patLabel": "With proxy", "patCost": "Only what's on screen is ever loaded.",
            "patFile": "same client code",
            "patLines": ln(
                ("doc.open();          // instant — all proxies", "add"),
                ("doc.drawPage(1);     // loads ~3 images", "add"),
                ("// pages never scrolled to cost nothing", "add"))},
         "narration":
            "Now the payoff, in numbers. [pause] Open a two-hundred-image report and read page "
            "one. [pause] Eagerly, that is roughly eight seconds to open and two gigabytes "
            "resident — to decode a hundred and ninety-nine images the reader never scrolls to. "
            "[pause] With the proxy, opening is instant, because every image is just a proxy "
            "holding a filename. Drawing page one loads the two or three images actually on it. "
            "[pause] And here is the quiet beauty: the client code did not change at all. The "
            "exact same draw calls now cost a tiny fraction, because the expense moved behind a "
            "stand-in that only pays when asked."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Proxy Pattern",
            "plain": "A stand-in that implements the same interface as a real object and "
                     "controls access to it — here, delaying its expensive creation.",
            "nodes": [
                {"id": "subj", "title": "Image", "stereo": "interface",
                 "members": ["+ draw() / width()"], "x": 760, "y": 200, "w": 400,
                 "color": "#22D3EE"},
                {"id": "real", "title": "RealImage", "stereo": "real subject",
                 "members": ["- pixels (heavy)", "+ draw()"],
                 "x": 150, "y": 470, "w": 380, "color": "#8B93B0"},
                {"id": "proxy", "title": "ImageProxy", "stereo": "proxy",
                 "members": ["- real: RealImage", "+ draw(): load,", "  then delegate"],
                 "x": 1400, "y": 470, "w": 400, "color": "#A78BFA"}],
            "edges": [
                {"from": "real", "to": "subj", "kind": "impl"},
                {"from": "proxy", "to": "subj", "kind": "impl"},
                {"from": "proxy", "to": "real", "kind": "has"}]},
         "narration":
            "This is the Proxy pattern. [pause] At the top, the interface both sides share — "
            "Image. [pause] On the left, RealImage: the genuine, expensive object. [pause] On "
            "the right, ImageProxy — and look at its two relationships. It implements Image, so "
            "it is usable anywhere an image is. And it holds a reference to a RealImage, which "
            "it creates lazily and then forwards calls to. [pause] That is the whole shape. A "
            "stand-in that looks like the real thing to the client, and controls when and how "
            "the real thing is reached."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Subject", "your": "interface Image"},
                {"role": "RealSubject", "your": "RealImage (the costly one)"},
                {"role": "Proxy", "your": "ImageProxy (stands in)"},
                {"role": "Client", "your": "Document — sees only Image"}],
            "plain": "The proxy shares the subject's interface and holds the real subject, "
                     "forwarding calls while adding control: lazy load, access checks, caching, "
                     "remoting.",
            "gof": "Provide a surrogate or placeholder for another object to control access to "
                   "it."},
         "narration":
            "The names, mapped to your code. [pause] The Subject is the Image interface. The "
            "RealSubject is RealImage, the costly object. The Proxy is ImageProxy, the stand-in. "
            "And the Client is the Document, which only ever sees the Image interface. [pause] "
            "Ours is a virtual proxy — it controls creation, delaying an expensive object. But "
            "the same shape does more. A protection proxy adds access checks. A caching proxy "
            "remembers results. A remote proxy stands in for an object on another machine. "
            "[pause] The Gang of Four: provide a surrogate or placeholder for another object to "
            "control access to it."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "A stand-in has its own costs",
            "costs": ["Another class mirroring the full interface",
                      "One more hop on every call",
                      "A 'cheap' call can secretly do I/O"],
            "dont": ["The real object is already cheap to make",
                     "You don't need to control access at all",
                     "A plain lazy field would do"],
            "signal": "you want to control access to an object — delay it, guard it, cache it, "
                      "or reach it remotely — without the client knowing."},
         "narration":
            "Proxy is not free either. [pause] You are writing another class that must mirror "
            "the real object's entire interface — every method forwarded. And every call now "
            "takes one extra hop through the stand-in. [pause] There is a subtler cost too. A "
            "proxy can make an innocent-looking method secretly expensive — a call that used to "
            "be instant might now quietly touch the disk or the network. That can surprise "
            "whoever is reading the client. [pause] So skip it when the real object is already "
            "cheap to build, when there is no access to control, or when a simple lazy field "
            "would do the job. [pause] Reach for it when you genuinely need to control access to "
            "an object — to delay it, guard it, cache it, or reach it across a network — without "
            "the client ever knowing the difference."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Proxy, in one breath",
            "items": [
                "Eagerly creating expensive objects wasted time and memory on things no one "
                "ever used.",
                "The client only needs the interface — so a lightweight stand-in can implement "
                "it and defer the real work.",
                "Proxy: same interface as the real object, holds it, and controls access — "
                "here, creating it lazily on first use."],
            "challenge": "You call a slow remote pricing service. You want callers to use it "
                         "like a local object, but cache each result for 60 seconds.",
            "question": "Does Proxy fit? What's the subject, the real subject, and what does "
                        "this proxy control?"},
         "narration":
            "Proxy, in one breath. [pause] Eagerly building expensive objects wasted time and "
            "memory on things no one ever used. [pause] But the client only needs the interface "
            "— so a lightweight stand-in can implement it and defer the real work until it is "
            "genuinely needed. [pause] Proxy: the same interface as the real object, a reference "
            "to it, and control over access — here, creating it lazily on first use. [pause] Now "
            "one to carry out. [pause] You call a slow remote pricing service, and you want your "
            "callers to use it like an ordinary local object — but to cache each result for "
            "sixty seconds. [pause] Does Proxy fit? What is the subject, what is the real "
            "subject, and what exactly does this proxy control? [pause] Pause, and sketch it "
            "before the next episode."},
    ],
}


FACADE = {
    "id": "dp13-facade",
    "title": "Facade",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 13",
            "line1": "One call,", "line2": "not seven",
            "sub": "a single front door to a whole subsystem of moving parts"},
         "narration":
            "Some jobs are one idea to you, but many steps to your code. [pause] Place an order. "
            "To you, that is a single intent. To the machine, it is reserve the inventory, "
            "charge the card, schedule the shipment, send the email — in the right order, with "
            "the right rollback when something fails. [pause] And every caller that wants to "
            "place an order has to know that whole dance. [pause] What if there were one front "
            "door, and behind it, all the mess? Let's place an order."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "Placing an order",
            "situation": "Placing an order means coordinating four subsystems — inventory, "
                         "payments, shipping, and email — in a specific sequence, each with its "
                         "own API and its own failure modes.",
            "actors": [
                {"emoji": "📦", "label": "Inventory"},
                {"emoji": "💳", "label": "Payments"},
                {"emoji": "🚚", "label": "Shipping + email"}],
            "ask": "How do you let a caller place an order without wiring up all four "
                   "themselves?"},
         "narration":
            "Here is the situation: placing an order. [pause] It sounds like one action, but it "
            "touches four separate subsystems. Inventory, to reserve the items. Payments, to "
            "charge the card. Shipping, to schedule delivery. And email, to confirm. [pause] "
            "They must run in a particular order — you do not ship before the payment clears — "
            "and each one can fail in its own way. [pause] So the question is: how do you let a "
            "caller simply place an order, without making it wire up and babysit all four "
            "subsystems itself?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "The controller does it all.",
            "file": "OrderController.java",
            "lines": ln(
                "void checkout(Cart cart) {",
                ("  inventory.reserve(cart.items());", "hi"),
                ("  payment.charge(cart.total());", "hi"),
                ("  shipping.schedule(cart.address());", "hi"),
                ("  email.sendConfirmation(cart.user());", "hi"),
                "  // ...and undo it all if any step throws",
                "}"),
            "note": "The controller knows all 4 subsystems, their order, their rollback."},
         "narration":
            "The direct approach: the controller just does every step. [pause] Reserve the "
            "inventory. Charge the payment. Schedule the shipment. Send the confirmation email. "
            "[pause] It works — and honestly, it reads clearly enough, right here. [pause] But "
            "look at what this one method now knows. It knows all four subsystems, and each of "
            "their APIs. It knows the exact order they must run in. And it owns the rollback if "
            "step three fails after step two already charged the card. [pause] All of that — the "
            "orchestration of a whole subsystem — living inside a controller whose real job was "
            "just to handle a web request."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"The mobile app needs to order too. And the admin. And a cron job.\"",
            "file": "everywhere.java",
            "lines": ln(
                ("class WebController   { /* the same 4 steps */ }", "hi"),
                ("class MobileApi       { /* the same 4 steps */ }", "hi"),
                ("class AdminPanel      { /* the same 4 steps */ }", "hi"),
                ("class ReorderCronJob  { /* the same 4 steps */ }", "hi"),
                "// change the flow → change all four. miss one → a bug."),
            "smell": "The orchestration copied into every entry point",
            "touched": ["4 callers, one 4-step dance each",
                        "add a step → edit all four",
                        "each re-implements rollback",
                        "every caller coupled to every subsystem"]},
         "narration":
            "Then the same order has to be placeable from somewhere else. The mobile API. An "
            "internal admin panel. A cron job that reorders staples. [pause] And each of them "
            "copies the same four-step sequence, the same ordering, the same rollback. [pause] "
            "Now change the flow — say you must reserve inventory only after payment clears — "
            "and you have to find and fix that logic in four different places. Miss one, and you "
            "have a subtle, expensive bug. [pause] Worse, every one of these callers is now "
            "welded to all four subsystems. A change to the payment API ripples into the admin "
            "panel, the cron job, everywhere."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["Callers all want one thing: place an order",
                      "The four subsystems and their order",
                      "Rollback belongs with the sequence"],
            "varies": ["Which caller asks (web, mobile, cron)",
                       "Occasionally, the steps in the flow"],
            "principle": "Wrap the whole subsystem behind one simple entry point — callers ask "
                         "it, not the parts."},
         "narration":
            "So what is fixed, and what varies? [pause] Fixed: every caller wants the exact same "
            "thing — place this order. The four subsystems, and the sequence they run in, are "
            "the same each time. And the rollback logic belongs with that sequence, not "
            "scattered. [pause] What varies is only who is asking — the web, the mobile app, a "
            "cron job — and, once in a while, a tweak to the steps themselves. [pause] Here is "
            "the move. [pause] Wrap the entire subsystem behind a single, simple entry point. "
            "One object, with one method that means place an order. Callers talk to it — and "
            "never touch the four parts directly again."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "A hotel concierge", "emoji": "🛎️",
            "analogy": "You make one request; the concierge coordinates housekeeping, the "
                       "kitchen, and the car — you never call them yourself.",
            "map": [
                {"from": "The concierge", "to": "the facade object"},
                {"from": "Housekeeping, kitchen, valet", "to": "the subsystem classes"},
                {"from": "\"Arrange my evening\"", "to": "one method, placeOrder()"},
                {"from": "You can still call the kitchen", "to": "subsystems stay usable directly"}],
            "breaks": "a concierge can improvise; a facade only does the orchestration you "
                      "coded into it."},
         "narration":
            "Think of a hotel concierge. [pause] You want dinner, a pressed shirt, and a car at "
            "eight. [pause] You do not call housekeeping, then the kitchen, then the valet, in "
            "the right order, yourself. You make one request to the concierge, and they "
            "coordinate all of it behind the desk. [pause] The concierge is the facade. "
            "Housekeeping, the kitchen, the valet are the subsystems. Your single request is the "
            "one method. [pause] And crucially — you can still walk down to the kitchen and talk "
            "to them directly if you ever need to. The concierge is a convenience, not a wall. A "
            "facade works the same way: it simplifies, but it does not lock the subsystems "
            "away."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "One object in front of the subsystem",
            "file": "OrderService.java",
            "lines": ln(
                ("public class OrderService {         // the facade", "add"),
                ("  private final Inventory inventory;", "add"),
                ("  private final Payment payment;", "add"),
                ("  private final Shipping shipping;", "add"),
                ("  private final Email email;         // holds them all", "add"),
                "}"),
            "note": "The facade owns a reference to every subsystem it will coordinate."},
         "narration":
            "The refactor, step one. [pause] We create one new class — OrderService, the facade. "
            "[pause] Its job is not to do the work of inventory or payment itself. Its job is to "
            "hold a reference to each of the four subsystems, and to coordinate them. [pause] "
            "Nothing clever yet. It is simply the one place that gets to know about all four "
            "parts at once — so that no one else has to."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "One method that runs the whole flow",
            "file": "OrderService.java",
            "lines": ln(
                ("public void placeOrder(Cart cart) {", "hi"),
                "  inventory.reserve(cart.items());",
                ("  try { payment.charge(cart.total()); }", "hi"),
                ("  catch (Exception e) { inventory.release(); throw e; }", "hi"),
                "  shipping.schedule(cart.address());",
                "  email.sendConfirmation(cart.user());",
                "}"),
            "note": "The sequence — and its rollback — now lives in exactly one place."},
         "narration":
            "Step two: the one method that matters. [pause] placeOrder takes a cart, and inside "
            "it, the whole dance finally lives in a single place. [pause] Reserve the inventory. "
            "Try to charge the card — and if that fails, release the inventory you just reserved "
            "and stop. Then schedule the shipment, and send the confirmation. [pause] Every "
            "subtle thing the callers used to get wrong — the ordering, the rollback when a "
            "later step fails — is now written once, correctly, right here. [pause] This is the "
            "heart of the facade: not hiding the subsystems, but owning the choreography between "
            "them."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Where does a fraud check go?",
            "file": "OrderService.java",
            "lines": ln(
                "public void placeOrder(Cart cart) {",
                "  // a new rule: screen for fraud BEFORE charging",
                ("  // ▯ where does this step belong?", "ghost"),
                "  payment.charge(cart.total());",
                "}"),
            "prompt": "A fraud-screening step must run before payment. Which code changes — and "
                      "which doesn't?",
            "hint": "Add fraud.screen(cart) inside placeOrder. Zero callers change."},
         "narration":
            "Your turn — pause here. [pause] A new requirement lands: every order must be "
            "screened for fraud before the card is charged. [pause] The question is not how to "
            "write the check. It is where it goes — and, just as important, what does not have "
            "to change. [pause] Think about the web controller, the mobile API, the admin "
            "panel, the cron job. How many of them need to be touched to add a fraud check to "
            "every order? [pause] Sit with that answer, because it is the entire payoff of this "
            "pattern."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "Every caller shrinks to one line",
            "file": "callers.java",
            "lines": ln(
                ("class WebController {", "add"),
                ("  void checkout(Cart c) { orders.placeOrder(c); }", "add"),
                ("}", "add"),
                "// mobile, admin, cron — all identical:",
                ("orders.placeOrder(cart);   // that's the whole flow", "hi")),
            "note": "Callers know one method. The subsystems, and their order, are hidden."},
         "narration":
            "Step three, and watch every caller collapse. [pause] The web controller's checkout "
            "method is now a single line — ask the order service to place the order. [pause] The "
            "mobile API, the admin panel, the cron job — every one of them becomes that same "
            "single call. [pause] None of them knows there are four subsystems. None of them "
            "knows the order, or the rollback, or that a fraud check was just added. [pause] "
            "They know one thing: place an order. That is the front door, and everything "
            "complicated is behind it."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Add loyalty points and an SMS on every order\"",
            "naiveLabel": "Before", "naiveCost": "Edit all 4 callers, hope you match.",
            "naiveSteps": ["find every place that orders", "add 2 steps to each, in order",
                           "one inconsistent copy → a bug"],
            "patLabel": "Now", "patCost": "Two lines in placeOrder(). Everyone benefits.",
            "patFile": "OrderService.java",
            "patLines": ln(
                ("  loyalty.award(cart.user(), cart.total());", "add"),
                ("  sms.notify(cart.user());", "add"),
                ("  // every caller gets this, unchanged", "add"))},
         "narration":
            "Now the requirement that used to mean touching everything. Award loyalty points and "
            "send an SMS on every order. [pause] Before the facade, that meant hunting down all "
            "four callers and adding two more steps to each — in the right spot, consistently, "
            "without missing one. [pause] Now? You add two lines inside placeOrder. [pause] And "
            "instantly the web, the mobile app, the admin panel, and the cron job all award "
            "points and send the SMS — every one of them, without a single line changing in any "
            "caller. The behavior lives in one place, so it improves in one place."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Facade Pattern",
            "plain": "One simplified object stands in front of a complex subsystem, giving "
                     "clients a single entry point while the parts stay usable underneath.",
            "nodes": [
                {"id": "client", "title": "Client", "members": ["placeOrder(cart)"],
                 "x": 120, "y": 440, "w": 340, "color": "#8B93B0"},
                {"id": "facade", "title": "OrderService", "stereo": "facade",
                 "members": ["+ placeOrder(cart)", "coordinates all 4"],
                 "x": 620, "y": 415, "w": 460, "color": "#A78BFA"},
                {"id": "inv", "title": "Inventory", "members": ["reserve()"],
                 "x": 1360, "y": 190, "w": 440, "color": "#22D3EE"},
                {"id": "pay", "title": "Payment", "members": ["charge()"],
                 "x": 1360, "y": 360, "w": 440, "color": "#22D3EE"},
                {"id": "shp", "title": "Shipping", "members": ["schedule()"],
                 "x": 1360, "y": 530, "w": 440, "color": "#22D3EE"},
                {"id": "eml", "title": "Email", "members": ["send()"],
                 "x": 1360, "y": 700, "w": 440, "color": "#22D3EE"}],
            "edges": [
                {"from": "client", "to": "facade", "kind": "assoc"},
                {"from": "facade", "to": "inv", "kind": "has"},
                {"from": "facade", "to": "pay", "kind": "has"},
                {"from": "facade", "to": "shp", "kind": "has"},
                {"from": "facade", "to": "eml", "kind": "has"}]},
         "narration":
            "This is the Facade pattern. [pause] On the left, the client — every caller, now "
            "identical. [pause] In the middle, the facade, OrderService: the single front door. "
            "[pause] And on the right, the subsystems it coordinates — inventory, payment, "
            "shipping, email — each with its own real work to do. [pause] Look at the shape. The "
            "client talks only to the facade. The facade fans out to all four subsystems, in "
            "the right order, with the right recovery. [pause] One simple entry point in front; "
            "all the genuine complexity, organized, behind it."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Facade", "your": "OrderService.placeOrder()"},
                {"role": "Subsystems", "your": "Inventory, Payment, Shipping, Email"},
                {"role": "Client", "your": "controllers, cron — call the facade"},
                {"role": "(Not hidden)", "your": "subsystems still usable directly"}],
            "plain": "The facade offers a simple, unified method over a set of subsystems, "
                     "without preventing direct access to them when needed.",
            "gof": "Provide a unified interface to a set of interfaces in a subsystem. Facade "
                   "defines a higher-level interface that makes the subsystem easier to use."},
         "narration":
            "The names, mapped to your code. [pause] The Facade is OrderService, and its "
            "placeOrder method. [pause] The Subsystems are inventory, payment, shipping, and "
            "email — the classes doing the real work. [pause] The Client is any controller or "
            "job that now just calls the facade. [pause] And note the fourth row, because it "
            "separates a facade from a wall — the subsystems are not hidden. If some special "
            "caller genuinely needs to talk to payment directly, it still can. [pause] The Gang "
            "of Four: provide a unified interface to a set of interfaces in a subsystem — a "
            "higher-level interface that makes the subsystem easier to use."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "A front door can grow too big",
            "costs": ["The facade can swell into a god object",
                      "It doesn't remove complexity — it relocates it",
                      "One more layer between caller and work"],
            "dont": ["The subsystem is already one simple call",
                     "Callers genuinely need fine-grained control",
                     "You'd just be forwarding a single method"],
            "signal": "several clients repeat the same multi-step dance across the same set of "
                      "subsystems."},
         "narration":
            "Facade has its own failure mode. [pause] The most common one: the facade becomes a "
            "dumping ground. Every new cross-subsystem operation gets bolted on, until "
            "OrderService is a two-thousand-line god object that knows everything. [pause] And "
            "remember — a facade does not remove the complexity. The four subsystems are still "
            "there, still complicated. The facade just relocates the mess into one managed "
            "place, and adds a layer to pass through. [pause] So skip it when the subsystem is "
            "already a single simple call, or when your callers genuinely need fine-grained "
            "control over the parts. [pause] Reach for it when several clients keep repeating "
            "the same multi-step dance across the same set of subsystems. That repetition is "
            "the facade, asking to exist."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Facade, in one breath",
            "items": [
                "Every caller re-implemented the same multi-step subsystem dance — coupled to "
                "every part, and easy to get subtly wrong.",
                "Callers all want one thing, and the subsystems and their order are fixed — so "
                "wrap them behind one simple entry point.",
                "Facade: a single object that coordinates the subsystems, so clients ask it, "
                "not the parts — while the parts stay reachable."],
            "challenge": "A video pipeline must probe, decode, filter, encode, and mux a file — "
                         "five libraries, one correct order — and three tools all need to 'just "
                         "convert this.'",
            "question": "Does Facade fit? What's the facade, the subsystems, and what stays "
                        "directly accessible?"},
         "narration":
            "Facade, in one breath. [pause] Every caller re-implemented the same multi-step "
            "subsystem dance, coupled to every part, and easy to get subtly wrong. [pause] But "
            "they all want the same one thing, and the subsystems and their order are fixed — so "
            "you wrap them behind a single simple entry point. [pause] Facade: one object that "
            "coordinates the subsystems, so clients ask it instead of the parts — while the "
            "parts stay reachable for anyone who truly needs them. [pause] Here is one to carry "
            "out. [pause] A video pipeline must probe a file, decode it, apply a filter, encode "
            "it, and mux the result — five libraries, one correct order — and three different "
            "tools all just want to convert this. [pause] Does Facade fit? What is the facade, "
            "what are the subsystems, and what should stay directly accessible? [pause] Pause, "
            "and sketch it before the next episode."},
    ],
}


ITERATOR = {
    "id": "dp14-iterator",
    "title": "Iterator",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 14",
            "line1": "Walk it", "line2": "without knowing its shape",
            "sub": "one way to visit every element, whatever the collection is underneath"},
         "narration":
            "You have a collection, and you want to visit every item in it. [pause] Simple — "
            "until the collection is not a flat list. It is a tree, or a ring buffer, or a "
            "stream of pages from a server. [pause] If your loop knows how the items are stored, "
            "then the day you change the storage, every loop that touched it breaks. [pause] "
            "There is a way to walk any collection without ever knowing its shape. Let's build a "
            "playlist."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "Play every song in a playlist",
            "situation": "A playlist holds songs. Today it's backed by an array. Tomorrow it "
                         "might be a shuffled linked structure, or a tree of nested playlists — "
                         "but callers just want each song, in order.",
            "actors": [
                {"emoji": "🎵", "label": "A playlist"},
                {"emoji": "🗂️", "label": "…some internal store"},
                {"emoji": "▶️", "label": "visit each in order"}],
            "ask": "How do callers walk every song without knowing how it's stored inside?"},
         "narration":
            "Here is the collection: a playlist of songs. [pause] Right now, it happens to be "
            "backed by a plain array. [pause] But that could change. Tomorrow it might be a "
            "linked structure so shuffling is cheap, or even a tree of nested playlists — an "
            "album inside a mix inside a mix. [pause] Through all of that, every caller wants "
            "the same simple thing: give me each song, in order, until there are no more. "
            "[pause] So how do they walk the whole playlist without knowing, or caring, how the "
            "songs are stored inside it?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "Loop over the index.",
            "file": "Player.java",
            "lines": ln(
                "Playlist pl = ...;",
                ("for (int i = 0; i < pl.size(); i++) {", "hi"),
                ("  Song s = pl.get(i);        // assumes an index", "hi"),
                "  play(s);",
                "}",
                "// or worse: for (Song s : pl.songsArray()) ...",
                "//          the internal array, handed right out"),
            "note": "size() + get(i) leak that it's index-based. songsArray() leaks it entirely."},
         "narration":
            "The obvious approach: loop by index. [pause] Ask the playlist its size, then pull "
            "song zero, song one, song two, and play each. [pause] It works — as long as the "
            "playlist is an array underneath. Because get of i, and size, quietly assume there "
            "is an index to count through. [pause] And the tempting shortcut is even worse — "
            "expose the internal array directly and let callers loop over that. [pause] Now the "
            "player is not just using the playlist. It knows exactly how the playlist stores its "
            "songs — and it has welded itself to that."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Make shuffle cheap. Also, nested playlists.\"",
            "file": "breaks.java",
            "lines": ln(
                ("// switch backing to a linked list for O(1) shuffle", "hi"),
                ("pl.get(i);   // now O(n) — the loop is O(n²)!", "hi"),
                ("// and a TREE of playlists has no 'index' at all", "hi"),
                "for (int i...) // ...cannot express a tree walk",
                ("player, exporter, shuffler — every loop rewrites", "hi")),
            "smell": "Every caller re-encodes how the collection is traversed",
            "touched": ["array → linked list: get(i) goes O(n)",
                        "index loop silently becomes O(n²)",
                        "a tree has no index to loop at all",
                        "player, export, shuffle — all rewritten"]},
         "narration":
            "Then the requirements shift. [pause] Make shuffle cheap, so you switch the backing "
            "to a linked list. [pause] Suddenly get of i is no longer instant — it has to walk "
            "from the front every time. Your innocent index loop just became quietly quadratic. "
            "[pause] And then someone wants nested playlists — a tree. A tree has no index at "
            "all. The for-i loop cannot even express how to walk it. [pause] Every place that "
            "looped — the player, the exporter, the shuffler — has to be rewritten, because each "
            "of them encoded, by hand, how to traverse a structure that just changed underneath "
            "them."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["Callers want each element, one at a time",
                      "\"Is there another?\" then \"give it to me\"",
                      "They stop when the collection is exhausted"],
            "varies": ["How the elements are stored",
                       "How you advance to the next one"],
            "principle": "Extract a cursor object that knows how to walk THIS structure: "
                         "hasNext(), then next()."},
         "narration":
            "So what is fixed, and what varies? [pause] Fixed: every caller wants the elements "
            "one at a time. The pattern of use is always the same two questions — is there "
            "another one? and if so, give it to me — repeated until the collection runs out. "
            "[pause] What varies is only how the elements are stored, and therefore how you step "
            "from one to the next. [pause] Here is the move. [pause] Pull that stepping logic "
            "out into its own little object — a cursor that knows how to walk this particular "
            "structure. It answers just two methods: has-next, and next. The caller asks those; "
            "the cursor keeps the place."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "A museum audio guide", "emoji": "🎧",
            "analogy": "You press 'next' and hear the next exhibit; the guide knows the route — "
                       "you never read the floor plan.",
            "map": [
                {"from": "Pressing 'next'", "to": "the next() call"},
                {"from": "\"Is the tour over?\"", "to": "hasNext()"},
                {"from": "The guide's hidden route", "to": "the traversal logic"},
                {"from": "The museum's layout", "to": "the collection's internal store"}],
            "breaks": "an audio guide has one fixed route; a collection can hand out a fresh, "
                      "independent cursor to each caller at once."},
         "narration":
            "Think of a museum audio guide. [pause] You put on the headphones and press next. It "
            "plays the next exhibit. Press next again — the one after that. [pause] You never "
            "look at the floor plan. You do not know if the route runs clockwise, or by theme, "
            "or up one wing and down another. The guide holds the route; you just press next "
            "until it tells you the tour is over. [pause] Pressing next is the next call. Asking "
            "whether the tour is over is has-next. The route the guide keeps to itself is the "
            "traversal logic, and the museum's actual layout is the collection's internal store. "
            "[pause] Where it strains: one audio guide has one fixed route, but a collection can "
            "hand a fresh, independent cursor to every caller at once."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "Name the two questions: Iterator",
            "file": "Iterator.java",
            "lines": ln(
                ("interface Iterator<T> {   // Java already has this", "add"),
                ("  boolean hasNext();", "add"),
                ("  T next();", "add"),
                ("}", "add"),
                "class Playlist implements Iterable<Song> {",
                ("  public Iterator<Song> iterator() { ... }", "hi"),
                "}"),
            "note": "Playlist promises only to HAND OUT a cursor — not to reveal its store."},
         "narration":
            "The refactor, step one. [pause] Name the two questions as an interface — and Java "
            "already has it for you. Iterator, with just has-next and next. [pause] Then the "
            "playlist implements Iterable, which promises exactly one thing: I can give you an "
            "iterator. [pause] Notice what the playlist no longer promises. It does not expose "
            "an array. It does not expose an index. Its entire public contract for looping is: "
            "ask me for a cursor, and I will hand you one. How that cursor works is nobody "
            "else's business."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "The cursor holds the traversal state",
            "file": "PlaylistIterator.java",
            "lines": ln(
                ("class PlaylistIterator implements Iterator<Song> {", "hi"),
                "  private Node cursor = head;   // walks a linked list",
                ("  public boolean hasNext() { return cursor != null; }", "hi"),
                "  public Song next() {",
                "    Song s = cursor.song; cursor = cursor.nextNode;",
                "    return s;",
                "  }",
                "}"),
            "note": "All the 'how to walk it' logic — the cursor — lives here, and only here."},
         "narration":
            "Step two: the cursor itself. [pause] PlaylistIterator implements Iterator, and "
            "inside it lives all the knowledge of how to walk this structure. [pause] Here it "
            "holds a node reference into a linked list. Has-next just checks whether the cursor "
            "has run off the end. And next grabs the current song, steps the cursor forward one "
            "node, and returns what it took. [pause] Every messy detail of the traversal — where "
            "we are, how we advance — is sealed inside this one class. [pause] If the store were "
            "an array instead, only this cursor would change. A tree? A cursor with a stack "
            "inside. The caller never sees any of it."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Write hasNext() for an array store",
            "file": "ArrayPlaylistIterator.java",
            "lines": ln(
                "private final Song[] songs;",
                "private int pos = 0;      // cursor into the array",
                "public boolean hasNext() {",
                ("  // ▯ is there still a song at pos?", "ghost"),
                "}"),
            "prompt": "This cursor walks an array by index. When is there another song to give?",
            "hint": "return pos < songs.length;"},
         "narration":
            "Your turn — pause here. [pause] Say this playlist really is backed by an array, and "
            "the cursor is just an integer position into it. [pause] Write has-next. It should "
            "answer one question: from where the cursor sits right now, is there still a song "
            "left to hand out? [pause] Think about the boundary — what is the very last valid "
            "position, and where does the cursor have to be for the answer to become false?"},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "Every caller becomes one for-each",
            "file": "callers.java",
            "lines": ln(
                ("for (Song s : playlist)   // Java calls iterator()", "add"),
                ("  play(s);                // for you, invisibly", "add"),
                "// exporter, shuffler — the exact same loop",
                "// swap array → linked list → tree:",
                ("//   the for-each above does not change", "hi")),
            "note": "for-each just calls iterator(). Change the store; the loop is untouched."},
         "narration":
            "Step three, and every caller collapses into one line. [pause] For each song in the "
            "playlist, play it. That is the whole loop. [pause] And here is the quiet magic — "
            "Java's for-each is not built into arrays. It is built on Iterable. Behind that "
            "clean syntax, Java calls your iterator method and drives has-next and next for you. "
            "[pause] The player uses it. The exporter uses it. The shuffler uses it — all the "
            "identical loop. [pause] And when you swap the backing from an array to a linked "
            "list to a tree? Not one of those for-each loops changes. The traversal moved into "
            "the cursor, where it belongs."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Play a TREE of nested playlists, in order\"",
            "naiveLabel": "Before", "naiveCost": "The index loop can't walk a tree at all.",
            "naiveSteps": ["for-i assumes a flat index",
                           "a tree has none — rewrite everything",
                           "traversal logic bleeds into callers"],
            "patLabel": "Now", "patCost": "One new cursor. Every for-each just works.",
            "patFile": "TreeIterator.java",
            "patLines": ln(
                ("class TreeIterator implements Iterator<Song> {", "add"),
                ("  Deque<Node> stack = ...;   // depth-first", "add"),
                ("  public Song next() { /* pop, push kids */ }", "add"),
                ("}   // for (Song s : tree) — unchanged", "add"))},
         "narration":
            "Now the requirement that used to be impossible. Play a whole tree of nested "
            "playlists, in order. [pause] Before, the index loop could not even begin — a tree "
            "has no flat index to count through, so every caller would need rewriting. [pause] "
            "Now? You write one new cursor. A tree iterator that keeps a stack inside it and "
            "walks depth-first — pop a node, push its children, hand back its song. [pause] And "
            "the callers? For each song in the tree, play it. The very same for-each you already "
            "wrote. The new structure needed a new cursor, and absolutely nothing else."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Iterator Pattern",
            "plain": "Give a collection a cursor object that walks its elements one at a time, "
                     "so clients traverse it without ever seeing how it's stored.",
            "nodes": [
                {"id": "iter", "title": "Iterator<Song>", "stereo": "interface",
                 "members": ["+ hasNext(): bool", "+ next(): Song"],
                 "x": 760, "y": 200, "w": 400, "color": "#22D3EE"},
                {"id": "agg", "title": "Playlist", "stereo": "Iterable",
                 "members": ["- songs (any store)", "+ iterator()"],
                 "x": 150, "y": 470, "w": 380, "color": "#8B93B0"},
                {"id": "conc", "title": "PlaylistIterator", "stereo": "iterator",
                 "members": ["- cursor / stack", "+ hasNext() / next()"],
                 "x": 1400, "y": 470, "w": 400, "color": "#A78BFA"}],
            "edges": [
                {"from": "conc", "to": "iter", "kind": "impl"},
                {"from": "agg", "to": "conc", "kind": "assoc"}]},
         "narration":
            "This is the Iterator pattern. [pause] At the top, the interface — Iterator, with "
            "just has-next and next. [pause] On the left, the aggregate: the Playlist, which is "
            "Iterable. Its only looping duty is to hand out a cursor. [pause] On the right, the "
            "concrete iterator — the cursor itself, holding an index, or a node, or a stack, and "
            "implementing has-next and next. [pause] The arrow from the playlist to the cursor "
            "is the key: the collection creates a fresh iterator on demand. [pause] The client "
            "holds only the interface at the top, and walks anything — array, list, or tree — "
            "the exact same way."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Iterator", "your": "java.util.Iterator<T>"},
                {"role": "ConcreteIterator", "your": "PlaylistIterator (holds the cursor)"},
                {"role": "Aggregate", "your": "Playlist implements Iterable<Song>"},
                {"role": "Client", "your": "for (Song s : playlist) — hidden calls"}],
            "plain": "The aggregate creates a concrete iterator that holds the traversal state; "
                     "the client drives hasNext()/next() — usually via for-each.",
            "gof": "Provide a way to access the elements of an aggregate object sequentially "
                   "without exposing its underlying representation."},
         "narration":
            "The names, mapped to your code. [pause] The Iterator is Java's own Iterator "
            "interface. [pause] The ConcreteIterator is PlaylistIterator — the object that holds "
            "the cursor and knows the walk. [pause] The Aggregate is the Playlist, which "
            "implements Iterable. [pause] And the Client is any for-each loop, which calls "
            "has-next and next for you, invisibly. [pause] The Gang of Four: provide a way to "
            "access the elements of an aggregate object sequentially, without exposing its "
            "underlying representation. That last clause is the entire point — sequential "
            "access, zero exposure."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "A cursor is still an object",
            "costs": ["A separate iterator class per structure",
                      "The cursor holds mutable position state",
                      "Modify the collection mid-walk → it may throw"],
            "dont": ["It's already a List you can for-each",
                     "You need random access by index",
                     "The collection is tiny and fixed"],
            "signal": "you expose, or keep rewriting, how a collection is traversed — especially "
                      "if its internal structure might change."},
         "narration":
            "Iterator has its costs too. [pause] Each new kind of structure means another "
            "iterator class. And a cursor is stateful — it remembers a position — so two walks "
            "need two iterators, and you cannot casually share one. [pause] There is a famous "
            "trap here: if you modify the collection while an iterator is walking it, a "
            "well-built iterator will notice and fail fast, throwing rather than quietly "
            "returning garbage. [pause] So do not reach for it when you already have a plain "
            "List you can for-each, when you genuinely need random access by index, or when the "
            "collection is tiny and never changes shape. [pause] Reach for it when you find "
            "yourself exposing how a collection is stored, or rewriting its traversal every time "
            "the structure changes underneath you."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Iterator, in one breath",
            "items": [
                "Index loops assumed how the collection was stored — so changing the store "
                "silently broke, or slowed, every caller.",
                "Callers only ever ask 'another?' then 'give it' — so hand them a cursor that "
                "answers exactly that: hasNext(), next().",
                "Iterator: the collection creates a cursor holding the traversal; clients walk "
                "any shape the same way. New structure, new cursor."],
            "challenge": "A REST API returns results one page at a time. You want callers to "
                         "treat it as one endless stream of items — each next() may quietly "
                         "fetch the following page.",
            "question": "Does Iterator fit? What's the aggregate, the cursor, and what state "
                        "does next() hide?"},
         "narration":
            "Iterator, in one breath. [pause] Index loops assumed how the collection was stored, "
            "so the day you changed the store, every caller silently broke or slowed to a crawl. "
            "[pause] But callers only ever ask two things — is there another, and give it to me "
            "— so you hand them a cursor that answers exactly that. [pause] Iterator: the "
            "collection creates a cursor that holds the traversal, and clients walk any shape "
            "the same way. A new structure needs only a new cursor. [pause] Here is one to carry "
            "out. [pause] A REST API returns results one page at a time, but you want your "
            "callers to treat it as a single, endless stream of items — where each call to next "
            "might quietly fetch the following page. [pause] Does Iterator fit? What is the "
            "aggregate, what is the cursor, and what state does next hide from the caller? "
            "[pause] Pause, and sketch it before the next episode."},
    ],
}


CHAIN = {
    "id": "dp15-chain-of-responsibility",
    "title": "Chain of Responsibility",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 15",
            "line1": "Who can", "line2": "approve this?",
            "sub": "a request travels a line of handlers until one of them can say yes"},
         "narration":
            "A request comes in, and the question is: who deals with it? [pause] Not always the "
            "same person. A small expense, a team lead can approve. A big one has to climb to a "
            "manager, a director, the CFO. [pause] The wrong instinct is to make the sender "
            "figure out who — to bake the whole org chart into the code that just wanted to "
            "submit an expense. [pause] There is a way to let the request find its own approver. "
            "Let's approve an expense."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "Approve an expense report",
            "situation": "Expenses are approved by limit: a team lead up to $500, a manager up "
                         "to $5,000, a director up to $50,000, the CFO beyond. Each request "
                         "needs exactly one approver who can cover it.",
            "actors": [
                {"emoji": "🧾", "label": "An expense"},
                {"emoji": "🪜", "label": "Tiered approvers"},
                {"emoji": "✅", "label": "…exactly one approves"}],
            "ask": "How does a request reach the right approver without the submitter knowing "
                   "the whole hierarchy?"},
         "narration":
            "Here is the request: an expense report that needs a sign-off. [pause] Approval "
            "runs by limit. A team lead can approve up to five hundred dollars. A manager up to "
            "five thousand. A director up to fifty thousand. Above that, it is the CFO. [pause] "
            "Every expense needs exactly one approver — the first one whose limit is high enough "
            "to cover it. [pause] So how does a submitted expense reach the right approver, "
            "without the person submitting it having to know the entire hierarchy and every "
            "threshold in it?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "One big if-else ladder.",
            "file": "ExpenseService.java",
            "lines": ln(
                "void approve(Expense e) {",
                ("  if (e.amount() <= 500)", "hi"),
                "    teamLead.sign(e);",
                ("  else if (e.amount() <= 5_000)", "hi"),
                "    manager.sign(e);",
                ("  else if (e.amount() <= 50_000)", "hi"),
                "    director.sign(e);",
                "  else cfo.sign(e);",
                "}"),
            "note": "The submitter's code hard-codes every tier, every limit, every order."},
         "narration":
            "The direct approach: an if-else ladder. [pause] If the amount is under five "
            "hundred, the team lead signs. Under five thousand, the manager. Under fifty "
            "thousand, the director. Otherwise, the CFO. [pause] It works, and it even reads "
            "clearly. [pause] But look at what this method now contains. It knows every "
            "approver. It knows every limit. It knows the exact order they escalate in. [pause] "
            "The organization's entire approval policy is hard-coded into a method whose only "
            "real job was to submit one expense."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Add a VP tier. And Finance submits expenses too. And Procurement.\"",
            "file": "ladders.java",
            "lines": ln(
                ("class ExpenseService { /* the if-else ladder */ }", "hi"),
                ("class TravelPortal   { /* the SAME ladder */ }", "hi"),
                ("class ProcurementApp { /* the SAME ladder */ }", "hi"),
                "// insert a VP tier between manager & director:",
                ("// ...find and edit EVERY ladder. change a limit? same.", "hi")),
            "smell": "The approval hierarchy copied into every submitter",
            "touched": ["3 submitters, one ladder each",
                        "new VP tier → edit all three",
                        "change a limit → edit all three",
                        "miss one → the wrong approver signs"]},
         "narration":
            "Then it spreads. The travel portal submits expenses too, and so does procurement — "
            "and each copies the same if-else ladder. [pause] Now the company inserts a VP tier "
            "between manager and director. [pause] You have to find and edit every ladder, in "
            "every submitter, and get the new boundaries exactly right in all of them. [pause] "
            "Change a single limit — say the manager's cap rises to eight thousand — and again, "
            "every copy. [pause] Miss one, and an expense quietly goes to the wrong approver. "
            "The policy lives in a dozen places, when it should live in exactly one."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["A request needs exactly one approver",
                      "Each approver can cover up to a limit",
                      "If they can't, it escalates upward"],
            "varies": ["The set of approvers and their limits",
                       "Their order in the chain"],
            "principle": "Give each approver a limit and a 'next'; let the request walk the line "
                         "until one handles it."},
         "narration":
            "What is fixed, and what varies? [pause] Fixed: a request needs exactly one "
            "approver. Each approver can handle amounts up to some limit. And if they cannot, it "
            "escalates to whoever is above them. That shape never changes. [pause] What varies "
            "is only the set of approvers, their limits, and the order they sit in. [pause] Here "
            "is the move. [pause] Give each approver two things: a limit, and a reference to the "
            "next approver up. Then hand the request to the first one, and let it walk the line "
            "by itself — each approver either handles it or passes it along — until one can say "
            "yes."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "Escalating a support call", "emoji": "☎️",
            "analogy": "The front-line rep helps if they can; if not, they transfer you up — you "
                       "called once, the call travels.",
            "map": [
                {"from": "You, calling once", "to": "submitting the request"},
                {"from": "The front-line rep", "to": "the first handler"},
                {"from": "\"Beyond me — transferring you\"", "to": "passing to the next"},
                {"from": "Whoever finally helps", "to": "the handler that handles it"}],
            "breaks": "a phone tree can dead-end in hold music; a good chain ends in someone — "
                      "or an explicit 'no one can.'"},
         "narration":
            "Think about calling customer support. [pause] You explain your problem once, to "
            "whoever picks up. [pause] The front-line rep either solves it — or says, that is "
            "beyond what I can do, let me transfer you. And up you go, to a supervisor, maybe a "
            "manager, until you reach someone who can actually help. [pause] You only made one "
            "call. The call traveled. [pause] Calling once is submitting the request. The "
            "front-line rep is the first handler. Each transfer is passing to the next. And "
            "whoever finally helps is the handler that handles it. [pause] Where it breaks: a "
            "real phone tree can dead-end in hold music. A well-built chain should always end in "
            "someone — or in an explicit nobody can approve this."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "Each approver: a limit, a next, a handle()",
            "file": "Approver.java",
            "lines": ln(
                ("abstract class Approver {", "add"),
                ("  protected Approver next;          // the one above", "add"),
                ("  protected final long limit;", "add"),
                ("  void handle(Expense e) {", "add"),
                ("    if (e.amount() <= limit) sign(e);       // I can", "add"),
                ("    else if (next != null) next.handle(e);  // escalate", "add"),
                ("  }", "add"),
                "}"),
            "note": "The escalation logic is written ONCE, in the base handler."},
         "narration":
            "The refactor, step one. [pause] We define an abstract Approver. Every approver has "
            "a limit, and a reference to the next approver above them. [pause] And the handle "
            "method — written once, here in the base class — captures the entire policy. If the "
            "amount is within my limit, I sign it. Otherwise, if there is someone above me, I "
            "pass it up. [pause] That is the whole mechanism. Every concrete approver inherits "
            "this exact behavior. The escalation rule now lives in one place, and one place "
            "only."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "Concrete approvers, then wire the chain",
            "file": "setup.java",
            "lines": ln(
                ("class TeamLead extends Approver { TeamLead(){ super(500); } }", "hi"),
                ("class Manager  extends Approver { Manager(){ super(5_000); } }", "hi"),
                "class Director extends Approver { Director(){ super(50_000); } }",
                "// link them into a chain, low to high:",
                ("lead.next = manager;  manager.next = director;", "hi"),
                "director.next = cfo;   // the order lives here, once"),
            "note": "Each subclass just declares its limit. The chain order is one wiring step."},
         "narration":
            "Step two: the concrete approvers, and wiring them together. [pause] Each subclass "
            "does almost nothing — it just declares its limit. Team lead, five hundred. Manager, "
            "five thousand. Director, fifty thousand. [pause] Then, in one place, you link them "
            "into a chain from low to high. Team lead's next is the manager. The manager's next "
            "is the director. The director's next is the CFO. [pause] That single wiring step is "
            "where the order now lives. Change the escalation order, or the limits, and you "
            "change it here — nowhere else."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Write handle() for one approver",
            "file": "Approver.java",
            "lines": ln(
                "void handle(Expense e) {",
                "  if (e.amount() <= limit) { sign(e); return; }",
                ("  // ▯ otherwise, send it up the chain", "ghost"),
                "}"),
            "prompt": "If this approver can't cover it, what happens — and what if there's no "
                      "one above?",
            "hint": "if (next != null) next.handle(e);  else reject(e);"},
         "narration":
            "Your turn — pause here. [pause] The first half is done: if the expense is within my "
            "limit, I sign it, and we are finished. [pause] Now write the other half. If it is "
            "beyond my limit, the request has to keep moving. [pause] But think carefully about "
            "the edge — what happens if I am the last approver in the chain, the CFO, and even I "
            "have no next? The request cannot just vanish. [pause] Handle both: pass it up if "
            "there is someone above, and do something explicit if there is not."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "The submitter just hands it to the chain",
            "file": "callers.java",
            "lines": ln(
                "// every submitter, now identical:",
                ("chain.handle(expense);   // starts at the team lead", "add"),
                "// travel portal, procurement — same one line",
                ("// they know NOTHING about limits or tiers", "hi")),
            "note": "Submitters hold one reference: the front of the chain. That's all."},
         "narration":
            "Step three, and every submitter collapses. [pause] To approve an expense, you hand "
            "it to the front of the chain — the team lead — and call handle. That is the entire "
            "submission. [pause] The travel portal, procurement, the expense service — all of "
            "them become that same single line. [pause] None of them knows the limits. None of "
            "them knows the tiers, or the order, or that a VP was just added. [pause] They know "
            "one thing: give the request to the chain, and it will find its own approver."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Insert a VP tier: limit $20,000, above Director\"",
            "naiveLabel": "Before", "naiveCost": "Edit every if-else ladder, get boundaries right.",
            "naiveSteps": ["find every ladder, everywhere",
                           "add an else-if in the right spot",
                           "one wrong boundary → misrouted"],
            "patLabel": "Now", "patCost": "One class, spliced into the chain once.",
            "patFile": "setup.java",
            "patLines": ln(
                ("class VP extends Approver { VP(){ super(20_000); } }", "add"),
                ("director.next = vp;   // splice VP in...", "add"),
                ("vp.next = cfo;        // ...between director and CFO", "add"),
                ("// every submitter: unchanged", "add"))},
         "narration":
            "Now the change that used to touch everything. Insert a VP tier — limit twenty "
            "thousand — above the director. [pause] Before, that meant finding every if-else "
            "ladder and inserting a new branch in exactly the right spot, with exactly the right "
            "boundaries, everywhere. [pause] Now? One new class that declares its limit. Then "
            "two lines of wiring to splice it into the chain, between the director and the CFO. "
            "[pause] And every submitter — the portal, procurement, all of them — is completely "
            "unchanged. The policy moved into the chain, so the policy changes only in the "
            "chain."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Chain of Responsibility Pattern",
            "plain": "Give each handler a limit and a link to the next; a request travels the "
                     "chain until a handler takes it.",
            "nodes": [
                {"id": "base", "title": "Approver", "stereo": "abstract",
                 "members": ["# limit", "- next: Approver", "+ handle(req)"],
                 "x": 760, "y": 190, "w": 400, "color": "#A78BFA"},
                {"id": "lead", "title": "TeamLead", "members": ["≤ $500"],
                 "x": 120, "y": 480, "w": 320, "color": "#8B93B0"},
                {"id": "mgr", "title": "Manager", "members": ["≤ $5,000"],
                 "x": 570, "y": 480, "w": 320, "color": "#8B93B0"},
                {"id": "dir", "title": "Director", "members": ["≤ $50,000"],
                 "x": 1020, "y": 480, "w": 320, "color": "#8B93B0"},
                {"id": "cfo", "title": "CFO", "members": ["any amount"],
                 "x": 1470, "y": 480, "w": 320, "color": "#8B93B0"}],
            "edges": [
                {"from": "lead", "to": "base", "kind": "impl"},
                {"from": "mgr", "to": "base", "kind": "impl"},
                {"from": "dir", "to": "base", "kind": "impl"},
                {"from": "cfo", "to": "base", "kind": "impl"},
                {"from": "lead", "to": "mgr", "kind": "assoc"},
                {"from": "mgr", "to": "dir", "kind": "assoc"},
                {"from": "dir", "to": "cfo", "kind": "assoc"}]},
         "narration":
            "This is the Chain of Responsibility. [pause] At the top, the abstract Approver — a "
            "limit, a link to the next, and the handle method that either signs or escalates. "
            "[pause] Below it, the concrete approvers, each declaring only its limit: five "
            "hundred, five thousand, fifty thousand, and the CFO for anything larger. [pause] "
            "Look at the two kinds of arrows. Each approver is an Approver — that is the "
            "inheritance, running up to the top. And each points to the next along the row — "
            "that is the chain itself. [pause] A request enters at the left and travels right, "
            "approver by approver, until one whose limit covers it says yes."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Handler", "your": "abstract Approver (limit + next)"},
                {"role": "ConcreteHandlers", "your": "TeamLead, Manager, Director, CFO"},
                {"role": "The link", "your": "each handler's next Approver"},
                {"role": "Client", "your": "chain.handle(expense) — head only"}],
            "plain": "Each handler decides to handle the request or pass it to its successor; "
                     "the client only knows the head of the chain.",
            "gof": "Avoid coupling the sender of a request to its receiver by giving more than "
                   "one object a chance to handle it. Chain the receivers and pass the request "
                   "along until one handles it."},
         "narration":
            "The names, mapped to your code. [pause] The Handler is the abstract Approver, with "
            "its limit and its next. [pause] The ConcreteHandlers are the individual approvers — "
            "team lead, manager, director, CFO. [pause] The link is simply each handler's "
            "reference to its successor — the thread that makes it a chain. [pause] And the "
            "Client is any submitter, which knows only the head of the chain and calls handle. "
            "[pause] The Gang of Four: avoid coupling the sender of a request to its receiver by "
            "giving more than one object a chance to handle it — chain the receivers, and pass "
            "the request along until one handles it."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "A request can fall off the end",
            "costs": ["No guarantee anyone handles it",
                      "Debugging: which handler took it?",
                      "A long chain adds latency per request"],
            "dont": ["There's exactly one known receiver",
                     "Every request needs every handler",
                     "The order would never change"],
            "signal": "several handlers could process a request, the right one depends on the "
                      "request, and the set or order may change."},
         "narration":
            "Chain of Responsibility has real risks. [pause] The biggest: a request can travel "
            "the entire chain and be handled by no one — if you forget the end case, it silently "
            "falls off. A robust chain must always terminate in a handler that either acts or "
            "explicitly refuses. [pause] It can also be harder to debug — when something is "
            "handled, you may have to trace the chain to see who actually took it. And a very "
            "long chain adds a little latency to every request that walks it. [pause] So skip it "
            "when there is exactly one known receiver — just call it directly — or when every "
            "handler must run on every request, which is a different pattern. [pause] Reach for "
            "it when several handlers could process a request, the right one depends on the "
            "request itself, and the set or the order of handlers is likely to change."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Chain of Responsibility, in one breath",
            "items": [
                "An if-else ladder hard-coded every handler, limit, and order into the sender — "
                "copied everywhere, and fragile.",
                "A request just needs the first handler that can cover it — so give each a limit "
                "and a 'next', and let it walk the line.",
                "Chain of Responsibility: handlers linked in order; each handles or passes on. "
                "New handler, splice it in — senders unchanged."],
            "challenge": "An HTTP server runs each request through auth, then rate-limiting, "
                         "then logging, then the route handler — and you want to reorder or "
                         "insert steps freely.",
            "question": "Does the chain fit? What's the handler, the link, and where can a "
                        "request fall off the end?"},
         "narration":
            "Chain of Responsibility, in one breath. [pause] An if-else ladder hard-coded every "
            "handler, every limit, and their order into the sender — copied everywhere, and "
            "fragile. [pause] But a request just needs the first handler that can cover it — so "
            "give each one a limit and a link to the next, and let the request walk the line "
            "until someone takes it. [pause] Chain of Responsibility: handlers linked in order, "
            "each choosing to handle or pass on. A new handler is spliced in, and the senders "
            "never change. [pause] Here is one to carry out. [pause] An HTTP server runs each "
            "request through authentication, then rate-limiting, then logging, then the route "
            "handler — and you want to reorder or insert those steps freely. [pause] Does the "
            "chain fit? What is the handler, what is the link between them, and where could a "
            "request fall off the end unhandled? [pause] Pause, and sketch it before the next "
            "episode."},
    ],
}


BRIDGE = {
    "id": "dp16-bridge",
    "title": "Bridge",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 16",
            "line1": "Two things vary.", "line2": "Don't multiply them.",
            "sub": "when a class grows along two axes at once, subclassing explodes"},
         "narration":
            "Sometimes a class has to vary in two directions at once. [pause] A notification is "
            "one kind of thing — an alert, a reminder, a daily digest. But it also has to travel "
            "some way — email, SMS, Slack. [pause] Reach for inheritance, and you end up making "
            "one class for every combination: alert-by-email, alert-by-SMS, reminder-by-email, "
            "on and on. Two lists, multiplied. [pause] There is a way to add instead of "
            "multiply. Let's send some notifications."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "Notifications, over any channel",
            "situation": "You have notification types — alert, reminder, digest — and delivery "
                         "channels — email, SMS, Slack. Any type can go over any channel, and "
                         "both lists keep growing.",
            "actors": [
                {"emoji": "🔔", "label": "Types: alert, reminder…"},
                {"emoji": "📡", "label": "Channels: email, SMS…"},
                {"emoji": "✖️", "label": "…every combination"}],
            "ask": "How do you support every type-by-channel pairing without a class for each?"},
         "narration":
            "Here is the system: notifications. [pause] On one side, the kinds of notification — "
            "an urgent alert, a gentle reminder, a daily digest. Each formats its content "
            "differently. [pause] On the other side, the channels they go out over — email, SMS, "
            "Slack. Each sends differently. [pause] Any notification type can go over any "
            "channel. And both lists keep growing — new types, new channels, all the time. "
            "[pause] So how do you support every pairing of type and channel, without writing a "
            "separate class for every single combination?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "A subclass for every combination.",
            "file": "explosion.java",
            "lines": ln(
                ("class AlertEmail    extends Notification { ... }", "hi"),
                ("class AlertSms      extends Notification { ... }", "hi"),
                ("class AlertSlack    extends Notification { ... }", "hi"),
                ("class ReminderEmail extends Notification { ... }", "hi"),
                "class ReminderSms   extends Notification { ... }",
                "// ...digest × 3 more. 3 types × 3 channels = 9."),
            "note": "Each class fuses one type with one channel. 3 × 3 already = nine."},
         "narration":
            "The obvious approach: make a class for each combination. [pause] Alert over email. "
            "Alert over SMS. Alert over Slack. Then reminder over email, reminder over SMS, and "
            "so on. [pause] Three notification types, three channels — and you already have nine "
            "classes. [pause] And notice the waste. The SMS-sending logic is written inside "
            "alert-SMS, and again inside reminder-SMS, and again inside digest-SMS — the same "
            "code, three times. [pause] Each class welds one type to one channel, permanently. "
            "The two things that should be free to vary are fused together."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Add WhatsApp. Oh, and a new 'promo' type.\"",
            "file": "multiply.java",
            "lines": ln(
                ("// add a 4th channel (WhatsApp):", "hi"),
                ("//   AlertWhatsApp, ReminderWhatsApp, DigestWhatsApp", "hi"),
                ("// add a 4th type (Promo):", "hi"),
                ("//   PromoEmail, PromoSms, PromoSlack, PromoWhatsApp", "hi"),
                "// 4 × 4 = 16 classes, and climbing"),
            "smell": "M types × N channels = M×N classes",
            "touched": ["add 1 channel → add M classes",
                        "add 1 type → add N classes",
                        "channel logic duplicated per type",
                        "the class count multiplies, never adds"]},
         "narration":
            "Then both lists grow, and the multiplication bites. [pause] Add one channel — "
            "WhatsApp — and you must add it for every existing type: alert-WhatsApp, "
            "reminder-WhatsApp, digest-WhatsApp. [pause] Add one type — a promo — and you must "
            "add it for every channel. [pause] Three by three was nine; four by four is sixteen; "
            "and it only accelerates. [pause] Every new item on either list multiplies against "
            "the whole other list. The class count does not grow by addition — it grows by "
            "multiplication. That is the explosion."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["A notification has content, and gets sent",
                      "'What it says' is one concern",
                      "'How it's delivered' is a separate concern"],
            "varies": ["The notification type — independently",
                       "The channel — independently"],
            "principle": "Two things vary independently — so split them into two hierarchies and "
                         "let one hold the other."},
         "narration":
            "So what is actually going on? [pause] A notification always has two parts: what it "
            "says, and how it is delivered. [pause] And here is the crucial realization — those "
            "two vary completely independently. A new channel has nothing to do with the "
            "notification types. A new type has nothing to do with the channels. [pause] "
            "Inheritance forced them into one hierarchy, so they multiplied. [pause] The move is "
            "to stop fusing them. Split them into two separate hierarchies — one for the types, "
            "one for the channels — and let a notification hold a channel, rather than inherit "
            "from one. Composition, not combination."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "A remote and a TV", "emoji": "📺",
            "analogy": "Any universal remote drives any TV through the same interface — nobody "
                       "builds a 'Sony-remote-for-one-Samsung-TV'.",
            "map": [
                {"from": "The remote (what you want)", "to": "the abstraction (Notification)"},
                {"from": "The TV (how it happens)", "to": "the implementor (the channel)"},
                {"from": "The standard signal", "to": "the send() interface"},
                {"from": "Pair any remote with any TV", "to": "compose any type with any channel"}],
            "breaks": "a remote is physically separate; here you still write both sides — the "
                      "win is only that they no longer multiply."},
         "narration":
            "Think of a remote control and a television. [pause] A universal remote can operate "
            "any TV. Nobody manufactures a special Sony remote that only works with one Samsung "
            "model. [pause] The remote is what you want done — raise the volume. The TV is how "
            "it actually happens. Between them sits a standard signal, an agreed interface. "
            "Because of that interface, any remote pairs with any TV. [pause] The remote is the "
            "abstraction — the notification. The TV is the implementor — the channel. The "
            "standard signal is the send interface. And pairing any remote with any TV is "
            "composing any type with any channel. [pause] Where it strains: a remote and a TV "
            "are physically separate objects. Here you still write both sides in code — the win "
            "is only that they stop multiplying against each other."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "The implementor side: how to send",
            "file": "MessageSender.java",
            "lines": ln(
                ("interface MessageSender {        // the 'how'", "add"),
                ("  void send(String text);", "add"),
                ("}", "add"),
                "class EmailSender implements MessageSender { ... }",
                "class SmsSender   implements MessageSender { ... }",
                "class SlackSender implements MessageSender { ... }"),
            "note": "One clean hierarchy for the CHANNELS — three classes, not nine."},
         "narration":
            "The refactor, step one. [pause] Pull the how — the delivery — into its own "
            "hierarchy. [pause] A MessageSender interface with a single method: send some text. "
            "[pause] Then one concrete sender per channel — email, SMS, Slack. Three classes, "
            "and each holds its channel's sending logic exactly once. [pause] No notification "
            "types in sight here. This side knows only how to put text on a wire. That SMS logic "
            "that used to be copied three times? It now lives in one SmsSender, and nowhere "
            "else."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "The abstraction holds a sender — the bridge",
            "file": "Notification.java",
            "lines": ln(
                ("abstract class Notification {       // the 'what'", "hi"),
                ("  protected final MessageSender sender;   // ← the bridge", "hi"),
                ("  Notification(MessageSender s) { this.sender = s; }", "hi"),
                "  abstract void notify(User u);",
                "}",
                "class Alert extends Notification { /* formats urgently */ }"),
            "note": "Notification HAS-A sender. That reference is the bridge between the sides."},
         "narration":
            "Step two: the what — the notification hierarchy — and the bridge that joins the two "
            "sides. [pause] The abstract Notification holds a reference to a MessageSender. That "
            "one field is the bridge. [pause] A notification no longer is a channel; it has a "
            "channel, handed in when it is built. [pause] Then the refined types — Alert, "
            "Reminder, Digest — extend Notification. Each knows only how to format its own "
            "content. When it needs to actually send, it delegates to the sender it holds. "
            "[pause] Two small hierarchies, joined by a single reference. That reference is the "
            "entire pattern."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Write Alert.notify()",
            "file": "Alert.java",
            "lines": ln(
                "class Alert extends Notification {",
                "  void notify(User u) {",
                '    String text = "🚨 ALERT: " + details;   // format',
                ("    // ▯ now actually send it — over which channel?", "ghost"),
                "  }",
                "}"),
            "prompt": "Alert formats its text. How does it send — without knowing if it's email "
                      "or SMS?",
            "hint": "sender.send(text);  // whichever channel was injected"},
         "narration":
            "Your turn — pause here. [pause] The Alert has formatted its message — the urgent "
            "text is ready. [pause] Now it has to send. But here is the point of the whole "
            "pattern: Alert must not know or care whether it is going out by email, SMS, or "
            "Slack. [pause] It holds a MessageSender. Use it. [pause] Write the one line that "
            "sends the text — and notice that the same line works for every channel, because "
            "Alert only ever talks to the interface."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "Compose any pairing at runtime",
            "file": "app.java",
            "lines": ln(
                ("Notification n = new Alert(new SmsSender());   // alert × SMS", "add"),
                "n.notify(user);",
                "// mix and match freely, at runtime:",
                ("new Digest(new EmailSender());   // digest × email", "add"),
                ("new Reminder(new SlackSender()); // reminder × Slack", "add")),
            "note": "Pick a type, pick a channel, snap them together. No fused subclass."},
         "narration":
            "Step three, and the payoff appears. [pause] To send an alert over SMS, you build an "
            "Alert, and hand it an SmsSender. To send a digest over email, an EmailSender. A "
            "reminder over Slack, a SlackSender. [pause] You are not choosing from nine fused "
            "classes anymore. You are picking one type, picking one channel, and snapping them "
            "together — at runtime, however you like. [pause] Any of the three types, with any "
            "of the three channels, from just three plus three classes. The combinations are "
            "composed, not coded."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Add a WhatsApp channel\"",
            "naiveLabel": "Fused", "naiveCost": "One new class per notification type.",
            "naiveSteps": ["AlertWhatsApp, ReminderWhatsApp…", "one per existing type, forever",
                           "re-implement WhatsApp each time"],
            "patLabel": "Bridged", "patCost": "One class. It pairs with every type.",
            "patFile": "WhatsAppSender.java",
            "patLines": ln(
                ("class WhatsAppSender implements MessageSender {", "add"),
                ("  public void send(String text) { /* WhatsApp API */ }", "add"),
                ("}", "add"),
                ("// works with Alert, Reminder, Digest — instantly", "add"))},
         "narration":
            "Now the change that used to multiply. Add a WhatsApp channel. [pause] In the fused "
            "design, that meant a new class for every existing type — alert-WhatsApp, "
            "reminder-WhatsApp, digest-WhatsApp — each re-implementing the WhatsApp call. "
            "[pause] With the bridge? One class. A single WhatsAppSender that implements the "
            "send interface. [pause] And the instant it exists, it pairs with every notification "
            "type there is — alert, reminder, digest — and every type you add later. One new "
            "class on one side now serves the entire other side. Addition, not multiplication."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Bridge Pattern",
            "plain": "Split a class that varies two ways into two hierarchies — an abstraction "
                     "and an implementor — and let one hold a reference to the other.",
            "nodes": [
                {"id": "abs", "title": "Notification", "stereo": "abstraction",
                 "members": ["# sender: MessageSender", "+ notify()"],
                 "x": 160, "y": 210, "w": 400, "color": "#A78BFA"},
                {"id": "alert", "title": "Alert", "members": ["formats urgently"],
                 "x": 60, "y": 470, "w": 300, "color": "#8B93B0"},
                {"id": "rem", "title": "Reminder", "members": ["formats gently"],
                 "x": 400, "y": 470, "w": 300, "color": "#8B93B0"},
                {"id": "impl", "title": "MessageSender", "stereo": "implementor",
                 "members": ["+ send(text)"], "x": 1360, "y": 210, "w": 400, "color": "#22D3EE"},
                {"id": "email", "title": "EmailSender", "members": ["send → email"],
                 "x": 1260, "y": 470, "w": 300, "color": "#8B93B0"},
                {"id": "sms", "title": "SmsSender", "members": ["send → SMS"],
                 "x": 1600, "y": 470, "w": 300, "color": "#8B93B0"}],
            "edges": [
                {"from": "alert", "to": "abs", "kind": "impl"},
                {"from": "rem", "to": "abs", "kind": "impl"},
                {"from": "email", "to": "impl", "kind": "impl"},
                {"from": "sms", "to": "impl", "kind": "impl"},
                {"from": "abs", "to": "impl", "kind": "has"}]},
         "narration":
            "This is the Bridge pattern. [pause] Two separate hierarchies. [pause] On the left, "
            "the abstraction — Notification — with its refined types, Alert and Reminder, "
            "beneath it. This side is the what. [pause] On the right, the implementor — "
            "MessageSender — with its concrete channels, email and SMS, beneath it. This side is "
            "the how. [pause] And the single arrow across the middle, from Notification to "
            "MessageSender — that is the bridge. A notification holds a sender. [pause] Because "
            "the two hierarchies are joined by that one reference instead of by inheritance, "
            "they grow by addition. Add on the left, or add on the right — the other side never "
            "multiplies."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Abstraction", "your": "abstract Notification (holds a sender)"},
                {"role": "RefinedAbstraction", "your": "Alert, Reminder, Digest"},
                {"role": "Implementor", "your": "interface MessageSender"},
                {"role": "ConcreteImplementor", "your": "EmailSender, SmsSender, SlackSender"}],
            "plain": "The abstraction delegates the real work to an implementor it holds; both "
                     "sides subclass freely and independently.",
            "gof": "Decouple an abstraction from its implementation so that the two can vary "
                   "independently."},
         "narration":
            "The names, mapped to your code. [pause] The Abstraction is the Notification class, "
            "which holds a sender. [pause] The RefinedAbstractions are the concrete types — "
            "alert, reminder, digest. [pause] The Implementor is the MessageSender interface. "
            "[pause] And the ConcreteImplementors are the individual channels — email, SMS, "
            "Slack. [pause] The abstraction delegates the real sending to the implementor it "
            "holds, and each side can be subclassed freely, without touching the other. [pause] "
            "The Gang of Four, and it is worth memorizing: decouple an abstraction from its "
            "implementation, so that the two can vary independently. That last word — "
            "independently — is the whole pattern."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "Only worth it when BOTH vary",
            "costs": ["Two hierarchies plus a bridge — more upfront",
                      "More indirection to follow when reading",
                      "Over-engineered if only one side changes"],
            "dont": ["Only one dimension actually varies",
                     "There'll only ever be a few combinations",
                     "The implementation will never change"],
            "signal": "a class is subclassed along two independent dimensions, and you can feel "
                      "the M×N explosion coming."},
         "narration":
            "Bridge earns its keep in exactly one situation, and it is important to be honest "
            "about it. [pause] You are setting up two hierarchies and a reference between them — "
            "that is real upfront structure, and more indirection for the next reader to follow. "
            "[pause] If only one dimension ever varies, this is over-engineering; a simple "
            "hierarchy is clearer. If there will only ever be a couple of combinations, just "
            "write them. [pause] So skip it when only one side changes, or when the "
            "implementation is fixed forever. [pause] Reach for it the moment you notice a class "
            "being subclassed along two independent axes at once — when you can feel the M-by-N "
            "explosion coming. Bridge turns that multiplication back into addition."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Bridge, in one breath",
            "items": [
                "Subclassing along two axes — type and channel — multiplied into M×N fused "
                "classes, with logic duplicated across them.",
                "The two axes vary independently — so split them into two hierarchies and let "
                "the abstraction HOLD an implementor.",
                "Bridge: compose a type with a channel at runtime; add to either side and the "
                "other never multiplies. M+N, not M×N."],
            "challenge": "You have shapes — circle, square — that must draw on multiple backends "
                         "— SVG, Canvas, PDF. Both lists will keep growing.",
            "question": "Does Bridge fit? Which is the abstraction, which is the implementor, "
                        "and where's the bridge?"},
         "narration":
            "Bridge, in one breath. [pause] Subclassing along two axes at once — notification "
            "type and delivery channel — multiplied into M-by-N fused classes, with the same "
            "channel logic duplicated across all of them. [pause] But the two axes vary "
            "independently, so you split them into two hierarchies, and let the abstraction hold "
            "an implementor rather than inherit from one. [pause] Bridge: compose a type with a "
            "channel at runtime, and adding to either side leaves the other untouched. M plus N, "
            "not M times N. [pause] Here is one to carry out. [pause] You have shapes — a "
            "circle, a square — that must draw themselves on several backends — SVG, Canvas, PDF "
            "— and both of those lists will keep growing. [pause] Does Bridge fit? Which "
            "hierarchy is the abstraction, which is the implementor, and where exactly is the "
            "bridge between them? [pause] Pause, and sketch it before the next episode."},
    ],
}


MEDIATOR = {
    "id": "dp17-mediator",
    "title": "Mediator",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 17",
            "line1": "Everyone talking", "line2": "to everyone",
            "sub": "when every object references every other, the wiring becomes a mesh"},
         "narration":
            "When a group of objects all need to talk to each other, the obvious thing is to let "
            "them — directly. [pause] Each one holds a reference to the others, and calls them "
            "when it needs to. [pause] But with five objects, that is twenty connections. With "
            "ten, ninety. Every new object has to be introduced to all the others, and every "
            "rule about who talks to whom is smeared across all of them. [pause] There is a way "
            "to turn that mesh into a star. Let's build a chat room."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "A chat room of users",
            "situation": "Users in a chat room send messages to each other. New users join and "
                         "leave. And rules appear: mute someone, filter profanity, log every "
                         "message.",
            "actors": [
                {"emoji": "💬", "label": "Users who chat"},
                {"emoji": "🕸️", "label": "…all talking directly"},
                {"emoji": "📋", "label": "…and evolving rules"}],
            "ask": "How do users communicate without each one wiring itself to every other?"},
         "narration":
            "Here is the system: a chat room. [pause] Users send messages, and every message "
            "needs to reach the other users in the room. [pause] People join and leave "
            "constantly, so the set of participants is always shifting. [pause] And rules keep "
            "arriving — mute this user, filter out profanity, log every message for compliance. "
            "[pause] So how do the users communicate with each other, without every single user "
            "having to hold a wire to every other user in the room?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "Everyone holds everyone.",
            "file": "User.java",
            "lines": ln(
                "class User {",
                ("  List<User> others;          // every other user!", "hi"),
                "  void send(String msg) {",
                ("    for (User u : others)", "hi"),
                ("      u.receive(msg, this);   // call each directly", "hi"),
                "  }",
                "}"),
            "note": "Each user references every other. N users → N×N wiring."},
         "narration":
            "The direct approach: each user holds a list of all the other users. [pause] To send "
            "a message, a user loops over that list and calls receive on each one, directly. "
            "[pause] It works for three or four people. [pause] But look at the wiring. Every "
            "user must hold a reference to every other user. Five users is twenty references to "
            "keep in sync; ten users is ninety. [pause] And every time someone joins, every "
            "existing user's list has to be updated to include them. The room is a tangled mesh, "
            "and it grows by the square."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Mute a user. Filter profanity. Log everything.\"",
            "file": "smeared.java",
            "lines": ln(
                "void send(String msg) {",
                "  for (User u : others) {",
                ("    if (mutedBy(u)) continue;      // mute logic...", "hi"),
                ("    if (hasProfanity(msg)) ...     // ...in EVERY user", "hi"),
                ("    log(msg); u.receive(msg, this);", "hi"),
                "  }",
                "}"),
            "smell": "Routing + rules duplicated inside every colleague",
            "touched": ["every User re-implements the rules",
                        "new rule → edit every User",
                        "a joiner must be added everywhere",
                        "N×N references to keep in sync"]},
         "narration":
            "Then the rules arrive, and they land in the worst possible place. [pause] Mute "
            "logic — skip users who muted the sender — now lives inside every user's send "
            "method. Profanity filtering, the same. Logging, the same. [pause] Each rule is "
            "copied into every colleague, because every colleague does its own routing. [pause] "
            "Change how muting works, and you edit every user class. Add a rule, and you edit "
            "every user class. [pause] The objects are drowning in each other's business — the "
            "communication logic has no home of its own, so it lives everywhere at once."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["Users send and receive messages",
                      "Messages must be routed to recipients",
                      "Rules apply to that routing"],
            "varies": ["Who is in the room right now",
                       "The routing rules — mute, filter, log"],
            "principle": "Route every message through ONE mediator; each user knows only the "
                         "mediator, never the others."},
         "narration":
            "What is fixed, and what varies? [pause] Fixed: users send messages and receive "
            "them. Messages have to be routed to the right recipients. And rules — muting, "
            "filtering, logging — apply to that routing. [pause] What varies is who happens to "
            "be in the room, and what the routing rules are. [pause] Here is the move. [pause] "
            "Stop letting the users talk to each other directly. Put one object in the middle — "
            "a mediator — and route every message through it. Each user knows only the mediator. "
            "The mediator knows the users, and owns all the routing and the rules. The mesh "
            "collapses into a star."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "Air-traffic control", "emoji": "🛫",
            "analogy": "Pilots don't negotiate plane-to-plane; they all talk to the tower, and "
                       "the tower coordinates.",
            "map": [
                {"from": "The pilots", "to": "the colleagues (users)"},
                {"from": "The control tower", "to": "the mediator (chat room)"},
                {"from": "Radioing the tower", "to": "user.send() → room"},
                {"from": "The tower's rules", "to": "routing, muting, logging"}],
            "breaks": "a tower issues commands back; a mediator can be lighter — sometimes it "
                      "only relays."},
         "narration":
            "Think about air-traffic control. [pause] Dozens of planes share the sky around an "
            "airport. [pause] They do not negotiate with each other, plane to plane — that would "
            "be chaos, and it would grow impossibly as more planes arrive. Instead, every pilot "
            "talks only to the control tower. The tower has the full picture, and it coordinates "
            "everyone. [pause] The pilots are the colleagues — our users. The tower is the "
            "mediator — the chat room. Radioing the tower is a user sending to the room. And the "
            "tower's rules are the routing, the muting, the logging. [pause] Where it strains: a "
            "control tower actively issues commands back. A mediator can be lighter — sometimes "
            "it just relays messages between colleagues that would otherwise have to know each "
            "other."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "One mediator; users point only to it",
            "file": "ChatRoom.java",
            "lines": ln(
                ("interface ChatRoom {                 // the mediator", "add"),
                ("  void send(String msg, User from);", "add"),
                ("}", "add"),
                "class User {",
                ("  private final ChatRoom room;       // NOT other users", "hi"),
                ("  void send(String msg) { room.send(msg, this); }", "hi"),
                "}"),
            "note": "A user holds ONE reference — the room. It no longer knows any peer."},
         "narration":
            "The refactor, step one. [pause] Define the mediator — a ChatRoom, with a single "
            "send method that takes a message and who it came from. [pause] Now change the user. "
            "Instead of a list of every other user, a user holds exactly one reference: the "
            "room. [pause] And its send method shrinks to a single line — hand the message to "
            "the room, and say it came from me. [pause] That is the pivotal change. A user no "
            "longer knows a single one of its peers. It knows only the mediator in the middle."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "The mediator owns routing and rules",
            "file": "GroupChat.java",
            "lines": ln(
                ("class GroupChat implements ChatRoom {", "hi"),
                "  private final List<User> users = ...;",
                ("  public void send(String msg, User from) {", "hi"),
                ("    log(msg);                         // rules, ONCE", "hi"),
                "    for (User u : users)",
                ("      if (u != from && !muted(u, from))", "hi"),
                "        u.receive(msg);               // route it",
                "  }",
                "}"),
            "note": "Every rule — log, mute, route — lives here, in the one mediator."},
         "narration":
            "Step two: the mediator does the real work. [pause] GroupChat holds the list of "
            "users — it is the one object that knows who is in the room. [pause] And its send "
            "method is where everything now lives. Log the message, once. Then route it to every "
            "user except the sender, skipping anyone who has muted them. [pause] Muting, "
            "logging, filtering — all of it, in this one place. [pause] The users got simpler "
            "because the mediator absorbed their shared complexity. The routing logic finally "
            "has a home."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Write GroupChat.send()",
            "file": "GroupChat.java",
            "lines": ln(
                "public void send(String msg, User from) {",
                "  for (User u : users) {",
                ("    // ▯ deliver to everyone EXCEPT the sender", "ghost"),
                "  }",
                "}"),
            "prompt": "Broadcast the message to all users in the room — but not back to the one "
                      "who sent it.",
            "hint": "if (u != from) u.receive(msg);"},
         "narration":
            "Your turn — pause here. [pause] The mediator holds every user in the room. A "
            "message has come in, along with the user it came from. [pause] Write the routing. "
            "Deliver the message to everyone in the room — except the sender, who obviously "
            "should not receive their own message back. [pause] It is just a loop with one "
            "guard. But notice where you are writing it: once, in the mediator — not smeared "
            "across every user."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "Add a user — nobody else changes",
            "file": "app.java",
            "lines": ln(
                ("GroupChat room = new GroupChat();", "add"),
                ("User alice = new User(room);   // knows only the room", "add"),
                ("User bob   = new User(room);", "add"),
                ("room.join(alice); room.join(bob);   // room tracks them", "add"),
                ('alice.send("hi");   // → room → everyone but alice', "hi")),
            "note": "A new user tells the room it exists. No other user is touched."},
         "narration":
            "Step three, and adding people becomes trivial. [pause] You create the room, then "
            "create users — each one handed only the room. They know nothing about each other. "
            "[pause] Each user joins by telling the room it exists, and the room adds it to its "
            "list. [pause] When Alice sends hi, it goes to the room, and the room fans it out to "
            "everyone but Alice. [pause] Add a tenth user, a hundredth user — and not one "
            "existing user class changes. The only thing that learns about a new participant is "
            "the mediator. The square-law mesh is gone."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Add a profanity filter and an audit log\"",
            "naiveLabel": "Mesh", "naiveCost": "Edit every User's send loop.",
            "naiveSteps": ["the filter goes in every User", "so does the audit log",
                           "miss one → an unfiltered leak"],
            "patLabel": "Mediated", "patCost": "One method in the mediator. Done.",
            "patFile": "GroupChat.java",
            "patLines": ln(
                ("public void send(String msg, User from) {", "add"),
                ("  if (hasProfanity(msg)) msg = clean(msg);   // once", "add"),
                ("  audit.record(from, msg);                    // once", "add"),
                ("  route(msg, from);   // users unchanged", "add"),
                ("}", "add"))},
         "narration":
            "Now the change that used to touch everyone. Add a profanity filter, and an audit "
            "log for compliance. [pause] In the mesh design, both would go inside every user's "
            "send loop — and if you missed even one user, an unfiltered message would slip "
            "through. [pause] With a mediator, you add both to one method, in one class. [pause] "
            "Clean the message once, record it once, then route it. [pause] Every user in the "
            "room is now filtered and audited — and not a single user class changed. The rules "
            "live where the routing lives: in the middle."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Mediator Pattern",
            "plain": "Route all communication through one mediator, so a mesh of objects that "
                     "each knew each other becomes a star that knows only the hub.",
            "nodes": [
                {"id": "room", "title": "ChatRoom", "stereo": "mediator",
                 "members": ["- users: List<User>", "+ send(msg, from)"],
                 "x": 760, "y": 190, "w": 400, "color": "#A78BFA"},
                {"id": "u1", "title": "Alice", "members": ["send / receive"],
                 "x": 80, "y": 480, "w": 320, "color": "#8B93B0"},
                {"id": "u2", "title": "Bob", "members": ["send / receive"],
                 "x": 540, "y": 480, "w": 320, "color": "#8B93B0"},
                {"id": "u3", "title": "Carol", "members": ["send / receive"],
                 "x": 1000, "y": 480, "w": 320, "color": "#8B93B0"},
                {"id": "u4", "title": "Dave", "members": ["send / receive"],
                 "x": 1460, "y": 480, "w": 320, "color": "#8B93B0"}],
            "edges": [
                {"from": "u1", "to": "room", "kind": "assoc"},
                {"from": "u2", "to": "room", "kind": "assoc"},
                {"from": "u3", "to": "room", "kind": "assoc"},
                {"from": "u4", "to": "room", "kind": "assoc"}]},
         "narration":
            "This is the Mediator pattern. [pause] In the center, the mediator — the ChatRoom — "
            "holding the list of users and the one send method that routes everything. [pause] "
            "Around it, the colleagues: Alice, Bob, Carol, Dave. [pause] Look at the arrows. "
            "Every user points only to the room in the middle. Not one of them points to another "
            "user. [pause] That is the whole idea. The mesh, where everyone connected to "
            "everyone, has become a star, where everyone connects only to the hub. [pause] "
            "Communication still happens between the users — but it always travels through the "
            "one object that owns the rules."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Mediator", "your": "interface ChatRoom"},
                {"role": "ConcreteMediator", "your": "GroupChat (holds users + rules)"},
                {"role": "Colleagues", "your": "User (each knows only the room)"},
                {"role": "Communication", "your": "room.send() → routes to users"}],
            "plain": "Colleagues send to the mediator; the mediator holds them and coordinates "
                     "who receives what.",
            "gof": "Define an object that encapsulates how a set of objects interact. Mediator "
                   "promotes loose coupling by keeping objects from referring to each other "
                   "explicitly."},
         "narration":
            "The names, mapped to your code. [pause] The Mediator is the ChatRoom interface. "
            "[pause] The ConcreteMediator is GroupChat — it holds the users and owns the rules. "
            "[pause] The Colleagues are the users, each of which knows only the room. [pause] "
            "And the communication flows through the mediator's send method, which routes "
            "messages to the right recipients. [pause] The Gang of Four: define an object that "
            "encapsulates how a set of objects interact — Mediator promotes loose coupling by "
            "keeping objects from referring to each other explicitly. That phrase — keeping them "
            "from referring to each other — is the entire point."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "The hub can become a monster",
            "costs": ["The mediator can grow into a god object",
                      "Complexity moves — it doesn't vanish",
                      "One central point everything depends on"],
            "dont": ["The objects barely interact anyway",
                     "There are only two of them",
                     "Direct calls are clear and stable"],
            "signal": "a set of objects all reference each other, and the interaction rules keep "
                      "changing and spreading."},
         "narration":
            "Mediator has a real danger, and it is the mirror of Facade's. [pause] All the "
            "interaction logic you pulled out of the colleagues has to go somewhere — and it all "
            "goes into the mediator. Left unchecked, that hub swells into a god object that "
            "knows and does everything. [pause] The complexity did not vanish; it moved to the "
            "center. You have traded a tangled mesh for a single, powerful, and now critical hub "
            "that everything depends on. [pause] So skip it when the objects barely interact, "
            "when there are only two of them, or when direct calls are perfectly clear and "
            "stable. [pause] Reach for it when a set of objects all reference each other, and "
            "the rules about how they interact keep changing and spreading across all of them. "
            "Give those rules one home."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Mediator, in one breath",
            "items": [
                "Every object referencing every other made an N×N mesh, with routing and rules "
                "duplicated across all of them.",
                "Communication and its rules are one concern — so route everything through one "
                "mediator each object knows.",
                "Mediator: colleagues talk to the hub, never each other; the mesh becomes a "
                "star. New colleague or rule — one place changes."],
            "challenge": "A complex form: toggling a checkbox enables a field, a dropdown "
                         "updates a button, a date bounds another date — controls reacting to "
                         "each other.",
            "question": "Does Mediator fit? What's the mediator, who are the colleagues, and "
                        "what moves into the hub?"},
         "narration":
            "Mediator, in one breath. [pause] Every object referencing every other made an "
            "N-by-N mesh, with routing and rules duplicated across all of them. [pause] But "
            "communication, and the rules around it, are really one concern — so you route "
            "everything through a single mediator that each object knows. [pause] Mediator: the "
            "colleagues talk to the hub, never to each other, and the mesh becomes a star. A new "
            "colleague, or a new rule, changes just one place. [pause] Here is one to carry out. "
            "[pause] A complex form — toggling a checkbox enables a field, a dropdown updates a "
            "button, one date bounds another — controls all reacting to each other. [pause] Does "
            "Mediator fit? What is the mediator, who are the colleagues, and what logic moves "
            "into the hub? [pause] Pause, and sketch it before the next episode."},
    ],
}


ABSTRACT_FACTORY = {
    "id": "dp18-abstract-factory",
    "title": "Abstract Factory",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 18",
            "line1": "A family", "line2": "that must match",
            "sub": "creating related objects that have to belong to the same set — never mixed"},
         "narration":
            "Some objects only make sense together. [pause] A macOS button, a macOS checkbox, a "
            "macOS menu — they share a look, and they belong as a set. Put a macOS button next "
            "to a Windows checkbox, and the interface looks broken. [pause] So when your code "
            "creates one of them, it quietly commits to a whole family — and it is dangerously "
            "easy to reach into the wrong one. [pause] There is a way to create an entire "
            "matching family through one door. Let's build a cross-platform UI."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "One UI, two platforms",
            "situation": "Your app runs on macOS and Windows. It builds buttons, checkboxes, and "
                         "menus — and every widget on screen must match the platform. A mixed "
                         "set looks broken.",
            "actors": [
                {"emoji": "🍎", "label": "macOS widgets"},
                {"emoji": "🪟", "label": "Windows widgets"},
                {"emoji": "🧩", "label": "…must never mix"}],
            "ask": "How do you create a whole matching family of widgets without hard-coding the "
                   "platform everywhere?"},
         "narration":
            "Here is the system: one application, running on two platforms — macOS and Windows. "
            "[pause] It builds the usual widgets — buttons, checkboxes, menus. [pause] But every "
            "widget on the screen has to match the platform it runs on. All macOS, or all "
            "Windows — never a mix. A single Windows-style checkbox in an otherwise macOS window "
            "looks instantly wrong. [pause] So how does the app create a whole matching family "
            "of widgets, without hard-coding which platform at every single place it makes one?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "Check the platform, everywhere.",
            "file": "Dialog.java",
            "lines": ln(
                ("Button b = (os == MAC)", "hi"),
                ("  ? new MacButton() : new WinButton();", "hi"),
                ("Checkbox c = (os == MAC)", "hi"),
                ("  ? new MacCheckbox() : new WinCheckbox();", "hi"),
                "// ...the same os check at every widget you build",
                "// forget one → a Mac button in a Windows window"),
            "note": "The platform check is copied to every creation site. One slip = a mixed UI."},
         "narration":
            "The direct approach: check the platform wherever you build a widget. [pause] Making "
            "a button? If we are on macOS, new a Mac button, otherwise a Windows one. Making a "
            "checkbox? The same check again. A menu? Again. [pause] It works. [pause] But that "
            "platform check is now copied to every place that creates any widget — dozens of "
            "sites across the app. [pause] Add a screen, and you write the check again. And the "
            "day someone forgets it, or gets the ternary backwards, you get a Mac button sitting "
            "in a Windows window. The families leak into each other."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Now add a Linux theme. And a high-contrast one.\"",
            "file": "everywhere.java",
            "lines": ln(
                ("if (os == MAC) ...      // in Dialog", "hi"),
                ("if (os == MAC) ...      // in Toolbar", "hi"),
                ("if (os == MAC) ...      // in Settings, Wizard, ...", "hi"),
                ("// add LINUX: touch EVERY one of these checks", "hi"),
                "// each check must list every widget's variant"),
            "smell": "Platform branching scattered across every creation site",
            "touched": ["os check at every widget site",
                        "add a platform → edit them all",
                        "add a widget → add it to each check",
                        "one missed branch → a mixed UI"]},
         "narration":
            "Then the platforms multiply. Add Linux. Add a high-contrast accessibility theme. "
            "[pause] Every one of those scattered platform checks now needs a new branch — in "
            "the dialog, in the toolbar, in settings, in the wizard, everywhere. [pause] And "
            "each check has to know how to build every kind of widget for the new platform. "
            "[pause] Miss one branch in one place, and that screen silently falls back to the "
            "wrong family. [pause] The knowledge of which widgets go together — which should "
            "live in exactly one place — is instead smeared across every corner of the app that "
            "builds a UI."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["The app builds buttons, checkboxes, menus",
                      "Every widget must match its family",
                      "The client shouldn't name concrete classes"],
            "varies": ["Which family — macOS, Windows, Linux",
                       "And it must be chosen consistently"],
            "principle": "Bundle the creation of a whole family behind one factory object; pick "
                         "the factory once."},
         "narration":
            "What is fixed, and what varies? [pause] Fixed: the app always builds the same kinds "
            "of widget — a button, a checkbox, a menu. Every widget it builds has to belong to "
            "one consistent family. And the app itself should never have to name a concrete "
            "class like Mac-button. [pause] What varies is only which family — macOS, Windows, "
            "Linux — and that choice has to be made consistently, everywhere at once. [pause] "
            "Here is the move. [pause] Bundle the creation of the entire family behind a single "
            "object — a factory. One factory makes all the macOS widgets; another makes all the "
            "Windows ones. The app picks a factory once, then asks it for widgets — never "
            "choosing a concrete class again."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "An interior designer", "emoji": "🛋️",
            "analogy": "You pick one designer; everything they bring — sofa, chair, lamp — "
                       "matches, because it all comes from the same hand.",
            "map": [
                {"from": "The designer you hire", "to": "the concrete factory"},
                {"from": "The matching furniture set", "to": "a family of products"},
                {"from": "\"Bring me a chair\"", "to": "createButton() / createCheckbox()"},
                {"from": "Choosing the designer once", "to": "picking the factory at startup"}],
            "breaks": "a designer improvises; a factory only makes the exact product types its "
                      "interface declares."},
         "narration":
            "Think of hiring an interior designer. [pause] You do not buy a sofa from one place, "
            "a chair from another, a lamp from a third, and pray they match. [pause] You pick "
            "one designer, and everything they bring you — the sofa, the chair, the lamp — "
            "belongs together, because it all comes from the same taste, the same hand. [pause] "
            "The designer you hire is the concrete factory. The matching furniture is a family "
            "of products. Asking for a chair is calling create-button, or create-checkbox. And "
            "choosing the designer, once, is picking your factory at startup. [pause] Where it "
            "strains: a real designer can improvise anything. A factory only makes the exact "
            "product types its interface declares — button, checkbox, menu, and no more."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "One factory interface for the whole family",
            "file": "GUIFactory.java",
            "lines": ln(
                ("interface GUIFactory {           // makes a family", "add"),
                ("  Button   createButton();", "add"),
                ("  Checkbox createCheckbox();", "add"),
                ("}", "add"),
                "interface Button   { void render(); }",
                "interface Checkbox { void toggle(); }"),
            "note": "The factory declares a whole family; the products are interfaces too."},
         "narration":
            "The refactor, step one. [pause] Define one factory interface — GUIFactory — that "
            "declares how to make the whole family. Create a button. Create a checkbox. One "
            "method per product in the family. [pause] And the products themselves are "
            "interfaces too — a Button you can render, a Checkbox you can toggle — with no "
            "mention of any platform. [pause] Notice what this interface promises: not a single "
            "widget, but a coordinated set. Whoever implements it commits to producing a button "
            "and a checkbox that belong together."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "One concrete factory per family",
            "file": "MacFactory.java",
            "lines": ln(
                ("class MacFactory implements GUIFactory {", "hi"),
                ("  public Button   createButton()   { return new MacButton(); }", "hi"),
                ("  public Checkbox createCheckbox() { return new MacCheckbox(); }", "hi"),
                "}",
                "class WinFactory implements GUIFactory {",
                "  public Button createButton() { return new WinButton(); } ...",
                "}"),
            "note": "Each factory returns ONLY its own family — matching by construction."},
         "narration":
            "Step two: one concrete factory per family. [pause] The Mac factory implements the "
            "interface by returning Mac widgets — a Mac button, a Mac checkbox. [pause] The "
            "Windows factory returns Windows widgets. [pause] And here is the guarantee that the "
            "scattered if-checks could never give you: because a single factory builds the whole "
            "family, everything it produces automatically matches. It is structurally impossible "
            "for the Mac factory to hand you a Windows checkbox. Consistency is no longer "
            "something you must remember — it is built into which object you asked."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Build a dialog from a factory",
            "file": "Dialog.java",
            "lines": ln(
                "class Dialog {",
                "  Dialog(GUIFactory f) {         // any family",
                ("    // ▯ build a button and a checkbox — no 'new Mac...'", "ghost"),
                "  }",
                "}"),
            "prompt": "Create a button and a checkbox using only the factory. Which platform is "
                      "this code tied to?",
            "hint": "Button b = f.createButton();  Checkbox c = f.createCheckbox();"},
         "narration":
            "Your turn — pause here. [pause] Here is a dialog. It is handed a GUIFactory — but "
            "it is not told, and does not know, which one. [pause] Build a button and a checkbox "
            "for the dialog, using only that factory. [pause] And as you write it, ask yourself "
            "the key question: which platform is this dialog code tied to? [pause] The answer "
            "should be none. If you never write new-Mac-anything, this exact code renders "
            "correctly on every platform you will ever add."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "Choose the family once, at the top",
            "file": "App.java",
            "lines": ln(
                ("GUIFactory factory = switch (currentOS()) {", "add"),
                ("  case MAC -> new MacFactory();", "add"),
                ("  case WIN -> new WinFactory();", "add"),
                ("};   // the ONLY platform check in the app", "hi"),
                ("new Dialog(factory);   // everything below just matches", "add")),
            "note": "One decision, at startup. Everything downstream is platform-blind."},
         "narration":
            "Step three, and the scattered checks collapse into one. [pause] At startup — and "
            "only here — the app looks at the current platform and picks the matching factory. "
            "Mac, Windows, whatever it is. [pause] That is now the single platform check in the "
            "entire application. [pause] It hands that one factory down to the dialog, the "
            "toolbar, every screen. [pause] And all of that code below is completely "
            "platform-blind. It just asks its factory for widgets, and gets a perfectly matched "
            "family, every time. The one decision was made once, at the top."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Add a Linux theme\"",
            "naiveLabel": "Scattered", "naiveCost": "A new branch in every platform check.",
            "naiveSteps": ["find every os check", "add a Linux branch to each",
                           "miss one → wrong widget"],
            "patLabel": "Factory", "patCost": "One new factory + its widgets. App unchanged.",
            "patFile": "LinuxFactory.java",
            "patLines": ln(
                ("class LinuxFactory implements GUIFactory {", "add"),
                ("  public Button   createButton()   { return new LinuxButton(); }", "add"),
                ("  public Checkbox createCheckbox() { return new LinuxCheckbox(); }", "add"),
                ("}   // add one case at startup — nothing else changes", "add"))},
         "narration":
            "Now the change that used to touch the whole codebase. Add a Linux theme. [pause] "
            "With the scattered checks, that meant finding every platform branch and adding a "
            "Linux case to each — and missing one meant a broken screen. [pause] With abstract "
            "factory? You write one new factory — LinuxFactory — and its Linux widgets. Then you "
            "add a single case to that one startup switch. [pause] Every dialog, every toolbar, "
            "every screen in the app now renders in Linux widgets — with not one line changed "
            "anywhere below the top. And a Linux button can never accidentally appear beside a "
            "Mac checkbox, because no factory ever mixes families."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Abstract Factory Pattern",
            "plain": "One factory interface creates a whole family of related products; each "
                     "concrete factory produces one matching family.",
            "nodes": [
                {"id": "fac", "title": "GUIFactory", "stereo": "abstract factory",
                 "members": ["+ createButton()", "+ createCheckbox()"],
                 "x": 700, "y": 190, "w": 420, "color": "#A78BFA"},
                {"id": "mac", "title": "MacFactory", "members": ["→ Mac family"],
                 "x": 300, "y": 470, "w": 340, "color": "#8B93B0"},
                {"id": "win", "title": "WinFactory", "members": ["→ Win family"],
                 "x": 760, "y": 470, "w": 340, "color": "#8B93B0"},
                {"id": "btn", "title": "Button", "stereo": "product", "members": ["+ render()"],
                 "x": 1420, "y": 210, "w": 360, "color": "#22D3EE"},
                {"id": "chk", "title": "Checkbox", "stereo": "product", "members": ["+ toggle()"],
                 "x": 1420, "y": 430, "w": 360, "color": "#22D3EE"}],
            "edges": [
                {"from": "mac", "to": "fac", "kind": "impl"},
                {"from": "win", "to": "fac", "kind": "impl"},
                {"from": "fac", "to": "btn", "kind": "has"},
                {"from": "fac", "to": "chk", "kind": "has"}]},
         "narration":
            "This is the Abstract Factory pattern. [pause] In the center, the abstract factory — "
            "GUIFactory — declaring how to create a whole family: a button, a checkbox. [pause] "
            "Below it, the concrete factories — Mac and Windows — each implementing that "
            "interface to produce one matching family. [pause] On the right, the product "
            "interfaces the factory creates — Button and Checkbox — each with its own concrete "
            "versions per family. [pause] Follow it through. The client holds a GUIFactory. It "
            "asks for a button and a checkbox. And whichever concrete factory is behind the "
            "interface, the two products it returns always belong to the same family. [pause] "
            "One choice of factory fixes the entire look, consistently."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "AbstractFactory", "your": "interface GUIFactory"},
                {"role": "ConcreteFactory", "your": "MacFactory, WinFactory"},
                {"role": "AbstractProduct", "your": "Button, Checkbox (interfaces)"},
                {"role": "ConcreteProduct", "your": "MacButton, WinCheckbox, …"}],
            "plain": "A concrete factory produces a full family of matching products; the client "
                     "uses only the abstract factory and product types.",
            "gof": "Provide an interface for creating families of related or dependent objects "
                   "without specifying their concrete classes."},
         "narration":
            "The names, mapped to your code. [pause] The AbstractFactory is the GUIFactory "
            "interface. [pause] The ConcreteFactories are Mac-factory and Win-factory. [pause] "
            "The AbstractProducts are the Button and Checkbox interfaces. [pause] And the "
            "ConcreteProducts are the specific widgets — Mac-button, Win-checkbox, and the rest. "
            "[pause] The client only ever touches the abstract factory and the abstract "
            "products; it never names a concrete class. [pause] The Gang of Four: provide an "
            "interface for creating families of related or dependent objects, without specifying "
            "their concrete classes. Compare it to Factory Method, from earlier — that made one "
            "product; this makes a whole matching family."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "Rigid on the product axis",
            "costs": ["A lot of classes: factories × products",
                      "Adding a NEW product type is hard",
                      "Every factory must implement every product"],
            "dont": ["The products aren't a matched family",
                     "There's only ever one family",
                     "Products change more than families do"],
            "signal": "you create families of products that must stay consistent, and the family "
                      "varies as a whole."},
         "narration":
            "Abstract Factory has a specific weakness, and it is worth knowing exactly where. "
            "[pause] It is comfortable adding a new family — a new platform is one new factory. "
            "But it is rigid the other way. Add a new product type — say, a slider — and you "
            "must change the factory interface, and then every single concrete factory, to "
            "create it. The pattern is easy to extend by family, hard to extend by product. "
            "[pause] And it comes with a lot of classes — every factory times every product. "
            "[pause] So skip it when the products are not really a matched family, when there is "
            "only ever one family, or when you add product types far more often than families. "
            "[pause] Reach for it when you create families of related products that must stay "
            "consistent, and the whole family varies together."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Abstract Factory, in one breath",
            "items": [
                "Platform checks scattered at every creation site let families leak — a Mac "
                "button beside a Windows checkbox.",
                "The app builds the same widgets; only the family varies and must stay "
                "consistent — so bundle a family behind one factory.",
                "Abstract Factory: one factory makes a whole matching family; pick it once. New "
                "family, new factory — client unchanged."],
            "challenge": "A data layer must produce a Connection, a Command, and a DataReader — "
                         "matched for either MySQL or Postgres, never mixed.",
            "question": "Does Abstract Factory fit? What's the factory, the family of products, "
                        "and where is the choice made?"},
         "narration":
            "Abstract Factory, in one breath. [pause] Platform checks scattered at every "
            "creation site let the families leak into each other — a Mac button ending up beside "
            "a Windows checkbox. [pause] But the app always builds the same widgets; only the "
            "family varies, and it has to stay consistent — so you bundle the whole family "
            "behind one factory. [pause] Abstract Factory: a single factory makes an entire "
            "matching family, and you pick it once. A new family is one new factory, and the "
            "client never changes. [pause] Here is one to carry out. [pause] A data-access layer "
            "must produce a connection, a command, and a data reader — all matched for either "
            "MySQL or Postgres, and never mixed between them. [pause] Does Abstract Factory fit? "
            "What is the factory, what is the family of products, and where is the choice of "
            "family made? [pause] Pause, and sketch it before the next episode."},
    ],
}


MEMENTO = {
    "id": "dp19-memento",
    "title": "Memento",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 19",
            "line1": "Ctrl + Z", "line2": "needs a memory",
            "sub": "snapshot an object's state so you can put it back — without exposing its guts"},
         "narration":
            "Undo is one of the most reassuring features software has. [pause] Make a mistake, "
            "press Ctrl-Z, and the world rolls back. [pause] But to roll back, something has to "
            "have remembered the previous state — the whole state — and be able to restore it "
            "exactly. The naive way to do that pries open the object and copies out its private "
            "fields, and that quietly destroys everything encapsulation gave you. [pause] There "
            "is a way to capture state without exposing it. Let's build undo for an editor."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "Undo in a text editor",
            "situation": "A text editor holds a document — content, cursor, selection. Every "
                         "edit should be undoable: restore the full previous state on Ctrl-Z, "
                         "any number of steps back.",
            "actors": [
                {"emoji": "📝", "label": "The editor's state"},
                {"emoji": "💾", "label": "…snapshotted"},
                {"emoji": "↩️", "label": "…restored on undo"}],
            "ask": "How do you save and restore full state without exposing the editor's "
                   "internals?"},
         "narration":
            "Here is the feature: undo, in a text editor. [pause] The editor holds a document — "
            "the text content, where the cursor is, what is selected. [pause] Every edit the "
            "user makes should be undoable. Press Ctrl-Z, and the entire previous state comes "
            "back — the text, the cursor, the selection, all of it. And not just once; many "
            "steps back. [pause] So the question is: how do you capture and restore the editor's "
            "full state, over and over — without prying open the editor and exposing everything "
            "inside it?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "The history reaches inside.",
            "file": "History.java",
            "lines": ln(
                "class History {",
                ("  void save(Editor e) {", "hi"),
                ("    this.content = e.content;    // grab privates", "hi"),
                ("    this.cursor  = e.cursor;     // one by one", "hi"),
                "  }",
                "  void restore(Editor e) {",
                ("    e.content = this.content; e.cursor = this.cursor;", "hi"),
                "  }",
                "}"),
            "note": "History knows every private field of Editor. Encapsulation is gone."},
         "narration":
            "The direct approach: let the history object reach into the editor and copy its "
            "state out. [pause] To save, it grabs the content, the cursor, each private field, "
            "one by one. To restore, it writes them all back. [pause] It works. [pause] But look "
            "at what just happened. The editor had to expose all of its internals — every "
            "private field is now readable and writable from outside. And the history is "
            "intimately coupled to the editor's exact shape. [pause] The editor can no longer "
            "change how it stores anything without breaking the history. Encapsulation, the "
            "thing that let the editor evolve safely, is gone."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Also remember the selection. And the scroll position.\"",
            "file": "coupled.java",
            "lines": ln(
                "void save(Editor e) {",
                "  this.content   = e.content;",
                "  this.cursor    = e.cursor;",
                ("  this.selection = e.selection;   // new field...", "hi"),
                ("  this.scrollTop = e.scrollTop;   // ...and another", "hi"),
                "}",
                "// every new bit of state → edit save() AND restore()"),
            "smell": "The caretaker duplicates the originator's field list",
            "touched": ["History mirrors every Editor field",
                        "add a field → edit save + restore",
                        "Editor internals are fully public",
                        "two classes locked together"]},
         "narration":
            "Then the state grows, as it always does. Remember the selection too. And the scroll "
            "position. And undo needs those back as well. [pause] So the history's save method "
            "grows a line for each — and its restore method grows a matching line. [pause] Every "
            "single piece of state the editor gains has to be manually mirrored, in two places, "
            "inside a completely different class. [pause] The history has become a fragile "
            "duplicate of the editor's field list. [pause] And because all those fields must "
            "stay public for the history to touch them, the editor's internals are exposed to "
            "the entire program. Two classes, welded together, and an object that can keep no "
            "secrets."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["You must snapshot and restore full state",
                      "The state should stay the object's secret",
                      "The history just stores snapshots in order"],
            "varies": ["What exactly is in that state",
                       "How many snapshots you keep"],
            "principle": "Let the object snapshot ITSELF into an opaque token; a caretaker just "
                         "holds tokens."},
         "narration":
            "What is fixed, and what varies? [pause] Fixed: you need to snapshot the full state "
            "and later restore it. That state should remain the object's own secret. And the "
            "history's job is only to store snapshots, in order. [pause] What varies is what "
            "exactly is inside the state, and how many snapshots you keep around. [pause] Here "
            "is the move. [pause] Stop letting anyone else read the object's fields. Instead, "
            "let the object snapshot itself — packaging its own state into an opaque token that "
            "only it can open. The history then just holds those tokens, in a stack, without "
            "ever looking inside. The object keeps its secrets, and still gets undo."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "A video-game save point", "emoji": "🎮",
            "analogy": "You save the game and later reload — but you never open the save file "
                       "and edit it by hand.",
            "map": [
                {"from": "Hitting 'save'", "to": "editor.save() → a memento"},
                {"from": "The save file", "to": "the opaque memento"},
                {"from": "The list of save slots", "to": "the caretaker / history"},
                {"from": "Reloading a save", "to": "editor.restore(memento)"}],
            "breaks": "a save file can be inspected with the right tools; a true memento stays "
                      "opaque to everyone but its creator."},
         "narration":
            "Think of a save point in a video game. [pause] Before a hard section, you save. If "
            "it goes badly, you reload, and you are exactly where you were — health, inventory, "
            "position, all restored. [pause] But you never open the save file in a text editor "
            "and tweak the numbers by hand. The game wrote it; the game reads it; to you, it is "
            "an opaque blob you simply keep and hand back. [pause] Hitting save is the editor "
            "snapshotting itself. The save file is the memento. Your list of save slots is the "
            "caretaker — the history. And reloading is the editor restoring from a memento. "
            "[pause] Where it strains: a real save file can be pried open with the right tools. "
            "A true memento stays genuinely opaque to everyone except the object that made it."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "An opaque snapshot only the editor can read",
            "file": "Editor.java",
            "lines": ln(
                "class Editor {",
                "  private String content; private int cursor;",
                ("  Memento save() {                    // snapshot self", "add"),
                ("    return new Memento(content, cursor);", "add"),
                ("  }", "add"),
                ("  void restore(Memento m) {           // reload self", "add"),
                ("    this.content = m.content(); this.cursor = m.cursor();", "add"),
                ("  }", "add"),
                "}"),
            "note": "The Editor makes and reads its own Memento — no one else touches its state."},
         "narration":
            "The refactor, step one. [pause] The editor gains two methods of its own. Save, "
            "which packages its current state into a Memento and hands it out. And restore, "
            "which takes a Memento and loads its state back in. [pause] Crucially, the editor's "
            "fields stay private. The only code that ever reads or writes them is the editor "
            "itself, inside these two methods. [pause] The Memento is a snapshot the object "
            "makes of itself, and only it knows how to read. From the outside, that memento is a "
            "sealed box."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "A caretaker that holds sealed snapshots",
            "file": "History.java",
            "lines": ln(
                ("class History {", "hi"),
                ("  private final Deque<Memento> stack = new ArrayDeque<>();", "hi"),
                ("  void push(Memento m) { stack.push(m); }   // just store", "hi"),
                "  Memento pop() { return stack.pop(); }     // just return",
                "}",
                "// History NEVER reads a memento's contents"),
            "note": "The caretaker keeps an ordered pile of opaque tokens. That's all it does."},
         "narration":
            "Step two: the caretaker — the history. [pause] It holds a stack of mementos. But "
            "look at how little it knows. It can push a memento on, and pop one off. That is the "
            "whole class. [pause] It never reads what is inside a memento. It cannot — the "
            "memento is opaque to it. To the history, a memento is just a token to keep in "
            "order. [pause] This is the key separation. The editor knows what state means; the "
            "history knows only when it was captured. Neither one depends on the other's "
            "internals."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Write undo()",
            "file": "App.java",
            "lines": ln(
                "History history = ...;  Editor editor = ...;",
                "void undo() {",
                ("  // ▯ restore the editor to its last snapshot", "ghost"),
                "}"),
            "prompt": "Undo pops the most recent memento and restores it. Two objects, one line "
                      "each.",
            "hint": "editor.restore(history.pop());"},
         "narration":
            "Your turn — pause here. [pause] You have an editor, and a history holding its past "
            "snapshots. [pause] Write undo. [pause] It has to do two things, but they compose "
            "into almost nothing: get the most recent snapshot from the history, and tell the "
            "editor to restore it. [pause] Think about which object pops the memento, and which "
            "object opens it — because that division is the entire point of the pattern."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "Save before each edit; undo pops",
            "file": "Editor.java  +  App.java",
            "lines": ln(
                "void type(String s) {",
                ("  history.push(save());   // snapshot BEFORE editing", "add"),
                ("  content += s;           // then mutate", "add"),
                "}",
                ("void undo() { restore(history.pop()); }   // roll back", "add")),
            "note": "Snapshot before every change; undo just restores the top of the stack."},
         "narration":
            "Step three, and undo comes to life. [pause] Before every edit, the editor snapshots "
            "itself and pushes that memento onto the history. Then it makes the change. [pause] "
            "So the history steadily accumulates a trail of past states. [pause] And undo is now "
            "trivial — pop the most recent snapshot and restore it. Press it again, and the one "
            "before that comes back. [pause] A full, multi-step undo, built from an object that "
            "snapshots itself and a stack that holds the snapshots. Neither knows the other's "
            "secrets."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Undo must also restore selection + scroll\"",
            "naiveLabel": "Exposed", "naiveCost": "Edit the caretaker's save AND restore.",
            "naiveSteps": ["add fields to History too", "mirror them in save + restore",
                           "keep two classes in sync"],
            "patLabel": "Memento", "patCost": "Only Editor.save/restore change. History untouched.",
            "patFile": "Editor.java",
            "patLines": ln(
                ("Memento save() {", "add"),
                ("  return new Memento(content, cursor,", "add"),
                ("                     selection, scrollTop);  // just here", "add"),
                ("}   // History never knew, never cared", "add"))},
         "narration":
            "Now the change that used to ripple. Undo must restore the selection and the scroll "
            "position too. [pause] In the exposed design, that meant adding those fields to the "
            "history class, and mirroring them in both its save and its restore. [pause] With "
            "mementos, you change exactly one place: the editor's own save and restore, where "
            "the memento is built and read. [pause] The history? It never knew what was in a "
            "memento, so it does not change at all. It is still just pushing and popping opaque "
            "tokens. [pause] New state costs a change in one class — the one that owns that "
            "state. That is encapsulation, doing its job."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Memento Pattern",
            "plain": "An object snapshots its own state into an opaque memento; a caretaker "
                     "stores mementos without ever reading them.",
            "nodes": [
                {"id": "orig", "title": "Editor", "stereo": "originator",
                 "members": ["+ save(): Memento", "+ restore(m)"],
                 "x": 180, "y": 400, "w": 420, "color": "#A78BFA"},
                {"id": "mem", "title": "Memento", "stereo": "memento",
                 "members": ["- content, cursor", "(opaque)"],
                 "x": 800, "y": 400, "w": 360, "color": "#22D3EE"},
                {"id": "care", "title": "History", "stereo": "caretaker",
                 "members": ["- Deque<Memento>", "+ push() / undo()"],
                 "x": 1360, "y": 400, "w": 400, "color": "#8B93B0"}],
            "edges": [
                {"from": "orig", "to": "mem", "kind": "assoc"},
                {"from": "care", "to": "mem", "kind": "has"}]},
         "narration":
            "This is the Memento pattern. [pause] Three roles. [pause] On the left, the "
            "originator — the Editor. It is the only one that can create a memento from its "
            "state, and the only one that can restore itself from one. [pause] In the middle, "
            "the memento — a snapshot of the editor's state, opaque to everyone but the editor. "
            "[pause] On the right, the caretaker — the History. It holds mementos and hands them "
            "back, but can never see inside them. [pause] Notice both arrows point at the "
            "memento. The editor produces it and reads it; the history merely stores it. The "
            "state travels between save and restore without ever leaking out."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Originator", "your": "Editor (save + restore)"},
                {"role": "Memento", "your": "the opaque snapshot object"},
                {"role": "Caretaker", "your": "History (a stack of mementos)"},
                {"role": "The rule", "your": "only the Originator reads a Memento"}],
            "plain": "The originator creates and reads mementos; the caretaker only holds them, "
                     "preserving encapsulation.",
            "gof": "Without violating encapsulation, capture and externalize an object's "
                   "internal state so that it can be restored later."},
         "narration":
            "The names, mapped to your code. [pause] The Originator is the Editor — the object "
            "whose state we capture and restore. [pause] The Memento is the opaque snapshot "
            "itself. [pause] The Caretaker is the History, the stack that holds mementos. "
            "[pause] And the rule that makes it all work: only the originator ever reads a "
            "memento's contents. The caretaker treats it as sealed. [pause] The Gang of Four, "
            "and notice the first three words: without violating encapsulation, capture and "
            "externalize an object's internal state, so that it can be restored later. The whole "
            "pattern exists to get undo without breaking encapsulation."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "Snapshots cost memory",
            "costs": ["Each memento copies real state — memory adds up",
                      "Frequent snapshots can be expensive",
                      "A deep history holds a lot of data"],
            "dont": ["The state is trivial to reconstruct",
                     "One field a public getter would expose fine",
                     "Undo isn't actually needed"],
            "signal": "you need to save and restore an object's full state repeatedly, without "
                      "exposing its internals."},
         "narration":
            "Memento is not free, and the cost is memory. [pause] Every snapshot is a real copy "
            "of the object's state. Take one before every keystroke, keep a thousand of them, "
            "and that adds up fast — especially if the state is large. [pause] So real editors "
            "optimize: they snapshot less often, or store only the difference between states "
            "rather than the whole thing. [pause] Skip the pattern when the state is trivial to "
            "reconstruct on the fly, or when a single field behind a getter would do, or when "
            "you simply do not need undo. [pause] Reach for it when you need to save and restore "
            "an object's full state, repeatedly, without tearing open its encapsulation to do "
            "it."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Memento, in one breath",
            "items": [
                "Letting the history reach into the object's private fields destroyed "
                "encapsulation — and locked the two classes together.",
                "The state must be snapshotted and restored, but stay the object's secret — so "
                "let the object snapshot ITSELF, opaquely.",
                "Memento: originator makes and reads snapshots; caretaker only stores them. New "
                "state, one class changes."],
            "challenge": "A drawing app needs undo across shapes, layers, and colors — many "
                         "steps back — while keeping each object's internals private.",
            "question": "Does Memento fit? Who's the originator, what's in the memento, and who "
                        "must never read it?"},
         "narration":
            "Memento, in one breath. [pause] Letting the history reach into an object's private "
            "fields destroyed encapsulation, and locked the two classes together, fragile and "
            "exposed. [pause] But the state only needs to be snapshotted and restored while "
            "staying the object's own secret — so you let the object snapshot itself, into an "
            "opaque token. [pause] Memento: the originator makes and reads the snapshots; the "
            "caretaker only stores them, never opening them. New state costs a change in exactly "
            "one class. [pause] Here is one to carry out. [pause] A drawing app needs undo "
            "across shapes, layers, and colors — many steps back — while keeping each object's "
            "internals private. [pause] Does Memento fit? Who is the originator, what goes "
            "inside the memento, and who must never be allowed to read it? [pause] Pause, and "
            "sketch it before the next episode."},
    ],
}


VISITOR = {
    "id": "dp20-visitor",
    "title": "Visitor",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 20",
            "line1": "New operation,", "line2": "don't touch the classes",
            "sub": "add behavior across a fixed set of types without editing a single one"},
         "narration":
            "Here is a tension every growing codebase hits. [pause] You have a stable set of "
            "types — the elements of a document, the nodes of a syntax tree. They rarely change. "
            "[pause] But the operations you want to run over them keep multiplying. Render them. "
            "Export them. Count words. Check accessibility. [pause] The obvious way piles every "
            "new operation onto every one of those classes, until the data types are buried in "
            "behavior. There is a way to add operations from the outside. Let's build a document "
            "model."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "Operations over a document",
            "situation": "A document is a tree of elements — text, images, tables. The element "
                         "types are stable. But you keep needing new operations: render HTML, "
                         "export Markdown, count words, check accessibility.",
            "actors": [
                {"emoji": "📄", "label": "Stable element types"},
                {"emoji": "⚙️", "label": "Growing operations"},
                {"emoji": "➕", "label": "…added constantly"}],
            "ask": "How do you add a new operation over every element type without editing each "
                   "one?"},
         "narration":
            "Here is the model: a document, made of elements. Text blocks, images, tables. "
            "[pause] That set of element types is stable — you are not inventing new kinds of "
            "element every week. [pause] But the operations you run over them never stop "
            "growing. Render the document to HTML. Export it to Markdown. Count its words. Run "
            "an accessibility check. [pause] Each is a different operation, over the same handful "
            "of element types. [pause] So how do you add a brand-new operation across every "
            "element — without cracking open and editing each element class every single time?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "A method per operation, on each class.",
            "file": "elements.java",
            "lines": ln(
                ("class Text  { String toHtml(); String toMarkdown();", "hi"),
                ("              int wordCount(); ... }", "hi"),
                ("class Image { String toHtml(); String toMarkdown();", "hi"),
                "              int wordCount(); ... }",
                ("class Table { String toHtml(); ... }   // same list", "hi"),
                "// add 'toPdf()' → edit Text, Image, Table, ..."),
            "note": "Every operation is smeared across every element. New op = edit them all."},
         "narration":
            "The obvious approach: give every element a method for every operation. [pause] Text "
            "gets to-HTML, to-Markdown, word-count. Image gets the same three. Table, the same. "
            "[pause] It works. [pause] But watch what happens to the classes. Each element is now "
            "stuffed with operations that have nothing to do with what it fundamentally is. The "
            "Image class knows about HTML, and Markdown, and word-counting, and PDF. [pause] And "
            "the moment you want a new operation — export to PDF — you have to open and edit "
            "every single element class to add it. The operations are scattered across the data, "
            "and every new one touches everything."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Add PDF export. And a spell-checker. And search indexing.\"",
            "file": "bloat.java",
            "lines": ln(
                ("// each new operation = a new method in EVERY element", "hi"),
                ("class Text  { ... toPdf(); spellCheck(); index(); }", "hi"),
                ("class Image { ... toPdf(); spellCheck(); index(); }", "hi"),
                ("class Table { ... toPdf(); spellCheck(); index(); }", "hi"),
                "// the HTML logic for all 3 lives in 3 different files"),
            "smell": "Operations scattered across the data classes",
            "touched": ["new operation → edit every element",
                        "one operation split across N files",
                        "element classes bloat endlessly",
                        "related logic can't be read together"]},
         "narration":
            "Then the operations keep coming. PDF export. A spell-checker. Search indexing. "
            "[pause] Every one of them means a new method added to Text, and to Image, and to "
            "Table, and to every element type there is. [pause] The classes swell without bound. "
            "[pause] And notice something subtler: a single operation — say, rendering to HTML — "
            "is now split across three different files, one fragment in each element. You cannot "
            "read the whole HTML-rendering logic in one place, because it does not live in one "
            "place. [pause] The data types and the operations over them have become hopelessly "
            "tangled."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["The set of element types is stable",
                      "Each operation must handle every type",
                      "One operation is really one idea"],
            "varies": ["The operations — HTML, PDF, word-count",
                       "And new operations arrive constantly"],
            "principle": "Move each operation OUT into its own object that knows how to visit "
                         "every element type."},
         "narration":
            "What is fixed, and what varies? [pause] Fixed: the set of element types barely "
            "changes — text, image, table. Each operation has to handle every one of those "
            "types. And any single operation, like rendering HTML, is really one coherent idea. "
            "[pause] What varies is the operations themselves — and they arrive constantly. "
            "[pause] Here is the move. [pause] Stop scattering each operation across the "
            "elements. Pull each operation out into its own object — a visitor — that knows how "
            "to handle every element type in one place. Then, instead of the element containing "
            "the operation, the operation visits the element. The data stays put; the behavior "
            "comes to it."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "A building inspector", "emoji": "🏢",
            "analogy": "The rooms don't change; a fire inspector, an electrician, an appraiser "
                       "each walk the same rooms and do their own job.",
            "map": [
                {"from": "The rooms", "to": "the element types (stable)"},
                {"from": "Each visiting inspector", "to": "a concrete visitor"},
                {"from": "What it does per room", "to": "visitText(), visitImage()…"},
                {"from": "Sending in a new inspector", "to": "adding one new visitor class"}],
            "breaks": "an inspector can just walk in; a visitor needs the element to 'accept' it "
                      "— the double-dispatch handshake."},
         "narration":
            "Think of a building, and the inspectors who visit it. [pause] The rooms do not "
            "change — the kitchen is the kitchen, the wiring is the wiring. [pause] But all "
            "kinds of specialists come through. A fire inspector, walking every room doing fire "
            "checks. An electrician, walking the same rooms doing electrical checks. An "
            "appraiser, valuing each one. [pause] The rooms are the stable element types. Each "
            "inspector is a visitor. What an inspector does in each kind of room is its visit "
            "methods. And adding a whole new inspection is just sending in one new inspector. "
            "[pause] Where it strains: a real inspector can just walk in. A software visitor "
            "needs the element to formally accept it — a small handshake we will see in a "
            "moment."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "A Visitor interface; elements just accept",
            "file": "Visitor.java",
            "lines": ln(
                ("interface Visitor {              // one visit per type", "add"),
                ("  void visitText(Text t);", "add"),
                ("  void visitImage(Image i);", "add"),
                ("}", "add"),
                ("interface Element { void accept(Visitor v); }", "hi"),
                "// each element implements ONE method: accept"),
            "note": "Elements gain a single method — accept — forever. Operations live in visitors."},
         "narration":
            "The refactor, step one. [pause] Define a Visitor interface with one method per "
            "element type — visit-text, visit-image, visit-table. Each represents what some "
            "operation does for that type. [pause] And the elements? They give up their pile of "
            "operation methods, and gain exactly one method, forever: accept, which takes a "
            "visitor. [pause] That is the trade. Instead of every element carrying every "
            "operation, every element carries a single door — accept — through which any "
            "operation can walk in."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "One visitor = one operation, all types",
            "file": "HtmlVisitor.java",
            "lines": ln(
                ('class HtmlVisitor implements Visitor {', "hi"),
                ('  public void visitText(Text t)  { out += "<p>"+t.body+"</p>"; }', "hi"),
                ('  public void visitImage(Image i){ out += "<img src="+i.url+">"; }', "hi"),
                '}',
                '// and Text.accept simply calls back:',
                ('void accept(Visitor v) { v.visitText(this); }  // double dispatch', "hi")),
            "note": "All the HTML logic, every element, in ONE class. accept picks the visit."},
         "narration":
            "Step two: a concrete visitor is one whole operation. [pause] The HTML visitor "
            "implements visit-text, visit-image, visit-table — the complete HTML-rendering logic "
            "for every element type, finally gathered in a single class. [pause] But how does "
            "the right method get called? Look at accept. When you call accept on a Text, it "
            "turns around and calls visit-text on the visitor, passing itself. [pause] That "
            "little two-step — the element calling back into the visitor — is called double "
            "dispatch. The element knows its own type, so it picks the correct visit method. The "
            "visitor knows the operation. Together, they land on exactly the right behavior."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Wire up double dispatch",
            "file": "Image.java",
            "lines": ln(
                "class Image implements Element {",
                "  void accept(Visitor v) {",
                ("    // ▯ call the visitor's method for THIS type", "ghost"),
                "  }",
                "}"),
            "prompt": "An Image must route an incoming visitor to the correct visit method. "
                      "Which one?",
            "hint": "v.visitImage(this);"},
         "narration":
            "Your turn — pause here. [pause] This is the heart of the pattern, in one line. "
            "[pause] An image has just been handed a visitor — any visitor, it does not know "
            "which operation. [pause] Its job in accept is to call back the one visit method "
            "that matches its own type, and pass itself along. [pause] Which method does an "
            "Image call? Write it. And notice: the image does not know or care what the visitor "
            "does — only that it is an image, so it calls the image method."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "Run a visitor; add another for free",
            "file": "app.java",
            "lines": ln(
                "HtmlVisitor html = new HtmlVisitor();",
                ("for (Element e : document) e.accept(html);   // render all", "add"),
                "// want word count instead? a whole new operation:",
                ("WordCountVisitor wc = new WordCountVisitor();", "add"),
                ("for (Element e : document) e.accept(wc);   // ZERO element edits", "hi")),
            "note": "Swap the visitor, get a whole new operation. Elements never changed."},
         "narration":
            "Step three, and the payoff arrives. [pause] To render the document to HTML, you "
            "make an HTML visitor and let every element accept it. Each element routes itself to "
            "the right visit method, and the HTML assembles. [pause] Now you want word count "
            "instead — a completely different operation. [pause] You write a WordCount visitor, "
            "and run the exact same loop with it. [pause] Not one element class changed. The "
            "document did not change. You added an entire new operation over the whole element "
            "hierarchy, purely by adding one class from the outside."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Add Markdown export\"",
            "naiveLabel": "Scattered", "naiveCost": "A new method in every element class.",
            "naiveSteps": ["edit Text, Image, Table…", "the logic split across all of them",
                           "recompile every element"],
            "patLabel": "Visitor", "patCost": "One new class. Elements untouched.",
            "patFile": "MarkdownVisitor.java",
            "patLines": ln(
                ('class MarkdownVisitor implements Visitor {', "add"),
                ('  public void visitText(Text t)  { out += t.body + "\\n"; }', "add"),
                ('  public void visitImage(Image i){ out += "!["+i.alt+"]"; }', "add"),
                ('}   // all Markdown logic, one file, zero element edits', "add"))},
         "narration":
            "Now the change that used to touch everything. Add Markdown export. [pause] In the "
            "scattered design, that meant a new to-Markdown method in Text, and Image, and "
            "Table, with the logic split across all three. [pause] With visitors? One new class "
            "— a Markdown visitor — holding the complete Markdown logic for every element type, "
            "in one readable place. [pause] And every element? Untouched. They already know how "
            "to accept any visitor. [pause] A new operation is now purely additive: one class, "
            "from the outside, and the whole document can be exported to Markdown."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Visitor Pattern",
            "plain": "Move operations into visitor objects; each element accepts a visitor and "
                     "calls back the method for its own type — double dispatch.",
            "nodes": [
                {"id": "vis", "title": "Visitor", "stereo": "visitor",
                 "members": ["+ visitText(t)", "+ visitImage(i)"],
                 "x": 160, "y": 210, "w": 400, "color": "#A78BFA"},
                {"id": "html", "title": "HtmlVisitor", "members": ["renders HTML"],
                 "x": 60, "y": 470, "w": 300, "color": "#8B93B0"},
                {"id": "wc", "title": "WordCount", "members": ["counts words"],
                 "x": 400, "y": 470, "w": 300, "color": "#8B93B0"},
                {"id": "elem", "title": "Element", "stereo": "element",
                 "members": ["+ accept(Visitor)"], "x": 1360, "y": 210, "w": 400,
                 "color": "#22D3EE"},
                {"id": "text", "title": "Text", "members": ["accept → visitText"],
                 "x": 1260, "y": 470, "w": 300, "color": "#8B93B0"},
                {"id": "image", "title": "Image", "members": ["accept → visitImage"],
                 "x": 1600, "y": 470, "w": 300, "color": "#8B93B0"}],
            "edges": [
                {"from": "html", "to": "vis", "kind": "impl"},
                {"from": "wc", "to": "vis", "kind": "impl"},
                {"from": "text", "to": "elem", "kind": "impl"},
                {"from": "image", "to": "elem", "kind": "impl"},
                {"from": "elem", "to": "vis", "kind": "has"}]},
         "narration":
            "This is the Visitor pattern. [pause] Two hierarchies. [pause] On the left, the "
            "Visitor — one method per element type — with concrete visitors beneath it: an HTML "
            "renderer, a word counter. Each is one operation. [pause] On the right, the Element "
            "— with its single accept method — and the concrete elements beneath it: Text, "
            "Image. Each knows only how to accept. [pause] And the arrow across the middle is "
            "the double dispatch: an element's accept calls back into the visitor, choosing the "
            "method that matches its own type. [pause] Adding a visitor on the left adds an "
            "operation, cheaply. Everything on the right stays exactly as it is."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Visitor", "your": "interface Visitor (visitText…)"},
                {"role": "ConcreteVisitor", "your": "HtmlVisitor, WordCountVisitor"},
                {"role": "Element", "your": "interface Element (accept)"},
                {"role": "ConcreteElement", "your": "Text, Image, Table"}],
            "plain": "Each element's accept() calls back the matching visit method; a visitor "
                     "gathers one operation across all element types.",
            "gof": "Represent an operation to be performed on the elements of an object "
                   "structure. Visitor lets you define a new operation without changing the "
                   "classes of the elements."},
         "narration":
            "The names, mapped to your code. [pause] The Visitor is the Visitor interface, with "
            "a visit method per element type. [pause] The ConcreteVisitors are the operations — "
            "HTML renderer, word counter. [pause] The Element is the interface with accept. "
            "[pause] And the ConcreteElements are the data types — text, image, table. [pause] "
            "Each element's accept calls back the matching visit method — that is the double "
            "dispatch — and each visitor gathers one whole operation across every element type. "
            "[pause] The Gang of Four: represent an operation to be performed on the elements of "
            "an object structure — Visitor lets you define a new operation without changing the "
            "classes of the elements."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "Easy new operations, hard new elements",
            "costs": ["A new ELEMENT type edits every visitor",
                      "Visitors often need the elements' internals",
                      "Double dispatch takes a beat to grasp"],
            "dont": ["The element types change often",
                     "There's really only one operation",
                     "The operations barely differ by type"],
            "signal": "a stable set of types, a growing set of operations over them, and you're "
                      "tired of editing every class."},
         "narration":
            "Visitor makes a sharp trade, and you must know which way it cuts. [pause] It makes "
            "adding a new operation trivial — one new visitor. But it makes adding a new element "
            "type painful: a new element means a new visit method on the Visitor interface, and "
            "therefore an edit to every single visitor you have written. [pause] It is the exact "
            "mirror of the naive approach — and the opposite of most patterns, which favor new "
            "types over new operations. [pause] Visitors also often need access to the elements' "
            "internals, which can strain encapsulation. And the double-dispatch dance takes a "
            "moment to get used to. [pause] So skip it when your element types change often, or "
            "when there is really only one operation. [pause] Reach for it when the set of types "
            "is stable, the operations over them keep growing, and you are tired of editing "
            "every class each time."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Visitor, in one breath",
            "items": [
                "Piling every operation onto every element bloated the data classes and split "
                "each operation across many files.",
                "The types are stable; the operations grow — so move each operation into a "
                "visitor that handles every type in one place.",
                "Visitor: elements accept a visitor and call back their own visit method (double "
                "dispatch). New operation, one new class."],
            "challenge": "A compiler has a stable AST — literals, binary ops, calls — and "
                         "growing passes: type-check, optimize, generate code.",
            "question": "Does Visitor fit? What are the elements, what's a visitor, and what's "
                        "the cost if the AST grows a new node?"},
         "narration":
            "Visitor, in one breath. [pause] Piling every operation onto every element bloated "
            "the data classes, and split each single operation across many files. [pause] But "
            "the types are stable while the operations grow — so you move each operation into "
            "its own visitor that handles every type in one place. [pause] Visitor: elements "
            "accept a visitor and call back their own visit method — the double dispatch — so a "
            "new operation is just one new class, and no element ever changes. [pause] Here is "
            "one to carry out. [pause] A compiler has a stable syntax tree — literals, binary "
            "operations, function calls — and a growing set of passes over it: type-checking, "
            "optimization, code generation. [pause] Does Visitor fit? What are the elements, "
            "what is a visitor, and what does it cost you the day the syntax tree grows a "
            "brand-new node type? [pause] Pause, and sketch it before the next episode."},
    ],
}


PROTOTYPE = {
    "id": "dp21-prototype",
    "title": "Prototype",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 21",
            "line1": "Copy,", "line2": "don't rebuild",
            "sub": "make new objects by cloning a ready-made one instead of constructing from scratch"},
         "narration":
            "Some objects are expensive to bring into existence. [pause] Loading assets, running "
            "setup, configuring a dozen fields — and then you need fifty of them, nearly "
            "identical. [pause] Building each one from scratch repeats all that cost, and forces "
            "whoever is spawning them to know every detail of how they are assembled. [pause] "
            "But if you already have one, fully built... why not just copy it? Let's spawn some "
            "enemies."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "Spawning a wave of enemies",
            "situation": "A game spawns waves of enemies. Each enemy is expensive to create — "
                         "load a mesh, set stats, wire up AI — and a wave needs dozens of nearly "
                         "identical ones.",
            "actors": [
                {"emoji": "👹", "label": "Expensive to build"},
                {"emoji": "🌊", "label": "…dozens per wave"},
                {"emoji": "⚡", "label": "…nearly identical"}],
            "ask": "How do you produce many configured copies without rebuilding each from "
                   "scratch?"},
         "narration":
            "Here is the situation: a game spawning waves of enemies. [pause] Creating a single "
            "enemy is not cheap. You load its mesh, set its stats, wire up its AI behavior, tune "
            "a dozen parameters. [pause] And a wave is not one enemy — it is thirty orcs, all "
            "nearly identical. [pause] Building each one from the ground up repeats that whole "
            "expensive setup, thirty times. And the spawner has to know, in full, how to "
            "construct and configure every kind of enemy. [pause] So how do you produce many "
            "configured copies, fast, without rebuilding each one from scratch?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "New one up, then configure. Again.",
            "file": "Spawner.java",
            "lines": ln(
                "Orc spawnOrc() {",
                ("  Orc o = new Orc();", "hi"),
                ('  o.mesh = load("orc.mesh");   // expensive!', "hi"),
                ("  o.hp = 100; o.speed = 3; o.ai = new PatrolAI();", "hi"),
                ("  o.loot = ...; o.sounds = ...;   // 12 more fields", "hi"),
                "  return o;                    // ...every single time",
                "}"),
            "note": "Every spawn reloads assets and re-sets every field. The spawner knows it all."},
         "narration":
            "The direct approach: new up an orc, then configure it. [pause] Create the object, "
            "load its mesh from disk — which is the expensive part — set its hit points, its "
            "speed, its AI, its loot table, its sounds, a dozen fields. [pause] And then do all "
            "of that again for the next orc. And the next. [pause] Every spawn re-runs the full, "
            "costly construction. [pause] Worse, the spawner now contains the complete recipe "
            "for building every enemy — every field, every asset path. It is not spawning "
            "enemies so much as manufacturing them from raw materials, over and over."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Add a FireOrc variant. Let designers make new ones.\"",
            "file": "factory-bloat.java",
            "lines": ln(
                ("Orc     spawnOrc()     { ...15 lines of setup... }", "hi"),
                ("Dragon  spawnDragon()  { ...20 lines of setup... }", "hi"),
                ("FireOrc spawnFireOrc() { ...an Orc, 2 fields differ... }", "hi"),
                "// a near-duplicate method per variant",
                ("// designers can't add a variant without new CODE", "hi")),
            "smell": "The full construction recipe, duplicated per type and variant",
            "touched": ["a build method per enemy type",
                        "a variant = a near-duplicate method",
                        "designers need code for a new enemy",
                        "asset loading repeated everywhere"]},
         "narration":
            "Then the variants multiply. Add a fire orc — which is just an orc with two "
            "different fields. [pause] But to build it, you write a whole new spawn method, a "
            "near-duplicate of the orc one. [pause] Every enemy type, every variant, gets its "
            "own construction method inside the spawner, most of them copies of each other. "
            "[pause] And here is the real wall: a level designer wants to invent a new enemy — a "
            "tougher orc, a faster dragon — at design time, by tweaking an existing one. [pause] "
            "But every enemy's construction lives in compiled code. They cannot create a new "
            "variant without a programmer. The recipe is trapped in the factory."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["You need many configured copies",
                      "The costly setup was already done once",
                      "A variant is a small tweak of an existing one"],
            "varies": ["Which base object you start from",
                       "A few fields, here and there"],
            "principle": "Build one fully-configured object, then CLONE it — let the object copy "
                         "itself."},
         "narration":
            "What is fixed, and what varies? [pause] Fixed: you need lots of configured copies. "
            "The expensive setup, for any given type, only truly needs to happen once. And a new "
            "variant is almost always a small tweak of one that already exists. [pause] What "
            "varies is which object you start from, and a few fields here and there. [pause] "
            "Here is the move. [pause] Build one object, fully configured — a prototype. Then, "
            "instead of constructing new ones from scratch, ask that prototype to clone itself. "
            "Copying an existing object skips all the setup, and a variant becomes: clone one, "
            "change two fields. The object knows how to copy itself; the spawner just says "
            "clone."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "A photocopier", "emoji": "🖨️",
            "analogy": "You set up the original once; after that, every copy is a press of a "
                       "button — no re-typing.",
            "map": [
                {"from": "The original document", "to": "the prototype"},
                {"from": "Pressing 'copy'", "to": "clone()"},
                {"from": "Edits on a copy", "to": "tweaking a cloned object"},
                {"from": "The stack of copies", "to": "your spawned instances"}],
            "breaks": "a photocopy is flat; a cloned object may share references — deep vs "
                      "shallow copy is the catch."},
         "narration":
            "Think of a photocopier. [pause] You type up a document once — carefully, with all "
            "its formatting. That is the expensive part. [pause] After that, you never retype "
            "it. You lay the original on the glass and press copy, and out come as many as you "
            "want, instantly. Want a variant? Copy it, then mark up that copy by hand. [pause] "
            "The original is the prototype. Pressing copy is clone. Marking up a copy is "
            "tweaking a cloned object. And the stack of copies is your spawned instances. "
            "[pause] Where it breaks — and this is the real catch of the pattern: a photocopy is "
            "completely flat and separate. A cloned object might still share references with its "
            "original. Whether a copy is shallow or deep is the one thing you must get right."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "The object clones itself",
            "file": "Enemy.java",
            "lines": ln(
                ("interface Enemy { Enemy clone(); }", "add"),
                "class Orc implements Enemy {",
                "  Mesh mesh; int hp; AI ai; ...;",
                ("  public Orc clone() {              // copy myself", "add"),
                ("    Orc c = new Orc();", "add"),
                ("    c.mesh = this.mesh; c.hp = this.hp;   // share/copy", "add"),
                ("    c.ai = this.ai.clone();   // deep-copy mutable bits", "add"),
                ("    return c;", "add"),
                "  }",
                "}"),
            "note": "The Orc knows how to copy itself — including which parts to deep-copy."},
         "narration":
            "The refactor, step one. [pause] Give every enemy a clone method — the ability to "
            "produce a copy of itself. [pause] Inside the orc's clone, it makes a new orc and "
            "copies its fields across. [pause] But watch the AI line. The mesh can be shared — "
            "it is read-only. But the AI has mutable state, so a copy needs its own; the orc "
            "deep-copies it. [pause] This is the crux: the object itself decides what to copy "
            "shallowly and what to copy deeply, because only it knows which of its parts are "
            "safe to share. No outside code could get that right."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "A registry of ready-made prototypes",
            "file": "Bestiary.java",
            "lines": ln(
                ("class Bestiary {", "hi"),
                ("  private Map<String,Enemy> prototypes = new HashMap<>();", "hi"),
                ("  void register(String key, Enemy p) { prototypes.put(key, p); }", "hi"),
                ("  Enemy spawn(String key) {", "hi"),
                ("    return prototypes.get(key).clone();   // copy, don't build", "hi"),
                "  }",
                "}"),
            "note": "Configure each prototype ONCE, register it. Spawning is just clone()."},
         "narration":
            "Step two: a registry of prototypes — call it the bestiary. [pause] It holds a map "
            "from a name to one fully-configured example of each enemy. You build the orc "
            "prototype once, with all its expensive setup, and register it under orc. [pause] "
            "Now spawning is trivial. Ask the bestiary to spawn an orc, and it looks up the orc "
            "prototype and returns a clone. [pause] No construction. No asset loading. No "
            "field-setting. Just a copy of something already built. [pause] The costly work "
            "happened exactly once, when the prototype was registered."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Write Orc.clone()",
            "file": "Orc.java",
            "lines": ln(
                "class Orc implements Enemy {",
                "  Mesh mesh; int hp;  AI ai;   // ai is mutable!",
                "  public Orc clone() {",
                ("    // ▯ copy fields — but the AI needs its OWN copy", "ghost"),
                "  }",
                "}"),
            "prompt": "Copy the orc. The mesh can be shared, but the mutable AI must be "
                      "deep-copied. Why?",
            "hint": "new Orc(mesh, hp, ai.clone())"},
         "narration":
            "Your turn — pause here. [pause] Write the orc's clone. [pause] Copy its fields into "
            "a new orc — but think hard about one distinction. The mesh is read-only, so every "
            "clone can safely share the same one. [pause] The AI, though, has mutable state. If "
            "two orcs shared one AI object, moving one would move the other. [pause] So the AI "
            "must be deep-copied — each clone gets its own. Get that shallow-versus-deep line "
            "right, and you understand the whole pattern."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "Spawn by cloning; register variants at runtime",
            "file": "game.java",
            "lines": ln(
                ('bestiary.register("orc", configuredOrc);   // once', "add"),
                ("for (int i=0;i<30;i++) wave.add(bestiary.spawn(\"orc\"));", "add"),
                "// a designer's tweak, at RUNTIME — no new class:",
                ('Orc fireOrc = bestiary.spawn("orc"); fireOrc.hp = 200;', "add"),
                ('bestiary.register("fireOrc", fireOrc);   // a new "type"!', "hi")),
            "note": "New enemy types are registered live — no new class, no spawner change."},
         "narration":
            "Step three, and the payoff. [pause] Register the configured orc once. Then spawn a "
            "wave of thirty by cloning it — fast, no repeated setup. [pause] But here is the "
            "part that was impossible before. [pause] A designer takes a clone of the orc, bumps "
            "its hit points to two hundred, and registers it as a fire-orc. [pause] They just "
            "created a new enemy type — at runtime, with no new class, and no change to the "
            "spawner. From now on, spawn fire-orc clones that new prototype. New types are born "
            "by copying and tweaking, not by writing code."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Designers invent a boss variant at runtime\"",
            "naiveLabel": "Factory", "naiveCost": "A programmer writes a new build method.",
            "naiveSteps": ["new spawnBoss() in code", "near-duplicate of spawnDragon()",
                           "recompile, redeploy to test"],
            "patLabel": "Prototype", "patCost": "Clone a dragon, tweak, register. Live.",
            "patFile": "designer tool",
            "patLines": ln(
                ('Enemy boss = bestiary.spawn("dragon").clone();', "add"),
                ("boss.hp *= 5;  boss.scale = 2.0;  // buff it", "add"),
                ('bestiary.register("dragonBoss", boss);  // no code!', "add"),
                ("// spawner spawns it, never knowing its class", "add"))},
         "narration":
            "Now the change that used to require an engineer. Designers want to invent a boss — "
            "a beefed-up dragon — while the game is running. [pause] In the factory world, that "
            "meant a programmer writing a new build method, a near-duplicate of the dragon one, "
            "then recompiling and redeploying just to test it. [pause] With prototypes? A "
            "designer clones the dragon, multiplies its health, doubles its size, and registers "
            "it as a dragon-boss. [pause] No new class. No recompile. No engineer. [pause] And "
            "the spawner spawns that boss exactly like anything else — by cloning a prototype it "
            "has never heard of. New content, created live, by copying."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Prototype Pattern",
            "plain": "Create new objects by cloning a fully-configured prototype, so the client "
                     "copies instead of constructing — and can even add types at runtime.",
            "nodes": [
                {"id": "proto", "title": "Enemy", "stereo": "prototype",
                 "members": ["+ clone(): Enemy"], "x": 720, "y": 210, "w": 440,
                 "color": "#22D3EE"},
                {"id": "orc", "title": "Orc", "members": ["+ clone()"],
                 "x": 240, "y": 470, "w": 340, "color": "#8B93B0"},
                {"id": "dragon", "title": "Dragon", "members": ["+ clone()"],
                 "x": 800, "y": 470, "w": 340, "color": "#8B93B0"},
                {"id": "client", "title": "Bestiary", "stereo": "client",
                 "members": ["- prototypes: Map", "+ spawn(k) = clone"],
                 "x": 1400, "y": 360, "w": 380, "color": "#A78BFA"}],
            "edges": [
                {"from": "orc", "to": "proto", "kind": "impl"},
                {"from": "dragon", "to": "proto", "kind": "impl"},
                {"from": "client", "to": "proto", "kind": "assoc"}]},
         "narration":
            "This is the Prototype pattern. [pause] At the top, the prototype interface — Enemy "
            "— whose defining ability is to clone itself. [pause] Below it, the concrete "
            "prototypes — Orc, Dragon — each knowing how to copy itself correctly, deep where it "
            "must be. [pause] On the right, the client — the Bestiary — which holds configured "
            "prototypes and spawns new objects by cloning them. [pause] Notice what the client "
            "never does: it never calls new on a concrete enemy. It only ever clones. [pause] "
            "Because creation is just copying an example, you can hand the bestiary a brand-new, "
            "pre-configured prototype at runtime — and it will happily spawn a type that did not "
            "exist when the code was written."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Prototype", "your": "interface Enemy (clone)"},
                {"role": "ConcretePrototype", "your": "Orc, Dragon (clone themselves)"},
                {"role": "Client", "your": "Bestiary — spawns via clone()"},
                {"role": "The catch", "your": "deep vs shallow copy in clone()"}],
            "plain": "Each prototype returns a copy of itself; the client builds new objects by "
                     "cloning registered prototypes.",
            "gof": "Specify the kinds of objects to create using a prototypical instance, and "
                   "create new objects by copying this prototype."},
         "narration":
            "The names, mapped to your code. [pause] The Prototype is the Enemy interface, with "
            "its clone method. [pause] The ConcretePrototypes are the orc and the dragon, each "
            "able to copy itself. [pause] The Client is the bestiary, which spawns by cloning. "
            "[pause] And the catch, always: getting deep-versus-shallow copy right inside clone. "
            "[pause] The Gang of Four: specify the kinds of objects to create using a "
            "prototypical instance, and create new objects by copying this prototype. In Java, "
            "this is exactly why the copy constructor and Cloneable exist — though most teams "
            "prefer a plain copy constructor to Java's built-in clone."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "Cloning is deceptively tricky",
            "costs": ["Deep vs shallow copy is easy to get wrong",
                      "Shared mutable state leaks between copies",
                      "Circular references make cloning hard"],
            "dont": ["Objects are cheap to just construct",
                     "Each instance is genuinely unique",
                     "There's no costly setup to reuse"],
            "signal": "creating a configured object is expensive, and you need many copies — or "
                      "new types added at runtime."},
         "narration":
            "Prototype's danger lives entirely inside clone. [pause] The moment an object holds "
            "another mutable object, you have to decide: copy the reference, or copy the thing? "
            "Get it wrong — a shallow copy where you needed a deep one — and two clones silently "
            "share state, and mutating one corrupts the other. It is one of the classic, "
            "maddening bugs. [pause] Circular references make it harder still. [pause] So skip "
            "the pattern when objects are cheap to just build, when every instance is genuinely "
            "one-of-a-kind, or when there is no expensive setup worth reusing. [pause] Reach for "
            "it when constructing a configured object is costly and you need many copies — or "
            "when you want to add whole new object types at runtime, by example."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Prototype, in one breath",
            "items": [
                "Rebuilding each object from scratch repeated expensive setup and trapped every "
                "type's recipe inside the spawner.",
                "You already have one configured, and a variant is a small tweak — so build one "
                "prototype and CLONE it.",
                "Prototype: the object copies itself (deep where needed); the client spawns by "
                "cloning. New type, registered live."],
            "challenge": "A graphics editor lets users duplicate any shape — even a complex "
                         "group with nested styling — and drag the copy away, fully independent.",
            "question": "Does Prototype fit? What's the prototype, what must clone() deep-copy, "
                        "and where's the shallow-copy trap?"},
         "narration":
            "Prototype, in one breath. [pause] Rebuilding each object from scratch repeated the "
            "expensive setup every time, and trapped every type's construction recipe inside the "
            "spawner. [pause] But you already have one configured, and a variant is just a small "
            "tweak — so you build a single prototype and clone it. [pause] Prototype: the object "
            "copies itself, deep where it must be, and the client spawns new objects by cloning "
            "— even types registered live, at runtime. [pause] Here is one to carry out. [pause] "
            "A graphics editor lets a user duplicate any shape — even a complex group with "
            "nested styling — and drag the copy away, fully independent of the original. [pause] "
            "Does Prototype fit? What is the prototype, what exactly must clone deep-copy, and "
            "where is the shallow-copy trap waiting? [pause] Pause, and sketch it before the "
            "final episode."},
    ],
}


FLYWEIGHT = {
    "id": "dp22-flyweight",
    "title": "Flyweight",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 22",
            "line1": "A million objects,", "line2": "a few megabytes",
            "sub": "share the heavy, identical parts so millions of instances cost almost nothing"},
         "narration":
            "Sometimes you need not dozens of objects, but millions. [pause] A forest with a "
            "million trees. A document with a million characters. A map with a million markers. "
            "[pause] If each one carries its own copy of the heavy data — the mesh, the glyph, "
            "the icon — you multiply that weight by a million, and you run out of memory before "
            "you begin. [pause] But most of that data is identical across all of them. There is "
            "a way to share it. Let's grow a forest."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "Rendering a forest",
            "situation": "A game renders a forest of a million trees. Each tree has a position. "
                         "But there are only three species — and each species' mesh and texture "
                         "is several megabytes.",
            "actors": [
                {"emoji": "🌲", "label": "1,000,000 trees"},
                {"emoji": "🎨", "label": "3 heavy species"},
                {"emoji": "📍", "label": "…each at a position"}],
            "ask": "How do you give a million trees their own position without a million copies "
                   "of the mesh?"},
         "narration":
            "Here is the scene: a forest of a million trees. [pause] Every tree needs its own "
            "position in the world — that part is genuinely unique to each one. [pause] But "
            "there are only three species of tree. And each species carries a mesh and a texture "
            "that weigh several megabytes. [pause] A million trees, but only three actual "
            "appearances. [pause] So how do you give every tree its own position, without "
            "storing a million separate copies of a mesh that is really only one of three "
            "things?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "Each tree carries everything.",
            "file": "Tree.java",
            "lines": ln(
                "class Tree {",
                "  int x, y;                     // unique per tree",
                ("  Mesh mesh;                    // ~2 MB — DUPLICATED", "hi"),
                ("  Texture texture;              // ~2 MB — DUPLICATED", "hi"),
                "  String species;",
                "}",
                ("// 1,000,000 trees × 4 MB = 4 TERABYTES. it won't fit.", "hi")),
            "note": "Every tree stores its own mesh + texture. A million near-identical copies."},
         "narration":
            "The direct approach: each tree is a self-contained object with everything it needs. "
            "[pause] Its position — fine, that is unique. [pause] But also its own mesh, and its "
            "own texture. Several megabytes each. [pause] Now multiply. A million trees, each "
            "holding four megabytes of mesh and texture, is four terabytes of memory — for data "
            "that is really just three distinct appearances, copied a million times over. "
            "[pause] The program does not run slowly. It does not run at all. It cannot allocate "
            "that, and it never could."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"We need a denser forest. And two more species.\"",
            "file": "memory.java",
            "lines": ln(
                ("// 1,000,000 trees, each with its own mesh+texture:", "hi"),
                ("//   4 TB — impossible", "hi"),
                ("// push to 5,000,000 for a denser forest:", "hi"),
                ("//   20 TB — more impossible", "hi"),
                "// the mesh bytes are IDENTICAL across most trees"),
            "smell": "Massive per-object data that is identical across objects",
            "touched": ["mesh + texture copied per tree",
                        "memory scales with tree COUNT",
                        "denser forest → linearly worse",
                        "3 real appearances, millions of copies"]},
         "narration":
            "And the requirements only push harder. A denser forest — five million trees. "
            "[pause] The memory does not just grow; it grows with the raw count of objects, "
            "because each one drags its own full copy of the heavy data. [pause] Five million "
            "times four megabytes is twenty terabytes. [pause] But step back and look at what is "
            "being stored. Across those millions of trees, the mesh bytes are identical — there "
            "are only three distinct meshes in the entire forest. [pause] You are paying, "
            "millions of times over, to store the exact same thing. The waste is not a little "
            "overhead; it is essentially all of the memory."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["The mesh + texture — one per species",
                      "Shared, identical across most trees",
                      "Call this the INTRINSIC state"],
            "varies": ["Each tree's position (and scale)",
                       "Unique per instance",
                       "Call this the EXTRINSIC state"],
            "principle": "Split shared (intrinsic) from unique (extrinsic); store the shared "
                         "part ONCE and point to it."},
         "narration":
            "What is fixed, and what varies? This is the whole insight, so look closely. [pause] "
            "The mesh and texture are fixed per species — three of them, identical across every "
            "tree of that kind. Call that the intrinsic state: shared, and the same for many "
            "objects. [pause] The position is unique to each tree. Call that the extrinsic "
            "state: it varies per instance. [pause] The naive design fused the two, so the "
            "shared part got copied a million times. [pause] Here is the move. [pause] Split "
            "them apart. Store the heavy, shared intrinsic state exactly once — one object per "
            "species — and let every tree simply point to it, while keeping only its own tiny "
            "extrinsic position."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "Movable type", "emoji": "🔤",
            "analogy": "A press has ONE metal 'e' and stamps it in thousands of places — it "
                       "doesn't cast a new 'e' for every word.",
            "map": [
                {"from": "The one metal letter", "to": "the shared flyweight"},
                {"from": "Where it's stamped", "to": "the extrinsic position"},
                {"from": "The type case (pool)", "to": "the flyweight factory"},
                {"from": "The printed page", "to": "your million trees"}],
            "breaks": "metal type physically moves between spots; a flyweight is referenced from "
                      "many places at once, never moved."},
         "narration":
            "Think of an old printing press, and movable type. [pause] To print a page full of "
            "the letter e, the printer does not cast a new metal e for every single occurrence. "
            "[pause] There is one metal e, and it is inked and stamped at thousands of "
            "positions. The letter is shared; only where it lands changes. [pause] The one metal "
            "letter is the shared flyweight — our tree type. Where it gets stamped is the "
            "extrinsic position. The case that holds the reusable letters is the flyweight "
            "factory. And the finished page is your million trees. [pause] Where it strains: a "
            "piece of metal type is physically moved from spot to spot. A flyweight in memory is "
            "not moved — it is referenced from a million places at once."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "Extract the shared intrinsic state",
            "file": "TreeType.java",
            "lines": ln(
                ("class TreeType {                  // the flyweight", "add"),
                ("  final Mesh mesh;                // heavy, SHARED", "add"),
                ("  final Texture texture;          // heavy, SHARED", "add"),
                ("  final String species;", "add"),
                ("  void draw(int x, int y) { ... } // extrinsic passed IN", "add"),
                "}"),
            "note": "One TreeType per species — created once, shared by millions. Immutable."},
         "narration":
            "The refactor, step one. [pause] Pull the heavy, shared state into its own class — "
            "the TreeType. It holds the mesh, the texture, the species. The intrinsic state. "
            "[pause] There will be exactly one of these per species — three objects, total, for "
            "the whole forest. [pause] And notice its draw method takes the position as "
            "parameters. The flyweight does not store where it is drawn; that extrinsic detail "
            "is handed in at draw time. [pause] Crucially, a TreeType is immutable. Because it "
            "is shared by millions of trees, no single tree can be allowed to change it."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "A factory that shares, never duplicates",
            "file": "TreeFactory.java",
            "lines": ln(
                ("class TreeFactory {", "hi"),
                ("  static Map<String,TreeType> pool = new HashMap<>();", "hi"),
                ("  static TreeType get(String species, ...) {", "hi"),
                ("    return pool.computeIfAbsent(species,", "hi"),
                ("      s -> new TreeType(loadMesh(s), ...));   // once", "hi"),
                "  }",
                "}"),
            "note": "First request for a species builds it; every request after shares that one."},
         "narration":
            "Step two: a factory that guarantees sharing. [pause] The tree factory keeps a pool "
            "— a map from species name to its one TreeType. [pause] The first time anyone asks "
            "for an oak, the factory builds the oak type, loads its heavy mesh, and stores it. "
            "[pause] Every request after that returns the very same object. [pause] So no matter "
            "how many million oaks you plant, there is exactly one oak TreeType in memory, "
            "handed out over and over. The factory is the single gate that makes sure the heavy "
            "data is never duplicated."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Write TreeFactory.get()",
            "file": "TreeFactory.java",
            "lines": ln(
                "static Map<String,TreeType> pool = new HashMap<>();",
                "static TreeType get(String species) {",
                ("  // ▯ return the shared one, or make it if it's new", "ghost"),
                "}"),
            "prompt": "Return the existing TreeType for a species, creating and caching it only "
                      "the first time.",
            "hint": "pool.computeIfAbsent(species, s -> new TreeType(load(s)));"},
         "narration":
            "Your turn — pause here. [pause] Write the factory's get. [pause] Given a species, "
            "it must return the one shared TreeType for it. [pause] If this is the first time "
            "anyone has asked for that species, build it — load the heavy mesh — and cache it in "
            "the pool. Every time after, return the cached one. [pause] The whole memory saving "
            "hinges on this method never building the same type twice."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "A million tiny trees, three shared types",
            "file": "Forest.java",
            "lines": ln(
                ("class Tree {                      // the context", "add"),
                ("  int x, y;                       // ONLY extrinsic state", "add"),
                ("  TreeType type;                  // a POINTER, not a copy", "add"),
                ("}", "add"),
                "for (int i=0;i<1_000_000;i++)",
                ('  forest.add(new Tree(rx(), ry(), TreeFactory.get("oak")));', "hi")),
            "note": "Each Tree = 2 ints + one shared pointer. The mesh exists once."},
         "narration":
            "Step three, and the forest comes together. [pause] A Tree is now tiny. It holds its "
            "position — its extrinsic state — and a pointer to a shared TreeType. That is all. "
            "Two integers and a reference. [pause] To plant a million trees, you loop a million "
            "times, each time making a small Tree and pointing it at a shared type from the "
            "factory. [pause] The million Tree objects are featherweight. And behind them all "
            "sit just three heavy TreeType objects, referenced again and again. [pause] The mesh "
            "that used to exist a million times now exists exactly three."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Fit a 5,000,000-tree forest in memory\"",
            "naiveLabel": "Fused", "naiveCost": "Mesh copied into every tree.",
            "naiveSteps": ["5M × ~4 MB each", "≈ 20 TB — impossible",
                           "memory scales with COUNT"],
            "patLabel": "Flyweight", "patCost": "3 shared types + 5M tiny trees.",
            "patFile": "the math",
            "patLines": ln(
                ("3 TreeTypes  × ~4 MB   = 12 MB   (shared)", "add"),
                ("5,000,000 Trees × ~16 B = 80 MB   (positions)", "add"),
                ("// total ≈ 92 MB, not 20 TB", "add"),
                ("// memory scales with SPECIES, not tree count", "add"))},
         "narration":
            "Now the requirement that was flatly impossible. Fit a five-million-tree forest in "
            "memory. [pause] Fused, that was five million times four megabytes — twenty "
            "terabytes. It could never load. [pause] With flyweights, do the math. Three shared "
            "tree types, at four megabytes each, is twelve megabytes total. Five million trees, "
            "at sixteen bytes of position each, is eighty megabytes. [pause] The whole forest "
            "fits in about ninety megabytes, instead of twenty terabytes. [pause] And here is "
            "the deep shift: memory no longer scales with the number of trees. It scales with "
            "the number of species. You could plant fifty million for barely more. The count "
            "became almost free."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Flyweight Pattern",
            "plain": "Split shared intrinsic state from unique extrinsic state; store the "
                     "intrinsic part once and reference it from every object.",
            "nodes": [
                {"id": "fly", "title": "TreeType", "stereo": "flyweight",
                 "members": ["- mesh, texture", "(shared intrinsic)"],
                 "x": 740, "y": 360, "w": 440, "color": "#22D3EE"},
                {"id": "fac", "title": "TreeFactory", "stereo": "factory",
                 "members": ["- pool: Map", "+ get(species)"],
                 "x": 150, "y": 360, "w": 380, "color": "#8B93B0"},
                {"id": "ctx", "title": "Tree", "stereo": "context",
                 "members": ["- x, y (extrinsic)", "→ shared TreeType"],
                 "x": 1400, "y": 360, "w": 380, "color": "#A78BFA"}],
            "edges": [
                {"from": "fac", "to": "fly", "kind": "has"},
                {"from": "ctx", "to": "fly", "kind": "has"}]},
         "narration":
            "This is the Flyweight pattern. [pause] In the center, the flyweight itself — the "
            "TreeType — holding the heavy intrinsic state that is shared by many objects. "
            "[pause] On the left, the factory, which keeps a pool and guarantees that each "
            "flyweight is created only once and then shared. [pause] On the right, the context — "
            "the Tree — which holds only the extrinsic state, its position, plus a reference to "
            "a shared flyweight. [pause] Both arrows point at the flyweight in the middle: the "
            "factory pools it, the millions of contexts reference it. [pause] One heavy object "
            "in the center, pointed to from everywhere. That is how a million objects cost "
            "almost nothing."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "Flyweight", "your": "TreeType (intrinsic: mesh…)"},
                {"role": "FlyweightFactory", "your": "TreeFactory (the shared pool)"},
                {"role": "Extrinsic state", "your": "Tree's x, y — passed or stored"},
                {"role": "Client", "your": "Forest — a million Trees"}],
            "plain": "The factory shares immutable flyweights; each context supplies the "
                     "extrinsic state the flyweight needs.",
            "gof": "Use sharing to support large numbers of fine-grained objects efficiently."},
         "narration":
            "The names, mapped to your code. [pause] The Flyweight is the TreeType, carrying the "
            "intrinsic, shared state. [pause] The FlyweightFactory is the TreeFactory, which "
            "owns the pool and enforces sharing. [pause] The extrinsic state is each tree's "
            "position — the part that varies, kept in the context or passed in at draw time. "
            "[pause] And the Client is the forest full of trees. [pause] The Gang of Four, and "
            "it is refreshingly short: use sharing to support large numbers of fine-grained "
            "objects efficiently. The entire pattern is that one word — sharing — applied to the "
            "heavy, identical parts."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "Only pays at massive scale",
            "costs": ["Splitting intrinsic vs extrinsic adds complexity",
                      "Flyweights must be immutable and shared",
                      "Extrinsic state must live elsewhere"],
            "dont": ["You don't have that many objects",
                     "Little state is actually shared",
                     "The objects are already small"],
            "signal": "you have a huge number of objects and most of each object's memory is "
                      "identical across them."},
         "narration":
            "Flyweight only earns its complexity at scale. [pause] You have to carefully split "
            "each object's state into intrinsic and extrinsic — what can be shared, and what "
            "cannot — and that split is not always obvious. [pause] The flyweights must be "
            "immutable, since they are shared; and the extrinsic state has to live somewhere "
            "else, either in a context object or passed in on every call, which complicates the "
            "code. [pause] So skip it entirely when you simply do not have that many objects, "
            "when little of their state is actually shared, or when the objects are already "
            "small. [pause] Reach for it when you have a truly huge number of objects, and most "
            "of each object's memory is identical to all the others. Then, and only then, "
            "sharing turns the impossible into the trivial."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Flyweight, in one breath",
            "items": [
                "Storing heavy, identical data in every one of millions of objects multiplied "
                "it into terabytes.",
                "Most of that state is shared — so split intrinsic (shared) from extrinsic "
                "(unique), and store the shared part once.",
                "Flyweight: a factory shares one immutable object across millions of contexts. "
                "Memory scales with species, not count."],
            "challenge": "A text editor renders a document of millions of characters — each "
                         "glyph shares a font, but each has a position and color.",
            "question": "Does Flyweight fit? What's intrinsic, what's extrinsic, and what does "
                        "the factory share?"},
         "narration":
            "Flyweight, in one breath. [pause] Storing heavy, identical data inside every one of "
            "millions of objects multiplied it into terabytes that could never fit. [pause] But "
            "most of that state is shared — so you split intrinsic, the shared part, from "
            "extrinsic, the unique part, and store the shared part exactly once. [pause] "
            "Flyweight: a factory shares one immutable object across millions of contexts, so "
            "memory scales with the number of distinct kinds, not the number of objects. [pause] "
            "Here is one to carry out. [pause] A text editor renders a document of millions of "
            "characters — each glyph shares a font and shape, but each character has its own "
            "position and color. [pause] Does Flyweight fit? What is intrinsic, what is "
            "extrinsic, and what exactly should the factory share? [pause] Pause, and sketch it "
            "before the final episode."},
    ],
}


INTERPRETER = {
    "id": "dp23-interpreter",
    "title": "Interpreter",
    "segments": [

        {"id": "title", "variant": "dp_title", "props": {
            "kicker": "DESIGN PATTERNS · IN JAVA", "ep": "EPISODE 23",
            "line1": "A language", "line2": "made of objects",
            "sub": "turn a little grammar into a tree of classes that evaluates itself"},
         "narration":
            "This is the twenty-third and final pattern — and a fitting one, because it is the "
            "others, combined into a language. [pause] You keep receiving little rules as text. "
            "A discount applies if amount is over a thousand and country is US. An alert fires if "
            "CPU is over ninety. [pause] These rules change constantly, and the people who write "
            "them are not always programmers. [pause] There is a way to turn a small language "
            "like that into objects that evaluate themselves. Let's build a rule engine."},

        {"id": "scenario", "variant": "dp_scenario", "props": {
            "kicker": "THE SCENARIO", "title": "Evaluating business rules",
            "situation": "Rules arrive as text — 'amount > 1000 AND country == US' — they change "
                         "often, non-programmers author them, and you must evaluate each against "
                         "live data.",
            "actors": [
                {"emoji": "📜", "label": "Rules as text"},
                {"emoji": "🔀", "label": "AND / OR / compare"},
                {"emoji": "✅", "label": "…evaluated on data"}],
            "ask": "How do you evaluate an evolving little rule language against real data?"},
         "narration":
            "Here is the problem: business rules, arriving as text. [pause] A discount rule — "
            "amount greater than a thousand, and country equals US. An alert rule — CPU greater "
            "than ninety, or memory greater than eighty. [pause] These rules are a tiny "
            "language, with values, comparisons, and the words AND and OR. [pause] They change "
            "all the time, and often the people writing them are analysts, not engineers. "
            "[pause] So how do you take an evolving little language like this, and evaluate its "
            "sentences against your live data — cleanly enough that adding a new kind of rule "
            "does not mean rewriting everything?"},

        {"id": "naive", "variant": "dp_code", "props": {
            "kicker": "THE OBVIOUS FIRST ATTEMPT", "title": "One giant evaluate() function.",
            "file": "RuleEngine.java",
            "lines": ln(
                "boolean evaluate(String rule, Data d) {",
                ('  String[] parts = rule.split(" ");   // fragile!', "hi"),
                ('  if (parts[1].equals(">"))', "hi"),
                "    return d.get(parts[0]) > num(parts[2]);",
                ('  else if (parts[1].equals("=="))', "hi"),
                ('    ... // AND, OR, parens? all tangled in here', "hi"),
                "}"),
            "note": "Parsing and evaluating, tangled in one function. Nesting? Good luck."},
         "narration":
            "The obvious approach: one function that takes the rule string and evaluates it. "
            "[pause] Split the text on spaces, look at the operator, and branch — if it is "
            "greater-than, compare these two; if it is equals, compare those. [pause] It limps "
            "along for the simplest rules. [pause] But the moment you need AND, or OR, or "
            "parentheses to group things, this function becomes a nightmare. Parsing the text "
            "and evaluating the logic are hopelessly tangled together in one place. [pause] And "
            "every new operator you support means another branch bolted onto an already fragile, "
            "ever-growing monolith."},

        {"id": "pain", "variant": "dp_pain", "props": {
            "title": "\"Support OR, parentheses, and a BETWEEN operator.\"",
            "file": "monolith.java",
            "lines": ln(
                ("boolean evaluate(String rule, Data d) {", "hi"),
                ("  // handle >, ==, !=, <, AND, OR, NOT, (), BETWEEN, IN...", "hi"),
                ("  // ...500 lines of string-parsing and branching", "hi"),
                ("  // nested rules? re-parse substrings by hand", "hi"),
                "}   // one bug here breaks EVERY rule"),
            "smell": "Grammar + parsing + evaluation fused in one function",
            "touched": ["new operator → edit the monolith",
                        "nesting handled by ad-hoc string surgery",
                        "can't compose or reuse sub-rules",
                        "one function owns the whole language"]},
         "narration":
            "Then the language grows, as languages do. Support OR. Support parentheses for "
            "grouping. Add a BETWEEN operator, an IN operator, negation. [pause] Every one of "
            "them piles into the same function, until it is five hundred lines of string surgery "
            "and nested branching. [pause] Nesting — a rule inside a rule — is handled by "
            "re-parsing substrings by hand, which is exactly as error-prone as it sounds. "
            "[pause] The grammar, the parsing, and the evaluation are fused into one monolith. "
            "[pause] And a single bug anywhere in it can break every rule in the system at once. "
            "The language has no structure, so neither does the code."},

        {"id": "insight", "variant": "dp_insight", "props": {
            "title": "What is actually changing here?",
            "fixed": ["A rule is a tree of sub-expressions",
                      "Each sub-expression evaluates to a value",
                      "Against the same shared context (data)"],
            "varies": ["The kinds of operator and terminal",
                       "And new ones keep being added"],
            "principle": "Make each grammar rule a CLASS with interpret(context); compose them "
                         "into a tree."},
         "narration":
            "What is fixed, and what varies? [pause] Fixed: a rule, however complex, is really a "
            "tree. Amount-greater-than-a-thousand AND country-equals-US is an AND node, with two "
            "comparison nodes under it. Each node evaluates to a value, against the same shared "
            "data — the context. [pause] What varies is the kinds of node — the operators and "
            "the terminals — and new ones keep arriving. [pause] Here is the move. [pause] Give "
            "the language a structure by giving each grammar rule its own class, with one "
            "method: interpret, which evaluates it against the context. Then compose those "
            "classes into a tree that mirrors the rule. The tree interprets itself."},

        {"id": "analogy", "variant": "dp_analogy", "props": {
            "title": "Reading a formula", "emoji": "🧮",
            "analogy": "To evaluate 3 + 4 × 2 you don't read left to right — you build a tree "
                       "and let each operation ask its parts.",
            "map": [
                {"from": "Each number", "to": "a terminal expression"},
                {"from": "Each operator (+, ×)", "to": "a nonterminal expression"},
                {"from": "\"Ask my two parts\"", "to": "interpret() on children"},
                {"from": "The whole formula", "to": "the expression tree"}],
            "breaks": "you evaluate a formula in your head; here the tree is real objects you "
                      "can inspect, reuse, and extend."},
         "narration":
            "Think about how you actually evaluate a formula like three plus four times two. "
            "[pause] You do not read it strictly left to right. You understand its structure — "
            "the multiply binds tighter, so it sits below the plus — and you evaluate the tree "
            "from the bottom up. Four times two is eight; three plus eight is eleven. [pause] "
            "Each number is a terminal — a leaf. Each operator is a node that asks its two parts "
            "for their values, then combines them. [pause] The numbers are terminal expressions. "
            "The operators are nonterminal expressions. Asking your parts for their values is "
            "calling interpret on the children. And the whole formula is the expression tree. "
            "[pause] The difference from doing it in your head: here the tree is made of real "
            "objects, which you can inspect, reuse, and extend."},

        {"id": "refactor1", "variant": "dp_refactor", "props": {
            "step": 1, "of": 3, "move": "Every grammar rule becomes a class",
            "file": "Expression.java",
            "lines": ln(
                ("interface Expression {                 // one grammar rule", "add"),
                ("  boolean interpret(Context ctx);", "add"),
                ("}", "add"),
                ("class Var implements Expression {      // a terminal", "hi"),
                "  String name;",
                ("  public boolean interpret(Context c){ return c.flag(name); }", "hi"),
                "}"),
            "note": "Each element of the language — value, comparison, AND — is its own class."},
         "narration":
            "The refactor, step one. [pause] Define an Expression interface with a single method "
            "— interpret — that evaluates the expression against a context and returns a result. "
            "[pause] Then every element of the language becomes a class that implements it. "
            "[pause] Here is a terminal — a variable — the simplest kind. It just looks its name "
            "up in the context. [pause] A terminal is a leaf: it interprets itself directly, "
            "with no sub-parts. The comparisons and the AND-s and OR-s will be the branches."},

        {"id": "refactor2", "variant": "dp_refactor", "props": {
            "step": 2, "of": 3, "move": "Nonterminals hold and combine sub-expressions",
            "file": "And.java",
            "lines": ln(
                ("class And implements Expression {      // a nonterminal", "hi"),
                ("  Expression left, right;              // two sub-rules", "hi"),
                "  public boolean interpret(Context c) {",
                ("    return left.interpret(c) && right.interpret(c);", "hi"),
                "  }                                    // ...asks its parts",
                "}"),
            "note": "A nonterminal holds sub-expressions and combines them. That's the recursion."},
         "narration":
            "Step two: the nonterminals — the operators. [pause] An AND expression holds two "
            "sub-expressions, a left and a right. [pause] And its interpret is beautifully "
            "simple: interpret the left, interpret the right, and combine them with a logical "
            "and. [pause] Notice it does not know or care what its two parts are. They might be "
            "comparisons, or other AND-s, or deeply nested rules. It just asks each to interpret "
            "itself, and combines the answers. [pause] That is the recursion. A nonterminal "
            "holds expressions, and is itself an expression — the very same self-reference you "
            "saw in Composite, now applied to a grammar."},

        {"id": "try", "variant": "dp_try", "props": {
            "title": "Write GreaterThan.interpret()",
            "file": "GreaterThan.java",
            "lines": ln(
                "class GreaterThan implements Expression {",
                "  Expression var; int threshold;",
                "  public boolean interpret(Context c) {",
                ("    // ▯ is the variable's value above the threshold?", "ghost"),
                "  }",
                "}"),
            "prompt": "Evaluate the variable against the context, then compare it to the "
                      "threshold.",
            "hint": "return c.value(var) > threshold;"},
         "narration":
            "Your turn — pause here. [pause] Write interpret for a greater-than expression. "
            "[pause] It holds a variable and a threshold — say, amount, and a thousand. [pause] "
            "Evaluate the variable against the context to get its actual value, then return "
            "whether that value is above the threshold. [pause] One line. And with terminals "
            "like this and combiners like AND, you already have enough to express, and evaluate, "
            "arbitrarily complex rules."},

        {"id": "refactor3", "variant": "dp_refactor", "props": {
            "step": 3, "of": 3, "move": "Build the tree; interpret walks it",
            "file": "app.java",
            "lines": ln(
                '// amount > 1000 AND country == "US"',
                ("Expression rule =", "add"),
                ("  new And(new GreaterThan(amount, 1000),", "add"),
                ('          new Equals(country, "US"));', "add"),
                ("boolean ok = rule.interpret(context);   // walks the tree", "hi")),
            "note": "The rule is now a tree of objects. Interpreting it is one recursive call."},
         "narration":
            "Step three, and the language comes alive. [pause] The rule amount greater than a "
            "thousand AND country equals US becomes a tree of objects — an AND node holding a "
            "greater-than and an equals. [pause] You built it by nesting constructors, but a "
            "small parser could build the very same tree from the text. [pause] And to evaluate "
            "it against your data? One call — interpret on the root. [pause] The AND asks its "
            "two children; each comparison asks the context for a value and compares. The answer "
            "flows back up the tree. The rule evaluates itself, no monolith in sight."},

        {"id": "payoff", "variant": "dp_payoff", "props": {
            "requirement": "\"Add an OR operator. And BETWEEN.\"",
            "naiveLabel": "Monolith", "naiveCost": "New branches in the 500-line function.",
            "naiveSteps": ["edit the one evaluate()", "risk breaking every rule",
                           "re-test the whole language"],
            "patLabel": "Interpreter", "patCost": "One new class per operator. Nothing else.",
            "patFile": "Or.java",
            "patLines": ln(
                ("class Or implements Expression {", "add"),
                ("  Expression left, right;", "add"),
                ("  public boolean interpret(Context c) {", "add"),
                ("    return left.interpret(c) || right.interpret(c);", "add"),
                ("  }", "add"),
                ("}   // plugs into any tree — others untouched", "add"))},
         "narration":
            "Now the change that used to endanger everything. Add an OR operator. Then a "
            "BETWEEN. [pause] In the monolith, each meant new branches threaded into the "
            "five-hundred-line function — with the risk of breaking every existing rule, and a "
            "full re-test of the whole language. [pause] With the interpreter, an OR is one new "
            "class. Hold two sub-expressions, combine them with a logical or. [pause] That is "
            "the entire change. [pause] It plugs into any expression tree, composes with "
            "everything already there, and not one existing rule class is touched. The language "
            "grows one small, safe class at a time."},

        {"id": "reveal", "variant": "dp_reveal", "props": {
            "name": "The Interpreter Pattern",
            "plain": "Represent each rule of a grammar as a class with interpret(); compose them "
                     "into a tree that evaluates a sentence against a context.",
            "nodes": [
                {"id": "expr", "title": "Expression", "stereo": "abstract",
                 "members": ["+ interpret(ctx)"], "x": 760, "y": 210, "w": 400,
                 "color": "#22D3EE"},
                {"id": "var", "title": "Variable", "stereo": "terminal",
                 "members": ["reads context"], "x": 120, "y": 470, "w": 320,
                 "color": "#8B93B0"},
                {"id": "gt", "title": "GreaterThan", "stereo": "nonterminal",
                 "members": ["- var, threshold"], "x": 640, "y": 470, "w": 340,
                 "color": "#8B93B0"},
                {"id": "and", "title": "And", "stereo": "nonterminal",
                 "members": ["- left, right", "+ interpret()"], "x": 1360, "y": 470, "w": 380,
                 "color": "#A78BFA"}],
            "edges": [
                {"from": "var", "to": "expr", "kind": "impl"},
                {"from": "gt", "to": "expr", "kind": "impl"},
                {"from": "and", "to": "expr", "kind": "impl"},
                {"from": "and", "to": "expr", "kind": "has"}]},
         "narration":
            "This is the Interpreter pattern — and notice its shape: it is Composite, wearing "
            "the clothes of a grammar. [pause] At the top, the Expression interface, with its "
            "interpret method. [pause] The terminals, like a Variable, are the leaves — they "
            "interpret themselves directly from the context. [pause] The nonterminals, like "
            "greater-than and AND, are the branches — and look at AND's second arrow. It is an "
            "expression, and it holds expressions. [pause] That self-reference lets rules nest "
            "to any depth. [pause] To evaluate a whole rule, you call interpret on the root, and "
            "the tree walks itself, each node asking its children, until an answer flows back to "
            "the top."},

        {"id": "map", "variant": "dp_map", "props": {
            "title": "The names, mapped to your code",
            "participants": [
                {"role": "AbstractExpression", "your": "interface Expression (interpret)"},
                {"role": "TerminalExpression", "your": "Variable, Literal"},
                {"role": "NonterminalExpression", "your": "And, Or, GreaterThan"},
                {"role": "Context", "your": "the data a rule evaluates against"}],
            "plain": "Terminals interpret directly; nonterminals interpret their children and "
                     "combine — the tree evaluates a sentence.",
            "gof": "Given a language, define a representation for its grammar along with an "
                   "interpreter that uses the representation to interpret sentences in the "
                   "language."},
         "narration":
            "The names, mapped to your code. [pause] The AbstractExpression is the Expression "
            "interface, with interpret. [pause] The TerminalExpressions are the leaves — "
            "variables and literals. [pause] The NonterminalExpressions are the operators — AND, "
            "OR, greater-than — which hold and combine sub-expressions. [pause] And the Context "
            "is the data each rule is evaluated against. [pause] The Gang of Four: given a "
            "language, define a representation for its grammar, along with an interpreter that "
            "uses the representation to interpret sentences in the language. [pause] It is the "
            "pattern that turns a little language into an object tree."},

        {"id": "tradeoffs", "variant": "dp_tradeoffs", "props": {
            "title": "For small languages only",
            "costs": ["One class per grammar rule — they multiply",
                      "A complex grammar becomes unwieldy fast",
                      "Not built for speed or big inputs"],
            "dont": ["The grammar is large or complex",
                     "You need real parsing + performance",
                     "A library or DSL already exists"],
            "signal": "a simple, stable little language you evaluate often, and you keep bolting "
                      "operators onto one big function."},
         "narration":
            "Interpreter has a narrow home, and it is important to respect its edges. [pause] "
            "Every rule of the grammar becomes a class — so a small language is elegant, but a "
            "rich one explodes into dozens of classes and becomes genuinely hard to manage. "
            "[pause] It is also not built for performance, or for large inputs. [pause] So the "
            "honest guidance: for anything beyond a simple grammar, do not hand-roll this. Reach "
            "for a real parser generator, or an existing expression library, which handle the "
            "hard parts for you. [pause] Reach for Interpreter itself only when you have a "
            "simple, stable little language that you evaluate often — and you notice yourself "
            "bolting operator after operator onto one ever-growing function. That growing "
            "function is a grammar, asking to become a tree."},

        {"id": "recap", "variant": "dp_recap", "props": {
            "title": "Interpreter, in one breath",
            "items": [
                "One giant evaluate() function fused grammar, parsing, and logic — fragile, and "
                "a nightmare to extend.",
                "A rule is really a tree of sub-expressions — so give each grammar rule a class "
                "with interpret(), and compose them.",
                "Interpreter: terminals interpret directly, nonterminals interpret their "
                "children. Composite over a grammar. New operator, one class."],
            "challenge": "A search box supports a mini-query language: field:value, quoted "
                         "phrases, AND / OR / NOT, and parentheses.",
            "question": "Does Interpreter fit — or has the grammar grown big enough that a real "
                        "parser is the wiser call?"},
         "narration":
            "Interpreter, in one breath — and with it, all twenty-three patterns. [pause] A "
            "single giant evaluate function fused the grammar, the parsing, and the logic into "
            "one fragile monolith that was a nightmare to extend. [pause] But a rule is really a "
            "tree of sub-expressions — so you give each grammar rule its own class with an "
            "interpret method, and compose them into that tree. [pause] Interpreter: terminals "
            "interpret themselves directly, nonterminals interpret their children and combine — "
            "it is Composite, applied to a grammar. A new operator is one new class. [pause] "
            "Here is a last one to carry out. [pause] A search box supports a mini-query "
            "language — field-colon-value, quoted phrases, AND, OR, NOT, and parentheses. "
            "[pause] Does Interpreter fit here — or has the grammar grown just big enough that a "
            "real parser is the wiser call? [pause] That judgment — knowing when a pattern fits, "
            "and when it does not — is what all twenty-three of these were really about. Thanks "
            "for building them with me."},
    ],
}


# --- registry: order = the course order (each renders to its own MP4) ---------------
PATTERNS = [
    STRATEGY,
    OBSERVER,
    DECORATOR,
    FACTORY_METHOD,
    COMMAND,
    ADAPTER,
    STATE,
    TEMPLATE_METHOD,
    COMPOSITE,
    BUILDER,
    SINGLETON,
    PROXY,
    FACADE,
    ITERATOR,
    CHAIN,
    BRIDGE,
    MEDIATOR,
    ABSTRACT_FACTORY,
    MEMENTO,
    VISITOR,
    PROTOTYPE,
    FLYWEIGHT,
    INTERPRETER,
]
