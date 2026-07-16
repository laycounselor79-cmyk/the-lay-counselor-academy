/*
  GA4 lead-action click tracking (vanilla TS, framework-agnostic).

  One delegated capture-phase click listener classifies clicks on links by
  their href and fires a named GA4 event — so every enrolment / email / phone
  CTA across the site is covered automatically, including ones added later,
  with no per-component wiring.

  Events (mark as Key Events in GA4 to count as conversions):
    - enroll_click    Teachfloor enrolment links (app.teachfloor.com)
    - email_click     mailto: links (e.g. Angelica@emorrisonconsulting.com)
    - phone_click     tel: links
    - whatsapp_click  wa.me / api.whatsapp.com links

  The sample-lesson form fires `generate_lead` separately from its own submit
  handler (GA4's recommended lead event). Self-hosted <video> elements fire
  video_start / video_progress (50%) / video_complete. No-ops when gtag is
  absent.
*/
type GtagParams = Record<string, unknown>;

const track = (event: string, params: GtagParams): void => {
  const gtag = (window as unknown as { gtag?: (...args: unknown[]) => void }).gtag;
  if (typeof gtag !== "function") return;
  gtag("event", event, params);
};

const classify = (href: string): string | null => {
  if (/\/\/app\.teachfloor\.com\//i.test(href)) return "enroll_click";
  if (/^mailto:/i.test(href)) return "email_click";
  if (/^tel:/i.test(href)) return "phone_click";
  if (/^(https?:)?\/\/(wa\.me|api\.whatsapp\.com)\//i.test(href)) return "whatsapp_click";
  return null;
};

document.addEventListener(
  "click",
  (e) => {
    const target = e.target as Element | null;
    const link = target?.closest<HTMLAnchorElement>("a[href]");
    if (!link) return;
    const event = classify(link.getAttribute("href") || "");
    if (event) {
      track(event, {
        link_url: link.href,
        link_text: (link.textContent || "").trim().slice(0, 100),
        page_path: window.location.pathname,
      });
    }
  },
  /* capture phase so it fires before navigation */
  true,
);

/*
  Video engagement for self-hosted <video> elements (GA4's enhanced
  measurement only auto-tracks YouTube embeds). Fires GA4's recommended
  video events once per page view: video_start on first play,
  video_progress at 50%, video_complete at end.
*/
document.querySelectorAll<HTMLVideoElement>("video").forEach((video) => {
  const title =
    video.getAttribute("data-video-title") ||
    video.getAttribute("poster")?.split("/").pop()?.replace(/-poster\.\w+$/, "").replace(/-/g, " ") ||
    "self-hosted video";
  const params = { video_title: title, page_path: window.location.pathname };
  let started = false;
  let passedHalf = false;

  video.addEventListener("play", () => {
    if (started) return;
    started = true;
    track("video_start", params);
  });
  video.addEventListener("timeupdate", () => {
    if (passedHalf || !video.duration) return;
    if (video.currentTime / video.duration >= 0.5) {
      passedHalf = true;
      track("video_progress", { ...params, video_percent: 50 });
    }
  });
  video.addEventListener("ended", () => {
    track("video_complete", params);
  });
});
