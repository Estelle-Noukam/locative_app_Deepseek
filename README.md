# Gestion Locative Immobilière

Application web pour la gestion de biens immobiliers avec Flask et PostgreSQL.

## Installation et lancement

```bash
# Démarrer l'application
docker-compose up --build

# Accéder à l'application
http://localhost:5000
Comptes par défaut
Rôle	Email	Mot de passe
Administrateur	admin@example.com	admin123
Fonctionnalités
Gestion des utilisateurs (3 rôles : admin, propriétaire, locataire)

CRUD propriétés, baux, paiements, réclamations

Demandes de location

Tableau de bord administrateur

API RESTful

Commandes utiles
bash
docker-compose up -d          # Démarrer en arrière-plan
docker-compose down           # Arrêter
docker-compose down -v        # Réinitialiser
docker-compose logs -f        # Voir les logs
Structure
text
backend/
├── app.py           # Application principale
├── requirements.txt # Dépendances
└── templates/       # Templates HTML
Dockerfile
docker-compose.yml
Dépannage
Port déjà utilisé :

bash
# Changer les ports dans docker-compose.yml
ports:
  - "5433:5432"  # PostgreSQL
  - "5001:5000"  # Web
