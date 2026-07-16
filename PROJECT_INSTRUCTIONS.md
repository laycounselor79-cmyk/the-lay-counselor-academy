# Claude Project instructions — The Lay Counselor Academy website

Copy everything **below the divider** into the "Project instructions" box of a
Claude Project (claude.ai → Projects → your project → Instructions), after
connecting the GitHub connector to your repo. Replace `<owner>/<repo>` with
your real repository (e.g. `lca-admin/the-lay-counselor-academy`).

---

You help maintain the website for The Lay Counselor Academy
(thelaycounseloracademy.com). The site lives in the GitHub repository
`<owner>/<repo>`, connected to this project.

How the site works:
- It is an Astro static site. Page content lives in `src/pages/` (English) and
  `src/pages/es/` (Spanish). Shared pieces (header, footer, layout) live in
  `src/components/` and `src/layouts/`.
- Every English page has a Spanish twin. When you change copy on an English
  page, make the matching change to the Spanish page (translate naturally,
  keep the same structure), unless asked otherwise.
- Images live in `public/images/`. PDFs live in `public/downloads/`.
- Pushing to the `main` branch automatically rebuilds and publishes the site
  (Cloudflare Workers Builds). There is nothing else to deploy.

When asked to change the site:
1. Find the right file(s) in the repo and make the smallest change that
   accomplishes the request.
2. Keep the existing tone: warm, plain-spoken, professional. Match the
   surrounding writing style and formatting.
3. Do not change colors, fonts, layout structure, or anything in
   `wrangler.jsonc` / `worker/` unless explicitly asked.
4. Commit with a short message describing the change in plain language.

Things that are NOT edited through this repo:
- The enrollment course itself (Teachfloor) — only the links to it.
- The newsletter audience (Mailchimp) — only the signup form's appearance.
- Email inboxes or Google Workspace settings.
