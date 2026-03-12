# Stack Research

**Domain:** Image Processing / Web Tools
**Researched:** 2026-03-12
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python | 3.12.x | Runtime | Best balance of performance (Specialized Adaptive Interpreter) and ecosystem stability in 2026. |
| Streamlit | 1.45.0+ | App Framework | Standard for rapid Python web tools; enhanced state management for batch processing. |
| Pillow (PIL) | 11.0.0+ | Image Engine | Core library for image manipulation; optimized WebP encoding and secure metadata handling. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| zipfile | Standard | Archiving | Creating in-memory ZIP archives for batch downloads. |
| io | Standard | IO Handling | Processing images in-memory (BytesIO) for speed and privacy. |
| os | Standard | OS Utils | Path handling and environment interaction. |
| streamlit-image-comparison | Latest | UI Enhancement | Side-by-side comparison of original vs converted images. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| pytest | Testing | Unit tests for conversion logic. |
| ruff | Linting/Formatting | Fast and efficient code quality tool. |

## Installation

```bash
# Core
pip install streamlit pillow streamlit-image-comparison

# Dev dependencies
pip install pytest ruff
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Streamlit | Flask/FastAPI + React | For more complex, customized UI/UX requirements. |
| Pillow | OpenCV | For advanced computer vision tasks (overkill for simple conversion). |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Manual JPEG conversion | Error-prone and slow. | Pillow's optimized WebP encoder. |
| Storing uploads on disk | Privacy risks and cleanup overhead. | In-memory processing with BytesIO. |

## Sources

- Official Streamlit Documentation — verified state management patterns.
- Pillow (PIL) Documentation — verified WebP feature support.

---
*Stack research for: Image Processing / Web Tools*
*Researched: 2026-03-12*
