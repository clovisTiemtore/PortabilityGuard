# PortabilityGuard

> A static analysis library to detect cross-platform compatibility issues in Python code.

## Description

**PortabilityGuard** est une bibliothèque d'analyse statique conçue pour aider les développeurs à identifier les problèmes de portabilité entre systèmes d'exploitation (Linux, Windows, macOS) directement dans leur code source.

Ce projet est développé dans le cadre d'un cursus en école d'ingénieur (ENSISA).

## Fonctionnalités actuelles

- **Détection des chemins codés en dur** : Repérage des chemins absolus spécifiques à un OS (`/home/...` ou `C:\...`) qui cassent la compatibilité multi-plateforme.

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

### Détection des accès aux variables d'environnement propres à Windows

La fonction `find_platform_specific_env_vars` repère les lectures directes de
`APPDATA` et `LOCALAPPDATA` via `os.environ[...]`. Ces accès peuvent lever une
`KeyError` si la variable est absente. L'analyse est statique et fonctionne sur
tous les systèmes.

```python
from portabilityguard.env_detector import find_platform_specific_env_vars

source = 'import os\ncache = os.environ["APPDATA"]'
find_platform_specific_env_vars(source)
# [(2, "APPDATA")]
```

Chaque résultat contient le numéro de ligne et le nom de la variable. La règle
reconnaît la syntaxe littérale `os.environ[...]` et ignore les appels à
`os.environ.get()`. La résolution des alias, des noms réaffectés et des clés
calculées est hors périmètre.

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
