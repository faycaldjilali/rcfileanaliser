import os
import streamlit as st
from src.zip_extractor import save_uploaded_file, extract_zip, delete_zip_files
from src.rc_handler import copy_r_files, copy_rc_files, create_zip_from_folder , move_files
from src.pdfreader import process_all_pdfs_in_folder
from src.rc_handler import delete_files_with_same_size
from src.docxreader import process_all_docx_in_folder
from src.db import create_db_from_json_files
from src.dbtopdf import generate_project_fiche  # Import the function to generate PDFs
from src.docx import process_single_docx
from src.pdf import process_single_pdf
import shutil

# Streamlit Interface for uploading ZIP files
st.title("ZIP File Processor")

# Directory paths (you may adjust these based on your environment)
zip_file_location = "./uploaded_zips/"
unzip_file_location = "./unzipped_files/"
rc_file_location = "./rc_files/"
database="project.db"
project_folder="./project_folder/"
# Ensure folders exist
os.makedirs(zip_file_location, exist_ok=True)
os.makedirs(unzip_file_location, exist_ok=True)
os.makedirs(rc_file_location, exist_ok=True)

# Upload ZIP file using Streamlit's file uploader
uploaded_zip = st.file_uploader("Upload a ZIP file", type="zip")
uploaded_docx = st.file_uploader("Upload a DOCX file for processing", type="docx")
uploaded_pdf = st.file_uploader("Upload a PDF file for processing", type="pdf")



# Main application logic
if uploaded_zip is not None:
    # Save uploaded ZIP file
    zip_file_path = save_uploaded_file(uploaded_zip, zip_file_location)

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
            json_files += [f for f in os.listdir(rc_file_location) if f.endswith('_docx_cr_synthes.json')]
            csv_files += [f for f in os.listdir(rc_file_location) if f.endswith('_docx_todo_list.csv')]

            # Create database from JSON files
            create_db_from_json_files(rc_file_location, database)
            db_path = os.path.join(rc_file_location, database)
            generate_project_fiche(db_path, rc_file_location)
            # Generate project fiches (PDFs) from the database
            # Create a ZIP file for RC files including the database
            move_files(rc_file_location, project_folder)

            rc_zip_buffer = create_zip_from_folder(project_folder) 
            download_clicked = st.download_button(
                label="Download RC Files",
                data=rc_zip_buffer,
                file_name="rc_files.zip",
                mime="application/zip"
            )

            if download_clicked:
                shutil.rmtree(zip_file_location, ignore_errors=True)
                shutil.rmtree(unzip_file_location, ignore_errors=True)
                shutil.rmtree(rc_file_location, ignore_errors=True)
                shutil.rmtree(project_folder, ignore_errors=True)


                st.success("Folders deleted after download.")

            st.success("Files processing completed! JSON, CSV files, and the database are available for download.")
        else:
            st.warning("No RC files found in the RC Files directory.")
else:
    st.info("Please upload a ZIP file to begin processing.")



# PDF file uploader and processing
if uploaded_pdf is not None:
    # Save uploaded PDF file
    pdf_path = os.path.join(rc_file_location, uploaded_pdf.name)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_pdf.getbuffer())
    
    # Process the PDF file
    process_single_pdf(pdf_path)  # Make sure this function processes only the given file
    st.success("PDF file processed!")
            # Create database from JSON files
    create_db_from_json_files(rc_file_location,database)
    db_path = os.path.join(rc_file_location, database)
    generate_project_fiche(db_path, rc_file_location)
    # Button to save and download PDF output
    move_files(rc_file_location, project_folder)

    pdf_zip_buffer = create_zip_from_folder(project_folder)
    download_clicked=st.download_button(
        label="Download Processed PDF Output",
        data=pdf_zip_buffer,
        file_name="processed_pdf_output.zip",
        mime="application/zip"
    )
    if download_clicked:
        shutil.rmtree(project_folder)
        shutil.rmtree(rc_file_location)

# DOCX file uploader and processing
if uploaded_docx is not None:
    # Save uploaded DOCX file
    docx_path = os.path.join(rc_file_location, uploaded_docx.name)
    with open(docx_path, "wb") as f:
        f.write(uploaded_docx.getbuffer())
    
    # Process the DOCX file
    process_single_docx(docx_path)  # Make sure this function processes only the given file
    st.success("DOCX file processed!")
                # Create database from JSON files
    create_db_from_json_files(rc_file_location,database)
    db_path = os.path.join(rc_file_location, database)
    generate_project_fiche(db_path, rc_file_location)
    # Button to save and download DOCX output
    move_files(rc_file_location, project_folder)

    docx_zip_buffer = create_zip_from_folder(project_folder)
    st.download_button(
        label="Download Processed DOCX Output",
        data=docx_zip_buffer,
        file_name="processed_docx_output.zip",
        mime="application/zip"
    )