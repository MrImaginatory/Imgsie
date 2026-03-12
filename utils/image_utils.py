import io
import logging
from PIL import Image, ImageOps

def convert_to_webp(image_bytes, quality=80, lossless=False, target_width=None, target_height=None, preserve_exif=True):
    """
    Converts image bytes to WebP format with optional resizing and metadata preservation.
    
    Returns:
        tuple: (bytes, int, tuple) -> (Converted image bytes, New file size, New dimensions)
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        
        # Preserve orientation if EXIF is present
        img = ImageOps.exif_transpose(img)
        
        # Extract EXIF before any processing
        exif_data = img.info.get("exif") if preserve_exif else None
        
        # Ensure image is in RGB or RGBA mode (e.g., convert CMYK to RGB)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")
        
        # Handle resizing while maintaining aspect ratio
        if target_width or target_height:
            width, height = img.size
            if target_width and not target_height:
                target_height = int((target_width / width) * height)
            elif target_height and not target_width:
                target_width = int((target_height / height) * width)
            # If both provided, we use them as-is, which might stretch 
            # (matches current behavior but documented now)
            
            img = img.resize((target_width, target_height), Image.LANCZOS)
        
        # Save to buffer
        output_buffer = io.BytesIO()
        save_kwargs = {
            "format": "WEBP",
            "quality": quality,
            "lossless": lossless,
            "method": 6 # High quality compression effort
        }
        
        if exif_data:
            save_kwargs["exif"] = exif_data
            
        img.save(output_buffer, **save_kwargs)
        
        converted_bytes = output_buffer.getvalue()
        return converted_bytes, len(converted_bytes), img.size
        
    except Exception as e:
        logging.error(f"Failed to convert image: {e}")
        raise ValueError(f"Image conversion failed: {str(e)}")
