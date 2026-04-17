# Logo Styles Reference

Present these options when the user asks "what styles are available?" or wants guidance
on choosing a logo style. Each style includes a brief description, when it works best,
and well-known examples for reference.

---

## 1. Minimalist with Negative Space ⭐ (Default)

**Description:** Clean, geometric forms where the empty space between shapes reveals a
hidden symbol or second meaning. Less is more — every element earns its place.

**Best for:** Tech, modern brands, products that value cleverness and sophistication.

**Famous examples:** FedEx (arrow between E and x), NBC (peacock in negative space),
Toblerone (bear in mountain), WWF (panda).

**SVG characteristics:** Simple paths, 2-3 colors max, heavy use of clip-paths or
overlapping shapes to create the negative space effect.

---

## 2. Geometric / Abstract

**Description:** Pure geometric shapes (circles, triangles, squares, polygons) combined
into abstract forms. No literal representation — meaning comes from form and color.

**Best for:** Tech companies, startups, brands wanting a modern/forward-looking feel.

**Famous examples:** Airbnb (bélo), Google Drive, Mitsubishi (three diamonds), Mastercard.

**SVG characteristics:** Basic shape elements, gradients optional, symmetry important.

---

## 3. Wordmark / Logotype

**Description:** The brand name itself IS the logo, rendered in a distinctive typeface
(custom or modified). No separate icon.

**Best for:** Brands with short, distinctive names; companies wanting name recognition first.

**Famous examples:** Google, Coca-Cola, FedEx, Disney, Supreme.

**SVG characteristics:** Text paths (converted to outlines), custom letter modifications,
careful kerning. May include subtle symbol integration within letterforms.

---

## 4. Lettermark / Monogram

**Description:** Initials or a single letter, stylized into a compact symbol. Works
especially well when the full name is long.

**Best for:** Companies with long names, luxury brands, institutions.

**Famous examples:** IBM, HBO, CNN, Louis Vuitton (LV), Chanel (CC).

**SVG characteristics:** Interlocking or overlapping letterforms, often within a geometric
container (circle, square, shield).

---

## 5. Emblem / Badge

**Description:** Text enclosed within a shape (circle, shield, crest). Has a traditional,
established, authoritative feel.

**Best for:** Schools, government, breweries, sports teams, heritage brands.

**Famous examples:** Starbucks, Harley-Davidson, NFL, Harvard, BMW.

**SVG characteristics:** Circular or shield-shaped container, text on path (curved),
layered elements, potentially more complex than other styles.

---

## 6. Mascot

**Description:** A character (human, animal, or object) that represents the brand.
Friendly, approachable, memorable.

**Best for:** Family brands, food/beverage, sports teams, brands targeting younger audiences.

**Famous examples:** Mailchimp (Freddie), Duolingo (Duo), KFC (Colonel), Michelin (Bibendum).

**SVG characteristics:** More complex paths, character illustration, may need a simplified
icon variant for small sizes. Harder to execute well in pure SVG code generation —
consider keeping the mascot very geometric/stylized.

---

## 7. Line Art / Continuous Line

**Description:** Single-weight strokes forming the logo, often in a continuous or near-continuous
line. Elegant, modern, slightly artistic.

**Best for:** Creative agencies, studios, cafés, personal brands, lifestyle brands.

**Famous examples:** Airbnb (partly), many boutique/artisan brands.

**SVG characteristics:** Stroke-based paths (no fill), consistent stroke-width, potentially
a single `<path>` element for the continuous line effect.

---

## 8. Gradient / Dimensional

**Description:** Uses color gradients to create depth, dimension, or a sense of motion.
More vibrant and dynamic than flat styles.

**Best for:** Tech platforms, social media, entertainment, brands wanting energy and modernity.

**Famous examples:** Instagram, Firefox, iTunes, Tinder.

**SVG characteristics:** `<linearGradient>` or `<radialGradient>` elements, often on
simple base shapes. Can get visually rich with minimal geometry.

---

## 9. Hand-Drawn / Organic

**Description:** Imperfect, human-touched strokes that feel crafted rather than computed.
Warm, authentic, approachable.

**Best for:** Artisan brands, organic/natural products, indie studios, personal brands.

**Famous examples:** Innocent Drinks, Etsy (older logo), many craft brewery logos.

**SVG characteristics:** Irregular paths with slight wobble (randomized control points),
varied stroke widths. Harder to make look intentional in code — use subtle noise.

---

## 10. Responsive / Adaptive Logo System

**Description:** Not a single logo but a system of variants that adapt to context:
full lockup → horizontal → icon → favicon. Increasingly the standard for digital-first brands.

**Best for:** Any brand with significant digital presence. This is really an approach
rather than a style — it can be combined with any of the above.

**Famous examples:** Responsive logos by Google, Spotify, most modern tech companies.

**SVG characteristics:** Generate multiple SVG files — one per variant. Share the same
core geometry across variants.

---

## Choosing a Style

When helping the user choose, consider these factors:

| Factor | Recommendation |
|--------|---------------|
| Name is short (≤6 chars) | Wordmark or Lettermark work well |
| Name is long | Lettermark or abstract icon + separate wordmark |
| Digital-first product | Minimalist, Geometric, or Gradient (needs to work as app icon) |
| Traditional/established feel | Emblem or Wordmark |
| Playful/approachable | Mascot or Hand-drawn |
| Premium/luxury | Minimalist, Lettermark, or thin Line Art |
| Multiple contexts needed | Responsive system with any base style |
