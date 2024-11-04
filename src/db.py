


import sqlite3
import json
import os
import glob
def create_db_from_json_files(folder_path):

    # Path to the folder containing JSON files
    # Replace with your folder path

    # Define the path to save the database file in the same folder
    db_path = os.path.join(folder_path, 'example.db')

    # Connect to SQLite database (or create it)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table if it doesn't already exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS project_info (
        project_name TEXT,
        rc_number TEXT,
        submission_deadline TEXT,
        address TEXT,
        mandatory_visits TEXT,
        consultation_subject TEXT,
        your_lot TEXT,
        contract_duration TEXT,
        buyer_name TEXT,
        buyer_phone TEXT,
        buyer_email TEXT
    )
    ''')

    # Loop through each JSON file in the folder
    for json_file_path in glob.glob(os.path.join(folder_path, '*.json')):
        # Read data from the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Prepare data for insertion
        values = (
            data.get("1. Nom du projet"),
            data.get("2. Numéro du RC"),
            data.get("3. Date limite de soumission"),
            data.get("4. Adresse"),
            data.get("5. Visites obligatoires"),
            data.get("6. Objet de la consultation"),
            data.get("7. Votre lot"),
            data.get("8. Durée des marchés"),
            data.get("9. Nom de l'acheteur"),
            data.get("10. Téléphone de l'acheteur"),
            data.get("11. Mail de l'acheteur")
        )

        # Insert data into the table
        cursor.execute('''
        INSERT INTO project_info (
            project_name, rc_number, submission_deadline, address, mandatory_visits,
            consultation_subject, your_lot, contract_duration, buyer_name, buyer_phone, buyer_email
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', values)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print(f"All JSON files in the folder have been processed and data inserted into the database at {db_path}.")
