import streamlit as st
import requests
import qrcode
import zipfile
from io import BytesIO

# --- App Configuration ---
st.set_page_config(page_title="SnapFile", page_icon="📂")
st.title("📂 SnapFile")
st.markdown("Upload files to generate a download link. **Multiple files** will be zipped automatically. Link valid for **60 minutes**.")

# --- File Uploader ---
uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, help="Select multiple files to share as a ZIP folder. Max size 100 MB.")

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
                    file_to_upload = ("archive.zip", buffer.getvalue())
                else:
                    # Single file
                    file_to_upload = (uploaded_files[0].name, uploaded_files[0].getvalue())

                # --- 2. Upload to tmpfiles.org ---
                url = "https://tmpfiles.org/api/v1/upload"
                files = {"file": file_to_upload}
                
                # Send POST request
                response = requests.post(url, files=files)
                response.raise_for_status()
                
                result = response.json()
                
                if result.get("status") == "success":
                    raw_link = result["data"]["url"]
                    # Transform to direct download link: tmpfiles.org/ -> tmpfiles.org/dl/
                    download_link = raw_link.replace("tmpfiles.org/", "tmpfiles.org/dl/")
                    
                    # --- 3. Generate QR Code ---
                    qr = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr.add_data(download_link)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    
                    # Convert QR to bytes
                    buf = BytesIO()
                    img.save(buf)
                    byte_im = buf.getvalue()
                    
                    # --- 4. Display Results ---
                    st.success("File uploaded successfully!")
                    
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.image(byte_im, caption="Scan to Download", width=200)
                    with col2:
                        st.subheader("Download Link")
                        st.code(download_link, language="text")
                        st.info("⚠️ This file is temporary and will be deleted after 60 minutes.")
                        
                else:
                    st.error("Upload failed: " + str(result))
                    
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

# --- Footer ---
st.markdown("---")
st.caption("Powered by Streamlit & tmpfiles.org")