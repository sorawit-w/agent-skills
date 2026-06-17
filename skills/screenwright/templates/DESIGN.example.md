---
version: alpha
name: Example Project
description: A clean, calm SaaS look — high-contrast neutrals with a single warm accent.
colors:
  primary: "#c2410c"      # brand hero — CTAs, headlines, emphasis
  secondary: "#1f2937"    # supporting ink
  tertiary: "#0e7490"     # accent / highlight, NOT the hero
  neutral: "#6b7280"      # muted text, borders
  surface: "#ffffff"      # default page background
  on-surface: "#1f2937"   # default text on surface
  error: "#b91c1c"        # semantic error
typography:
  h1:
    fontFamily: "ui-sans-serif, system-ui, sans-serif"
    fontSize: 40px
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: -0.02em
  body-md:
    fontFamily: "ui-sans-serif, system-ui, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  label-sm:
    fontFamily: "ui-monospace, monospace"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.04em
rounded:
  none: 0
  sm: 4px
  md: 8px
  lg: 16px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  "2xl": 48px
# ── screenwright extension keys (optional; defaulted when absent) ──
a11y:
  wcag: "2.2-AA"
breakpoints:
  mobile: 390
  tablet: 768
  desktop: 1280
---

# Example Project — DESIGN.md

## Overview

A calm, professional SaaS surface: spacious, high-contrast, one warm accent doing the
emphasis work. Should feel trustworthy and uncluttered, never loud.

## Colors

High-contrast neutrals rooted in near-black ink on white, with a single burnt-orange accent
reserved for the one most important action per screen.

- **Primary (#c2410c):** the single primary CTA / key emphasis. Never more than one per view.
- **Secondary (#1f2937):** body ink, headings.
- **Tertiary (#0e7490):** links, secondary highlights — not the hero.
- **Neutral (#6b7280):** muted captions, borders, placeholders.

## Typography

System sans for narrative; monospace for small technical labels.

- **Headlines (h1):** semibold, tight leading.
- **Body (body-md):** regular, generous 1.6 line-height for readability.
- **Labels (label-sm):** mono, slight letter-spacing.

## Layout

Fluid single column on mobile; fixed max-width ~1120px centered on desktop. 8px spacing
scale with a 4px half-step. Group with 24px internal padding.

## Shapes

Soft but architectural: 4px on inputs, 8px on cards, 16px on hero containers. Don't mix
sharp and round in one view.

## Do's and Don'ts

- Do use `primary` for only the single most important action per screen.
- Do maintain WCAG 2.2-AA contrast (4.5:1 normal text, 3:1 large).
- Do give every interactive control a visible focus indicator.
- Don't use more than two font weights on one screen.
- Don't mix rounded and sharp corners in the same view.

## Voice

- Plain language over jargon.
- Confident, not loud.
- Short sentences; let whitespace carry calm.
