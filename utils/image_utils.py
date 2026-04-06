import io
import logging
from PIL import Image, ImageOps

# Output format metadata
FORMAT_EXTENSIONS = {
    "WEBP": ".webp",
    "JPEG": ".jpg",
    "PNG":  ".png",
}

FORMAT_MIME = {
    "WEBP": "image/webp",
    "JPEG": "image/jpeg",
    "PNG":  "image/png",
}

# Accepted input file extensions per format (keys match selectbox display names)
INPUT_EXTENSIONS = {
    "JPEG": ["jpg", "jpeg"],
    "PNG":  ["png"],
    "WebP": ["webp"],
}


def convert_image(
    image_bytes,
    output_format="WEBP",
    quality=80,
    lossless=False,
    compress_level=6,
    target_width=None,
    target_height=None,
    preserve_exif=True,
):
    """
    Converts image bytes to the specified output format.

    Args:
        image_bytes (bytes): Original image data.
        output_format (str): Target format — "WEBP", "JPEG", or "PNG".
        quality (int): Compression quality (0-100). Used for JPEG and lossy WebP.
        lossless (bool): Lossless compression (WebP only).
        compress_level (int): PNG compression level (0-9).
        target_width (int): Target width for resizing.
        target_height (int): Target height for resizing.
        preserve_exif (bool): Whether to keep EXIF metadata.

    Returns:
        tuple: (bytes, int, tuple) -> (Converted image bytes, new file size, new dimensions)
    """
    output_format = output_format.upper()
    try:
        img = Image.open(io.BytesIO(image_bytes))

        # Preserve orientation from EXIF
        img = ImageOps.exif_transpose(img)

        # Extract EXIF before any processing
        exif_data = img.info.get("exif") if preserve_exif else None

        # Handle resizing with aspect-ratio preservation
        if target_width or target_height:
            width, height = img.size
            if target_width and not target_height:
                target_height = int((target_width / width) * height)
            elif target_height and not target_width:
                target_width = int((target_height / height) * width)
            img = img.resize((target_width, target_height), Image.LANCZOS)

        # JPEG has no alpha channel — composite transparent pixels onto white
        if output_format == "JPEG":
            if img.mode == "P":
                img = img.convert("RGBA")
            if img.mode in ("RGBA", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode != "RGB":
                img = img.convert("RGB")
        elif img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        # Build format-specific save arguments
        output_buffer = io.BytesIO()

        if output_format == "WEBP":
            save_kwargs = {
                "format": "WEBP",
                "quality": quality,
                "lossless": lossless,
                "method": 6,
            }
            if exif_data:
                save_kwargs["exif"] = exif_data

        elif output_format == "JPEG":
            save_kwargs = {
                "format": "JPEG",
                "quality": quality,
                "optimize": True,
            }
            if exif_data:
                save_kwargs["exif"] = exif_data

        elif output_format == "PNG":
            save_kwargs = {
                "format": "PNG",
                "compress_level": compress_level,
                "optimize": True,
            }

        else:
            raise ValueError(f"Unsupported output format: {output_format}")

        img.save(output_buffer, **save_kwargs)

        converted_bytes = output_buffer.getvalue()
        return converted_bytes, len(converted_bytes), img.size

    except Exception as e:
        logging.error(f"Failed to convert image: {e}")
        raise ValueError(f"Image conversion failed: {str(e)}")
