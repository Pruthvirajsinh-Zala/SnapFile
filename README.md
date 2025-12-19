# 📂 SnapFile

**SnapFile** is a simple, secure, and fast file sharing application built with [Streamlit](https://streamlit.io/). It allows you to upload files and folders, automatically zipping multiple files, and generates a QR code and download link for easy sharing.

Files are hosted on [tmpfiles.org](https://tmpfiles.org/) and are temporary.

## ✨ Features

-   **File Upload**: Upload any file up to **100 MB**.
-   **Folder Support**: Select multiple files to automatically create a Downloadable ZIP archive.
-   **QR Code Generation**: Instantly scan to download on mobile devices.
-   **Temporary Hosting**: Files are available for **60 minutes** before being automatically deleted.
-   **Privacy Focused**: One-time use links (provider dependent) and auto-deletion.

## 🚀 Getting Started

### Prerequisites

-   Python 3.8+
-   pip

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Pruthvirajsinh-Zala/SnapFile.git
    cd SnapFile
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Run the application:
    ```bash
    streamlit run app.py
    ```

## 🛠 Configuration

The application is configured via `.streamlit/config.toml`.
-   **maxUploadSize**: Set to `100` (MB) to match the provider limits.

## 📦 Dependencies

-   `streamlit` - Web framework
-   `requests` - HTTP client for API uploads
-   `qrcode` - QR code generator
-   `Pillow` - Image processing

## 📜 License

MIT License. See `LICENSE` for more information.
