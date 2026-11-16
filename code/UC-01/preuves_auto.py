
import csv
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

dossier = Path(__file__).parent
donnees = dossier.parent / "retail_project" / "retail_project" / "data"
sortie = dossier / "livrables" / "UC01_preuves"
sortie.mkdir(parents=True, exist_ok=True)

police = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 17)
titre_police = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 27)

# Créer une image lisible
def image_preuve(nom, titre, lignes):
    image = Image.new(
        "RGB",
        (1800, max(400, 120 + len(lignes) * 28)),
        "white"
    )
    dessin = ImageDraw.Draw(image)

    dessin.rectangle((0, 0, 1800, 80), fill="#193b5c")
    dessin.text((30, 20), titre, font=titre_police, fill="white")

    y = 105
    for ligne in lignes:
        dessin.text((30, y), str(ligne)[:145], font=police, fill="black")
        y += 28

    image.save(sortie / (nom + ".png"))
    print("Créé :", nom + ".png")


# 1 - Arborescence des données
lignes = []

if donnees.exists():
    for element in sorted(donnees.iterdir()):
        if element.is_dir():
            lignes.append("[DOSSIER] " + element.name)
            for fichier in element.iterdir():
                if fichier.is_file():
                    lignes.append("    " + fichier.name)
else:
    lignes.append("Dossier des données introuvable")

image_preuve("01_arborescence", "Arborescence des données", lignes)


# 2 - Extrait de l'inventaire
lignes = []
inventaire = dossier / "inventaire_sources.csv"

with open(inventaire, encoding="utf-8-sig", newline="") as f:
    lecteur = csv.reader(f, delimiter=";")
    for numero, ligne in enumerate(lecteur):
        if numero >= 10:
            break
        lignes.append(" | ".join(ligne))

image_preuve("02_inventaire", "Extrait de l'inventaire", lignes)


# 3 - Aperçu des fichiers représentatifs
lignes = []

for nom in ["store_sales", "item", "customer"]:
    fichier = donnees / nom / (nom + ".dat")
    lignes.append("Fichier : " + nom + ".dat")

    with open(fichier, encoding="utf-8") as f:
        lecteur = csv.reader(f, delimiter="|")

        for numero, ligne in enumerate(lecteur):
            if numero == 2:
                break
            lignes.append("Ligne " + str(numero + 1))
            lignes.append(" | ".join(ligne))

    lignes.append("")

image_preuve("03_apercu", "Aperçu des fichiers", lignes)


# 4 et 5 - Types et contrôles
fichier = donnees / "store_sales" / "store_sales.dat"

nb_lignes = 0
structure_incorrecte = 0
vides = [0] * 23
erreurs = [0] * 23
negatifs = [0] * 23

with open(fichier, encoding="utf-8") as f:
    lecteur = csv.reader(f, delimiter="|")

    for ligne in lecteur:
        nb_lignes += 1

        if len(ligne) != 23:
            structure_incorrecte += 1
            continue

        for i in range(23):
            valeur = ligne[i].strip()

            if valeur == "":
                vides[i] += 1
                continue

            if valeur.startswith("-"):
                negatifs[i] += 1

            try:
                if i < 11:
                    int(valeur)
                else:
                    float(valeur)
            except ValueError:
                erreurs[i] += 1

lignes = ["Fichier : store_sales.dat", ""]

for i in range(23):
    typ = "Entier" if i < 11 else "Décimal"
    lignes.append(
        "Colonne " + str(i + 1)
        + " | Type testé : " + typ
        + " | Vides : " + str(vides[i])
        + " | Erreurs : " + str(erreurs[i])
    )

image_preuve("04_colonnes_types", "Colonnes et types", lignes)

lignes = [
    "Fichier : store_sales.dat",
    "",
    "Nombre de lignes : " + str(nb_lignes),
    "Lignes mal structurées : " + str(structure_incorrecte),
    "Valeurs vides : " + str(sum(vides)),
    "Formats incorrects : " + str(sum(erreurs)),
    "Valeurs négatives : " + str(sum(negatifs)),
]

for i in range(23):
    if negatifs[i] > 0:
        lignes.append(
            "Colonne " + str(i + 1)
            + " : " + str(negatifs[i]) + " valeurs négatives"
        )

image_preuve("05_controles", "Résultats des contrôles", lignes)


# 6 - Schéma des besoins métier
image = Image.new("RGB", (1500, 750), "white")
dessin = ImageDraw.Draw(image)

dessin.text(
    (420, 30),
    "Schéma des besoins métier",
    font=titre_police,
    fill="#193b5c"
)

profils = [
    ("Direction générale", "Évolution des ventes", "Comparer les magasins"),
    ("Direction commerciale", "Produits les plus vendus", "Ventes web / magasin"),
    ("Responsable magasin", "Ventes quotidiennes", "Suivi des stocks")
]

for i, (profil, besoin1, besoin2) in enumerate(profils):
    x = 70 + i * 490

    dessin.rounded_rectangle(
        (x, 130, x + 430, 220),
        radius=12,
        fill="#193b5c"
    )
    dessin.text(
        (x + 20, 160), profil,
        font=police, fill="white"
    )

    dessin.line(
        (x + 215, 220, x + 215, 300),
        fill="#193b5c", width=4
    )

    dessin.rounded_rectangle(
        (x, 300, x + 430, 470),
        radius=12,
        outline="#193b5c",
        width=3
    )

    dessin.text((x + 15, 330), besoin1, font=police, fill="black")
    dessin.text((x + 15, 390), besoin2, font=police, fill="black")

image.save(sortie / "06_besoins_metier.png")
print("Créé : 06_besoins_metier.png")


# 7 - Dictionnaire de KPI
source = dossier / "dictionnaire_KPI.md"
lignes = source.read_text(encoding="utf-8-sig").splitlines()

image_preuve(
    "07_dictionnaire_KPI",
    "Dictionnaire initial des KPI",
    lignes
)

print()
print("Les 7 preuves demandées ont été générées.")
