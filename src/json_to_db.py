import json
import sqlite3
import os

def create_db_from_json_files(json_folder):
    # Step 1: Connect to SQLite database (or create it)
    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()

    # Step 2: Create the table structure if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_du_projet TEXT,
            numero_du_rc TEXT,
            date_limite_de_soumission TEXT,
            adresse TEXT,
            visites_obligatoires TEXT,
            objet_de_la_consultation TEXT,
            votre_lot TEXT,
            duree_des_marches TEXT,
            nom_de_lacheteur TEXT,
            telephone_de_lacheteur TEXT,
            mail_de_lacheteur TEXT
        )
    ''')

    # Step 3: Loop through all JSON files in the specified folder
    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):  # Check if the file is a JSON file
            file_path = os.path.join(json_folder, filename)
            
            # Load JSON data from the file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Step 4: Insert each project from the JSON file into the database
            for project in data.get("projects", []):  # Safely get 'projects' key in case it's missing
                cursor.execute('''
                    INSERT INTO projects (
                        nom_du_projet, numero_du_rc, date_limite_de_soumission,
                        adresse, visites_obligatoires, objet_de_la_consultation,
                        votre_lot, duree_des_marches, nom_de_lacheteur,
                        telephone_de_lacheteur, mail_de_lacheteur
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    project.get("Nom du projet"),
                    project.get("Numéro du RC"),
                    project.get("Date limite de soumission"),
                    project.get("Adresse"),
                    project.get("Visites obligatoires"),
                    project.get("Objet de la consultation"),
                    project.get("Votre lot"),
                    project.get("Durée des marchés"),
                    project.get("Nom de l'acheteur"),
                    project.get("Téléphone de l'acheteur"),
                    project.get("Mail de l'acheteur")
                ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Data from all JSON files has been inserted into the database successfully.")
