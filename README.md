# Pseudo_pdf_tool
Un outil open source afin de pseudonymiser des fichiers PDF. Créé sous Etalab.

## Objectifs
Le but initial était de créer un outil capable de pseudonymiser un fichier PDF en caviardant ou modifiant les entités nommées (des personnes, des lieux...) sur le fichier PDF plutôt que de pseudonymiser son contenu uniquement. Ceci est utile pour des organismes souhaitant automatiser ce processus de protection d'individu ou d'informations sensibles.

## Remarque
Cet outil n'est pas exact, il est nécessaire de vérifier à la main la qualité de la pseudonymisation avant de publier les fichiers PDF protégés.

## Méthodes choisies
Afin de modifier le PDF tel quel, il est nécessaire de savoir identifier les entités nommées et leur position sur le fichier. Pour ce faire, ce module procède de la manière suivante :
- Etant donné un PDF, on convertit toutes ses pages en fichier image `.jpeg`.
- Le contenu du PDF est déterminé grâce au module `èasyocr` qui extrait le contenu textuel de chaque page du fichier.
- Ensuite, les entités nommées sont identifiées grace au module de NER en français [CamemBERT-NER](https://huggingface.co/Jean-Baptiste/camembert-ner)
- Le module `fitz` est utilisé pour trouver les positions de toutes les occurences des entités nommées (à travers tout le document)
- En fonction de la nature de l'entité nommée (personne, lieu) une fonction de pseudonymisation est appliquée. Le choix de quel type d'entité nommée doit être pseudonymisé est un paramètre à fixer, mais par défaut toutes les entités nommées seront protégées.
- Ce même module (`fitz`) est utilisé pour caviarder toutes les occurences des entités nommées et les cacher par leur version pseudonymisée
- Les fichiers image sont supprimés et le PDF protégé est créé à partir de la fusion des pages


## Structure de fichiers
### Données
Cet outil prend en entrée n'importe quel fichier pdf.

## API
Le dossier [api](api/) contient la création de l'API utilisant l'outil `Pseudo_PDF` pour pseudonymiser un document.

### Dossier src
Le dossier[src](api/src/) contient le code source de l'objet PDF.

#### Fichier utils
Le fichier [utils](api/src/utils.py) contient toutes les fonctions basiques nécessaires pour le fonctionnement de l'outil, comme des fonctions de pseudonymisation ou de conversion pdf-image.

#### Classe PDF
Le fichier [object_pdf](api/src/object_pdf.py) crée la structure de classe `Pseudo_pdf` nécessaire pour pseudonymiser un fichier PDF. 

### Fichier main
Le fichier[main.py](api/main.py) crée la structure de l'API.

## Docs

Le dossier docs justifie les chiffres de performance de l'outil. Pour trois fichiers du CNDA distincts (mettre liens), on retrouve la version originale, la version annotée, et deux versions pseudonymisées différentes (en fonction de l'attribut `as_image`).




## Quickstart
Pour installer les modules nécessaires pour tester cet outil, utilisez le `docker-compose.yml`

Pour tester la classe pseudo_pdf sur un fichier, modifier le fichier `example.pdf` dans la fonction main de (object_pdf)[api/src/object_pdf.py] et run ce fichier.

Pour tester l'API en local, lancer dans un terminal (à la racine) :
`uvicorn api.main:app --reload`

## Licence
Retrouvez la licence [ici](LICENSE).

