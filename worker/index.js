/**
 * Cloudflare Worker entry — serves the static site (via the assets binding)
 * and handles the two form endpoints that used to be Pages Functions:
 *
 *   POST /api/sample-lesson  — emails the sample article via Resend
 *   POST /api/newsletter     — Mailchimp double-opt-in signup
 *
 * Static requests never reach this script: with an `assets` config and no
 * `run_worker_first`, Cloudflare serves matching assets directly and only
 * invokes the worker for non-asset routes like /api/*.
 *
 * Required secrets (wrangler secret put <NAME>):
 *   RESEND_API_KEY         — API key from the Resend dashboard
 *   SAMPLE_FROM            — verified sender, e.g. "The Lay Counselor Academy <hello@thelaycounseloracademy.com>"
 *   MAILCHIMP_API_KEY      — e.g. "xxxxxxxx-us19" (datacenter after the dash)
 *   MAILCHIMP_AUDIENCE_ID  — the audience / list id
 * Optional vars:
 *   SAMPLE_REPLY_TO        — defaults to Angelica@emorrisonconsulting.com
 *   SAMPLE_PDF_URL         — defaults to the copy hosted on this site
 *   SITE_BASE_URL          — canonical base for email links
 */

import { onRequestPost as sampleLesson } from "./api/sample-lesson.js";
import { onRequestPost as newsletter } from "./api/newsletter.js";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/sample-lesson" || url.pathname === "/api/sample-lesson/") {
      if (request.method !== "POST") return methodNotAllowed();
      return sampleLesson({ request, env });
    }

    if (url.pathname === "/api/newsletter" || url.pathname === "/api/newsletter/") {
      if (request.method !== "POST") return methodNotAllowed();
      return newsletter({ request, env });
    }

    // Anything else that fell through to the worker: let the assets binding
    // resolve it (covers 404-page handling for unknown paths).
    return env.ASSETS.fetch(request);
  },
};

function methodNotAllowed() {
  return new Response(JSON.stringify({ ok: false, error: "Method not allowed." }), {
    status: 405,
    headers: { "content-type": "application/json; charset=utf-8", allow: "POST" },
  });
}
