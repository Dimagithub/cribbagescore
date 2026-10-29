# SEO log: cribbagescoring.com

Keyword research: `seo/keyword_report.md` (raw data in `seo/`). Production origin: `https://www.cribbagescoring.com` (the bare domain redirects to `www`).

## Search engine accounts
A daily GitHub Action (`.github/workflows/search-engines.yml`, script `tools/search_engines.py`) resubmits the sitemap to Google and Bing, submits URLs to Bing, inspects the key pages listed in `.github/search-engines-pages.txt` in Google, and opens one issue "Search engine problems" when something is broken (it closes the issue on the next clean run). Until the secrets below exist, each engine is skipped and the run passes.

The owner does these steps in their own browser (they need the owner's Google and Microsoft logins). Never paste a key or the JSON into chat; secrets go straight into GitHub.

### Google (about 5 minutes the first time; a second site needs only steps 6 and 5)
1. console.cloud.google.com, project picker, **New project** (e.g. `devcom-seo`), Create.
2. APIs & Services, Library, **Google Search Console API**, **Enable**.
3. IAM & Admin, Service accounts, **Create service account** `search-console`, Done (no roles needed).
4. Open it, Keys, Add key, Create new key, **JSON** (a file downloads).
5. Add the file contents as GitHub secret `GSC_SERVICE_ACCOUNT_JSON`, then delete the file.
6. Search Console: add the property (**Domain** `cribbagescoring.com`, verified with a DNS TXT record), submit `https://www.cribbagescoring.com/sitemap.xml` once under Indexing, Sitemaps, then Settings, Users and permissions, **Add user**: the service account email (`...iam.gserviceaccount.com`), permission **Full**.

### Bing (about 2 minutes)
1. bing.com/webmasters, sign in, **Add site**, **Import from Google Search Console**, tick the site, Import.
2. First time only: Settings (gear), **API access**, API Key, **Generate**. The key works for every site in that Bing account.
3. Add it as GitHub secret `BING_API_KEY`.

### GitHub secrets
Repo, Settings, **Secrets and variables**, Actions, **Secrets** tab, New repository secret. Not "Variables", not "Environments", not Codespaces or Dependabot secrets.

After setup, run the "Search engines" workflow by hand (Actions tab, Run workflow) and read the "Check Google and Bing" step. A first failed run during setup opens the issue and it closes itself on the next clean run. "Request indexing" in Search Console stays manual: Google's Indexing API is only allowed for job postings and livestreams.

## Changes
- 2026-10-27: keyword research (`seo/`), added `sitemap.xml`, `robots.txt`, the daily search-engines check and this file.
- 2026-10-27: on-page SEO. Removed the `noindex, nofollow` robots meta tags from `index.html` (present since the first commit; they blocked all search engines). New title, meta description, canonical, Open Graph tags and `SoftwareApplication` JSON-LD for `/`. New static pages `/cribbage-scoring` and `/how-to-play-cribbage` (with FAQPage JSON-LD), linked from the splash, the Help overlay and each other; added to the sitemap and the key-pages list. `vercel.json` gets `cleanUrls`. Service worker: page loads are network-first (rules pages cached under their own URL). Fixed the New Game form covering the splash for first-time visitors.
- 2026-10-27: content round. Homepage splash now scrolls to a crawlable "About" section (features, install tips, links, 7-question FAQ with FAQPage JSON-LD; taps inside it no longer start the game). New `/cribbage-score-sheet` page plus `cribbage-score-sheet.pdf`, `llms.txt`, cross-links between all pages, sitemap and key-pages list updated, service worker cache v16.
- 2026-10-27: added the "web version free and ad-free forever" promise to the homepage About section and FAQ (with matching FAQPage JSON-LD) and llms.txt; service worker cache v17.
- 2026-10-28: free Score Helper (card-picker hand and crib calculator with step-by-step explanation) added to the app: toolbar button, splash link, New Game screen link, Help section, `/#helper` deep link, About feature and FAQ (with FAQPage JSON-LD), llms.txt; service worker cache v18. The premium/photo version is for the future mobile app.
