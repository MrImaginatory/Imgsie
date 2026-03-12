# Research: Streamlit Image Converter (JPEG to WebP)

**Researched:** 2026-03-12
**Domain:** Image Processing & Streamlit Web Apps
**Confidence:** HIGH

## Summary

This research identifies the core components and libraries needed to build a batch JPEG to WebP converter using Streamlit and Pillow. The application will leverage in-memory processing to ensure speed and privacy, avoiding disk I/O for temporary files.

**Primary recommendation:** Use Python's `io.BytesIO` for all image handling and the `zipfile` library to bundle converted images for download.

---

## 10-Step Implementation Plan

This plan outlines the roadmap for creating the application, from environment setup to final deployment readiness.

1.  **Environment Setup & Dependencies**: Verify the existing `venv` and install `streamlit`, `Pillow`, and `watchdog`. This ensures a stable development environment.
2.  **Streamlit UI Skeleton**: Build the basic layout using `st.title`, `st.sidebar`, and `st.container`. Set up the page configuration (title, icon).
3.  **Batch File Upload**: Implement `st.file_uploader` with `accept_multiple_files=True`. Validate that uploaded files are JPEG format.
4.  **Core Image Processing Function**: Develop a function using `Pillow` to open a JPEG and save it as WebP into an `io.BytesIO` object.
5.  **Compression & Quality Settings**: Add a sidebar slider for WebP quality (0-100) and a toggle for Lossless vs. Lossy mode, passing these parameters to the conversion function.
6.  **Image Resizing Logic**: Implement target width/height inputs in the sidebar. Apply resizing using `Image.LANCZOS` while maintaining the aspect ratio.
7.  **Preview & Side-by-Side Comparison**: Create a preview section where users can see the original and converted images side-by-side (using `st.columns`) and compare file sizes/savings.
8.  **Batch Conversion Loop**: Orchestrate the conversion of all uploaded images, displaying a `st.progress` bar and status updates for each file.
9.  **ZIP Archive Generation**: Use `zipfile.ZipFile` and `io.BytesIO` to package all converted WebP images into a single in-memory ZIP archive.
10. **Final Download & Clean-up**: Implement the `st.download_button` for the ZIP file and individual images. Add final UX touches like success messages and "Clear All" functionality.

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| streamlit | Latest | Web UI | Rapid prototyping and built-in widget support. |
| Pillow | Latest | Image processing | The industry standard for Python image manipulation. |
| zipfile | Built-in | Archive generation | Part of standard library, reliable for ZIP creation. |
| io | Built-in | Memory management | Essential for diskless, in-memory processing. |

## Architecture Patterns

### Recommended Project Structure
```
.
├── .planning/           # All GSD planning docs
├── app.py               # Main Streamlit application
├── utils/
│   ├── image_utils.py   # Core conversion & resizing logic
│   └── zip_utils.py     # Archive generation
└── requirements.txt     # Dependency list
```

### Pattern: In-Memory Processing
Avoid saving images to the filesystem. Instead, use `io.BytesIO` to pass binary data between Pillow, Streamlit, and the ZIP archiver. This improves performance and simplifies cleanup.

## Common Pitfalls

- **Memory Overflow**: Processing too many large images at once might exceed RAM. *Solution: Process images sequentially, not in parallel, and clear references.*
- **Transparency Loss**: Converting formats with transparency to WebP can be tricky, though not an issue for JPEG. *Note: Keep it simple for JPEG-only v1.*
- **EXIF Stripping**: Pillow saves don't include EXIF by default. *Solution: Explicitly pass `exif=image.info.get('exif')` to `save()`.*

## Verification Plan

### Automated Tests
- Run `pytest` on conversion functions (once implemented).
- Verify WebP output validity using `imghdr`.

### Manual Verification
- Upload 5+ JPEGs and verify ZIP download contains 5+ WebP files.
- Compare file sizes reported in UI with actual downloaded file sizes.
- Test quality slider impact on output file size.
