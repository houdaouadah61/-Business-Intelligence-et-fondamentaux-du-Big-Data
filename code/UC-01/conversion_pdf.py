import csv
import re
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, LongTable, TableStyle)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


dossier = Path(__file__).parent
sortie = dossier / "livrables"
sortie.mkdir(exist_ok=True)


pdfmetrics.registerFont(
    TTFont("Arial", "C:/Windows/Fonts/arial.ttf")
)
pdfmetrics.registerFont(
    TTFont("Arial-Bold", "C:/Windows/Fonts/arialbd.ttf")
)

styles = getSampleStyleSheet()

styles["BodyText"].fontName = "Arial"
styles["BodyText"].fontSize = 10
styles["BodyText"].leading = 15
styles["BodyText"].spaceAfter = 5

for nom in ["Heading1", "Heading2", "Heading3"]:
    styles[nom].fontName = "Arial-Bold"
    styles[nom].textColor = colors.HexColor("#193B5C")
    styles[nom].spaceAfter = 10
    styles[nom].spaceBefore = 10

style_cellule = ParagraphStyle(
    "Cellule",
    fontName="Arial",
    fontSize=8,
    leading=11,
    splitLongWords=1
)

style_entete = ParagraphStyle(
    "Entete",
    parent=style_cellule,
    fontName="Arial-Bold",
    textColor=colors.white
)


def formater(texte):
    texte = escape(texte)

    # Texte en gras
    texte = re.sub(
        r"\*\*(.*?)\*\*",
        r"<b>\1</b>",
        texte
    )

    # Code entre accents graves
    texte = re.sub(
        r"`(.*?)`",
        r'<font color="#245A80">\1</font>',
        texte
    )

    return texte



def est_separateur(ligne):
    cellules = ligne.strip().strip("|").split("|")

    return all(
        re.fullmatch(r":?-{3,}:?", c.strip())
        for c in cellules
    )



def creer_tableau(lignes, largeur):
    donnees = []

    for numero, ligne in enumerate(lignes):
        if est_separateur(ligne):
            continue

        cellules = ligne.strip().strip("|").split("|")
        style = style_entete if numero == 0 else style_cellule

        donnees.append([
            Paragraph(formater(c.strip()), style)
            for c in cellules
        ])

    if not donnees:
        return None

    nb_colonnes = max(len(ligne) for ligne in donnees)

    for ligne in donnees:
        while len(ligne) < nb_colonnes:
            ligne.append(Paragraph("", style_cellule))

    tableau = LongTable(
        donnees,
        colWidths=[largeur / nb_colonnes] * nb_colonnes,
        repeatRows=1,
        hAlign="LEFT"
    )

    tableau.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#193B5C")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#F0F4F8")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7)
    ]))

    return tableau



documents = [
    "cadrage_metier",
    "questions_decisionnelles",
    "dictionnaire_KPI",
    "qualification_donnees",
    "limites_et_hypotheses"
]


for nom in documents:

    source = dossier / (nom + ".md")
    destination = sortie / ("UC01_" + nom + ".pdf")

    if not source.exists():
        print("Fichier introuvable :", source.name)
        continue

    lignes = source.read_text(
        encoding="utf-8-sig"
    ).splitlines()

    pdf = SimpleDocTemplate(
        str(destination),
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=45
    )

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

            tableau = creer_tableau(lignes_tableau, A4[0] - 90)

            if tableau is not None:
                contenu.append(tableau)
                contenu.append(Spacer(1, 12))

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

        
        if ligne.startswith("- "):
            ligne = "• " + ligne[2:]

        contenu.append(Paragraph(formater(ligne), style))
        i += 1

    pdf.build(contenu)
    print("PDF créé :", destination.name)



source = dossier / "inventaire_sources.csv"
destination = sortie / "UC01_inventaire_sources.pdf"

if source.exists():

    with open(source, encoding="utf-8-sig", newline="") as f:
        lignes = list(csv.reader(f, delimiter=";"))

    if lignes:
        largeur = landscape(A3)[0] - 60

        
        lignes_tableau = []

        for ligne in lignes:
            lignes_tableau.append(
                "| " + " | ".join(ligne) + " |"
            )

        tableau = creer_tableau(lignes_tableau, largeur)

        pdf = SimpleDocTemplate(
            str(destination),
            pagesize=landscape(A3),
            leftMargin=30,
            rightMargin=30,
            topMargin=30,
            bottomMargin=30
        )

        pdf.build([tableau])
        print("PDF créé :", destination.name)

print()
print("Conversion des 6 PDF terminée.")
print("Dossier :", sortie)
