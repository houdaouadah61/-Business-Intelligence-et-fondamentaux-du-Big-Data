
import csv

fichier = "retail_project/retail_project/data/store_sales/store_sales.dat"

erreurs = 0
valeurs_vides = 0

with open(fichier, "r") as f:
    lecteur = csv.reader(f, delimiter="|")

    for ligne in lecteur:
        for i in range(23):
            valeur = ligne[i].strip()

            if valeur == "":
                valeurs_vides += 1
            else:
                try:
                    if i < 11:
                        int(valeur)
                    else:
                        float(valeur)
                except ValueError:
                    erreurs += 1

print("Valeurs vides :", valeurs_vides)
print("Valeurs avec un format incorrect :", erreurs)
