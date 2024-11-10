# src/prompt.py
def prompt1(text):
    return (
        f"Extrayez les informations détaillées suivantes du texte :\n"
        f"Gardez le format de sortie de l'LLM comme spécifié ; si des données sont manquantes, insérez 'N/A' dans le champ.\n"
        f"1. Nom du projet : donnez le nom du projet\n"
        f"2. Numéro du RC : donnez le numéro de règlement de consultation\n"
        f"3. Date limite de soumission : donnez la date limite de soumission\n"
        f"4. Adresse : donnez l'adresse du projet\n"
        f"5. Visites obligatoires : listez les visites obligatoires\n"
        f"6. Objet de la consultation : donnez l'objet de la consultation\n"
        f"7. Votre lot : donnez les lots\n"
        f"8. Durée des marchés : donnez la durée des marchés\n"
        f"9. Nom de l'acheteur : donnez le nom de l'acheteur\n"
        f"10. Téléphone de l'acheteur : donnez le numéro de téléphone de l'acheteur\n"
        f"11. Mail de l'acheteur : donnez l'adresse mail de l'acheteur\n"
        f"\nTexte :\n{text}"
    )




def prompt2(text):
    return (
f'From the following text, generate a numbered list of To-Do items:\n\nText:\n{text}\n\nTo-Do List:\n1. '
    )

