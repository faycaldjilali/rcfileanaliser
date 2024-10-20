import os
import streamlit as st
from src.zip_extractor import save_uploaded_file, extract_zip, delete_zip_files
from src.rc_handler import copy_r_files, copy_rc_files, create_zip_from_folder
from src.pdfreader import process_all_pdfs_in_folder
from src.rc_handler import delete_files_with_same_size
from src.docxreader import process_all_docx_in_folder
# Streamlit Interface for uploading ZIP files
st.title("ZIP File Processor")

# Directory paths (you may adjust these based on your environment)
zip_file_location = "./uploaded_zips/"
unzip_file_location = "./unzipped_files/"
rc_file_location = "./rc_files/"

# Ensure folders exist
os.makedirs(zip_file_location, exist_ok=True)
os.makedirs(unzip_file_location, exist_ok=True)
os.makedirs(rc_file_location, exist_ok=True)

# Upload ZIP file using Streamlit's file uploader
uploaded_file = st.file_uploader("Upload a ZIP file", type="zip")

# Main application logic
if uploaded_file is not None:
    # Save uploaded ZIP file
    zip_file_path = save_uploaded_file(uploaded_file, zip_file_location)

    # Extract uploaded ZIP file
    extract_zip(zip_file_path, unzip_file_location)

    # Delete ZIP files after extraction
    delete_zip_files(unzip_file_location)

    # Copy specific files based on keywords (Règlement de la consultation)
    keywords = ["Règlement de la consultation", "Reglement de consultation"]
    copy_r_files(unzip_file_location, rc_file_location, keywords)

    # Copy files matching 'rc' pattern
    copy_rc_files(unzip_file_location, rc_file_location)
    delete_files_with_same_size(rc_file_location)

    st.success("File processing completed!")

    # Create ZIP files for download
    unzip_zip_buffer = create_zip_from_folder(unzip_file_location)
    

    st.download_button(
        label="Download Unzipped Files",
        data=unzip_zip_buffer,
        file_name="unzipped_files.zip",
        mime="application/zip"
    )



    if st.button("Process RC Files"):
        if os.listdir(rc_file_location):
            process_all_pdfs_in_folder(rc_file_location)
            
            # Provide download links for JSON and CSV files
            json_files = [f for f in os.listdir(rc_file_location) if f.endswith('_pdf_cr_synthes.json')]
            csv_files = [f for f in os.listdir(rc_file_location) if f.endswith('_pdf_todo_list.csv')]
            
            process_all_docx_in_folder(rc_file_location)
            json_files = [f for f in os.listdir(rc_file_location) if f.endswith('_docx_cr_synthes.json')]
            csv_files = [f for f in os.listdir(rc_file_location) if f.endswith('_docx_todo_list.csv')]

            rc_zip_buffer = create_zip_from_folder(rc_file_location) 
            st.download_button(
            label="Download RC Files",
            data=rc_zip_buffer,
            file_name="rc_files.zip",
            mime="application/zip"   )
            st.success("files processing completed! JSON and CSV files are available for download.")
        else:
            st.warning("No RC files found in the RC Files directory.")
else:
    st.info("Please upload a ZIP file to begin processing.")