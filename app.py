import streamlit as st
import requests
import qrcode
import zipfile
from io import BytesIO

# --- App Configuration ---
st.set_page_config(page_title="SnapFile", page_icon="📂")
st.title("📂 SnapFile")
st.markdown("Upload files to generate a download link. **Multiple files** will be zipped automatically. **Unlimited size**.")

# --- File Uploader ---
uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, help="Select multiple files to share as a ZIP folder. Max size Unlimited.")

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

                # --- 2. Upload to gofile.io ---
                # Step A: Get the best server
                server_response = requests.get("https://api.gofile.io/getServer")
                server_response.raise_for_status()
                server_data = server_response.json()
                
                if server_data.get("status") != "ok":
                    st.error("Failed to get upload server from Gofile.io")
                    st.stop()
                    
                server = server_data["data"]["server"]
                
                # Step B: Upload file
                upload_url = f"https://{server}.gofile.io/uploadFile"
                files = {"file": (filename, file_data)}
                
                response = requests.post(upload_url, files=files)
                response.raise_for_status()
                
                result = response.json()
                
                if result.get("status") == "ok":
                    download_link = result["data"]["downloadPage"]
                    
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
                        st.info("⚠️ Files are deleted if inactive (no downloads) for a period of time (usually 10+ days).")
                        
                else:
                    st.error("Upload failed: " + str(result))
                    
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

# --- Footer ---
st.markdown("---")
st.caption("Powered by Streamlit & Gofile.io")