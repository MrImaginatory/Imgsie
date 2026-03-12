# Streamlit Image Converter (JPEG to WebP)

## What This Is

A Streamlit-based web application that allows users to batch convert JPEG images to WebP format. It is designed for web developers and content creators who need to optimize images for performance while maintaining control over quality and dimensions.

## Core Value

Efficiently optimize batches of images for the web through high-quality, configurable WebP conversion.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Batch upload multiple JPEG images.
- [ ] Side-by-side preview of original vs. converted images for quality comparison.
- [ ] User-adjustable quality slider (0-100) for WebP compression.
- [ ] Support for both Lossy and Lossless WebP conversion modes.
- [ ] Option to resize images (width/height) before conversion.
- [ ] Download all converted images as a single ZIP archive.

### Out of Scope

- **Cloud Deployment**: Initial focus is on a local-only tool running via Streamlit. — User preference for local only.
- **Other Formats**: Support for PNG, GIF, or other input/output formats. — Kept focused on JPEG to WebP for simplicity and core value.
- **Advanced Editing**: Filters, cropping, or color adjustments. — Out of scope for a conversion-focused tool.

## Context

- The user has already initialized a virtual environment named `venv`.
- The application will be built using Python and Streamlit.
- Image processing will likely rely on the Pillow (PIL) library.

## Constraints

- **Tech Stack**: Python, Streamlit — User specified.
- **Environment**: Local execution — User specified.
- **Dependencies**: Must work within the provided `venv`.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Streamlit | Rapid prototyping and easy-to-build UI for Python tools. | — Pending |
| Batch Processing | Higher utility for web optimization tasks. | — Pending |
| User Selectable Compression | Balancing quality vs. file size is subjective and use-case dependent. | — Pending |

---
*Last updated: 2026-03-12 after initialization*
