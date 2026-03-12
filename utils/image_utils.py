import io
from PIL import Image

def convert_to_webp(image_bytes, quality=80, lossless=False, target_width=None, target_height=None, preserve_exif=True):
    """
    Converts image bytes to WebP format.
    
    Args:
        image_bytes (bytes): Original image data.
        quality (int): Compression quality (0-100).
        lossless (bool): Whether to use lossless compression.
        target_width (int): Target width for resizing.
        target_height (int): Target height for resizing.
        preserve_exif (bool): Whether to keep EXIF metadata.
        
    Returns:
        tuple: (bytes, int, tuple) -> (Converted image bytes, New file size, New dimensions)
    """
    img = Image.open(io.BytesIO(image_bytes))
    original_format = img.format
    
    # Handle resizing
    if target_width or target_height:
        width, height = img.size
        if target_width and not target_height:
            target_height = int((target_width / width) * height)
        elif target_height and not target_width:
            target_width = int((target_height / height) * width)
            
        img = img.resize((target_width, target_height), Image.LANCZOS)
    
    # Extract EXIF if requested and if it exists
    exif_data = img.info.get("exif") if preserve_exif else None
    
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
