# PortabilityGuard

> A static analysis library to detect cross-platform compatibility issues in Python code.

## Description

**PortabilityGuard** est une bibliothèque d'analyse statique conçue pour aider les développeurs à identifier les problèmes de portabilité entre systèmes d'exploitation (Linux, Windows, macOS) directement dans leur code source. 

Ce projet est développé dans le cadre d'un cursus en école d'ingénieur (ENSISA).

## Fonctionnalités actuelles

- **Détection des chemins codés en dur** : Repérage des chemins absolus spécifiques à un OS (`/home/...` ou `C:\...`) qui cassent la compatibilité multi-plateforme.

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
```
pytest
```

## Auteurs
- [Clovis Tiemtoré](https://github.com/clovisTiemtore)
- [Erwan Vangu](https://github.com/erwan75019)

## Licence
Distribué sous la licence [MIT](LICENSE).