#!/usr/bin/env python3
"""Daily Google Search Console and Bing Webmaster check (GitHub Action "Search engines"; skill devcom-seo-webmaster).
Usage: python3 tools/search_engines.py --base https://example.com [--pages .github/search-engines-pages.txt] [--sitemap URL] [--problems problems.md]
--pages: one path per line (# comments) to inspect in Google, most important first, at most 20; default = first 20 sitemap URLs.
Google (secret GSC_SERVICE_ACCOUNT_JSON: a service account added in Search Console as a Full user; needs google-auth, requests):
  resubmits the sitemap and reads its status, inspects the key pages,
  reports clicks and top queries for the last 28 days. Problems: sitemap errors, robots or noindex blocks, failed fetches,
  Google picking another canonical, soft 404s.
Bing (secret BING_API_KEY): resubmits the sitemap, submits a slice of the sitemap's URLs within the daily quota
(a different slice each day, so every URL is submitted over time), and lists crawl issues.
Without a secret that part is skipped. Prints a Markdown summary (also to $GITHUB_STEP_SUMMARY); problems go to --problems."""
import os, sys, re, json, math, html, datetime, urllib.request, urllib.parse, urllib.error
arg = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
B = (arg('--base') or os.environ.get('SITE_URL') or sys.exit('Pass --base https://example.com (or set SITE_URL).')).rstrip('/'); HOST = B.split('//')[1]
SITEMAP = arg('--sitemap', B + '/sitemap.xml')
bare = lambda u: re.sub(r'^https?://(www\.)?', '', u).rstrip('/')  # compare sites ignoring scheme, www and trailing slash
summary, problems = [], []

def http(url, data=None, method=None, headers=None):
    body = json.dumps(data).encode() if data is not None else None
    h = {'User-Agent': 'search-engines-check/1', **({'Content-Type': 'application/json; charset=utf-8'} if body else {}), **(headers or {})}
    with urllib.request.urlopen(urllib.request.Request(url, data=body, method=method or ('POST' if body else 'GET'), headers=h), timeout=60) as r:
        t = r.read().decode()
        return json.loads(t) if t.strip() else {}

def sitemap_urls(url=None):
    with urllib.request.urlopen(urllib.request.Request(url or SITEMAP, headers={'User-Agent': 'search-engines-check/1'}), timeout=60) as r:
        x = r.read().decode()
    locs = [html.unescape(u.strip()) for u in re.findall(r'<loc>([^<]+)</loc>', x)]
    return [u for s in locs for u in sitemap_urls(s)] if '<sitemapindex' in x else locs  # a sitemap index lists child sitemaps

def key_pages():
    f = arg('--pages')
    if f and os.path.exists(f):
        return [l.split('#')[0].strip() for l in open(f) if l.split('#')[0].strip()][:20]
    return [u[len(B):] or '/' for u in sitemap_urls() if u.startswith(B)][:20]

# ---------- Google Search Console ----------
def google():
    raw = os.environ.get('GSC_SERVICE_ACCOUNT_JSON', '').strip()
    if not raw: summary.append('**Google:** skipped (secret `GSC_SERVICE_ACCOUNT_JSON` not set; see SEO.md "Search engine accounts").'); return
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request
    info = json.loads(raw)
    cr = service_account.Credentials.from_service_account_info(info, scopes=['https://www.googleapis.com/auth/webmasters'])
    cr.refresh(Request())
    auth = {'Authorization': f'Bearer {cr.token}'}
    g = lambda url, data=None, method=None: http(url, data, method, auth)
    sites = {s['siteUrl']: s['permissionLevel'] for s in g('https://www.googleapis.com/webmasters/v3/sites').get('siteEntry', [])}
    dom = bare(B).split('/')[0].removeprefix('www.')
    site = next((s for s in sites if s == f'sc-domain:{dom}'), None) or next((s for s in sites if bare(s) == bare(B)), None)
    if not site:
        problems.append(f"Google: the service account ({info.get('client_email')}) has no access to {HOST}. In Search Console: Settings → Users and permissions → Add user → that email, permission **Full**.")
        return
    q = urllib.parse.quote(site, safe='')
    api = f'https://www.googleapis.com/webmasters/v3/sites/{q}'
    sm = f"{api}/sitemaps/{urllib.parse.quote(SITEMAP, safe='')}"
    if sites[site] in ('siteOwner', 'siteFullUser'): g(sm, method='PUT')
    else: problems.append(f'Google: the service account is a {sites[site]} user, so it cannot resubmit the sitemap. Change it to **Full** in Search Console → Settings → Users and permissions.')
    s = g(sm)
    sub = sum(int(c.get('submitted', 0)) for c in s.get('contents', []))
    summary.append(f"**Google sitemap:** {sub:,} URLs submitted, last downloaded {s.get('lastDownloaded', 'never')[:10]}, {s.get('errors', 0)} errors, {s.get('warnings', 0)} warnings{' (processing)' if s.get('isPending') else ''}.")
    if int(s.get('errors', 0)): problems.append(f"Google: the sitemap has {s['errors']} errors (Search Console → Indexing → Sitemaps).")
    rows, known = [], 0
    for p in key_pages():
        try: r = g('https://searchconsole.googleapis.com/v1/urlInspection/index:inspect', {'inspectionUrl': B + p, 'siteUrl': site})['inspectionResult']['indexStatusResult']
        except urllib.error.HTTPError as e: problems.append(f'Google: inspecting {p} failed (HTTP {e.code}).'); continue
        cov, fetch, idx, rob = r.get('coverageState', ''), r.get('pageFetchState', ''), r.get('indexingState', ''), r.get('robotsTxtState', '')
        gc, uc = r.get('googleCanonical'), r.get('userCanonical')
        rows.append(f"| `{p}` | {r.get('verdict', '')} | {cov} | {(r.get('lastCrawlTime') or '')[:10] or 'not crawled'} |")
        known += r.get('verdict') == 'PASS'
        bad = []
        if rob == 'DISALLOWED': bad.append('blocked by robots.txt')
        if idx.startswith('BLOCKED'): bad.append(idx.lower().replace('_', ' '))
        if fetch and fetch not in ('SUCCESSFUL', 'PAGE_FETCH_STATE_UNSPECIFIED'): bad.append(f"fetch {fetch.lower().replace('_', ' ')}")
        if gc and uc and gc != uc: bad.append(f'Google chose another canonical: {gc}')
        if re.search(r'soft 404|duplicate|server error|redirect error', cov, re.I): bad.append(cov)
        if bad: problems.append(f"Google: `{p}`: {'; '.join(bad)}.")
    summary.append(f'**Google index, key pages:** {known} of {len(rows)} indexed.\n\n| Page | Verdict | Coverage | Last crawl |\n|---|---|---|---|\n' + '\n'.join(rows))
    end = datetime.date.today() - datetime.timedelta(days=3); start = end - datetime.timedelta(days=27)
    sa = lambda dims, n: g(f'{api}/searchAnalytics/query', {'startDate': str(start), 'endDate': str(end), 'dimensions': dims, 'rowLimit': n}).get('rows', [])
    tot = sa([], 1)
    t = tot[0] if tot else {'clicks': 0, 'impressions': 0}
    top = sa(['query'], 10)
    summary.append(f"**Google search, {start} to {end}:** {int(t['clicks']):,} clicks, {int(t['impressions']):,} impressions."
                   + ('\n\n| Query | Clicks | Impressions | Position |\n|---|---|---|---|\n' + '\n'.join(f"| {x['keys'][0]} | {int(x['clicks'])} | {int(x['impressions'])} | {x['position']:.1f} |" for x in top) if top else ''))

# ---------- Bing Webmaster Tools ----------
BING_ISSUES = {1: 'redirect 301', 2: 'redirect 302', 4: 'HTTP 4xx', 8: 'HTTP 5xx', 16: 'blocked by robots.txt', 32: 'malware', 64: 'important URL blocked by robots.txt', 128: 'DNS error', 256: 'timeout'}
def bing():
    key = os.environ.get('BING_API_KEY', '').strip()
    if not key: summary.append('**Bing:** skipped (secret `BING_API_KEY` not set; see SEO.md "Search engine accounts").'); return
    api = lambda m, **qs: 'https://ssl.bing.com/webmaster/api.svc/json/' + m + '?' + urllib.parse.urlencode({**qs, 'apikey': key})
    listed = http(api('GetUserSites')).get('d') or []
    site = next((s for s in listed if bare(s['Url']) == bare(B)), None)
    if not site: problems.append(f"Bing: {HOST} is not in this Bing Webmaster account (Add a site → Import from Google Search Console). Sites in the account: {', '.join(s['Url'] for s in listed) or 'none'}."); return
    su = site['Url']
    if not site.get('IsVerified', True): problems.append(f'Bing: {HOST} is not verified in Bing Webmaster Tools.'); return
    http(api('SubmitFeed'), {'siteUrl': su, 'feedUrl': SITEMAP})
    quota = (http(api('GetUrlSubmissionQuota', siteUrl=su)).get('d') or {}).get('DailyQuota', 0)
    urls = sitemap_urls()
    if quota and urls:
        q = min(quota, 500)  # SubmitUrlBatch takes at most 500 URLs
        k = datetime.date.today().toordinal() % math.ceil(len(urls) / q)  # a different slice each day, cycling through the sitemap
        batch = urls[k * q:(k + 1) * q]
        http(api('SubmitUrlBatch'), {'siteUrl': su, 'urlList': batch})
        summary.append(f'**Bing:** sitemap resubmitted; submitted {len(batch)} URLs today (daily quota {quota}; slice {k + 1} of {math.ceil(len(urls) / q)}, starting at `{batch[0][len(B):]}`).')
    else: summary.append(f'**Bing:** sitemap resubmitted; no URL submission quota left today.')
    issues = http(api('GetCrawlIssues', siteUrl=su)).get('d') or []
    if issues:
        lines = [f"`{x['Url'][len(B):] or '/'}`: {', '.join(v for b, v in BING_ISSUES.items() if x.get('Issues', 0) & b) or 'issue'} (HTTP {x.get('HttpCode')})" for x in issues[:20]]
        serious = [l for l, x in zip(lines, issues) if x.get('Issues', 0) & (8 | 16 | 32 | 64 | 128 | 256)]  # 4xx and redirects are listed, not problems (removed or old URLs)
        summary.append(f'**Bing crawl issues:** {len(issues)}\n\n' + '\n'.join('- ' + l for l in lines))
        problems.extend('Bing: ' + l for l in serious)
    else: summary.append('**Bing crawl issues:** none.')

def main():
    for name, f in (('Google', google), ('Bing', bing)):
        try: f()
        except urllib.error.HTTPError as e: problems.append(f"{name}: API error HTTP {e.code}: {e.read().decode('utf8', 'ignore')[:300]}")
        except Exception as e: problems.append(f'{name}: {type(e).__name__}: {e}')
    out = '\n\n'.join(summary) + ('\n\n**Problems:**\n' + '\n'.join('- ' + p for p in problems) if problems else '\n\nNo problems found.')
    print(out)
    if os.environ.get('GITHUB_STEP_SUMMARY'): open(os.environ['GITHUB_STEP_SUMMARY'], 'a').write(out + '\n')
    if arg('--problems'): open(arg('--problems'), 'w').write('\n'.join('- ' + p for p in problems))

if __name__ == '__main__':
    main()
