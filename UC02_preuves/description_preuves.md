
## 1. Schéma d'architecture

**Fichier :** `UC02_schema_architecture.png`

Ce schéma montre l'architecture proposée, depuis les fichiers TPCx-BB jusqu'aux analyses métier. Il présente l'ingestion, les zones Bronze, Silver et Gold ainsi que les traitements envisagés.

## 2. Schéma des flux

**Fichier :** `UC02_schema_flux.png`

Ce schéma montre le chemin prévu pour les données. Les fichiers sont récupérés, stockés, contrôlés puis préparés pour les indicateurs.

## 3. Comparaison des architectures

**Fichier :** `UC02_comparaison_architectures.pdf`

Ce document compare le Data Warehouse, le Data Lake et le Lakehouse. Il permet de justifier l'architecture retenue pour le projet.

## 4. Positionnement des composants

**Fichier :** `UC02_positionnement_composants.pdf`

Ce tableau présente le rôle des technologies étudiées et distingue les composants obligatoires des composants facultatifs.

## 5. Gouvernance des données

**Fichier :** `UC02_gouvernance.pdf`

Ce document présente les règles proposées pour la qualité des données, la traçabilité, les accès, la protection et le suivi des traitements.

## 6. Comparaison local et Azure

**Fichier :** `UC02_local_vers_azure.pdf`

Ce document compare l'architecture locale envisagée avec une cible Azure utilisant notamment ADLS Gen2.

Il s'agit d'une comparaison théorique. Aucun déploiement Azure n'est présenté comme réalisé.
## 7. Inventaire des sources

**Fichier :** `02_inventaire.png`

Cette capture montre les fichiers TPCx-BB identifiés pendant l'UC-01

## 8. Contrôles des données

**Fichier :** `05_controles.png`

Cette capture présente les contrôles réalisés pendant l'UC-01. Ils servent à justifier les vérifications prévues dans la zone Silver de l'architecture proposée.