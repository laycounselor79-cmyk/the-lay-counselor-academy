# Design Brief — The Lay Counselor Academy (Self-Paced) — Homepage

**Status:** CONFIRMED 2026-05-13. **Revised 2026-05-14** to tighten brand continuity with the parent site (see §3, and the parent-alignment note in §10). Build proceeded under this revised brief.
**Companion docs:** [PRODUCT.md](./PRODUCT.md) (strategic anchor), [LCA_BUILD_BRIEF.md](./LCA_BUILD_BRIEF.md) (content + business inputs), [DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md) (brand primitives).

This brief is the contract between strategy and code for the homepage at `thelaycounseloracademy.com`. Every implementation decision should trace back to a section here.

---

## 1. Feature Summary

The homepage for The Lay Counselor Academy — a $1,200, 70-hour, fully-asynchronous self-paced training program in mental health counseling for non-clinicians. It is a marketing surface, but written and composed as if it were the editorial front page of a small, well-funded publication that happens to sell a program. Its job is to convince a thoughtful adult who has already taken on the role of helping other people — sponsors, crisis-line volunteers, RAs, HR peer-listeners, fire department workers, paramedics, teachers, nonprofit leaders — that this academy is *serious, kind, and real*, and that a single quiet read of the sample lesson will tell them more than any marketing claim could.

## 2. Primary User Action

**Read the sample lesson — "Listening without fixing" (Lesson 1 of the Foundations module).** Email-gated; the form is in-page, not in a modal. This is the loudest, most-repeated CTA on the page and the entry to the conversion funnel.

**Secondary action:** *Enroll now* → handoff to TeachFloor (`https://app.teachfloor.com/the-lay-counselor-academy/c/31922`). Smaller, quieter, available for readers who have already decided.

The sample lesson is treated as a real artifact, not a lead magnet — its title, module placement, and a real one-paragraph tease appear before the email field.

## 3. Design Direction

**Color strategy: Committed**, anchored to the existing parent-brand palette in `DESIGN_SYSTEM.md`:

| Role | Token | Hex | OKLCH (computed) |
|------|-------|-----|------------------|
| Primary brand (ink + section ground) | navy | `#092a57` | `oklch(0.27 0.10 261)` |
| Secondary brand | dark blue | `#1f4172` | `oklch(0.38 0.10 261)` |
| Accent (CTA + brand voice) | coral | `#ff555e` | `oklch(0.68 0.20 21)` |
| Page background | near-white, navy-tinted | — | `oklch(0.985 0.004 261)` |
| Warm-section background | cream | `#fef5ef` | `oklch(0.97 0.012 70)` |
| Info wash | light blue | `#ecf4ff` | `oklch(0.96 0.020 261)` |
| Body text | cool dark grey, navy-tinted | ≈ `#1B1B1B` | `oklch(0.24 0.006 261)` |
| On-navy text (white) | cream-white | — | `oklch(0.97 0.012 70)` |

**Deployment** — coral, navy, and the parent's near-white are used **with the parent brand's confidence**, not held back. Sequence of section surfaces on the homepage:

1. Hero — near-white
2. Framing — near-white
3. Program — cream (warm interlude #1)
4. Teachers — near-white
5. Excerpt — info-blue wash
6. **Evaluation — navy ground, cream text, coral accents.** This is the parent-vocabulary "serious moment" and the strongest credibility surface on the page.
7. Press — near-white, coral-tinted publication links
8. Sample lesson — cream (warm interlude #2, where conversion happens)
9. Pricing doorway — near-white
10. Footer — navy-deep (already established)

Coral remains the single accent of consequence, but it shows up confidently in more than one moment: primary CTA, section eyebrows, marker glyphs, press-link color, and the evaluation-section CTA border on the navy ground. All neutrals tinted toward the navy hue per impeccable's OKLCH rule.

**Theme scene sentence (revised):** *A clinical social worker on a tablet at her desk between sessions, double-checking whether the academy is the same brand she trusts at emorrisonconsulting.com before forwarding the link to a volunteer who's asked her for training.* Forces **light mode, parent-continuous**, dominant feeling of a confident publication that belongs to a known practitioner — not a separate magazine.

**Anchor references (composition + density, not vibe):**
- emorrisonconsulting.com — the parent brand. Color confidence, big logo, navy as section ground, coral as a real presence.
- The Marginalian (themarginalian.org) — generous measure, named-voice respect, no marketing scaffolding.
- On Being (onbeing.org) — editorial composition, warmth without hype.

**Visual direction probes:** Skipped — Claude Code lacks native image generation. Direction grounded in the three references and direct color audit of the parent-site compiled stylesheet.

## 4. Scope

- **Fidelity:** Production-ready. Real teachers (Elizabeth Morrison PhD LCSW MAC, Ali Moreno), real 7-module / 14-session curriculum from LCA_BUILD_BRIEF.md, real pricing ($800 / $1,200 / $1,600 sliding scale + $2,200 hybrid), real press coverage (California Healthline, Steinberg Institute, Modesto Bee, STAT News, CHCF evaluation), real logo, real headshot of Elizabeth. **Known content gap:** Ali Moreno headshot not yet provided — use typographic treatment until photo arrives.
- **Breadth:** Homepage only. Five-page site total; bio pages (Elizabeth, Ali), Reviews/Endorsements, Contact, and the future Pricing/Curriculum/FAQ deeper pages are subsequent crafts.
- **Interactivity:** Shipped quality. Email-gated CTA wired to a **stubbed** `/api/sample-lesson` endpoint that returns 200; user will swap in Cloudflare Workers or ConvertKit before launch. Keyboard nav, focus-visible, reduced-motion baseline.
- **Time intent:** Polish until it ships.

## 5. Layout Strategy

A long-form editorial page reading like a single thoughtful column with deliberate widenings — **not** a marketing-template stack of feature cards. Vertical rhythm is generous and varied; section padding is intentionally non-uniform. Information flow:

1. **Quiet hero.** Serif headline (Lora 400, ~64–79px desktop), max two lines, in the voice of a teacher: *"Learn to sit with someone who is suffering, without making it worse."* Subhead in Poppins body type, set narrow (~52ch). Primary CTA *"Read the sample lesson"* right under the subhead, sized restrained (not a slab-button). Tiny accompanying line names the actual lesson title and module. A secondary, quieter *"Enroll now"* outline link. **One** quiet line beneath, set in italic body type, naming the trust signal: *"Now in its fourth year. Over twelve hundred students have come through the program."* No giant photo behind text. No hero-metric template, no number-stat row.

2. **Framing paragraph.** Three or four sentences in body type, no heading, set narrow, naming the audience honestly: *"If you're a sponsor, a crisis-line volunteer, an RA, an HR peer-listener, a fire department employee who keeps getting asked the hard questions, a paramedic, a teacher, a community health worker, or anyone else who has agreed to sit with people in hard moments without being a clinician — this program is for you."* Earns the right to the rest of the page.

3. **The program, as a table of contents.** The 7 modules listed typographically — each module name (Lora 28–40px), one-sentence tease in body type. **Not** an identical 7-card grid; closer to a literary book's table of contents with quiet horizontal rules between modules and slightly varied weight to mark module-level vs session-level. Each module is a doorway link to the (future) curriculum page anchor for that module. Includes the total course hours (70) named once, in plain prose ("seventy hours, paced for evenings and weekends").

4. **The teachers, presented as people.** Elizabeth Morrison and Ali Moreno, each with a real photograph (Elizabeth provided; Ali pending — typographic placeholder for now), real credential line, and one paragraph of bio in their own register. Read like an editor's-letter spread, not a testimonial grid. Each name links to the (future) full bio page.

5. **A real teaching moment.** A pulled excerpt drawn from Module 2 Session 1's *"Home Stance"* concept — one paragraph in slightly larger reading type (Lora 24–28px), framed quietly with a slim left margin and a small coral marker glyph (not a quote-mark icon, not a card). Attribution beneath in caption type: lesson title, module, teacher. This section does most of the credibility work that the marketing-template version of this page would have wasted on stock testimonials.

6. **The CHCF evaluation, named.** A short paragraph and a doorway link to the California Health Care Foundation external evaluation. This is the strongest credibility artifact on the entire page and gets its own moment — set in body type, mentioned by name, with a quiet "Read the evaluation" link. No badge, no logo soup.

7. **Press, as named citations.** A single line in body type listing publications by name — *"Coverage in California Healthline, the Modesto Bee, STAT News, and Steinberg Institute."* — with each name linking to the relevant article. **Not** a logo strip. (PRODUCT.md anti-reference: no "as seen in" logo soup.)

8. **The free sample lesson section.** Primary CTA repeated here with substantive copy: the sample-lesson title set as a chapter heading (Lora 40–52px), 3–4 sentence tease of what's inside, email input + button, single reassurance line. This is where most conversions happen on an editorial page; it breathes.

9. **Pricing doorway.** Single quiet paragraph: *"Self-paced is $1,200. Two sliding-scale tiers — $800 if cost is a barrier, $1,600 if you want to support a seat for someone who can't pay — work on the honor system. A hybrid program with live practice sessions is also available."* with a "See full pricing →" link to /pricing. **No** pricing card grid on the homepage.

10. **Footer.** Wordmark in larger restful type, brief mission line, nav links (Curriculum / Teachers / Reviews / Pricing / Contact / FAQ), parent-site link, accessibility statement link, privacy + terms (linking to existing parent-site policies until LCA has its own), copyright. The watermark logo variant on the dark navy footer ground.

**Rhythm:** Section padding varies. The hero breathes the most. The framing paragraph is tighter. The program-map has airy line-spacing. The teaching-moment excerpt is the densest typographic moment. The CTA section breathes again. Max measure ~65–72ch for prose; narrower (~52ch) for hero and CTA copy; wider for the program map and teacher row.

## 6. Key States

- **Default (page load):** Above-the-fold answers "what is this, who teaches it, what would I get" without scroll.
- **Sample-lesson form — default:** Email field, single coral button, one reassurance line.
- **Focus / typing:** Visible navy focus ring on the input (2px, no glow), button enabled.
- **Invalid email:** Inline error beneath field in body type, tinted warm-grey (not red-alert): *"Please check this — it doesn't look like an email."* Plain language, no em dash.
- **Submitting:** Button label *"Sending…"* with subtle inline spinner. Form stays visible; no full-page overlay.
- **Success:** Form area replaced by short editorial sentence: *"Sent. Check your inbox for Listening without fixing."* No confetti, no modal.
- **Server error:** Form remains; inline message: *"Something went wrong on our end. We've logged it. Please try again in a moment."*
- **JS disabled / progressive enhancement:** Form posts to real endpoint and lands on `/thanks` with the same editorial sentence. Page fully readable without JS.
- **Reduced motion (baseline):** No scroll-tied animation, no auto-play, no parallax. Section reveals are instant. Hover/focus are static color changes.
- **Motion-enabled (additive):** Single slow generous fade-in on hero text (~600ms ease-out-quart). Section reveals on scroll-into-view with a quiet 8px upward translate over 500ms. No bounce, no elastic, no choreography.
- **First visit vs return:** Identical, except return visitors who already submitted see the form replaced by *"You already have the sample lesson on its way. Want to see pricing?"* with a quiet link (localStorage-gated).

## 7. Interaction Model

- **Primary CTA click:** Smooth-scroll (instant under reduced-motion) to the in-page sample-lesson form section; focus the email field. **No modal.**
- **Secondary CTA (Enroll):** External link to TeachFloor enrollment URL with `rel="noopener"` and a brief leaving-site visual hint (small external-link glyph).
- **Doorway links (program map, teachers, pricing, press, CHCF):** Standard `<a>` navigation to the relevant page or external URL.
- **Form submit:** Async POST to `/api/sample-lesson` (stub), optimistic state transitions per State section.
- **Keyboard:** Full keyboard nav, visible focus on every interactive target, skip-to-main-content link first in tab order.
- **Touch targets:** ≥44×44px on touch.
- **Hover (desktop):** Underline thickens or color shifts on links — no transform, no layout change. Buttons darken ~6% lightness in OKLCH. No effects on touch.
- **Scroll feel:** Native scroll. No hijacking, no scroll-snap, no parallax.

## 8. Content Requirements

| Slot | Source | Status |
|------|--------|--------|
| Hero headline | *"Learn to sit with someone who is suffering, without making it worse."* | Approved |
| Hero subhead | *"A serious, paced training program for peer counselors, sponsors, and volunteer listeners. Taught by people who have done this work for decades."* | Drafted, awaiting sign-off |
| Trust line | *"Now in its fourth year. Over twelve hundred students have come through the program."* | Drafted from LCA_BUILD_BRIEF.md |
| Primary CTA label | *"Read the sample lesson"* | Approved |
| Secondary CTA label | *"Enroll now"* | Approved |
| Sample-lesson title | *"Listening without fixing"* — Foundations, Lesson 1 | Working title; user OK to swap if client provides different real lesson |
| Sample-lesson tease | Drafted paragraph showing the actual teaching | In brief; awaits final sign-off |
| Framing paragraph | Drafted | In brief |
| Program map (7 × 1-sentence teases) | LCA_BUILD_BRIEF.md module names + Claude-drafted teases | Drafted in build, flag for client review |
| Teacher bios (×2) | Elizabeth Morrison (PhD, LCSW, MAC) drafted; Ali Moreno needs real bio | **Open** |
| Teaching-moment excerpt | Drafted from Module 2 "Home Stance" concept | Drafted, flag for client review |
| CHCF doorway copy | Drafted; links to CHCF evaluation PDF | Drafted |
| Press list | Named publications from LCA_BUILD_BRIEF.md | Linked to public articles |
| Pricing doorway sentence | Drafted | In brief |
| Footer copy | Drafted | In brief |

**Microcopy hard rules (per impeccable + PRODUCT.md):**
- **No em dashes.** Use commas, colons, semicolons, periods, parentheses. (The visual em dash in this brief is in the meta-text, not in shipped copy.)
- No exclamation points.
- No "transform your," "unlock," "level up," "your best self," "30 days," "limited time," "10,000 students," "as seen in."
- Plain language target ≈ Grade 9 or lower for framing and CTA labels.

## 9. Recommended References

Consulted during implementation in order of weight:

1. `typography.md` — Lora + Poppins scale, weight contrast, measure, the page lives on type.
2. `spatial-design.md` — varied rhythm, the case against uniform padding, the case against single-container layouts.
3. `color-and-contrast.md` — OKLCH tinting, the navy-anchored neutral system, coral as scarce-resource accent.
4. `ux-writing.md` — voice, plain-language, no-em-dash rule, error message register.
5. `motion-design.md` — reduced-motion-as-baseline, ease-out-quart, no-bounce / no-elastic.
6. `responsive-design.md` — compositional adaptation, hero reflow.
7. `interaction-design.md` — form state matrix, focus treatment, keyboard paths.

## 10. Open Questions

Resolved by the user's adjustments:
- ✅ Sample-lesson title: *"Listening without fixing"* approved as working title.
- ✅ Hero headline: approved as-is.
- ✅ Email service: stub for now; wire to real service (likely Cloudflare Workers or ConvertKit) before launch.
- ✅ Hosting: Cloudflare Pages, Astro static.
- ✅ Domain: thelaycounseloracademy.com, DNS pending.
- ✅ Privacy/terms: link to parent-site policies. Accessibility statement: stub at `/accessibility`.
- ✅ Content: in project folder (LCA_BUILD_BRIEF.md, DESIGN_SYSTEM.md, /assets/).
- ✅ Wordmark: use circular LCA mark in nav, watermark variant on dark footer ground.
- ✅ Analytics: stub for now; Plausible likely added before launch.

Still open, surfacing for client follow-up:
1. **Ali Moreno headshot + bio.** Typographic placeholder used in build; needs real photo and bio paragraph from the client.
2. **Final sample-lesson body.** If the actual sample lesson the email hands over needs the body content of *Listening without fixing* — that body content is not yet drafted.
3. **TeachFloor enrollment URL confirmation.** Using `https://app.teachfloor.com/the-lay-counselor-academy/c/31922` from LCA_BUILD_BRIEF.md — confirm this is the correct production link.
4. **Hero imagery.** No hero photo decision is locked. Building hero as a type-led composition; can layer in a real classroom-texture image later if the client provides one.
5. **Pricing page content.** Out of scope for this craft, but the homepage doorway links to `/pricing` — that page needs its own craft pass.
6. **Press article URLs.** `pressLinks` in `src/pages/index.astro` currently points at publication homepages (statnews.com, modbee.com, californiahealthline.org, steinberginstitute.org). Replace with direct article URLs once provided.

**2026-05-14 parent-alignment course correction.** After first browser eyeball, the user flagged that the original "warm-editorial / Marginalian / Graywolf" deployment had drifted too far from the parent brand at emorrisonconsulting.com. §3 was revised to swap page background from warm cream to navy-tinted near-white, push body text toward the parent's #1B1B1B tone, deploy navy as a section ground (CHCF evaluation) instead of only as ink, give coral a more confident spread (press links, evaluation CTA, multiple eyebrows), and enlarge the nav logo + wordmark to match the parent's presence. Editorial *discipline* (no card grid, no hero-metric, narrow measures, generous whitespace, named-voice copy) is retained; what changed is brand-color *confidence*.

---

## Build constraints inherited from impeccable + DESIGN_SYSTEM.md

**Fonts:** Lora (serif, weights 400/500) for headings; Poppins (sans-serif, weights 400/500/600) for body, UI. Self-hosted via `@fontsource` for performance and offline build.

**Colors:** OKLCH for all computed values; the brand hex values are the anchor but tokens are expressed as OKLCH in CSS variables. No pure `#fff` or `#000` — backgrounds tint slightly toward navy.

**Forbidden patterns (impeccable):**
- No side-stripe borders as accent on cards/alerts.
- No gradient text.
- No glassmorphism.
- No hero-metric template (big number + small label stat row).
- No identical card grids (icon + heading + text repeated).
- No modal as first thought.
- No em dashes in copy.
- No animating CSS layout properties; ease-out-quart/quint/expo only.

**Type scale (from DESIGN_SYSTEM.md, lightly disciplined for this surface):** H1 79/81 → H2 64/74 → H3 60/65 → H4 52/60 → H5 40/50 → H6 36/46 → Subheading 28/36 → Body 21/32 → Small 18/27 → Button 16/24 → Caption 15/24. Mobile and tablet steps per DESIGN_SYSTEM.md. Weight contrast between adjacent steps ≥1.25 ratio honored via 400/500/600 mix.

**A11y:** WCAG 2.2 AA. Body type ≥17px equivalent (we exceed at 21px). Calm-by-default motion. Plain-language copy. Strong visible focus. Full keyboard. Alt text on all meaningful images. No info conveyed by color alone.

---

— end of brief —
