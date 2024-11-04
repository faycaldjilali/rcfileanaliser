import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_project_fiche(db_path, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Connect to the SQLite database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Retrieve all projects from the database
        cursor.execute("SELECT * FROM project_info")
        project_info = cursor.fetchall()

        for project in project_info:
            (nom_du_projet, numero_du_rc, date_limite_de_soumission, 
            adresse, visites_obligatoires, objet_de_la_consultation, votre_lot, 
            duree_des_marches, nom_de_lacheteur, telephone_de_lacheteur, 
            mail_de_lacheteur) = project

            # Create a PDF for each project
            pdf_filename = f"{nom_du_projet.replace(' ', '_')}_fiche.pdf"
            pdf_path = os.path.join(output_folder, pdf_filename)

            # Create a PDF canvas
            c = canvas.Canvas(pdf_path, pagesize=letter)
            width, height = letter

            # Write project details to the PDF
            details = [
                f"Nom du projet: {nom_du_projet}",
                f"Numéro du RC: {numero_du_rc}",
                f"Date limite de soumission: {date_limite_de_soumission}",
                f"Adresse: {adresse}",
                f"Visites obligatoires: {visites_obligatoires}",
                f"Objet de la consultation: {objet_de_la_consultation}",
                f"Votre lot: {votre_lot}",
                f"Durée des marchés: {duree_des_marches}",
                f"Nom de l'acheteur: {nom_de_lacheteur}",
                f"Téléphone de l'acheteur: {telephone_de_lacheteur}",
                f"Mail de l'acheteur: {mail_de_lacheteur}"
            ]

            # Loop through details to print each line in PDF
            y_position = height - 50
            for detail in details:
                c.drawString(100, y_position, detail)
                y_position -= 20

            # Finalize the PDF
            c.showPage()
            c.save()

        print("Project fiches have been generated successfully.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the database connection is closed
        if conn:
            conn.close()


