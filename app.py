import streamlit as st
import requests
import qrcode
from io import BytesIO

# --- App Configuration ---
st.set_page_config(page_title="Quick Share", page_icon="📂")
st.title("📂 Secure File Share")
st.markdown("Upload a file to generate a **one-time** download link valid for **12 hours**.")

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose a file", help="Max size depends on Streamlit config (usually 200MB)")

if uploaded_file is not None:
    # Button to confirm upload
    if st.button("Generate QR Code"):
        
        with st.spinner("Uploading to file.io..."):
            try:
                # --- 1. Upload to file.io ---
                # file.io API url
                url = "https://file.io"
                
                # Payload: 'expires' sets the retention time (e.g., 12h, 1d, 1w)
                # 'autoDelete' is True by default on file.io (delete after 1 download)
                payload = {"expires": "12h"} 
                
                # Prepare file for upload
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                
                # Send POST request
                response = requests.post(url, data=payload, files=files)
                response.raise_for_status() # Raise error if upload failed
                
                # Extract link from JSON response
                result = response.json()
                if result.get("success"):
                    download_link = result["link"]
                    
                    # --- 2. Generate QR Code ---
                    qr = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr.add_data(download_link)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    
                    # Convert QR image to bytes for Streamlit
                    buf = BytesIO()
                    img.save(buf)
                    byte_im = buf.getvalue()
                    
                    # --- 3. Display Results ---
                    st.success("File uploaded successfully!")
                    
                    # Layout: QR code on left, details on right
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.image(byte_im, caption="Scan to Download", width=200)
                        
                    with col2:
                        st.subheader("Download Link")
                        st.code(download_link, language="text")
                        st.info("⚠️ This file will be deleted immediately after the first download or in 12 hours.")
                        
                else:
                    st.error("File.io reported an error.")
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- Footer ---
st.markdown("---")
st.caption("Powered by Streamlit & File.io")