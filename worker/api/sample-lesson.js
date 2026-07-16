/**
 * Cloudflare Pages Function — sample-lesson form endpoint.
 *
 * Delivers the sample article ("Advice: Why (& How) We Avoid It") by emailing
 * the recipient a download link, via Resend (https://resend.com).
 *
 * Required environment variables (set in the Cloudflare Pages project):
 *   RESEND_API_KEY   — API key from the Resend dashboard
 *   SAMPLE_FROM      — verified sender, e.g. "The Lay Counselor Academy <hello@thelaycounseloracademy.com>"
 * Optional:
 *   SAMPLE_PDF_URL   — absolute URL to the article PDF. Defaults to the
 *                      copy hosted on this site at /downloads/LCA_Avoiding_Advice.pdf
 *
 * If RESEND_API_KEY / SAMPLE_FROM are not set, the endpoint returns a 500 so
 * the form shows its error state rather than falsely claiming the email sent.
 */

const ARTICLE_TITLE = "Advice: Why (& How) We Avoid It";

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

  const apiKey = env.RESEND_API_KEY;
  const from = env.SAMPLE_FROM;
  // Canonical base so the email's links are always clean, regardless of which
  // deployment (preview or production) actually serves the request.
  const base = env.SITE_BASE_URL || "https://thelaycounseloracademy.com";
  const pdfUrl = env.SAMPLE_PDF_URL || `${base}/downloads/LCA_Avoiding_Advice.pdf`;
  const logoUrl = `${base}/images/lca-logo-horizontal-transparent.png`;
  const siteUrl = `${base}/`;
  const replyTo = env.SAMPLE_REPLY_TO || "Angelica@emorrisonconsulting.com";

  if (!apiKey || !from) {
    // Not configured yet — do not pretend we sent anything.
    return json(
      { ok: false, error: "Something went wrong on our end. We've logged it. Please try again in a moment." },
      500,
    );
  }

  try {
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "content-type": "application/json",
      },
      body: JSON.stringify({
        from,
        to: [email],
        reply_to: replyTo,
        subject: `Your sample article: ${ARTICLE_TITLE}`,
        html: emailHtml({ pdfUrl, logoUrl, siteUrl }),
        text: emailText({ pdfUrl, siteUrl }),
      }),
    });

    if (!res.ok) {
      return json(
        { ok: false, error: "Something went wrong on our end. We've logged it. Please try again in a moment." },
        502,
      );
    }
  } catch {
    return json(
      { ok: false, error: "Something went wrong on our end. We've logged it. Please try again in a moment." },
      502,
    );
  }

  // For JS-disabled clients, do a real redirect to /thanks so the page works.
  if (!contentType.includes("application/json")) {
    return Response.redirect(new URL("/thanks", request.url).toString(), 303);
  }

  return json({ ok: true, message: `Sent. Check your inbox for ${ARTICLE_TITLE}.` });
}

function emailHtml({ pdfUrl, logoUrl, siteUrl }) {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<title>${ARTICLE_TITLE}</title>
</head>
<body style="margin:0; padding:0; background-color:#faf6f1;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#faf6f1;">
    <tr>
      <td align="center" style="padding:32px 16px;">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px; max-width:600px; background-color:#ffffff; border-radius:14px; overflow:hidden; border:1px solid #ece5dc;">
          <!-- mint header (showcases the brand's secondary colour) -->
          <tr>
            <td align="center" bgcolor="#bfe5cc" style="background-color:#bfe5cc; padding:32px 24px;">
              <img src="${logoUrl}" width="290" alt="The Lay Counselor Academy — Self-Paced" style="display:block; width:290px; max-width:84%; height:auto; border:0;">
            </td>
          </tr>
          <!-- content -->
          <tr>
            <td style="padding:38px 44px 30px 44px; font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">
              <p style="margin:0 0 10px 0; font-size:12px; letter-spacing:0.14em; text-transform:uppercase; color:#ff545e; font-weight:700;">Your sample article</p>
              <h1 style="margin:0 0 18px 0; font-family:Georgia,'Times New Roman',serif; font-weight:400; font-size:28px; line-height:1.2; color:#0a2957;">${ARTICLE_TITLE}</h1>
              <p style="margin:0 0 16px 0; font-size:16px; line-height:1.65; color:#2b2f38;">Thanks for your interest in The Lay Counselor Academy. Here is your sample article to read whenever you like, no strings attached.</p>
              <!-- button -->
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:22px 0 8px 0;">
                <tr>
                  <td align="center" bgcolor="#0a2957" style="background-color:#0a2957; border-radius:9999px;">
                    <a href="${pdfUrl}" style="display:inline-block; padding:14px 30px; font-family:'Helvetica Neue',Helvetica,Arial,sans-serif; font-size:16px; font-weight:600; color:#ffffff; text-decoration:none; border-radius:9999px;">Read the article (PDF)&nbsp;&rarr;</a>
                  </td>
                </tr>
              </table>
              <p style="margin:14px 0 0 0; font-size:13px; line-height:1.6; color:#8a8f98;">If the button doesn't work, copy and paste this link:<br>
                <a href="${pdfUrl}" style="color:#ff545e; word-break:break-all;">${pdfUrl}</a>
              </p>
              <hr style="border:0; border-top:1px solid #ece5dc; margin:28px 0 20px 0;">
              <p style="margin:0; font-family:Georgia,'Times New Roman',serif; font-style:italic; font-size:16px; color:#0a2957;">Warmly,<br>The Lay Counselor Academy</p>
              <p style="margin:18px 0 12px 0; font-family:'Helvetica Neue',Helvetica,Arial,sans-serif; font-size:13px; line-height:1.6; color:#6b7280;">P.S. Want occasional notes on lay counseling and news from the Academy?</p>
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0;">
                <tr>
                  <td align="center" bgcolor="#bfe5cc" style="background-color:#bfe5cc; border-radius:9999px;">
                    <a href="${siteUrl}#newsletter" style="display:inline-block; padding:11px 24px; font-family:'Helvetica Neue',Helvetica,Arial,sans-serif; font-size:14px; font-weight:600; color:#0a2957; text-decoration:none; border-radius:9999px;">Sign up for our newsletter&nbsp;&rarr;</a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <!-- navy footer (grounds the design; uses the brand's primary colour) -->
          <tr>
            <td align="center" bgcolor="#0a2957" style="background-color:#0a2957; padding:22px 30px; font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">
              <p style="margin:0 0 10px 0; font-size:12px; line-height:1.7;"><a href="${siteUrl}" style="color:#bfe5cc; text-decoration:underline;">thelaycounseloracademy.com</a> &nbsp;&middot;&nbsp; <a href="https://www.emorrisonconsulting.com/services/lay-counselor-training-academy/" style="color:#bfe5cc; text-decoration:underline;">Elizabeth Morrison Consulting</a></p>
              <p style="margin:0; font-size:11px; color:#9fb1cb; line-height:1.7;"><strong style="color:#cdd9ea;">Please do not reply to this email</strong> — it is sent automatically.<br>Questions? Email us at <a href="mailto:Angelica@emorrisonconsulting.com" style="color:#bfe5cc; text-decoration:underline; white-space:nowrap;">Angelica@emorrisonconsulting.com</a></p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>`;
}

function emailText({ pdfUrl, siteUrl }) {
  return [
    "Thanks for your interest in The Lay Counselor Academy.",
    "",
    `Here is your sample article, ${ARTICLE_TITLE}, to read whenever you like:`,
    pdfUrl,
    "",
    "Warmly,",
    "The Lay Counselor Academy — Self-Paced",
    "",
    `P.S. Sign up for our newsletter: ${siteUrl}#newsletter`,
    "",
    "Please do not reply to this email — it is sent automatically.",
    "Questions? Email us at Angelica@emorrisonconsulting.com",
    siteUrl,
    "Elizabeth Morrison Consulting: https://www.emorrisonconsulting.com/services/lay-counselor-training-academy/",
  ].join("\n");
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
