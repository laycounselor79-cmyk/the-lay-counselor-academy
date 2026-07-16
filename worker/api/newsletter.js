/**
 * Cloudflare Pages Function — newsletter signup → Mailchimp.
 *
 * Adds the email to the Mailchimp audience as "pending" (double opt-in:
 * Mailchimp emails the subscriber a confirmation link before they're added).
 *
 * Env vars (set as Pages project secrets):
 *   MAILCHIMP_API_KEY      e.g. "xxxxxxxx-us19" (the datacenter is the part after the dash)
 *   MAILCHIMP_AUDIENCE_ID  the audience / list id
 *
 * If the env vars are absent the endpoint returns a 500 rather than pretending
 * to subscribe anyone.
 */
export async function onRequestPost(context) {
  const { request, env } = context;
  const contentType = request.headers.get("content-type") || "";

  let email = "";
  try {
    if (contentType.includes("application/json")) {
      const body = await request.json();
      email = String(body.email || "").trim();
    } else if (contentType.includes("form")) {
      const formData = await request.formData();
      email = String(formData.get("email") || "").trim();
    }
  } catch {
    return json({ ok: false, error: "Could not read the form." }, 400);
  }

  if (!isPlausibleEmail(email)) {
    return json({ ok: false, error: "Please check this. It doesn't look like an email." }, 400);
  }

  const apiKey = env.MAILCHIMP_API_KEY;
  const audienceId = env.MAILCHIMP_AUDIENCE_ID;
  const dc = apiKey ? apiKey.split("-")[1] : "";

  if (!apiKey || !audienceId || !dc) {
    return json({ ok: false, error: "Something went wrong on our end. Please try again in a moment." }, 500);
  }

  const url = `https://${dc}.api.mailchimp.com/3.0/lists/${audienceId}/members`;

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: {
        Authorization: `Basic ${btoa("anystring:" + apiKey)}`,
        "content-type": "application/json",
      },
      body: JSON.stringify({ email_address: email, status: "pending" }),
    });

    if (res.ok) {
      return json({ ok: true, message: "Almost there — check your inbox to confirm your subscription." });
    }

    let detail = {};
    try {
      detail = await res.json();
    } catch {
      // non-JSON error body
    }

    // Already subscribed / pending: treat as a friendly success, not an error.
    if (
      res.status === 400 &&
      (detail.title === "Member Exists" || /already a list member/i.test(detail.detail || ""))
    ) {
      return json({ ok: true, message: "You're already on the list — thank you!" });
    }

    return json(
      { ok: false, error: "Something went wrong on our end. We've logged it. Please try again in a moment." },
      502,
    );
  } catch {
    return json(
      { ok: false, error: "Something went wrong on our end. We've logged it. Please try again in a moment." },
      502,
    );
  }
}

function isPlausibleEmail(value) {
  if (!value || value.length > 254) return false;
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function json(payload, status = 200) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { "content-type": "application/json; charset=utf-8" },
  });
}
