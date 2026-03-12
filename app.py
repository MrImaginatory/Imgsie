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
    /* Global Styles */
    # .stApp {
    #     background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    # }
    
    /* Card-like container for the main content */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1000px;
    }

    /* Primary Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5rem;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        color: #fff;
        border: none;
    }

    /* Success/Download Button Styling */
    .stDownloadButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5rem;
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        color: white;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stDownloadButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        color: #fff;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        # background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #182848;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🖼️ JPEG to WebP Batch Converter")
st.markdown("##### Optimize your images for the web with professional-grade compression.")
st.write("")

# Sidebar Settings
with st.sidebar:
    st.image("https://www.gstatic.com/images/branding/product/2x/photos_96dp.png", width=80) # Placeholder for professional look
    st.header("Control Panel")
    st.write("Adjust output settings below.")
    
    quality_placeholder = st.empty()
    method = st.radio("Mode", ["Lossy", "Lossless"], index=0)
    lossless = (method == "Lossless")
    
    with quality_placeholder:
        quality = st.slider(
            "Quality", 
            min_value=0, max_value=100, value=80, 
            help="0 is smallest size, 100 is best quality.",
            disabled=lossless,
            key="quality_slider"
        )
    
    if lossless:
        st.info("💡 **Note:** Quality slider is disabled in Lossless mode as it uses maximum compression compression effort.")

    st.divider()
    
    st.subheader("Resizing (Optional)")
    target_width = st.number_input("Target Width", min_value=0, value=0, help="Leave 0 to keep original width.")
    target_height = st.number_input("Target Height", min_value=0, value=0, help="Leave 0 to keep original height.")
    
    st.divider()
    
    preserve_exif = st.checkbox("Preserve EXIF Metadata", value=True)

# Main Interface
uploaded_files = st.file_uploader(
    "Upload JPEG images", 
    type=["jpg", "jpeg"], 
    accept_multiple_files=True,
    help="Select one or more JPEG files to convert."
)

if uploaded_files:
    # Basic validation: ensure we only process JPEGs (Streamlit handles extension, but we can double check)
    valid_files = [f for f in uploaded_files if f.name.lower().endswith(('.jpg', '.jpeg'))]
    
    if len(valid_files) < len(uploaded_files):
        st.warning(f"⚠️ {len(uploaded_files) - len(valid_files)} file(s) were skipped because they are not JPEG format.")
    
    if not valid_files:
        st.error("No valid JPEG files found.")
        st.stop()

    st.info(f"Loaded {len(valid_files)} images for processing.")
    
    converted_files = {}
    total_original_size = 0
    total_converted_size = 0
    
    # Progress Bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Results Container
    with st.expander("Show Conversion Results", expanded=True):
        for i, uploaded_file in enumerate(valid_files):
            # Read bytes
            file_bytes = uploaded_file.read()
            original_size = len(file_bytes)
            total_original_size += original_size
            
            # Convert
            status_text.text(f"Converting {uploaded_file.name}...")
            
            # Prepare resizing args
            res_w = target_width if target_width > 0 else None
            res_h = target_height if target_height > 0 else None
            
            try:
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
            except Exception as e:
                st.error(f"Error converting {uploaded_file.name}: {str(e)}")
                continue
                
            # Update progress
            progress_bar.progress((i + 1) / len(valid_files))
            
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
