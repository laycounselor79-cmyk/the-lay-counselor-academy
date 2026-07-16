/**
 * generate-md-twins.mjs — post-build step (runs via npm "postbuild").
 *
 * For every canonical page in dist/, writes a markdown twin next to it:
 *   /            -> /index.md
 *   /curriculum/ -> /curriculum.md
 *   /teachers/x/ -> /teachers/x.md
 * and concatenates them all into /llms-full.txt (expanded content map for
 * AI assistants; /llms.txt stays the hand-written short index in public/).
 *
 * Twins are rendered from the built HTML so they can never drift from the
 * live pages. Layout.astro advertises each twin with
 * <link rel="alternate" type="text/markdown"> using the same URL mapping.
 */
import { readFileSync, writeFileSync, readdirSync, statSync } from "node:fs";
import { join, relative, dirname } from "node:path";
import TurndownService from "turndown";

const SITE = "https://thelaycounseloracademy.com";
const DIST = new URL("../dist", import.meta.url).pathname;

/* Same exclusions as the sitemap filter in astro.config.mjs: utility pages
 * and the noindex Spanish fallback stubs are not canonical content. */
const EXCLUDE = [/^404\//, /^thanks\//, /^es\/404\//, /^es\/thanks\//, /^es\/teachers\//, /^es\/accessibility\//];

const td = new TurndownService({ headingStyle: "atx", codeBlockStyle: "fenced", bulletListMarker: "-" });
td.remove(["script", "style", "noscript", "form", "iframe", "svg"]);
/* Video posters/decorative imagery add noise, keep real content images only. */
td.addRule("dropEmptyLinks", {
  filter: (node) => node.nodeName === "A" && !node.textContent.trim(),
  replacement: () => "",
});

function* htmlFiles(dir) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) yield* htmlFiles(p);
    else if (name === "index.html") yield p;
  }
}

const pages = [];
for (const file of htmlFiles(DIST)) {
  const rel = relative(DIST, dirname(file)); // "" for root, "curriculum", "es/faq", ...
  const route = rel === "" ? "/" : `/${rel}/`;
  if (EXCLUDE.some((rx) => rx.test(rel + "/"))) continue;

  const html = readFileSync(file, "utf8");
  if (/name="robots"[^>]*noindex/i.test(html) || /http-equiv="refresh"/i.test(html)) continue;

  const title = (html.match(/<title>(.*?)<\/title>/s)?.[1] ?? route).trim();
  const description = html.match(/name="description" content="(.*?)"/)?.[1] ?? "";
  const main = html.match(/<main[^>]*>([\s\S]*?)<\/main>/)?.[1];
  if (!main) continue;

  const body = td
    .turndown(main)
    .replace(/\]\(\//g, `](${SITE}/`) // absolute links so the .md is portable
    .replace(/\n{3,}/g, "\n\n")
    .trim();

  const md = `# ${decodeEntities(title)}\n\n> ${decodeEntities(description)}\n\nCanonical: ${SITE}${route}\n\n${body}\n`;
  const twinPath = route === "/" ? join(DIST, "index.md") : join(DIST, rel + ".md");
  writeFileSync(twinPath, md);
  pages.push({ route, title: decodeEntities(title), md });
}

/* Stable, reader-friendly order: home first, then English pages, then Spanish. */
pages.sort((a, b) => {
  const key = (p) => (p.route === "/" ? "0" : p.route.startsWith("/es") ? "2" + p.route : "1" + p.route);
  return key(a).localeCompare(key(b));
});

const full = [
  "# The Lay Counselor Academy — full content",
  "",
  "> Expanded, machine-readable copy of every canonical page on " + SITE + ".",
  "> The short index lives at " + SITE + "/llms.txt.",
  "",
  ...pages.map((p) => "\n---\n\n" + p.md),
].join("\n");
writeFileSync(join(DIST, "llms-full.txt"), full);

function decodeEntities(s) {
  return s
    .replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
    .replace(/&#39;/g, "'").replace(/&quot;/g, '"').replace(/&#8217;/g, "’");
}

console.log(`md twins: ${pages.length} pages + llms-full.txt (${(full.length / 1024).toFixed(0)}KB)`);
