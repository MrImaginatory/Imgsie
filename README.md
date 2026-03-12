# 🖼️ JPEG to WebP Batch Converter

A professional-grade, web-based image conversion tool built with Streamlit that enables batch conversion of JPEG images to WebP format with advanced compression and customization options.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red.svg)
![Pillow](https://img.shields.io/badge/Pillow-10.x-green.svg)

## ✨ Features

- **Batch Conversion** - Convert multiple JPEG images to WebP simultaneously
- **Dual Conversion Modes**
  - Lossy Mode: Drastically reduces file size with minimal quality loss
  - Lossless Mode: Preserves every pixel with maximum compression
- **Quality Control** - Adjustable compression quality (0-100%)
- **Image Resizing** - Resize images by specifying target width and/or height (aspect ratio preserved)
- **EXIF Metadata Preservation** - Keep photo data like camera settings and location
- **Live Preview** - Side-by-side comparison of original and converted images
- **Performance Statistics** - Real-time metrics showing file count, size reduction, and savings percentage
- **Flexible Downloads** - Download individual files or batch ZIP archive

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Installation

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd "jpeg to webp"
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the Streamlit server:

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`.

## 📖 Usage Guide

### Step 1: Upload Images
- Click the file uploader or drag and drop JPEG files
- Supports multiple file selection
- Non-JPEG files are automatically skipped with a warning

### Step 2: Configure Settings (Sidebar)
- **Conversion Mode**: Choose between Lossy (smaller size) or Lossless (best quality)
- **Compression Quality**: Adjust slider (0-100) - 75-85 is the sweet spot
- **Advanced Resizing**: Set target width/height in pixels (0 = keep original)
- **EXIF Metadata**: Toggle to preserve or strip metadata

### Step 3: Convert
- Click "🚀 Start Batch Conversion" in the sidebar
- Watch the progress bar as files are processed
- Balloons appear on completion!

### Step 4: Review & Download
- Expand "Show Conversion Results" to see each converted file
- Click "Preview" to compare original vs. converted images
- View performance summary (total reduction, average savings)
- Download individually or as a ZIP archive

## 🛠️ Project Structure

```
jpeg to webp/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── utils/
│   ├── image_utils.py      # Image conversion logic
│   └── zip_utils.py        # ZIP archive creation
└── README.md               # This file
```

## 📦 Dependencies

| Package | Description |
|---------|-------------|
| [Streamlit](https://streamlit.io/) | Web framework for building data apps |
| [Pillow](https://pillow.readthedocs.io/) | Python Imaging Library for image processing |
| [watchdog](https://pythonhosted.org/watchdog/) | File system monitoring (optional) |

## 🔧 Technical Details

### Image Conversion (`utils/image_utils.py`)

The core conversion function:
- Opens JPEG images using Pillow
- Applies EXIF transpose for correct orientation
- Converts color modes (CMYK → RGB) as needed
- Resizes while maintaining aspect ratio
- Saves as WebP with configurable quality and method

### ZIP Creation (`utils/zip_utils.py`)

Creates in-memory ZIP archives for batch downloads without temporary files.

### Session State Management

The app uses Streamlit's session state to:
- Store converted files for download
- Track conversion statistics
- Manage the processing workflow

## 🎨 UI Features

- Custom gradient buttons for premium feel
- Responsive layout with sidebar controls
- Real-time progress indicators
- Color-coded savings display (green > 30%, yellow < 30%)
- Before/after image comparison

## 📝 License

This project is provided as-is for educational and personal use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Note**: WebP offers superior compression compared to JPEG, typically achieving 25-35% smaller file sizes at equivalent quality, making it ideal for web optimization.
