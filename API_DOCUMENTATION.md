Fonctionnalité : Authentification des utilisateurs

- Création de compte : /sign_up 
- Connexion des utilisateurs : /log_in
- Déconnexion des utilisateurs : /log_out

Fonctionnalité : Gestion Compte utilisateurs

- Modification des informations utilisateurs : /users/<int:id>/edit
- Voir les informations utilisateurs : /users/<int:id>/profile

Fonctionnalité : Gestion des lieux

- Liste des lieux : /lieux
- Détails d'un lieu : /lieux/<int:id>
- Ajouter un lieu : /lieux/add
- Modifier un lieu : /lieux/<int:id>/edit
- Supprimer un lieu : /lieux/<int:id>/delete
- Ajouter un avis : /lieux/<int:id>/avis/add
- Modifier un avis : /lieux/<int:id>/avis/edit
- Supprimer un avis : /lieux/<int:id>/avis/delete

Fonctionnalité : Gestion des évènements

- Liste des évènements : /evenements
- Détails d'un évènement : /evenements/<int:id>
- Ajouter un évènement : /evenements/add
- Modifier un évènement : /evenements/<int:id>/edit
- Supprimer un évènement : /evenements/<int:id>/delete
- Ajouter un avis : /evenements/<int:id>/avis/add
- Modifier un avis : /evenements/<int:id>/avis/edit
- Supprimer un avis : /evenements/<int:id>/avis/delete

Fonctionnalité : Gestion des Photos et Vidéos

- Liste des medias : /medias
- Détails d'un media : /medias/<int:id>
- Ajouter un media : /medias/add
- Modifier un media : /medias/<int:id>/edit
- Supprimer un media : /medias/<int:id>/delete
