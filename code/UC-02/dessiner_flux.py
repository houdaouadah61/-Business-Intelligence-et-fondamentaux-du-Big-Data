from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

dossier = Path(__file__).parent
sortie = dossier / "livrables"
sortie.mkdir(exist_ok=True)

image = Image.new("RGB", (1200, 900), "white")
dessin = ImageDraw.Draw(image)

titre = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 28)
police = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)

# Titre
dessin.text((360, 30), "Schema des flux de donnees - UC-02", font=titre, fill="black")

# Boites
boites = [
    ("Sources", (70, 140, 290, 260), "store_sales.dat\nitem.dat\ncustomer.dat\nstore.dat\ndate_dim.dat\ninventory.dat"),
    ("NiFi", (360, 160, 560, 240), "Chargement des fichiers"),
    ("Bronze", (650, 110, 980, 200), "Donnees brutes"),
    ("Silver", (650, 260, 980, 350), "Verification\net preparation"),
    ("Gold", (650, 410, 980, 500), "Donnees pretes\npour les KPI"),
    ("Analyses", (650, 570, 980, 680), "Ventes\nProduits\nMagasins\nStocks")
]

for nom, coords, texte in boites:
    dessin.rounded_rectangle(coords, radius=15, fill="#E7EFF8", outline="#274C77", width=3)
    x1, y1, x2, y2 = coords
    dessin.text((x1 + 15, y1 + 10), nom, font=titre, fill="#183153")
    dessin.multiline_text((x1 + 15, y1 + 50), texte, font=police, fill="black", spacing=6)

# Fleches
# Sources -> NiFi
dessin.line((290, 200, 360, 200), fill="black", width=4)
dessin.polygon([(360, 200), (345, 192), (345, 208)], fill="black")

# NiFi -> Bronze
dessin.line((560, 200, 650, 155), fill="black", width=4)
dessin.polygon([(650, 155), (635, 152), (642, 165)], fill="black")

# Bronze -> Silver
dessin.line((815, 200, 815, 260), fill="black", width=4)
dessin.polygon([(815, 260), (807, 245), (823, 245)], fill="black")

# Silver -> Gold
dessin.line((815, 350, 815, 410), fill="black", width=4)
dessin.polygon([(815, 410), (807, 395), (823, 395)], fill="black")

# Gold -> Analyses
dessin.line((815, 500, 815, 570), fill="black", width=4)
dessin.polygon([(815, 570), (807, 555), (823, 555)], fill="black")

# Notes
dessin.text((70, 760), "Traitement propose : batch", font=police, fill="#183153")
dessin.text((350, 760), "Controles : formats, valeurs vides, identifiants", font=police, fill="#183153")
dessin.text((70, 800), "Utilisateurs : direction, direction commerciale, responsables magasin", font=police, fill="#183153")

fichier = sortie / "UC02_schema_flux.png"
image.save(fichier)

print("Schema cree :", fichier)