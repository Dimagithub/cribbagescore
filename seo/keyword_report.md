# Cribbage Scorekeeper (cribbagescoring.com): keyword map by funnel stage
Prepared 2026-10-27. Country/language: US/en. Seeds: 16 head terms + 12 custom seeds = 171 autocomplete queries.

## Sources of demand data (no invented volumes)
- Google autocomplete (hl=en, gl=us): 171 seed queries, 405 local suggestions (319 unique keywords). Raw: `raw_autocomplete.csv`, classified: `keyword_map.csv`.
- Google Trends relative interest (US, past 12 months, anchor "cribbage rules", mean index 35.3): `trends.json`. Missing: none. Ratios are only comparable inside this table.
- Competition: one web search per P1/P2 theme on 2026-10-27 (5 searches, summarized below). Not a rank-tracker; it shows what kind of page appears.
- Existing pages: the site is one URL (`/`) with no sitemap, so the crawler gap check found 0 pages; its "319 missing" result was meaningless and is not kept. Coverage below was judged by hand from `index.html`.

Demand labels: High = 8+ local autocomplete variants; Med = 3-7; Low = 1-2. **Caution:** autocomplete caps at about 10 suggestions per seed, so High is saturated and does not rank terms against each other. Use Trends for that.

## Summary
### What the data says
1. **Rules and scoring questions have far more interest than app queries.** Relative to "cribbage rules" (1.00): "cribbage points" 0.62, "how to play cribbage" 0.55, "cribbage scoring" 0.28, "cribbage skunk" 0.10, "cribbage app" 0.08. Every other app/score-keeper phrase rounds to 0.00-0.01 (below Trends' reporting floor, so small but not zero).
2. **App queries are dominated by App Store listings** (Cribbage Pegboard Tracker, Cribtastic, Cribbage Go, CribCount, Cribbage Pro). None of the results was a free web-based scorekeeper. Phrases with "online", "no download", "free", "no ads", "offline" are where a web app fits and an App Store listing does not.
3. **Rules queries are weakly served.** Results mix a few real sources (cribbage.org's PDF, cardsjd.com, instructables) with many scraped, garbled "printable cheat sheet" pages on unrelated domains. A clean, accurate scoring page is realistic to rank.
4. **Skunk is a differentiator.** "what is a skunk / double skunk / skunk line in cribbage" is a cluster of High autocomplete variants, and this app already detects skunks and double skunks automatically.

### Top 10 P1 keywords
| # | Keyword | Stage | Target page | Why P1 |
|---|---|---|---|---|
| 1 | cribbage score keeper | Awareness | `/` (retitle) | Exact product match; AC 10 variants |
| 2 | cribbage scoring app | Awareness | `/` | Same intent; AC 10; App Store listings only |
| 3 | cribbage score keeper online / free / no download | Decision | `/` | Web-app advantage over store listings; AC 10 |
| 4 | cribbage app (free, no ads, for iphone/android) | Awareness | `/` + install section | Trends 0.08x, AC 10; the install guide and offline play already exist |
| 5 | cribbage scoring / cribbage scoring rules | Awareness | `/cribbage-scoring` (new) | Trends 0.28x; thin competition |
| 6 | cribbage points | Awareness | `/cribbage-scoring` | Trends 0.62x, the strongest signal in the set |
| 7 | how to play cribbage | Awareness | `/how-to-play-cribbage` (new) | Trends 0.55x; AC 10 |
| 8 | what is a skunk in cribbage / double skunk | Awareness | `/cribbage-scoring#skunk` + FAQ | AC 10 on 8+ variants; app feature |
| 9 | cribbage score tracker / score board | Awareness | `/` | AC 10; matches the app's tabletop scoreboard |
| 10 | highest cribbage hand / 29 points | Awareness | `/cribbage-scoring#hands` | AC 10; quick answer for AI results |

### Where we can win (patterns)
- "Free, no ads, no download, works offline" is the angle no store listing can claim for web use, and all four are true for this app.
- A short, correct scoring reference with a table, a worked example and a source link to the American Cribbage Congress rules can beat the scraped pages.
- Question-form searches ("what is a skunk", "how many points is nibs") suit FAQ entries that AI assistants can quote.

### Trends (relative interest; ratio to "cribbage rules")
| Term | Mean index | Ratio |
|---|---|---|
| cribbage points | 22.0 | 0.62 |
| how to play cribbage | 19.5 | 0.55 |
| cribbage scoring | 10.0 | 0.28 |
| cribbage skunk | 3.6 | 0.10 |
| cribbage app | 3.0 | 0.08 |
| cribbage scoring rules | 0.3 | 0.01 |
| cribbage hand scoring | 0.2 | 0.01 |
| cribbage hand calculator | 0.2 | 0.00 |
| cribbage score keeper / board app | 0.1 | 0.00 |
| cribbage scoring app / counter app / scoreboard / digital cribbage board / score counter | 0.0 | 0.00 |

Reading: the most searched things are the plain rule words ("points", "how to play"). Product-style phrases are small. Do not expect big numbers from the homepage alone; the content pages are what bring traffic that can then find the app.

### New pages to build
| Proposed URL | Type | Keywords it targets | Priority |
|---|---|---|---|
| `/cribbage-scoring` | Reference: hand scoring table, pegging, 29 hand, nibs/heels, skunk lines | cribbage scoring, cribbage points, cribbage scoring rules, highest hand, skunk cluster | P1 |
| `/how-to-play-cribbage` | Guide: deal, crib, play, show, winning | how to play cribbage (+ 2 players, beginners) | P1 |
| `/cribbage-score-sheet` | Printable PDF + link to the app | cribbage score sheet (pdf, free, printable) | P2 |
| `/install` (or a section on `/`) | Install guide for Android/iPhone (already built as an overlay) | cribbage app for iphone/android, free no download | P2 |

### Changes to existing pages
| Page | Change | Keywords |
|---|---|---|
| `/` | Title from "Cribbage" to something like "Cribbage Score Keeper: Free, No Ads, Works Offline"; add a meta description, canonical, Open Graph tags and `SoftwareApplication` structured data; add visible text content (what it does, features, FAQ) instead of only the app UI | cribbage score keeper, scoring app, tracker, free, no ads |
| `/` | Move the Help rules text out of the hidden overlay into crawlable page sections, or link to the new pages | scoring, points, skunk |

### Internal linking
Awareness pages (`/how-to-play-cribbage`, `/cribbage-scoring`) each carry a clear "Open the score keeper" button to `/`; `/` links back to both in a short "Learn the rules" section and the footer. The install guide is linked from `/`.

### Gaps
1. The site is a single URL, so it can target only one intent. Rules and how-to queries (the largest interest) have no page.
2. `<title>` is just "Cribbage"; there is no meta description, canonical, Open Graph, structured data, sitemap or robots.txt.
3. Rules content exists but sits in a hidden in-app overlay, which search engines may discount.
4. Product gaps seen in the data: 3-4 player scoring (competitors advertise it; "how to play with 3/4/6 players" is High), and a hand calculator ("cribbage hand/points calculator", AC 9-10; Trends 0.0-0.00, so low volume).
5. The "play cribbage online" / "online board" cluster is a different product (playing opponents). The app is a scorekeeper, so avoid targeting it and never claim online play.

## Decision (use it now / free / online): 22 keywords
| # | Keyword | Intent | Demand (signal) | Who ranks now | Target page | Status | Pri |
|---|---|---|---|---|---|---|---|
| 1 | cribbage score keeper online | transactional | High (AC 10) | App Store listings | `/` | missing | P1 |
| 2 | cribbage score board online | transactional | High (AC 10) | not checked | `/` | missing | P1 |
| 3 | cribbage score sheet online | transactional | High (AC 10) | not checked | `/cribbage-score-sheet` | missing | P2 |
| 4 | best free cribbage scoring calculator online | transactional | High (AC 10) | generic calculator pages | `/` + calculator idea | missing | P3 (product gap) |
| 5 | cribbage board online free (no download, virtual) | transactional | High (AC 10) | online games | none | skip | P3 (different intent: playing online) |
| 6 | can you play cribbage online (with a friend) | transactional | High (AC 9-10) | online games | none | skip | P3 |
| 7 | best cribbage board to buy | transactional | High (AC 10) | retailers | none | skip | P3 (physical boards) |

(The full list of 22 is in `keyword_map.csv`, filter stage = Decision.)

## Consideration (comparisons, best-of): 46 keywords
| # | Keyword | Intent | Demand (signal) | Who ranks now | Target page | Status | Pri |
|---|---|---|---|---|---|---|---|
| 1 | best cribbage app (iphone, android, no ads, free, for beginners) | comparison | High (AC 10) | App Store listings | `/` (feature-led section, no "best" claim) | missing | P2 |
| 2 | best cribbage scoring app | comparison | Med (AC 6) | App Store listings | `/` | missing | P2 |
| 3 | best cribbage hand / best scoring hand / 10 best hands | comparison | High (AC 10) | not checked | `/cribbage-scoring#hands` | missing | P2 |
| 4 | cribbage app reviews | comparison | Med (AC 4) | App Store, review sites | none | skip | P3 |
| 5 | best cribbage board (reddit, for adults, design) | comparison | High (AC 10) | retailers | none | skip | P3 (physical boards) |

(Full list in `keyword_map.csv`, stage = Consideration.)

## Awareness (rules, how-to, definitions): 251 keywords
| # | Keyword | Intent | Demand (signal) | Who ranks now | Target page | Status | Pri |
|---|---|---|---|---|---|---|---|
| 1 | cribbage score keeper / scoring app / tracker / counter app | informational | High (AC 10; Trends ~0.0x) | App Store listings | `/` | partial (app exists, page not targeted) | P1 |
| 2 | cribbage points | informational | High (Trends 0.62x) | not checked | `/cribbage-scoring` | missing | P1 |
| 3 | how to play cribbage (2/3/4 players, beginners, video) | informational | High (Trends 0.55x; AC 10) | cribbage.org PDF, cardsjd, instructables, scraped pages | `/how-to-play-cribbage` | partial (rules in hidden overlay) | P1 |
| 4 | cribbage scoring / how does cribbage scoring work / how to count hands | informational | High (Trends 0.28x) | scraped cheat-sheet pages | `/cribbage-scoring` | partial (overlay) | P1 |
| 5 | skunk, double skunk, skunk line, getting skunked | informational | High (Trends 0.10x; AC 10) | not checked | `/cribbage-scoring#skunk` | partial (overlay) | P1 |
| 6 | highest cribbage hand / what is 29 / four of a kind points / nibs | informational | High (AC 10) | not checked | `/cribbage-scoring#hands` | partial (overlay) | P1 |
| 7 | cribbage score sheet (pdf, free, printable) | informational | High (AC 10) | scraped printable pages | `/cribbage-score-sheet` | missing | P2 |
| 8 | cribbage points / hand calculator (app, free) | informational | High (AC 9-10; Trends 0.0x) | generic calculator pages | none (needs a calculator feature) | missing | P3 |

(Noise removed by judgment: "crossword clue", "nyt", "crib appliance", "tongue crib", "crib point postcode" are unrelated to the game.)

## GEO notes
- Question keywords to turn into FAQ entries with short, sourced answers and `FAQPage` markup: what is a skunk / double skunk / skunk line; what is the highest hand in cribbage (29); how many points is nibs / his heels; who gets the go point; how many points to win (121, or 61 for a short game); what is the most pegging points; how do you keep score in cribbage.
- Link rules claims to the American Cribbage Congress rules (cribbage.org) as the authority, since many competing pages contain wrong values (one search result claimed aces can count 11).
- Add a short "key facts" block to the homepage (free, no ads, no account, works offline, 2 players, 61/121-point games, skunk detection) and an `llms.txt` pointing at the rules pages.
- Check robots.txt allows GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended. There is no robots.txt yet, so by default everything is allowed.

## Method notes
- Autocomplete reflects what people type, not how often; compare topics with Trends. Trends ratios use "cribbage rules" as anchor in each batch.
- Very small Trends values (0.0-0.3) are below the reporting floor and mean "low", not "nothing".
- Re-rank after 4-6 weeks of Search Console impressions.
