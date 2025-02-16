PREDEFINED_RESPONSES = {
    "pourquoi le but sd": """La science des données est un domaine en pleine expansion, au cœur de l'innovation, et c'est précisément ce qui m'attire. Je suis passionné par les mathématiques et l'informatique, et j'ai toujours aimé jouer avec les chiffres. Ce qui me motive particulièrement, c'est d'apprendre à « faire parler les données », à en extraire du sens et des informations utiles pour la prise de décision.
Je suis de près l'actualité de la data science, car c'est un secteur qui évolue constamment, et j'ai besoin de cette stimulation intellectuelle. Pour moi, la science des données est bien plus qu'un domaine technique : c'est une manière de comprendre et d'agir sur le monde grâce aux chiffres.""",
    
    "parcours": """J'ai commencé en terminale STI2D, que j'ai quittée en cours d'année, avant de passer par la piscine de l'école 42. Après un détour par l'entrepreneuriat et un diplôme à l'École Nationale des Scaphandriers, j'ai décidé de me réorienter vers la science des données.

Cette année, je prépare un DAEU B à distance avec l'objectif d'intégrer un BUT Sciences des Données, puis de poursuivre en master ou école d'ingénieur pour devenir data analyst. En parallèle, je me certifie en Python sur Coursera et développe un projet entrepreneurial dans le domaine du gaming et de l'informatique.""",

    "motivations": """Ma motivation principale vient de ma passion pour les mathématiques et l'analyse de données. Mon parcours atypique m'a permis de développer une grande capacité d'adaptation et une détermination sans faille. Je suis convaincu que la data science est l'avenir et je veux en faire partie."""
}

def get_predefined_response(message):
    """Get predefined response if available"""
    message = message.lower().strip()
    if "parcours" in message:
        return PREDEFINED_RESPONSES["parcours"]
    if "but sd" in message:
        return PREDEFINED_RESPONSES["pourquoi le but sd"]
    return None
