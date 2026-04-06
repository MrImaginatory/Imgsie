import streamlit as st
import io
from PIL import Image
from utils.image_utils import convert_image, FORMAT_EXTENSIONS, FORMAT_MIME, INPUT_EXTENSIONS
from utils.zip_utils import create_zip_archive

st.set_page_config(
    page_title="Imgsie",
    page_icon="🖼️",
    layout="wide"
)

# Initialize Session State
if "converted_files" not in st.session_state:
    st.session_state.converted_files = {}
if "conversion_stats" not in st.session_state:
    st.session_state.conversion_stats = {
        "total_original_size": 0,
        "total_converted_size": 0,
        "valid_files_count": 0,
        "processing_done": False
    }

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

st.title("🖼️ Imgsie")
st.markdown("##### Optimize your images for the web with professional-grade compression.")
st.write("")

# Sidebar Settings
with st.sidebar:
    st.image("https://www.gstatic.com/images/branding/product/2x/photos_96dp.png", width=80)
    st.header("Control Panel")

    st.subheader("🔄 Format")
    input_format = st.selectbox("Input Format", ["JPEG", "PNG", "WebP"])
    output_format = st.selectbox("Output Format", ["WebP", "JPEG", "PNG"])

    if input_format == output_format:
        st.warning("⚠️ Same input and output format — the image will be re-encoded with current settings.")

    st.divider()

    # Compression settings adapt to the chosen output format
    st.subheader("⚙️ Compression")
    compress_level = 6
    lossless = False

    if output_format == "PNG":
        compress_level = st.slider(
            "Compression Level",
            min_value=0, max_value=9, value=6,
            help="0 = no compression (fastest), 9 = maximum compression (slowest)."
        )
        quality = 80  # unused for PNG
        st.info("💡 PNG is always lossless.")
    elif output_format == "WebP":
        quality_placeholder = st.empty()
        method = st.radio(
            "Conversion Mode",
            ["Lossy (Smaller size)", "Lossless (Best quality)"],
            index=0,
            help="Lossy drastically reduces file size with minimal quality loss. Lossless keeps every pixel identical."
        )
        lossless = ("Lossless" in method)
        with quality_placeholder:
            quality = st.slider(
                "Compression Quality",
                min_value=0, max_value=100, value=80,
                help="75-85 is usually the sweet spot for WebP.",
                disabled=lossless,
                key="quality_slider"
            )
        if lossless:
            st.info("💡 **Lossless Mode:** Uses maximum compression effort.")
        else:
            st.caption(f"Currently targeting **{quality}%** quality.")
    else:  # JPEG
        quality = st.slider(
            "Compression Quality",
            min_value=0, max_value=100, value=80,
            help="Higher quality = larger file size. 75-85 is the sweet spot for JPEG.",
            key="quality_slider"
        )
        st.caption(f"Currently targeting **{quality}%** quality.")

    with st.expander("🛠️ Advanced: Resizing", expanded=False):
        st.write("Leave at 0 to keep original dimensions. If only one is set, aspect ratio is preserved.")
        target_width = st.number_input(
            "Target Width (px)",
            min_value=0, value=0,
            help="Set the desired width in pixels. 0 = Original width."
        )
        target_height = st.number_input(
            "Target Height (px)",
            min_value=0, value=0,
            help="Set the desired height in pixels. 0 = Original height."
        )

    st.divider()

    if output_format in ["JPEG", "WebP"]:
        preserve_exif = st.checkbox("Preserve EXIF Metadata", value=True, help="Keep photo data like camera settings and location.")
    else:
        preserve_exif = False
        st.caption("EXIF metadata is not applicable for PNG output.")

    st.divider()
    if st.button("🚀 Start Batch Conversion", width='stretch'):
        st.session_state.converted_files = {}
        st.session_state.conversion_stats = {
            "total_original_size": 0,
            "total_converted_size": 0,
            "valid_files_count": 0,
            "processing_done": False,
            "output_format": output_format,
        }
        st.session_state.conversion_stats["processing_done"] = True

# Main Interface
st.subheader("📤 Upload Queue")
uploaded_files = st.file_uploader(
    f"Choose {input_format} files",
    type=INPUT_EXTENSIONS[input_format],
    accept_multiple_files=True,
    help=f"Drag and drop or click to upload one or more {input_format} files."
)

if uploaded_files:
    # Validation and Stats
    valid_files = []
    skipped_files = []
    
    valid_extensions = tuple("." + ext for ext in INPUT_EXTENSIONS[input_format])
    for f in uploaded_files:
        if f.name.lower().endswith(valid_extensions):
            valid_files.append(f)
        else:
            skipped_files.append(f.name)

    if skipped_files:
        st.warning(f"⚠️ Skipping {len(skipped_files)} unsupported file(s): {', '.join(skipped_files)}")

    if not valid_files:
        if uploaded_files:
            st.error(f"No valid {input_format} files detected in the selection.")
        st.stop()

    # Success message
    st.success(f"Successfully staged **{len(valid_files)}** {input_format} image(s) for conversion to **{output_format}**.")
    
    # Check if we need to start processing
    if st.session_state.conversion_stats["processing_done"] and not st.session_state.converted_files:
        total_original_size = 0
        total_converted_size = 0
        
        # Progress Bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, uploaded_file in enumerate(valid_files):
            # Read bytes (seek to 0 first to be safe)
            uploaded_file.seek(0)
            file_bytes = uploaded_file.read()
            original_size = len(file_bytes)
            total_original_size += original_size
            
            # Convert
            status_text.text(f"Converting {uploaded_file.name}...")
            
            # Prepare resizing args
            res_w = target_width if target_width > 0 else None
            res_h = target_height if target_height > 0 else None
            
            try:
                converted_bytes, new_size, new_dims = convert_image(
                    file_bytes,
                    output_format=output_format.upper(),
                    quality=quality,
                    lossless=lossless,
                    compress_level=compress_level,
                    target_width=res_w,
                    target_height=res_h,
                    preserve_exif=preserve_exif
                )

                total_converted_size += new_size
                new_filename = uploaded_file.name.rsplit('.', 1)[0] + FORMAT_EXTENSIONS[output_format.upper()]
                
                # Store in session state
                st.session_state.converted_files[new_filename] = {
                    "bytes": converted_bytes,
                    "original_name": uploaded_file.name,
                    "original_size": original_size,
                    "new_size": new_size,
                    "new_dims": new_dims,
                    "original_bytes": file_bytes,
                    "input_format": input_format,
                    "output_format": output_format,
                }
                
            except Exception as e:
                st.error(f"Error converting {uploaded_file.name}: {str(e)}")
                continue
                
            # Update progress
            progress_bar.progress((i + 1) / len(valid_files))
            
        # Store final stats
        st.session_state.conversion_stats.update({
            "total_original_size": total_original_size,
            "total_converted_size": total_converted_size,
            "valid_files_count": len(valid_files),
            "processing_done": True
        })
        status_text.text("✨ Batch processing complete!")
        # st.balloons()
    
    with st.sidebar:
        st.divider()
        with st.expander("ℹ️ How it works", expanded=False):
            st.markdown("""
                1. **Select** input and output formats in the sidebar.
                2. **Upload** your images above.
                3. **Adjust** quality/compression and optional resize.
                4. **Run** conversion, then **Download** as ZIP!
            """)
        st.caption("Powered by Pillow & Streamlit")

    # Always render results from session state if available
    if st.session_state.converted_files:
        # Results Container
        with st.expander("Show Conversion Results", expanded=True):
            for filename, data in st.session_state.converted_files.items():
                # Display per-file stats in a clean row
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1.5])
                    with col1:
                        st.markdown(f"📄 **{data['original_name']}**")
                        st.caption(f"Original: {data['original_size']/1024:.1f} KB")
                    with col2:
                        savings = (1 - (data['new_size'] / data['original_size'])) * 100
                        savings_color = "#28a745" if savings > 30 else "#ffc107"
                        st.markdown(f"✨ **{filename}**")
                        st.markdown(f"<span style='color:{savings_color}; font-weight:bold;'>{data['new_size']/1024:.1f} KB (-{savings:.1f}%)</span>", unsafe_allow_html=True)
                    with col3:
                        show_preview = st.checkbox("🔍 Preview", key=f"prev_{filename}")
                
                # Enhanced Preview Section
                if show_preview:
                    p_col1, p_col2 = st.columns(2)
                    with p_col1:
                        with Image.open(io.BytesIO(data['original_bytes'])) as orig_img:
                            orig_w, orig_h = orig_img.size
                        st.image(data['original_bytes'], caption=f"Original {data.get('input_format', input_format)} ({orig_w}x{orig_h})", width='stretch')
                    with p_col2:
                        st.image(data['bytes'], caption=f"Converted {data.get('output_format', output_format)} ({data['new_dims'][0]}x{data['new_dims'][1]})", width='stretch')
                    st.divider()
                else:
                    st.write("---")
        
        # Summary Dashboard
        st.write("")
        st.subheader("📊 Performance Summary")
        s_col1, s_col2, s_col3 = st.columns(3)
        
        stats = st.session_state.conversion_stats
        with s_col1:
            st.metric("Images Processed", stats["valid_files_count"])
        with s_col2:
            reduction_kb = (stats["total_original_size"] - stats["total_converted_size"])/1024
            st.metric("Total Size Reduction", f"{reduction_kb:.1f} KB", delta=f"-{reduction_kb:.1f} KB", delta_color="normal")
        with s_col3:
            if stats["total_original_size"] > 0:
                avg_savings = (1 - (stats["total_converted_size"] / stats["total_original_size"])) * 100
                st.metric("Average Savings", f"{avg_savings:.1f}%")
            
        # Download Section
        st.divider()
        d_col1, d_col2 = st.columns(2)
        
        # Prepare file mapping for ZIP
        files_for_zip = {name: d["bytes"] for name, d in st.session_state.converted_files.items()}
        
        with d_col1:
            # Single ZIP download
            zip_data = create_zip_archive(files_for_zip)
            import datetime
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="📦 Download All as ZIP",
                data=zip_data,
                file_name=f"converted_{ts}.zip",
                mime="application/zip",
                width='stretch'
            )
            
        with d_col2:
            if stats["valid_files_count"] == 1:
                # Individual download if only one file
                filename = list(st.session_state.converted_files.keys())[0]
                st.download_button(
                    label=f"💾 Download {filename}",
                    data=st.session_state.converted_files[filename]["bytes"],
                    file_name=filename,
                    mime=FORMAT_MIME.get(st.session_state.conversion_stats.get("output_format", output_format).upper(), "image/webp"),
                    width='stretch'
                )
            else:
                st.info("💡 Use the ZIP button to download your collection.")

else:
    # Clear session state if no files uploaded to allow fresh start
    if st.session_state.get("conversion_stats", {}).get("processing_done"):
        st.session_state.converted_files = {}
        st.session_state.conversion_stats = {
            "total_original_size": 0,
            "total_converted_size": 0,
            "valid_files_count": 0,
            "processing_done": False
        }
    
    st.write("---")
    st.write(f"Upload your **{input_format}** images above to convert them to **{output_format}**.")
    st.info("💡 **Tip:** Select your formats in the sidebar, adjust compression settings, then click 'Start Batch Conversion' when ready.")
