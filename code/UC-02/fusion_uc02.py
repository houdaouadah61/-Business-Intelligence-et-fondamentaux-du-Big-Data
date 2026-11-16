from pathlib import Path
from pypdf import PdfWriter

source = Path("retail_project/retail_project/UC-02/livrables")
sortie = Path("Jour1/UC02_architecture.pdf")

fichiers = [
    "UC02_comparaison_architectures.pdf",
    "UC02_architecture_cible.pdf",
    "UC02_schema_flux.pdf",
    "UC02_positionnement_composants.pdf",
    "UC02_gouvernance.pdf",
    "UC02_local_vers_azure.pdf"
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
