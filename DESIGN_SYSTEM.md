# LCA Design System (extracted from emorrisonconsulting.com/services/lay-counselor-training-academy/)

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| Primary | #1b1b1b | Text headings, dark text |
| Secondary | #092a57 | Deep navy, section backgrounds, heading color |
| Text | #323232 | Body text |
| Accent | #ff555e | Coral/red, buttons, CTAs, highlights |
| Blue Accent | #224983 | Counter numbers, pricing, secondary blue |
| Dark Blue | #1f4172 | Icon backgrounds, link color, primary brand blue |
| White | #ffffff | Backgrounds, button text |
| Light Gray | #f6f6f6 | Card backgrounds, section alternates |
| Light Pink | #f3e2e2 | Decorative |
| Warm Cream | #fef5ef | Section backgrounds |
| Light Blue BG | #ecf4ff | Pricing cards, info sections |
| Muted Text | #1B1B1B99 (60% opacity) | Subdued body text |
| Gray | #918f8f | Borders, muted elements |
| Dark Nav BG | #092a57 | Header/footer background |
| Footer Dark | #082349 | Footer bottom bar |
| Green Accent | #3af7bd | Decorative dots/circles in popup |

## Typography

### Font Families
- **Display/Headings:** Lora (serif) - weights 400, 500
- **Body/UI:** Poppins (sans-serif) - weights 400, 500, 600

### Type Scale (Desktop)

| Style | Font | Size | Weight | Line Height | Letter Spacing |
|-------|------|------|--------|-------------|----------------|
| H1 (Hero) | Lora | 79px | 400 | 81px | -0.8px |
| H2 (Section) | Lora | 64px | 400 | 74px | -0.7px |
| H3 (Sub-section) | Lora | 60px | 400 | 65px | -0.7px |
| H4 (Card title) | Lora | 52px | 500 | 60px | -0.7px |
| H5 (Smaller heading) | Lora | 40px | 500 | 50px | -0.4px |
| H6 (Card label) | Lora | 36px | 500 | 46px | -0.7px |
| Subheading | Lora | 28px | 500 | 36px | -0.7px |
| Body Large | Poppins | 21px | 400 | 32px | -0.6px |
| Body | Poppins | 21px | 500 | 32px | -0.7px |
| Body Small | Poppins | 18px | 600 | 27px | n/a |
| Button | Poppins | 16px | 600 | 24px | n/a |
| Caption/Label | Poppins | 15px | 500 | 24px | -0.6px |
| Small Label | Poppins | 13px | 600 | n/a | 1.2px |
| Pricing Number | Lora | 80px | 500 | 81px | n/a |

### Tablet Breakpoint (max-width: 1024px)
- H1: 60px/64px
- H2: 56px/64px
- H3: 50px/54px
- H4: 42px/50px
- H5: 32px/40px
- H6: 28px/36px

### Mobile Breakpoint (max-width: 767px)
- H1: 54px/60px
- H2: 48px/58px
- H3: 42px/48px
- H4: 36px/44px
- H5: 28px/36px
- H6: 24px/32px

## Layout

- **Max container width:** 1200px (desktop), 1024px (tablet), 767px (mobile)
- **Default padding:** 16px horizontal
- **Section padding:** 60-120px vertical, 16px horizontal
- **Card border radius:** 20px (large), 12px (small/icon boxes)
- **Image border radius:** 24px (feature images)
- **Button border radius:** 64px (fully rounded pill)
- **Grid gaps:** 32px (cards), 56px (feature sections), 12px (icon grid)

## Button Styles

### Primary CTA
- Background: #ff555e (accent)
- Text: white
- Padding: 16px 24px
- Border radius: 64px (pill)
- Font: Poppins 16px/600

### Secondary/Outline
- Background: transparent
- Border: 2px solid #ff555e
- Text: #092a57 (secondary navy)
- Arrow icon on right side (row-reverse flex)

### Popup CTA (large)
- Background: #ff545d
- Text: #fafafa
- Font: Poppins 18px/500 uppercase, letter-spacing 3.38px
- Padding: 25px 55px
- Border radius: 100px
- Hover: background changes to #092a57

## Component Patterns

### Course Option Cards (2x2 grid)
- Border: 1px solid #918f8f
- Background: #fcfbfb
- Border radius: 20px
- Layout: number column (18.5% width) + content column
- Number: Lora 60px accent color (#ff555e)
- Title: Lora 40px navy (#092a57)

### Pricing Cards
- Background: #ecf4ff
- Border radius: 20px
- Padding: 40px top, 24px sides/bottom
- Counter number: Lora 80px blue (#224983)
- Label: Poppins 24px uppercase blue

### Icon Boxes (Benefits grid, 2x3)
- Background: #f6f6f6
- Border radius: 12px
- Padding: 16px
- Icon: 32px, color #1f4172 on circle background
- Title: Poppins 21px/500

### Testimonial Carousel
- Text: Lora 36px/500 navy, line-height 46px
- Name: Poppins 24px/500
- Navigation: arrows + bullet pagination

### Feature Sections (alternating)
- Two-column layout: image (24px radius, overflow hidden) + text
- Image has parallax scale effect (1.3x, out-in)
- Text side: heading + body + arrow button
- Alternate background colors between #fef5ef and white

## Image Assets (from existing page)

| Asset | URL |
|-------|-----|
| LCA Logo | https://www.emorrisonconsulting.com/wp-content/uploads/2024/10/Lay-Counselor-Academy-logo-home.png |
| Hero BG | https://www.emorrisonconsulting.com/wp-content/uploads/2024/09/lay-counselor-training-academy-hero.webp |
| What is Lay Counselor | https://www.emorrisonconsulting.com/wp-content/uploads/2025/03/what-is-a-lay-counselor-hero.png |
| LCA Hero 2 | https://www.emorrisonconsulting.com/wp-content/uploads/2024/09/lay-counselor-academy-hero-2.webp |
| YouTube Thumbnail | https://www.emorrisonconsulting.com/wp-content/uploads/2024/09/The-Empathy-Effect-YouTube-Thumbnail.webp |
| Book Cover (English) | https://www.emorrisonconsulting.com/wp-content/uploads/2024/10/lca-book-cover.png |
| Book Cover (Spanish) | https://www.emorrisonconsulting.com/wp-content/uploads/2024/10/book-cover-spanish-emc.png |
| Evaluation Report | https://www.emorrisonconsulting.com/wp-content/uploads/2025/04/lca-evaluation-report.png |
| T-shirt Mockup | https://www.emorrisonconsulting.com/wp-content/uploads/2026/04/lca-tshirt-mockup.jpg |
| Self-Paced Promo | https://www.emorrisonconsulting.com/wp-content/uploads/2026/03/lay-counselor-academy-self-paced.jpg |
| Press Logos | https://www.emorrisonconsulting.com/wp-content/uploads/2024/11/press-logos-new.jpg |
| Shapes BG | https://www.emorrisonconsulting.com/wp-content/uploads/2024/09/Shapes-dark.svg |
| Dots BG | https://www.emorrisonconsulting.com/wp-content/uploads/2024/10/dots2.svg |
| EM Consulting Logo | https://www.emorrisonconsulting.com/wp-content/uploads/2021/09/EM-Consulting-Logo-2025-v2.png |
| Elizabeth Headshot | https://www.emorrisonconsulting.com/wp-content/uploads/2021/09/elizabeth.png |

## Key External Links

- TeachFloor Self-Paced enrollment: https://app.teachfloor.com/the-lay-counselor-academy/c/31922
- TeachFloor Hybrid enrollment: https://app.teachfloor.com/the-lay-counselor-academy/c/31953
- YouTube channel: https://www.youtube.com/channel/UC9AfJJrLIpeZl0Liigh1UDA
- LinkedIn: https://www.linkedin.com/in/elizabeth-morrison-consulting/
- Book purchase (English): https://buy.stripe.com/28EbJ15fT4Ej47ag4tcMM06
- Book purchase (Spanish): https://buy.stripe.com/00w4gzcIl0o3avy5pPcMM05
- T-shirt purchase: https://buy.stripe.com/14AbJ10ZD3AfeLO2dDcMM07
- CHCF Report: https://www.chcf.org/wp-content/uploads/2025/04/LayCounselorAcademyEvaluation.pdf
- CHCF Summary: https://www.chcf.org/publication/lay-counselor-academy-evaluation-strengthening-behavioral-health-workforce/

## Press Coverage
- California Healthline: Asian Health Center approach
- Steinberg Institute: 2023 Champions
- Modesto Bee: Stanislaus County bold approach
- STAT News: Therapist shortage, lay counselors
- CHCF Blog: New workforce bridging gaps
