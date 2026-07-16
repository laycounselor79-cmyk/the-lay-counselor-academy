# Editing your website

Your website is a set of files in a GitHub repository. When the files change,
the site republishes itself automatically within a couple of minutes. There is
no separate CMS or admin panel — the repository IS the website.

## The easy way: Claude

1. Sign in at claude.ai with your own account (a paid plan is required for
   Projects + the GitHub connector).
2. In **Settings → Connectors**, add the **GitHub** connector and authorize it
   for your website repository.
3. Create a **Project** (call it "LCA Website"). Open `PROJECT_INSTRUCTIONS.md`
   in this repository, copy everything below the divider into the Project's
   instructions box, and replace `<owner>/<repo>` with your repository name.
4. To make a change, open the project and just ask, for example:
   - "Change the price on the pricing page to $349."
   - "Swap the Spanish course link on the curriculum page to <url>."
   - "Add this testimonial to the reviews page: …"
   Claude will find the right files, make the edit (in English AND Spanish),
   and commit it. The site republishes on its own.

## What happens behind the scenes

- Files live on GitHub. Every change is saved with a history, so nothing is
  ever lost — any previous version can be restored.
- Cloudflare watches the repository. When `main` changes it rebuilds the site
  and publishes it worldwide. Hosting is on Cloudflare's free plan.

## Things to know

- **Two languages.** Every English page has a Spanish twin under `/es/`.
  Change both (Claude does this automatically if you use the project above).
- **Forms.** The sample-article form sends email through your Resend account;
  the newsletter form adds people to your Mailchimp audience. Their API keys
  are stored as private settings in your Cloudflare account, not in these
  files.
- **The course itself** lives on Teachfloor, not here. The site only links to
  it.
- **Don't rename or move** `wrangler.jsonc`, the `worker/` folder, or anything
  in `public/.well-known/` — they keep hosting, forms, and search-engine
  verification working.
