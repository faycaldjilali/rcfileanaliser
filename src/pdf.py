# src/pdfreader.py


import os
import PyPDF2
import json
import csv
import cohere
import streamlit as st 
from src.prompt import prompt1 , prompt2
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
COHERE_API_KEY = os.getenv('COHERE_API_KEY')

# Initialize the Cohere client with the hidden API key
client = cohere.Client(COHERE_API_KEY)

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        return f"An error occurred: {e}"

# Extract project details from CR text
def extract_project_details_cr_pdf(text):
    prompt = prompt1(text)

    response = client.generate(
        model='command-r-plus-08-2024',
        prompt= prompt,
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

# Save data to JSON file
def save_json_to_file(data, pdf_path):
    base_name = os.path.basename(pdf_path)
    json_name = f"{os.path.splitext(base_name)[0]}_pdf_cr_synthes.json"
    json_path = os.path.join(os.path.dirname(pdf_path), json_name)

    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return json_path

# Generate numbered To-Do list
def generate_numbered_todo_list_pdf(text):
    prompt = prompt2(text)

    response = client.generate(
        model='command-r-plus-08-2024',
        prompt=prompt,
        temperature=0.7,
        max_tokens=2000,
    )

    todo_list = response.generations[0].text.strip()
    formatted_todo_list = [
        f"{i+1}. {item.strip()}"
        for i, item in enumerate(todo_list.split('\n'))
        if item.strip()
    ]
    return formatted_todo_list

# Save numbered To-Do list to CSV
def save_numbered_todo_list_to_csv(todo_list, pdf_path):
    base_name = os.path.basename(pdf_path)
    csv_name = f"{os.path.splitext(base_name)[0]}_pdf_todo_list.csv"
    csv_path = os.path.join(os.path.dirname(pdf_path), csv_name)

    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["To-Do List"])
            for item in todo_list:
                writer.writerow([item])
    except Exception as e:
        return f"An error occurred while saving CSV file: {e}"

    return csv_path



# Single PDF processing function
def process_single_pdf(pdf_path):
    # Extract text from the uploaded PDF file
    pdf_text = extract_text_from_pdf(pdf_path)

    # Extract CR project details and save as JSON
    cr_details = extract_project_details_cr_pdf(pdf_text)
    cr_json_path = save_json_to_file(cr_details, pdf_path)
    st.write(f"CR details saved to {cr_json_path}")

    # Generate To-Do list and save as CSV
    todo_list = generate_numbered_todo_list_pdf(pdf_text)
    csv_path = save_numbered_todo_list_to_csv(todo_list, pdf_path)
    st.write(f"To-Do list saved to {csv_path}")

    # Display extracted data and To-Do list in the UI
    st.subheader("Extracted Project Details")
    st.json(cr_details)

    st.subheader("Generated To-Do List")
    st.write("\n".join(todo_list))

    # Return paths of saved files for download
    return cr_json_path, csv_path
