# Contribution à ASFEX Formation Tchad

Merci de votre intérêt pour contribuer à ce projet ! Ce document décrit les directives de contribution.

## Code de conduite

Tous les contributeurs s'engagent à maintenir un environnement respectueux et inclusif.

## Comment contribuer

### Rapport de bugs
1. Vérifier que le bug n'a pas déjà été signalé (Issues)
2. Si nouveau, créer une Issue avec :
   - Titre descriptif
   - Description détaillée du problème
   - Étapes de reproduction
   - Résultat attendu vs résultat obtenu
   - Environnement (OS, Python version, etc.)

### Suggestions de fonctionnalités
1. Créer une Issue avec le tag "enhancement"
2. Décrire clairement la fonctionnalité proposée
3. Expliquer le cas d'usage et les bénéfices

### Pull Requests
1. Fork le repository
2. Créer une branche : `git checkout -b feature/ma-feature`
3. Commit avec messages clairs : `git commit -m "Ajouter nouvelle fonctionnalité"`
4. Push : `git push origin feature/ma-feature`
5. Créer un Pull Request

## Conventions de code

### Python
- Suivre PEP 8
- Utiliser des noms descriptifs pour les variables et fonctions
- Ajouter des docstrings pour les fonctions complexes
- Limiter les lignes à 100 caractères

### Django
- Respecter la structure MVC (Models, Views, Templates)
- Utiliser les Forms pour valider les données
- Ajouter les tests pour les nouvelles fonctionnalités
- Utiliser des migrations pour les modifications de modèles

### HTML/CSS
- Utiliser Bootstrap pour la cohérence
- Classes BEM pour le CSS personnalisé
- Accessibilité (alt text, labels, etc.)

## Tests

Avant de soumettre un PR :
```bash
python manage.py test
python manage.py check --deploy
```

Ajouter des tests pour :
- Les nouveaux modèles
- Les nouvelles vues
- Les formulaires
- Les validations

## Documentation

Mettre à jour :
- README.md si nouveaux prérequis ou nouvelles fonctionnalités
- Commentaires de code pour les algorithmes complexes
- CONTRIBUTING.md pour les changements du processus

## Branches

- `main` : Version stable en production
- `develop` : Version de développement
- `feature/*` : Nouvelles fonctionnalités
- `bugfix/*` : Corrections de bugs

## Commit Messages

Format :
```
[TYPE] Titre court et descriptif

Description détaillée si nécessaire.

Fixes #numéro_issue
```

Types :
- `feat` : Nouvelle fonctionnalité
- `fix` : Correction de bug
- `docs` : Documentation
- `style` : Formatage du code
- `refactor` : Refactorisation sans changement fonctionnel
- `test` : Ajout/modification de tests
- `chore` : Tâches de maintenance

## Questions ?

Créer une Discussion dans le repository ou contacter : contact@asfex-formation-tchad.com

Merci pour votre contribution ! 🙏
