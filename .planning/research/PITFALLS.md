# Pitfalls Research: Streamlit Image Converter (JPEG to WebP)

This document identifies potential technical and user experience pitfalls during the development of the Streamlit Image Converter, along with recommended mitigation strategies.

## Critical Pitfalls

| Pitfall | Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| **Memory Exhaustion** | Processing large batches of high-resolution images in-memory can cause the Streamlit server or local machine to run out of RAM. | Implement a batch-size limit or provide a warning for large uploads. Consider processing one image at a time and clearing Pillow objects immediately after use. |
| **EXIF Data Handling** | Default Pillow `save()` often strips EXIF/IPTC metadata (e.g., orientation, location). This can lead to rotated images or loss of critical photo info. | Explicitly extract and re-inject EXIF data using `img.info.get('exif')` and the `exif=` parameter in the `save()` method. |
| **UI Blocking** | Heavy image processing is CPU-bound. If done in the main Streamlit thread, the UI will freeze and become unresponsive. | Use `st.spinner` or `st.status` to indicate processing. For extremely long tasks, use standard Python `multiprocessing` or `threading` (though Streamlit's execution model requires care with threading). |
| **Aspect Ratio Distortion** | Resizing images without maintaining aspect ratio results in "squashed" or "stretched" visuals. | Implement a "Maintain Aspect Ratio" toggle. Calculate the new height/width based on the original ratio if only one dimension is provided. |

## Technical Debt

| Debt Area | Risk | Mitigation |
| :--- | :--- | :--- |
| **Ignoring Unit Tests** | Image processing logic (quality vs size, resizing logic, metadata) is prone to edge-case bugs that are hard to catch manually. | Create a dedicated `tests/` directory and use `pytest`. Mock image files to verify that the processor handles various dimensions and quality settings correctly. |
| **Hardcoding Settings** | Hardcoding default quality or dimensions makes the tool less flexible for different use cases. | Use constants in a `config.py` or `settings.py` file and allow user overrides via the UI. |
| **In-Memory ZIP Complexity** | Building a ZIP archive entirely in-memory can be tricky with pointer management and `BytesIO` positioning. | Use a clean utility function with a `with zipfile.ZipFile(...) as zf:` context manager and ensure `.seek(0)` is called correctly on the final buffer. |

## UX Pitfalls

| Pitfall | User Impact | Mitigation |
| :--- | :--- | :--- |
| **Lack of Progress Indicators** | In batch mode, the user may think the app has crashed if there is no feedback for 30+ seconds. | **Mandatory**: Use `st.progress()` to show real-time completion status during batch conversion. |
| **Overwhelming Preview** | Previewing 100+ side-by-side images will make the page extremely long and slow to render. | Only preview the *first* image or a small subset (e.g., top 3) to give the user a sense of quality before the full batch process. |
| **Vague Error Messages** | "An error occurred" during conversion is unhelpful if a specific JPEG is corrupted. | Use `try-except` blocks around individual image processing. Log the error and notify the user which specific file failed while continuing with the rest of the batch. |
| **Hidden Download Button** | If the download button only appears *after* a long process, users might navigate away. | Provide clear status messages ("Preparing ZIP...") so the user knows to wait for the final button. |
