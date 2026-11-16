from pathlib import Path
from pypdf import PdfWriter

source = Path("UC-01/livrables")
sortie = Path("Jour1/UC01_besoin_donnees.pdf")

fichiers = [
    "UC01_cadrage_metier.pdf",
    "UC01_questions_decisionnelles.pdf",
    "UC01_dictionnaire_KPI.pdf",
    "UC01_inventaire_sources.pdf",
    "UC01_qualification_donnees.pdf",
    "UC01_limites_et_hypotheses.pdf"
]

pdf = PdfWriter()

for nom in fichiers:
    chemin = source / nom
    if not chemin.exists():
        raise FileNotFoundError(f"Fichier absent : {chemin}")
    pdf.append(str(chemin))
    print("Ajout :", nom)

with sortie.open("wb") as fichier:
    pdf.write(fichier)

pdf.close()
print("PDF final créé :", sortie)
