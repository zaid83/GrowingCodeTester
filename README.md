# Growing Code Tester

Un testeur automatisé pour les exercices Growing Code, inspiré des principes des libfttester avec vérifications de conformité complètes.

## ⚠️ Avertissement Important

**Ce testeur est un outil d'aide au développement et ne remplace en aucun cas :**
- ✋ **Un reviewer humain** - La relecture par un pair reste essentielle
- 🔍 **Une code review complète** - L'analyse critique du code nécessite un œil humain
- 🎯 **L'évaluation finale** - Seuls les correcteurs officiels valident votre travail

**Utilisez ce testeur comme :**
- 🚀 **Aide au développement** - Détection rapide des erreurs courantes
- ✅ **Vérification de conformité** - Respect des standards de base
- 🔧 **Outil de debugging** - Identification des problèmes avant soumission

## 📋 Prérequis OBLIGATOIRES

**Avant d'utiliser le testeur, installez flake8 :**
```bash
pip install flake8
```

**Vérifiez l'installation :**
```bash
flake8 --version  # Doit afficher la version de flake8
```

**Sans flake8, le testeur ne fonctionnera pas correctement !**

## 📁 Structure attendue

Le testeur s'attend à trouver vos exercices dans cette structure :
```
.
├── ex0/
│   └── ft_hello_garden.py
├── ex1/
│   └── ft_plot_area.py
├── ex2/
│   └── ft_harvest_total.py
├── ex3/
│   └── ft_plant_age.py
├── ex4/
│   └── ft_water_reminder.py
├── ex5/
│   ├── ft_count_harvest_iterative.py
│   └── ft_count_harvest_recursive.py
├── ex6/
│   └── ft_garden_summary.py
├── ex7/
│   └── ft_seed_inventory.py


## ✅ Vérifications de conformité

### 🗂️ Structure des fichiers
- Vérifie que chaque exercice est dans le bon répertoire (`ex0/`, `ex1/`, etc.)
- Détecte les fichiers mal placés

### 🔧 Fonctions autorisées
- **Ex0** : `print()`
- **Ex1-4** : `input()`, `int()`, `print()`
- **Ex5** : `input()`, `int()`, `print()`, `range()`
- **Ex6** : `input()`, `print()`
- **Ex7** : `print()`, `capitalize()` (méthodes string)

### 🚫 Validation d'entrée
- Vérifie qu'il n'y a pas de validation non demandée
- Pas de gestion des nombres négatifs (sauf si explicitement mentionné)

### 📝 Structure du code
- Une seule fonction par fichier
- Nom de fonction exact
- **Flake8 intégré** : Standards Python 3.10+

### 🎯 Tests de cas limites
- **Ex3** : Vérifie strictement > 60 jours (test avec 60, 75, 45)
- **Ex4** : Vérifie strictement > 2 jours (test avec 2, 4, 1)
- **Logique précise** : Conditions strictement supérieures

## 🧪 Tests fonctionnels

### Exercise 0 - ft_hello_garden
- Vérifie que la fonction affiche "Hello, Garden community!"

### Exercise 1 - ft_plot_area  
- Test avec longueur=5, largeur=3
- Vérifie le calcul correct (15)

### Exercise 2 - ft_harvest_total
- Test avec poids: 5, 8, 3
- Vérifie le total correct (16)

### Exercise 3 - ft_plant_age
- Test avec 75 jours (doit être prêt)
- Test avec 60 jours (cas limite - PAS prêt)
- Test avec 45 jours (doit attendre)
- Vérifie la logique strictement > 60 jours

### Exercise 4 - ft_water_reminder
- Test avec 4 jours (doit arroser)
- Test avec 2 jours (cas limite - plantes OK)
- Test avec 1 jour (plantes OK)
- Vérifie la logique strictement > 2 jours

### Exercise 5 - ft_count_harvest
- Test des versions itérative et récursive
- Vérifie le comptage de 1 à N avec "Harvest time!"

### Exercise 6 - ft_garden_summary
- Test avec "Community Garden" et 25 plantes
- Vérifie le format de sortie complet

### Exercise 7 - ft_seed_inventory
- Test avec différentes unités (packets, grams, area)
- Test avec unité inconnue
- Vérifie les type hints

## 🎨 Fonctionnalités avancées

- **Tests automatisés** : Simulation d'entrées utilisateur
- **Flake8 intégré** : Vérification officielle des standards Python
- **Tests de cas limites** : Vérification des conditions strictes (>60, >2)
- **Capture de sortie** : Vérification des outputs
- **Gestion d'erreurs** : Détection des exceptions et erreurs
- **Rapport coloré** : Résultats visuels avec couleurs
- **Double validation** : Conformité + Tests fonctionnels

## 🔧 Avantages par rapport au main.py

| main.py | growingcodetester.py |
|---------|---------------------|
| Tests manuels | Tests automatisés |
| Pas de validation | **6 vérifications de conformité** |
| Un test à la fois | Tests multiples + structure |
| Pas de rapport | Rapport détaillé séparé |
| Pas de flake8 | **Flake8 intégré officiel** |
| Pas de vérif fonctions | **Fonctions autorisées vérifiées** |
| Pas de cas limites | **Tests de frontière (>60, >2)** |

## 📊 Exemple de sortie

```
🌱 GROWING CODE TESTER 🌱
Automated Testing Suite for Growing Code Exercises
============================================================

Testing Exercise 1: ft_plot_area
--------------------------------------------------

COMPLIANCE CHECKS:
✅ ft_plot_area_file_structure: ✓ Correct file structure
✅ ft_plot_area_authorized_functions: ✓ Uses only authorized functions
✅ ft_plot_area_no_validation: ✓ No unnecessary input validation
✅ ft_plot_area_single_function: ✓ Contains only the requested function
✅ ft_plot_area_correct_name: ✓ Function name matches exactly
✅ ft_plot_area_flake8: ✓ Flake8 compliant

FUNCTIONAL TESTS:
✅ ft_plot_area: ✓ Correct calculation

Compliance: 6/6 checks passed
Functional: 1/1 tests passed
🎉 All tests and compliance checks passed! 🎉
```

## 🛠️ Développement technique

Le testeur utilise :
- **Subprocess + flake8** : Vérification officielle des standards
- **Fichiers temporaires** : Tests flake8 sécurisés
- **AST parsing** : Analyse syntaxique du code
- **Regex** : Détection des fonctions non autorisées
- **Capture stdout** : Vérification des sorties
- **Simulation input()** : Tests automatisés
- **Importation dynamique** : Chargement des modules
- **Gestion robuste des erreurs** : Rapports détaillés

## 🎯 Standards respectés

- **Python 3.10+** : Syntaxe moderne
- **Flake8** : E501, E225, W292, etc.
- **Type hints** : Exercice 7
- **Structure projet** : Arborescence stricte
- **Fonctions autorisées** : Selon le sujet
- **Pas de validation** : Comportement indéfini pour entrées invalides

Inspiré des meilleures pratiques des libfttester pour une validation complète et automatisée conforme aux standards 42.
