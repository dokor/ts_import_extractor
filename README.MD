# 🔍 Analyse des imports d'une librairie

Ce projet permet d'analyser plusieurs projets front-end pour identifier quels composants, types ou interfaces sont importés depuis le kit UI `XXXXXXXX`.     
Le résultat est exporté sous forme de fichier CSV compatible avec Excel.

---

## ✨ Fonctionnalités

- Parcourt récursivement les fichiers `.ts` et `.tsx` des projets spécifiés
- Identifie tous les composants importés depuis `XXXXXXXXX`, même sur plusieurs lignes
- Compte le nombre d'occurrences de chaque composant
- Récupère la version du kit UI et du projet via le `package.json`
- Génère un fichier CSV au format Excel-friendly (UTF-8 avec BOM, séparateur `;`)

---

## 🛠️ Prérequis

- Python 3.8+
- Les projets à analyser doivent être clonés localement

---

## 🚀 Utilisation

1. **Cloner ce dépôt (ou copier le script Python dans un fichier, par exemple `analyser_imports.py`)**

2. **Configurer les projets à analyser**  
   Dans le script, modifier ce dictionnaire avec les chemins vers tes projets :

   ```python
   projects_input = {
       "mon-super-projet": "/chemin/vers/mon-super-projet",
       "un-autre-projet": "/chemin/vers/un-autre-projet"
   }

3. **Lancer le script**  
    ```python
    python analyser_imports.py

4. **Récupérer le fichier CSV généré**
Il sera disponible à la racine dans analyse_kitui.csv

---

## 🧑‍💻 Auteur
Développé par Antoine LE LOUËT, avec ❤️.