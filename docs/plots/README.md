# docs/plots

<!-- RCC-MINI-README:START -->

## Purpose

Generated visual artifacts used by the README, blog, and reports to show accuracy trajectory, confusion behavior, feature growth, and summary graphics.

## S - Formal specification

Use this folder as generated-output documentation. Plot files should be regenerated from scripts/generate_plots.py when underlying logs or plotting logic changes.

## H - Hooks and integration edges

Consumes logs and evaluation summaries indirectly through plotting scripts; displayed by README and docs/blog.md.

## A - Artifacts

PNG plot artifacts including accuracy trajectory, per-class evolution, plateau analysis, confusion matrix, session timeline, hard-class progression, feature growth, and summary infographic.

## T - Theory or method basis

Plots visualize experimental traces; they do not independently validate classifier performance without the underlying evaluation logs and methodology notes.

## I - Invariants

- Do not hand-edit plot images.
- Do not cite plots without methodology context.
- Regenerate plots when logs or visualization logic change.

## E - Example

Run python scripts/generate_plots.py from the repo root when plot artifacts need refresh.

<!-- RCC-MINI-README:END -->
