# PortabilityGuard

> A static analysis library to detect cross-platform compatibility issues in Python code.

## Description

**PortabilityGuard** est une bibliothèque d'analyse statique conçue pour aider les développeurs à identifier les problèmes de portabilité entre systèmes d'exploitation (Linux, Windows, macOS) directement dans leur code source.

Ce projet est développé dans le cadre d'un cursus en école d'ingénieur (ENSISA).

## Fonctionnalités actuelles

- **Détection des chemins codés en dur** : Repérage des chemins absolus spécifiques à un OS (`/home/...` ou `C:\...`) qui cassent la compatibilité multi-plateforme.
- **Détection des encodages manquants** : Repérage des appels à `open()` en
  mode texte qui dépendent de l'encodage par défaut du système.

### Détection des chemins absolus

La fonction `find_absolute_paths` analyse du code Python sans l'exécuter et
retourne chaque littéral représentant un chemin absolu avec son numéro de ligne :

```python
from portabilityguard.path_detector import find_absolute_paths

source = 'config = "/home/alice/project/config.json"'
find_absolute_paths(source)
# [(1, "/home/alice/project/config.json")]
```

La règle reconnaît les chemins POSIX et Windows quel que soit le système sur
lequel PortabilityGuard est exécuté. Elle examine tous les littéraux de type
chaîne, sans déterminer s'ils sont réellement utilisés pour accéder à un
fichier. Elle ne résout pas les chemins construits dynamiquement, par exemple
par concaténation ou interpolation.

### Détection des encodages manquants

La fonction `find_missing_encodings` analyse les appels directs à `open()` et
retourne le numéro de ligne ainsi qu'un message pour chaque ouverture en mode
texte sans encodage explicite :

```python
from portabilityguard.encoding_detector import find_missing_encodings

source = '''
open("report.txt", "w")
open("data.bin", "rb")
open("config.txt", encoding="utf-8")
'''
find_missing_encodings(source)
# [(2, "open() uses text mode without an explicit encoding; results may vary across platforms.")]
```

Le mode par défaut et les modes texte `r`, `w`, `a` et `x` sont contrôlés. Les
modes binaires tels que `rb` ou `wb` sont ignorés, car ils n'acceptent pas
d'encodage. Les arguments peuvent être positionnels ou nommés, y compris
l'encodage passé comme quatrième argument positionnel.

L'analyse repose uniquement sur l'AST et n'exécute jamais le code. Pour éviter
les faux positifs, elle ignore les modes calculés dynamiquement et les appels
utilisant `*args` ou `**kwargs`. Elle cible la forme directe `open(...)` : elle
ne résout pas les alias, les redéfinitions locales du nom `open` ou les méthodes
comme `Path.open()`.

## Installation

Clone le dépôt et installe le projet en mode développement (avec les outils de test et de lintage) :

```bash
git clone https://github.com/clovisTiemtore/PortabilityGuard.git

cd PortabilityGuard

python3 -m venv .venv

source .venv/bin/activate

pip install -e ".[dev]"
```

## Utilisation et Tests

Pour lancer la suite de tests unitaires et mesurer la couverture de code :

```bash
pytest
```

## Auteurs

- [Clovis Tiemtoré](https://github.com/clovisTiemtore)
- [Erwan Vangu](https://github.com/erwan75019)

## Licence

Distribué sous la licence [MIT](LICENSE).
