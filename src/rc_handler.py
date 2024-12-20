# src/rc_handler.py

import os
import shutil
import re
import streamlit as st
import zipfile
import io
def copy_r_files(source_dir, target_dir, keywords):
    os.makedirs(target_dir, exist_ok=True)

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if any(keyword.lower() in file.lower() for keyword in keywords):
                file_path = os.path.join(root, file)
                destination_file_path = os.path.join(target_dir, file)
                shutil.copy(file_path, destination_file_path)
                st.write(f"Copied {file_path} to {destination_file_path}")

def copy_rc_files(source_dir, target_dir):
    os.makedirs(target_dir, exist_ok=True)

    pattern = r'(^|[_\.\s])rc([_\.\s]|$)'
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if re.search(pattern, os.path.splitext(file)[0], re.IGNORECASE):
                file_path = os.path.join(root, file)
                destination_file_path = os.path.join(target_dir, file)
                shutil.copy(file_path, destination_file_path)
                st.write(f"Copied {file_path} to {destination_file_path}")


def delete_files_with_same_size(directory):
    file_sizes = {}
    files_to_delete = set()

    # Iterate over files in the directory
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        size = os.path.getsize(file_path)

        # Check if this size is already seen
        if size in file_sizes:
            # If size is the same, add the new file to delete list
            files_to_delete.add(file_path)

    # Delete files
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Deleted {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
            


def move_files(source_folder, destination_folder):
    """
    Moves all files from the source folder to the destination folder.
    
    Args:
    - source_folder (str): The path of the folder to move files from.
    - destination_folder (str): The path of the folder to move files to.
    """
    # Create the destination folder if it does not exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Loop through each file in the source folder
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)
        destination_path = os.path.join(destination_folder, filename)

        # Move the file to the destination folder
        shutil.move(source_path, destination_path)

    print(f"Files have been moved from '{source_folder}' to '{destination_folder}'")



    
    # Call the move_files function


def create_zip_from_folder(folder_path):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zip_file.write(file_path, arcname)
    buffer.seek(0)
    return buffer
