def prompt1(text):
    return (
        f"Extract the following detailed information from the text:\n"
        f"1. Nom du projet\n"
        f"2. Numéro du RC\n"
        f"3. Description\n"
        f"4. Date limite de soumission\n"
        f"5. Adresse\n"
        f"6. Visites obligatoires\n"
        f"7. Objet de la consultation\n"
        f"8. Votre lot\n"
        f"9. Durée des marchés\n"
        f"10. Contact de l'acheteur (Nom, Titre, Téléphone, Courriel)\n"
        f"11. Acheteur\n\n"
        f"Synthèse des éléments pertinents :\n"
        f"Actions à prendre par SEF (Stores et Fermetures):\n"
        f"\nText:\n{text}"
    )



def prompt2(text):
    return (
f'From the following text, generate a numbered list of To-Do items:\n\nText:\n{text}\n\nTo-Do List:\n1. '
    )