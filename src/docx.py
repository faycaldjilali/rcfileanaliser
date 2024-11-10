# src/docxreader.py



import os
import docx
import json
import csv
from src.prompt import prompt1 , prompt2
import streamlit as st 
import cohere
from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
COHERE_API_KEY = os.getenv('COHERE_API_KEY')

# Initialize the Cohere client with the hidden API key
client = cohere.Client(COHERE_API_KEY)
def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        return f"An error occurred: {e}"

def extract_project_details_cr_dox(text):
    prompt = prompt1(text)

    response = client.generate(
        model='command-r-plus-08-2024',
        prompt=prompt,
        temperature=0.7,
        max_tokens=1500
               
    )
    
    extracted_data = response.generations[0].text.strip()
    
    project_info = {}
    try:
        for line in extracted_data.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                project_info[key.strip()] = value.strip()
    except Exception as e:
        return f"An error occurred during parsing: {e}"

    return project_info

def save_json_to_file(data, docx_path, suffix='_cr_synthes.json'):
    # Create the file name with the provided suffix
    base_name = os.path.basename(docx_path)
    json_name = f"{os.path.splitext(base_name)[0]}{suffix}"
    json_path = os.path.join(os.path.dirname(docx_path), json_name)

    # Write the data to a JSON file
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return json_path

def generate_numbered_todo_list_docx(text):
    prompt = prompt2(text)
    response = client.generate(
        model='command-r-plus-08-2024',
        prompt=prompt ,
        temperature=0.7,
        max_tokens=1500
    )

    todo_list = response.generations[0].text.strip()
    
    formatted_todo_list = [
        f"{i+1}. {item.strip()}"
        for i, item in enumerate(todo_list.split('\n'))
        if item.strip()
    ]
    return formatted_todo_list

def save_numbered_todo_list_to_csv(todo_list, docx_path):
    base_name = os.path.basename(docx_path)
    csv_name = f"{os.path.splitext(base_name)[0]}_docx_todo_list.csv"
    csv_path = os.path.join(os.path.dirname(docx_path), csv_name)

    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["To-Do List"])
            for item in todo_list:
                writer.writerow([item])
    except Exception as e:
        return f"An error occurred while saving CSV file: {e}"

    return csv_path


# Single DOCX processing function
def process_single_docx(docx_path):
    # Extract text from the uploaded DOCX file
    docx_text = extract_text_from_docx(docx_path)

    # Extract CR project details and save as JSON
    cr_details = extract_project_details_cr_dox(docx_text)
    cr_json_path = save_json_to_file(cr_details, docx_path)
    st.write(f"CR details saved to {cr_json_path}")

    # Generate To-Do list and save as CSV
    todo_list = generate_numbered_todo_list_docx(docx_text)
    csv_path = save_numbered_todo_list_to_csv(todo_list, docx_path)
    st.write(f"To-Do list saved to {csv_path}")

    # Display extracted data and To-Do list in the UI
    st.subheader("Extracted Project Details")
    st.json(cr_details)

    st.subheader("Generated To-Do List")
    st.write("\n".join(todo_list))

    # Return paths of saved files for download
    return cr_json_path, csv_path
