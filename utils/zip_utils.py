import io
import zipfile

def create_zip_archive(files_dict):
    """
    Creates a ZIP archive in memory.
    
    Args:
        files_dict (dict): Mapping of filenames to bytes { "file1.webp": b'...' }.
        
    Returns:
        bytes: The ZIP archive data as bytes.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for filename, content in files_dict.items():
            zip_file.writestr(filename, content)
            
    return zip_buffer.getvalue()
