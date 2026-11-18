# Suivi des tâches — JobBoard AWD

## Équipe

| Membre | Microservice |
|---|---|
| Mohamed Aziz Mehrez | `ms-candidate` |
| Mohamed Rayen Sboui | `ms-job` |
| Maryem Slatni | `ms-application` |
| Mohamed Ezzedine Zouiten | `ms-interview` |
| Dhia Jbali | `ms-notification` |

## GitHub Projects (à faire sur le dépôt public)

1. Créer le repo public et pousser ce dossier (sans secrets).
2. Onglet **Projects** → New project (Board).
3. Colonnes : `Backlog` · `In progress` · `Review` · `Done`.
4. Créer une Issue par microservice + Issues docs/infra.
5. Assigner chaque Issue au owner (voir tableau).

## Backlog Validation 1

| ID | Tâche | Owner | Statut |
|---|---|---|---|
| T2 | Créer repo Git public + push `main` | Mohamed Aziz Mehrez | À faire |
| T3 | Commit personnel sur `ms-candidate` | Mohamed Aziz Mehrez | À faire |
| T4 | Commit personnel sur `ms-job` | Mohamed Rayen Sboui | À faire |
| T5 | Commit personnel sur `ms-application` | Maryem Slatni | À faire |
| T6 | Commit personnel sur `ms-interview` | Mohamed Ezzedine Zouiten | À faire |
| T7 | Commit personnel sur `ms-notification` | Dhia Jbali | À faire |
| T8 | Relire présentation 10 min | Tous | À faire |
| T9 | Déposer lien repo + membres sur Blackboard | Chef d’équipe | À faire |
| T10 | Captures Workshop 1 (3 screenshots) | Volontaire | À faire |
| T11 | Export PNG des diagrammes (optionnel ; SVG déjà OK) | Docs | À faire |

## Backlog après Validation 1 (métier)

| ID | Tâche | Service |
|---|---|---|
| B1 | CRUD réel Candidate/Address | ms-candidate |
| B2 | CRUD Job/Category | ms-job |
| B3 | Apply + Feign + events | ms-application |
| B4 | Schedule interview | ms-interview |
| B5 | Consumer RabbitMQ + mail | ms-notification |
| B6 | Sécurité JWT Keycloak sur Gateway | api-gateway |

## Convention d’avancement

- Une Issue = une PR courte.
- Cocher aussi `TODO.md` au fur et à mesure.
