import streamlit as st
import requests
import qrcode
import zipfile
from io import BytesIO

# --- App Configuration ---
st.set_page_config(page_title="SnapFile", page_icon="📂")
st.title("📂 SnapFile")
st.markdown("Upload files to generate a download link. **Multiple files** will be zipped automatically. Link valid for **14 days**.")

# --- File Uploader ---
uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, help="Select multiple files to share as a ZIP folder. Max size 10 GB.")

if uploaded_files:
    if st.button("Generate QR Code"):
        
        with st.spinner("Processing & Uploading..."):
            try:
                # --- 1. Processing (Zip if needed) ---
                if len(uploaded_files) > 1:
                    # Create ZIP in memory
                    buffer = BytesIO()
                    with zipfile.ZipFile(buffer, "w") as z:
                        for file in uploaded_files:
                            z.writestr(file.name, file.getvalue())
                    buffer.seek(0)
                    filename = "archive.zip"
                    file_data = buffer.getvalue()
                else:
                    # Single file
                    filename = uploaded_files[0].name
                    file_data = uploaded_files[0].getvalue()

                # --- 2. Upload to transfer.sh ---
                # transfer.sh uses PUT requests: PUT https://transfer.sh/filename
                url = f"https://transfer.sh/{filename}"
                
                # Send PUT request with file data
                response = requests.put(url, data=file_data)
                
                # Check for HTTP errors
                if response.status_code != 200:
                    st.error(f"Upload failed: Server returned status code {response.status_code}")
                    st.code(response.text)
                    st.stop()

                # --- 3. Extract Link ---
                # transfer.sh returns the download link directly in the response body text
                download_link = response.text.strip()
                
                # --- 4. Generate QR Code ---
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(download_link)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                
                # Convert QR to bytes
                buf = BytesIO()
                img.save(buf)
                byte_im = buf.getvalue()
                
                # --- 5. Display Results ---
                st.success("File uploaded successfully!")
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(byte_im, caption="Scan to Download", width=200)
                with col2:
                    st.subheader("Download Link")
                    st.code(download_link, language="text")
                    st.info("⚠️ This file is valid for **14 days**.")
                    
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

# --- Footer ---
st.markdown("---")
st.caption("Powered by Streamlit & transfer.sh")