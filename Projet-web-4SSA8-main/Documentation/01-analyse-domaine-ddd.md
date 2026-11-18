# Analyse de domaine (DDD) — JobBoard

## 1. Sous-domaines

| Sous-domaine | Type | Justification |
|---|---|---|
| **Recrutement / Candidature** | **Core** | Cœur différenciant : lier candidat ↔ offre, règles d’unicité et de disponibilité |
| **Catalogue d’offres** | **Core** | Publication et cycle de vie des jobs (ouvert/fermé) |
| **Identité candidat** | **Support** | Nécessaire au recrutement mais pas le différenciateur principal |
| **Planification d’entretiens** | **Support** | Prolonge le processus après candidature |
| **Notifications** | **Generic** | Pattern transversal (message broker + e-mail), remplaçable |
| **Authentification / IAM** | **Generic** | Keycloak (produit générique) |

## 2. Bounded contexts & ubiquitous language

### BC Identité Candidat (`ms-candidate`)
**Langage** : Candidate, Address, email unique, profil.  
**Ne connaît pas** : Job, Application métier complète.

### BC Catalogue Offres (`ms-job`)
**Langage** : Job, Category, availability, publication date.  
**Ne connaît pas** : Candidate, Interview.

### BC Candidature (`ms-application`)
**Langage** : Application, motivation, applicationDate, candidateId, jobId (références).  
**Règles** : une candidature max par couple (candidat, job) ; job doit être disponible.

### BC Entretien (`ms-interview`)
**Langage** : Interview, slot, status (SCHEDULED/DONE/CANCELLED), applicationId.  
**Ne possède pas** : le profil candidat ni l’offre complète.

### BC Notification (`ms-notification`)
**Langage** : Notification, channel (EMAIL), template, payload d’événement.  
**Consomme** des domain events ; n’écrit pas dans les bases métier.

### BC Identité technique (Keycloak)
**Langage** : Realm, Client, Role, Token JWT. Hors code métier.

## 3. Context Map (relations)

| Upstream | Downstream | Relation |
|---|---|---|
| Identité Candidat | Candidature | **Customer/Supplier** (Feign sync pour valider l’existence) |
| Catalogue Offres | Candidature | **Customer/Supplier** (Feign sync disponibilité) |
| Candidature | Entretien | **Customer/Supplier** (Feign : candidature existante) |
| Candidature / Entretien / Offres | Notification | **Published Language** via événements RabbitMQ |
| Keycloak | Tous (via Gateway) | **Conformist** (JWT) |
| — | — | **Shared Kernel évité** (pas de schéma / lib métier partagés) |
| Modèles externes | Notification / Feign clients | **Anti-Corruption Layer** léger (DTO + mapping events) |

Voir diagramme : `Diagrams/context-map.mmd` / `.svg`.

## 4. Anti-patterns évités

- **Un service par table** : Address reste dans le BC Candidat ; Category dans le BC Offres.  
- **Base partagée** : interdite (chaque MS a sa DB).  
- **Chaîne sync longue** : la notification est **asynchrone** pour ne pas créer un monolithe distribué.
- **Extraire seulement la recherche** : insuffisant face aux exigences Karim / Leila / Ines (voir `02-decoupage-microservices.md` alt. E).
