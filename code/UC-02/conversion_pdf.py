import re
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,LongTable, TableStyle, Image)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

dossier = Path(__file__).parent
sortie = dossier / "livrables"
sortie.mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "C:/Windows/Fonts/arialbd.ttf"))

styles = getSampleStyleSheet()
styles["BodyText"].fontName = "Arial"
styles["BodyText"].fontSize = 10
styles["BodyText"].leading = 15

for nom in ["Heading1", "Heading2", "Heading3"]:
    styles[nom].fontName = "Arial-Bold"
    styles[nom].textColor = colors.darkblue

cellule = ParagraphStyle(
    "Cellule",
    fontName="Arial",
    fontSize=8,
    leading=11
)

entete = ParagraphStyle(
    "Entete",
    parent=cellule,
    fontName="Arial-Bold",
    textColor=colors.white
)

def formater(texte):
    texte = escape(texte)
    texte = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", texte)
    texte = re.sub(r"`(.*?)`", r"\1", texte)
    return texte

def tableau_pdf(lignes):
    donnees = []

    for numero, ligne in enumerate(lignes):
        valeurs = ligne.strip().strip("|").split("|")

        if all(
            re.fullmatch(r":?-{3,}:?", valeur.strip())
            for valeur in valeurs
        ):
            continue

        style = entete if numero == 0 else cellule

        donnees.append([
            Paragraph(formater(valeur.strip()), style)
            for valeur in valeurs
        ])

    if not donnees:
        return None

    nb_colonnes = len(donnees[0])

    tableau = LongTable(
        donnees,
        colWidths=[
    ((landscape(A4)[0] if nb_colonnes > 7 else A4[0]) - 90)
    / nb_colonnes
    ] * nb_colonnes,
        repeatRows=1
    )

    tableau.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7)
    ]))

    return tableau

documents = [
    "comparaison_architectures",
    "architecture_cible",
    "schema_flux",
    "positionnement_composants",
    "gouvernance",
    "local_vers_azure"
]

for nom in documents:
    source = dossier / (nom + ".md")
    destination = sortie / ("UC02_" + nom + ".pdf")

    if not source.exists():
        print("Fichier absent :", source.name)
        continue

    lignes = source.read_text(encoding="utf-8-sig").splitlines()

    contenu = []
    i = 0

    while i < len(lignes):
        ligne = lignes[i].strip()

        if not ligne:
            contenu.append(Spacer(1, 7))
            i += 1
            continue

        if ligne.startswith("|"):
            lignes_tableau = []

            while i < len(lignes) and lignes[i].strip().startswith("|"):
                lignes_tableau.append(lignes[i])
                i += 1

            tableau = tableau_pdf(lignes_tableau)
            if tableau:
                contenu.append(tableau)
                contenu.append(Spacer(1, 10))
            continue

        if ligne.startswith("### "):
            style = styles["Heading3"]
            ligne = ligne[4:]
        elif ligne.startswith("## "):
            style = styles["Heading2"]
            ligne = ligne[3:]
        elif ligne.startswith("# "):
            style = styles["Heading1"]
            ligne = ligne[2:]
        else:
            style = styles["BodyText"]

        contenu.append(Paragraph(formater(ligne), style))
        i += 1

    
    if nom == "architecture_cible":
        image_path = sortie / "UC02_schema_architecture.png"
        if image_path.exists():
            contenu.append(Spacer(1, 15))
            contenu.append(Paragraph("Schéma de l'architecture proposée", styles["Heading2"]))
            contenu.append(Spacer(1, 10))
            contenu.append(Image(str(image_path), width=480, height=552))

    if nom == "schema_flux":
        image_path = sortie / "UC02_schema_flux.png"
        if image_path.exists():
            contenu.append(Spacer(1, 15))
            contenu.append(Paragraph("Schéma des flux de données", styles["Heading2"]))
            contenu.append(Spacer(1, 10))
            contenu.append(Image(str(image_path), width=500, height=375))

    pdf = SimpleDocTemplate(
        str(destination),
        pagesize=landscape(A4) if nom == "schema_flux" else A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    pdf.build(contenu)
    print("PDF créé :", destination.name)

print()
print("Les 6 PDF de l'UC-02 sont générés.")