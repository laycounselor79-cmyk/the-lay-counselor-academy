#!/usr/bin/env node
/*
  Submit every sitemap URL to IndexNow (https://www.indexnow.org/).

  IndexNow pushes URL changes directly into the Bing, Yandex, Naver, and
  Seznam indexes within minutes instead of waiting for a crawl. Bing's index
  is what ChatGPT search and Microsoft Copilot cite from, so this is the
  fastest path to AI-answer-engine visibility. No Webmaster Tools
  verification is needed, only the key file at the site root.

  Run AFTER deploy (the key file and the new sitemap must be live before the
  ping, or the submission is rejected). Chain it into the deploy script.

  First run after the key file first goes live returns HTTP 403
  SiteVerificationNotCompleted while IndexNow fetches the key; retry every
  ~90s, verification completes within 2-10 minutes.
*/

const HOST = 'thelaycounseloracademy.com';          /* e.g. 'imperialnomadtours.com' */
const KEY = '42ccef88049cc6257e82a14716816589';     /* openssl rand -hex 16 */
const SITEMAP_INDEX = `https://${HOST}/sitemap-index.xml`;

const fetchText = async (url) => {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${url} -> HTTP ${res.status}`);
  return res.text();
};

/* Verify the key file is live before pinging. */
const keyUrl = `https://${HOST}/${KEY}.txt`;
const keyBody = (await fetchText(keyUrl)).trim();
if (keyBody !== KEY) {
  console.error(`Key file mismatch at ${keyUrl}, deploy before submitting.`);
  process.exit(1);
}

/* Collect page URLs from the sitemap index (ignore image:loc entries). */
const indexXml = await fetchText(SITEMAP_INDEX);
const sitemapUrls = [...indexXml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
const urls = new Set();
for (const sm of sitemapUrls) {
  const xml = await fetchText(sm);
  for (const m of xml.matchAll(/<url>\s*<loc>([^<]+)<\/loc>/g)) urls.add(m[1]);
}
const urlList = [...urls];
if (urlList.length === 0) {
  console.error('No URLs found in sitemap, aborting.');
  process.exit(1);
}

const res = await fetch('https://api.indexnow.org/indexnow', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json; charset=utf-8' },
  body: JSON.stringify({
    host: HOST,
    key: KEY,
    keyLocation: keyUrl,
    urlList,
  }),
});

/* 200 = submitted, 202 = accepted (key validation pending). Both are success. */
if (res.status === 200 || res.status === 202) {
  console.log(`IndexNow: submitted ${urlList.length} URLs (HTTP ${res.status}).`);
} else {
  console.error(`IndexNow submission failed: HTTP ${res.status} ${await res.text()}`);
  process.exit(1);
}
