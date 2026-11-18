# E2 — Découpage microservices

## 1. Vue d’ensemble (4 métier + 1 avancé)

| Service | Capacité métier | Bounded context | Responsabilités | Ce qu’il ne doit PAS faire | Pourquoi séparé |
|---|---|---|---|---|---|
| **ms-candidate** | Identité & profil candidat | BC Identité Candidat | CRUD Candidate/Address, unicité email | Gérer jobs, candidatures, mails, entretiens | Cycle de vie profil ≠ dépôt de candidature ; ownership Aziz |
| **ms-job** | Catalogue d’offres | BC Catalogue Offres | CRUD Job/Category, disponibilité | Gérer candidats, candidatures, entretiens | Charge lecture/recherche scalable indépendamment ; ownership Rayen |
| **ms-application** | Dépôt & suivi candidatures | BC Candidature | Agrégat Application, règles unicité/disponibilité | Posséder le profil ou l’offre ; envoyer les mails | Cœur différenciant ; orchestre des IDs seulement ; ownership Maryem |
| **ms-interview** | Planification d’entretiens | BC Entretien | CRUD Interview, créneaux, statut | Recréer Application/Job/Candidate | Apparaît après candidature ; modèle document ; ownership Ezzedine |
| **ms-notification** *(avancé)* | Diffusion d’alertes | BC Notification | Consommer events, envoyer e-mails (+ LLM optionnel) | Décider des règles métier candidature/offre | I/O lente + polyglotte Python ; ne doit pas bloquer le métier ; ownership Dhia |

## 2. Alternatives rejetées

### Alternative A — Un microservice par table
**Rejeté.** Address (1 table) et Category (1 table) ne sont pas des capacités métier autonomes. Les découper créerait de la latence Feign inutile et un monolithe distribué (trop d’appels sync). Address reste dans `ms-candidate` ; Category dans `ms-job`.

### Alternative B — Tout fusionner en 2 services (Profile + Recruiting)
**Rejeté.** Fusionner Job + Application + Interview empêche de scaler la recherche d’offres sans scaler aussi les écritures de candidatures, et empêche une équipe Python dédiée aux notifications.

### Alternative C — Notification synchrone dans ms-application
**Rejeté.** Un SMTP lent dans `POST /applications` bloque la transaction utilisateur (leçon monolithe / Prosit). Les mails passent par RabbitMQ → `ms-notification`.

### Alternative D — Base partagée `awd_db` entre MS
**Rejeté.** Contredit *database per service* ; recrée le couplage du monolithe (FK cross-domaine, schéma partagé).

### Alternative E — Extraire seulement un `ms-search` / lecture d’offres
**Rejeté.** Soulage Sami (×50 recherche) à court terme mais **ne résout pas** : ownership de schéma (Karim), équipes Node/Python (Leila), ni le couplage delete Job/Candidate → table `application`. Ce n’est pas un découpage par bounded context complet.

## 3. Owners

| Membre | Service / rôle |
|---|---|
| Mohamed Aziz Mehrez | ms-candidate |
| Mohamed Rayen Sboui | ms-job |
| Maryem Slatni | ms-application |
| Mohamed Ezzedine Zouiten | ms-interview |
| Dhia Jbali | ms-notification |
| **Samer** | Plateforme (Gateway, Eureka, Config, Keycloak) — pas un 6ᵉ MS métier |
