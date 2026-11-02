# TS Import Extractor — analyse des imports TypeScript et export CSV

**TS Import Extractor** (`ts_import_extractor`) est un script Python qui analyse les imports nommés d'une bibliothèque dans un ou plusieurs projets TypeScript. Il parcourt les fichiers `.ts` et `.tsx`, compte les symboles importés et génère un rapport CSV exploitable dans Excel ou LibreOffice Calc.

**English overview:** A Python TypeScript import analyzer for auditing library and design system adoption across local projects. Extract named imports from `.ts` and `.tsx` files, count import occurrences, and export a CSV report with dependency and project versions. No third-party Python packages required.

## À quoi sert ce script ?

- **Auditer l'adoption d'un design system ou d'un kit UI** : identifier les composants importés depuis un package partagé.
- **Préparer une migration de bibliothèque** : recenser les symboles importés et les versions déclarées dans plusieurs applications.
- **Comparer plusieurs projets front-end** : regrouper leurs résultats dans un même fichier CSV.

Le script analyse le code source local. Le compteur mesure le nombre d'apparitions de chaque symbole dans les déclarations d'import, pas le nombre d'utilisations du composant dans le code ou à l'exécution.

## Fonctionnalités

- Parcours récursif des fichiers TypeScript (`.ts`) et TSX (`.tsx`).
- Recherche des imports nommés depuis une bibliothèque configurée, y compris les imports sur plusieurs lignes.
- Comptage par symbole et par projet ; un alias comme `Button as PrimaryButton` est compté sous le nom `Button`.
- Lecture de la version du projet et de la version déclarée de la bibliothèque dans le `package.json` à la racine de chaque projet.
- Export CSV avec séparateur `;` et encodage UTF-8 avec BOM pour faciliter l'ouverture dans Excel.
- Utilisation de la bibliothèque standard de Python uniquement : aucune installation avec `pip` nécessaire.

## Démarrage rapide

### 1. Récupérer le script

Prérequis : Python 3.8 ou supérieur et des projets à analyser présents sur votre machine. Git est nécessaire pour la commande de clonage ci-dessous ; vous pouvez aussi télécharger le dépôt ou copier uniquement [main.py](main.py).

```bash
git clone https://github.com/dokor/ts_import_extractor.git
cd ts_import_extractor
```

### 2. Configurer la bibliothèque et les projets

Dans `main.py`, remplacez les valeurs de `dependance_to_analyze` et de `projects_input` par celles de vos projets :

```python
dependance_to_analyze = '@acme/ui'

projects_input = {
    "portail-client": "/chemin/vers/portail-client",
    "application-admin": "/chemin/vers/application-admin"
}
```

`@acme/ui` est un nom fictif : utilisez le nom du package tel qu'il apparaît dans vos imports et dans votre `package.json`. Les clés de `projects_input` sont les noms affichés dans le rapport ; les valeurs sont les chemins vers les racines des projets.

Sous Windows, utilisez par exemple `r"C:\projets\portail-client"` ou `"C:/projets/portail-client"` pour les chemins. Les chemins relatifs sont résolus depuis le dossier où vous lancez la commande.

### 3. Lancer l'analyse

```bash
python main.py
```

Selon votre installation, utilisez `python3 main.py` sous macOS/Linux ou `py main.py` sous Windows.

### 4. Ouvrir le rapport CSV

Le fichier `analyse_kitui.csv` est créé dans le **dossier depuis lequel vous lancez la commande**. Chaque exécution remplace ce fichier s'il existe déjà. Pour changer son nom ou son emplacement, modifiez `csv_output_path` dans `main.py`.

Le script n'affiche pas de rapport dans le terminal : ouvrez le CSV pour consulter les résultats. Si votre tableur ne sépare pas automatiquement les colonnes, choisissez le séparateur `;` à l'import.

## Exemple : des imports TypeScript au rapport CSV

Avec `dependance_to_analyze = '@acme/ui'`, supposons que le projet `portail-client` contienne ces deux fichiers :

```typescript
// src/pages/Home.tsx
import { Button, Card } from '@acme/ui';
```

```typescript
// src/pages/Settings.tsx
import {
  Button as PrimaryButton,
  Theme
} from '@acme/ui';
```

Et ce `package.json` à sa racine :

```json
{
  "name": "portail-client",
  "version": "1.2.0",
  "dependencies": {
    "@acme/ui": "^3.4.0"
  }
}
```

Le rapport contient les lignes suivantes pour ce projet ; leur ordre peut varier selon l'ordre de parcours des fichiers :

```csv
Project Name;Project Version;KitUI Version;Component;Usage Count
portail-client;1.2.0;^3.4.0;Button;2
portail-client;1.2.0;^3.4.0;Card;1
portail-client;1.2.0;^3.4.0;Theme;1
```

| Colonne | Signification |
| --- | --- |
| `Project Name` | Nom défini dans `projects_input`. |
| `Project Version` | Champ `version` du `package.json` du projet. |
| `KitUI Version` | Version déclarée du package analysé dans `dependencies`, ou à défaut dans `devDependencies`. |
| `Component` | Nom du symbole importé avant un éventuel alias : composant, fonction, type, etc. |
| `Usage Count` | Nombre d'apparitions du symbole dans les déclarations d'import du projet. |

Les intitulés `KitUI Version` et `Component` sont ceux du script actuel, même si vous analysez une autre bibliothèque qu'un kit UI. La version exportée est la valeur déclarée (par exemple `^3.4.0`), pas la version installée résolue dans un fichier de verrouillage. Si une version manque ou que le `package.json` est illisible, elle vaut `N/A`.

## Imports reconnus et limites

L'extraction repose sur une expression régulière, sans analyseur syntaxique TypeScript. Pour interpréter correctement les résultats :

- **Syntaxe attendue** : `import { Button } from '@acme/ui';`, avec des guillemets simples ou doubles et un point-virgule final.
- **Formes non prises en charge** : imports par défaut, imports de namespace (`import * as UI`), imports dynamiques (`import()`), `require()`, réexports et déclarations `import type { ... }`. La forme `import { type Theme }` n'est pas normalisée : elle est comptée sous le nom `type Theme`.
- **Chemin du package** : un import depuis `@acme/ui/button` n'est pas agrégé avec `@acme/ui`. Le nom configuré est inséré directement dans l'expression régulière ; les caractères spéciaux comme `.` peuvent modifier la correspondance.
- **Fichiers parcourus** : tous les sous-dossiers sont inclus, y compris `node_modules`, les dossiers de build et les fichiers `.d.ts`. Le script ne propose pas de règle d'exclusion. Les fichiers `.js`, `.jsx`, `.vue` et `.svelte` ne sont pas analysés.
- **Faux positifs possibles** : du texte ressemblant à un import dans un commentaire ou une chaîne de caractères peut être compté.
- **Résultats absents** : un projet sans import reconnu n'a aucune ligne dans le CSV. Un chemin inexistant peut donc produire uniquement l'en-tête, sans message d'erreur. Une erreur de lecture d'un fichier source peut interrompre l'analyse.

## Questions fréquentes

### Peut-on analyser des projets React ou Angular ?

Oui, pour leurs fichiers `.ts` et `.tsx` qui utilisent la syntaxe d'import reconnue ci-dessus. Le script parcourt les fichiers sans dépendre du framework ni de son système de build.

### Peut-on analyser plusieurs bibliothèques à la fois ?

Le script analyse une bibliothèque par exécution. Changez `dependance_to_analyze` pour un autre package et utilisez un nom de sortie différent si vous souhaitez conserver les rapports précédents.

### Faut-il installer les dépendances des projets à analyser ?

Non. Le script lit les fichiers source et les `package.json` locaux ; il n'exécute pas les applications et ne lance pas leur installation. Un dossier `node_modules` déjà présent sera toutefois parcouru.

## Contributions et auteur

Pour signaler un problème ou proposer une amélioration, [ouvrez une issue](https://github.com/dokor/ts_import_extractor/issues) ou une pull request. Pour un problème d'extraction, fournissez un exemple minimal d'import et le résultat attendu.

Développé par **Antoine LE LOUËT** ([antoine.lelouet.fr](https://antoine.lelouet.fr)).
