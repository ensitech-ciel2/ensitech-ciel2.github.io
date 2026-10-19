# Site de cours

Le site convertit les fichiers Markdown de `cours/` en pages web et PDF, puis publie automatiquement le résultat sur GitHub Pages.

## Ajouter des cours
- Place chaque `.md` dans `cours/NomDeMatiere/`.
- Garde les dossiers d'images à côté du Markdown, comme dans l'exemple.
- Fais un commit et un push vers la branche `main`. La publication est automatique.

Le chemin relatif identifie le cours : modifier `cours/Mathematiques/Integrales.md` met à jour ce cours. Deux matières peuvent avoir un cours du même nom.

## Activer GitHub Pages
Dans le dépôt : Settings → Pages → Build and deployment → Source : **GitHub Actions**.

## Attention
Le site GitHub Pages est public. Ne publie pas de données privées.
