# Jeu de la vie - Groupe 5

Simulation en Python du [jeu de la vie de Conway](https://fr.wikipedia.org/wiki/Jeu_de_la_vie). Le programme `main.py` génère une grille aléatoire ou lit une grille sur l'entrée standard, calcule son évolution avec des conditions aux limites fixes ou périodiques, puis écrit le résultat sous forme d'images PNG ou de texte.

- [Installation](#installation)
- [Exécution](#exécution)
- [Arguments](#arguments)
- [Vidéos](#vidéos)
- [Intégration continue](#intégration-continue)
- [Auteurs](#auteurs)
- [Liens utiles](#liens-utiles)

## Installation

Le programme utilise uniquement Python 3 et sa bibliothèque standard, avec le fichier `lib.py` fourni. Aucune bibliothèque Python externe n'est nécessaire. Les logiciels `ffmpeg` et Gource ne servent qu'à produire les vidéos.

### Récupérer le dépôt

```bash
git clone https://github.com/azirahmed346-hash/git-evaluation-jeu-de-la-vie_groupe-5.git
cd git-evaluation-jeu-de-la-vie_groupe-5
```

### Ubuntu ou Debian

```bash
sudo apt update
sudo apt install python3 git gource ffmpeg
```

### macOS

Avec [Homebrew](https://brew.sh/) :

```bash
brew install python git gource ffmpeg
```

### Windows

Installez [WSL](https://learn.microsoft.com/fr-fr/windows/wsl/install) afin de disposer d'un terminal Unix. Depuis un PowerShell ouvert en administrateur :

```powershell
wsl --install
```

Redémarrez si nécessaire, ouvrez la distribution Ubuntu, puis suivez la procédure Ubuntu ou Debian dans le terminal WSL. Les disques Windows sont accessibles dans `/mnt` (par exemple `cd /mnt/c/Users/Alice/projet`).

### Vérifier l'installation

```bash
python3 --version
gource --version
ffmpeg -version
```

## Exécution

Toutes les commandes se lancent depuis la racine du dépôt.

### Exécution sans option (scénario 1)

Sans option, le programme utilise les valeurs par défaut et crée 21 images dans `outputs`, de `grid_0000.png` à `grid_0020.png` :

```bash
$ python3 main.py
Generation of 21 images in directory outputs
$ echo $?
0
$ ls -p1 outputs | wc -l
 21
```

Pour que ce comptage soit exact, le dossier `outputs` ne doit contenir aucune autre entrée non cachée avant l'exécution (le fichier caché `.keep` n'est pas compté).

### Génération d'images avec options (scénario 2)

Grille de 50 cellules par côté, graine 4200, dernière génération numérotée 200, soit 201 images :

```bash
$ python3 main.py -n 50 -m 200 -s 4200
Generation of 201 images in directory outputs
$ echo $?
0
$ ls -p1 outputs | wc -l
 201
```

### Évolution d'une grille lue sur STDIN (scénario 3)

La grille d'entrée est décrite par sa taille sur la première ligne, puis par ses lignes, les cellules étant séparées par des espaces. Contenu de `tests/matrix3/input.txt` :

```text
3
1 0 1
0 0 1
1 0 1
```

Avec les conditions aux limites fixes (par défaut), une seule évolution :

```bash
$ cat tests/matrix3/input.txt | python3 main.py -m 1 -t text
iteration: 1
0 1 0
0 0 1
0 1 0
$ echo $?
0
```

Le pipe peut être remplacé par une redirection :

```bash
python3 main.py -m 1 -t text < tests/matrix3/input.txt
```

### Grille périodique (scénario 4)

L'option `-p` relie le bord gauche au bord droit et le bord supérieur au bord inférieur. Le résultat est différent pour la même grille :

```bash
$ cat tests/matrix3/input.txt | python3 main.py -m 1 -p -t text
iteration: 1
0 0 0
0 0 0
0 0 0
$ echo $?
0
```

### Sortie texte sur une grille aléatoire

Seule la dernière itération demandée est écrite sur la sortie standard :

```bash
python3 main.py -n 5 -m 10 -s 7 -t text
```

La même graine et la même taille donnent toujours la même grille initiale.

### Dossier de sortie personnalisé

```bash
python3 main.py -n 20 -m 5 -o resultats
```

Le programme annonce `Generation of 6 images in directory resultats`.

### Gestion des erreurs

En cas d'erreur, un message explicite est écrit sur la sortie d'erreur (STDERR) et le programme se termine avec un code de sortie différent de `0`. Sont notamment refusés : une grille vide ou mal formée, une cellule différente de `0` ou `1`, une taille non positive, une itération négative et un type de sortie différent de `image` ou `text`.

```bash
python3 main.py -n 0 ; echo $?
python3 main.py -m -1 ; echo $?
python3 main.py -t pdf ; echo $?
```

Chaque commande affiche un message d'erreur, puis un code de sortie non nul.

### Vérifier le programme

Les scripts fournis se lancent depuis la racine du dépôt :

```bash
sh check_script_options.sh
sh check_tests.sh
```

## Arguments

| Option courte | Option longue | Description | Valeur par défaut |
|---|---|---|---|
| `-n N` | `--nb_cells N` | nombre de cellules par côté pour une grille aléatoire (entier strictement positif) | `10` |
| `-m N` | `--max_iterations N` | numéro de la dernière itération à calculer (entier positif ou nul) | `20` |
| `-s N` | `--seed N` | graine du générateur de nombres aléatoires (entier, négatif, nul ou positif) | `42` |
| `-o DOSSIER` | `--output_directory DOSSIER` | dossier dans lequel écrire les images | `outputs` |
| `-t TYPE` | `--output_type TYPE` | type de sortie : `image` ou `text` | `image` |
| `-p` | `--periodic` | active les conditions aux limites périodiques | désactivée |
| `-h` | `--help` | affiche l'aide du programme | — |

Précisions :

- La génération initiale porte le numéro 0 : `-m 20` produit 21 générations, de 0 à 20 incluses.
- Les images sont nommées `grid_XXXX.png`, `XXXX` étant le numéro de l'itération sur quatre chiffres (`grid_0000.png` pour la génération initiale).
- Avec `-t text`, aucun fichier n'est généré : la sortie commence par `iteration: N`, suivie des lignes de la grille, cellules séparées par des espaces.
- Lorsqu'une grille est fournie sur l'entrée standard, elle remplace la grille aléatoire : `--nb_cells` et `--seed` n'ont alors aucun effet.
- Par défaut, tout ce qui est hors de la grille est considéré comme mort. Avec `-p`, la grille est un tore.
- Aide complète : `python3 main.py --help`.

## Vidéos

### Vidéo de simulation du jeu de la vie

Vidéo YouTube : https://youtube.com/shorts/AVOi-X01Hw0?feature=share

Graine utilisée : `4200` (grille de 50 cellules par côté, conditions aux limites fixes, 2001 images).

Commandes exactes de génération des images puis de la vidéo :

```bash
mkdir -p outputs/video-seed-4200
python3 main.py --nb_cells 50 --max_iterations 2000 --seed 4200 \
  --output_type image --output_directory outputs/video-seed-4200
ffmpeg -y -framerate 20 -start_number 0 \
  -i outputs/video-seed-4200/grid_%04d.png -frames:v 2001 \
  -c:v libx264 -pix_fmt yuv420p -movflags +faststart \
  outputs/video-seed-4200/game-of-life.mp4
```

Le programme annonce `Generation of 2001 images in directory outputs/video-seed-4200`. La vidéo dure 100,05 secondes (2001 images à 20 images par seconde).

### Vidéo Gource de l'historique du dépôt

Vidéo YouTube : [À COMPLÉTER : lien YouTube de Gource]

Commande utilisée, depuis la racine du dépôt :

```bash
gource -s 2 -r 60 --file-font-size 8 \
  --title 'Jeu de la vie' --filename-time 2 \
  --stop-at-end --hide date,usernames -o - | \
ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i - \
  -vcodec libx264 -preset medium -pix_fmt yuv420p \
  -crf 18 -threads 0 -bf 0 gource.mp4
```

Les images, les vidéos et le fichier intermédiaire `gource.ppm` ne sont pas versionnés : ils sont exclus par le fichier `.gitignore`.

## Intégration continue

Un workflow GitHub Actions (`.github/workflows/`) se déclenche à chaque `push` et à chaque *Pull Request*. Il exécute `sh check_script_options.sh` et `sh check_tests.sh` et signale un échec si l'un des scripts se termine avec un code différent de `0`.

Exécution réussie : [Tests #25](https://github.com/azirahmed346-hash/git-evaluation-jeu-de-la-vie_groupe-5/actions/runs/44527969517)

## Auteurs

Groupe 5 :

| Nom | Prénom | Numéro étudiant |
|---|---|---|
| ASSADILLAH | Ahmed | 45006173 |
| RAMAHENINA | Anditiana Stéphane | 45005335 |
| SOILIHI | Yakinat | 44008429 |
| KOGOE | Essossimna | 45006562 |

## Liens utiles

- [Workshop 3 : rebase et historique final](https://github.com/frozar/git-workshop-3) : décrit l'organisation Git attendue pour ce projet,
- [Historique final du workshop 3](https://github.com/frozar/git-workshop-3/blob/main/img/historique-final.png) : exemple du graphe à obtenir,
- [Jeu de la vie](https://fr.wikipedia.org/wiki/Jeu_de_la_vie) : présentation des règles du jeu de Conway,
- [Documentation argparse](https://docs.python.org/fr/3/library/argparse.html) : analyse des arguments d'un script Python,
- [Documentation random](https://docs.python.org/fr/3/library/random.html) : génération de grilles aléatoires reproductibles,
- [Philosophie d'Unix](https://fr.wikipedia.org/wiki/Philosophie_d%27Unix) : description de la philosophie Unix,
- [Pipeline (Unix)](https://en.wikipedia.org/wiki/Pipeline_(Unix%29) : description du pipe,
- [Installation de WSL](https://learn.microsoft.com/fr-fr/windows/wsl/install) : procédure officielle pour Windows,
- [Documentation ffmpeg](https://ffmpeg.org/documentation.html) : installation et utilisation de `ffmpeg`,
- [Site officiel de Gource](https://gource.io/) : présentation et téléchargement de Gource,
- [My Gource video production pipeline](https://dev.to/voieducode/my-gource-video-production-pipeline-5eb0) : exemple de création d'une vidéo Gource,
- [Documentation officielle de git rebase](https://git-scm.com/book/fr/v2/Les-branches-avec-Git-Rebaser-Rebasing) : fonctionnement du *rebase*.
