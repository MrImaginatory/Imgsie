import streamlit as st
import io
from PIL import Image
from utils.image_utils import convert_to_webp
from utils.zip_utils import create_zip_archive

st.set_page_config(
    page_title="JPEG to WebP Converter",
    page_icon="🖼️",
    layout="wide"
)

# Custom CSS for premium feel
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .stDownloadButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #28a745;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🖼️ JPEG to WebP Batch Converter")
st.markdown("Optimize your images for the web in seconds.")

# Sidebar Settings
with st.sidebar:
    st.header("Settings")
    
    quality = st.slider("Quality", min_value=0, max_value=100, value=80, help="0 is smallest size, 100 is best quality.")
    method = st.radio("Mode", ["Lossy", "Lossless"], index=0)
    lossless = (method == "Lossless")
    
    st.divider()
    
    st.subheader("Resizing (Optional)")
    target_width = st.number_input("Target Width", min_value=0, value=0, help="Leave 0 to keep original width.")
    target_height = st.number_input("Target Height", min_value=0, value=0, help="Leave 0 to keep original height.")
    
    st.divider()
    
    preserve_exif = st.checkbox("Preserve EXIF Metadata", value=True)

# Main Interface
uploaded_files = st.file_uploader("Upload JPEG images", type=["jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    st.info(f"Loaded {len(uploaded_files)} images.")
    
    converted_files = {}
    total_original_size = 0
    total_converted_size = 0
    
    # Progress Bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Results Container
    with st.expander("Show Conversion Results", expanded=True):
        for i, uploaded_file in enumerate(uploaded_files):
            # Read bytes
            file_bytes = uploaded_file.read()
            original_size = len(file_bytes)
            total_original_size += original_size
            
            # Convert
            status_text.text(f"Converting {uploaded_file.name}...")
            
            # Prepare resizing args
            res_w = target_width if target_width > 0 else None
            res_h = target_height if target_height > 0 else None
            
            converted_bytes, new_size, new_dims = convert_to_webp(
                file_bytes, 
                quality=quality, 
                lossless=lossless,
                target_width=res_w,
                target_height=res_h,
                preserve_exif=preserve_exif
            )
            
            total_converted_size += new_size
            new_filename = uploaded_file.name.rsplit('.', 1)[0] + ".webp"
            converted_files[new_filename] = converted_bytes
            
            # Display per-file stats
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{uploaded_file.name}** → {new_filename}")
            with col2:
                savings = (1 - (new_size / original_size)) * 100
                st.write(f"Size: {original_size/1024:.1f}KB → {new_size/1024:.1f}KB")
            with col3:
                st.write(f"**{savings:.1f}% saved**")
            
            # Preview Toggle
            if st.checkbox(f"Show Preview for {uploaded_file.name}", key=f"prev_{uploaded_file.name}"):
                p_col1, p_col2 = st.columns(2)
                with p_col1:
                    st.image(file_bytes, caption="Original (JPEG)", use_container_width=True)
                with p_col2:
                    st.image(converted_bytes, caption="Converted (WebP)", use_container_width=True)
                st.divider()
                
            # Update progress
            progress_bar.progress((i + 1) / len(uploaded_files))
            
    status_text.text("Batch processing complete!")
    
    # Summary Dashboard
    st.divider()
    s_col1, s_col2, s_col3 = st.columns(3)
    with s_col1:
        st.metric("Images Processed", len(uploaded_files))
    with s_col2:
        st.metric("Total Size Reduction", f"{(total_original_size - total_converted_size)/1024:.1f} KB")
    with s_col3:
        avg_savings = (1 - (total_converted_size / total_original_size)) * 100
        st.metric("Average Savings", f"{avg_savings:.1f}%")
        
    # Download Section
    st.divider()
    d_col1, d_col2 = st.columns(2)
    
    with d_col1:
        # Single ZIP download
        zip_data = create_zip_archive(converted_files)
        st.download_button(
            label="Download All as ZIP",
            data=zip_data,
            file_name="converted_images.zip",
            mime="application/zip"
        )
        
    with d_col2:
        if len(uploaded_files) == 1:
            # Individual download if only one file
            filename = list(converted_files.keys())[0]
            st.download_button(
                label=f"Download {filename}",
                data=converted_files[filename],
                file_name=filename,
                mime="image/webp"
            )
        else:
            st.info("Use the ZIP button to download all images at once.")

else:
    st.write("---")
    st.write("Upload some images in the section above to get started.")
    
    # Feature Showcase (Static)
    st.info("💡 **Tip:** You can adjust the quality slider in the sidebar to find the best balance between file size and visual clarity.")
