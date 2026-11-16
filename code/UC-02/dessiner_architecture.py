
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

dossier = Path(__file__).parent
sortie = dossier / "livrables"
sortie.mkdir(exist_ok=True)

image = Image.new("RGB", (1000, 1150), "white")
dessin = ImageDraw.Draw(image)

titre = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 30)
police = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 21)

etapes = [
    ("Sources TPCx-BB", "Ventes, produits, clients, magasins, dates, stocks"),
    ("Ingestion - NiFi", "Recuperation des fichiers"),
    ("Bronze - HDFS", "Conservation des donnees brutes"),
    ("Silver - Python / Spark", "Verification et preparation"),
    ("Gold", "Donnees preparees pour les KPI"),
    ("Analyses metier", "Suivi des ventes, produits et stocks")
]

dessin.text((120, 35), "Architecture proposee - UC-02",
            font=titre, fill="black")

y = 115

for nom, description in etapes:
    dessin.rounded_rectangle(
        (130, y, 870, y + 115),
        radius=15,
        fill="#E7EFF8",
        outline="#274C77",
        width=3
    )

    dessin.text((165, y + 20), nom, font=titre, fill="#183153")
    dessin.text((165, y + 70), description, font=police, fill="black")

    if nom != "Analyses metier":
        dessin.line((500, y + 115, 500, y + 155),
                    fill="black", width=4)
        dessin.line((490, y + 145, 500, y + 155, 510, y + 145),
                    fill="black", width=4)

    y += 165

dessin.text((125, 1100),
            "Qualite - Securite - Suivi des traitements",
            font=police, fill="#183153")

fichier = sortie / "UC02_schema_architecture.png"
image.save(fichier)

print("Schema cree :", fichier)
