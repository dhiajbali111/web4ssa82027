# Prosit 1 — Audit statique Symfony 6.4 JobBoard

> Analyse **statique uniquement** (pas d’exécution requise). Sources : `JobBoard_Symfony_6_4/`.

## 1. Problématique

Le JobBoard Symfony est un monolithe pédagogique de recrutement (Twig + Doctrine + Security session). Quelles preuves de couplage et quelles limites freinent une évolution multi-clients (web + mobile) et multi-équipes ?

## 2. Hypothèses

| # | Hypothèse | Verdict | Preuve |
|---|---|---|---|
| H1 | Une seule application déployable | **Validée** | Structure unique `src/`, `public/index.php`, README « Single deployment unit » |
| H2 | Une base relationnelle partagée | **Validée** | `config/packages/doctrine.yaml` + entités liées ; `.env` `DATABASE_URL` SQLite/MySQL unique |
| H3 | Auth centralisée par session formulaire | **Validée** | `config/packages/security.yaml` — `form_login`, un provider `User` |
| H4 | Collaboration métier in-process synchrone | **Validée** | `ApplicationManager::apply` |
| H5 | API REST publique déjà exposée | **Réfutée** | Controllers + Twig ; README « No public REST API » |
| H6 | Conteneurisation / discovery déjà en place | **Réfutée** | README contrainte 10 : Docker/K8s exclus du baseline |

## 3. Cartographie fonctionnelle

### Acteurs
- Visiteur, Candidat (`ROLE_CANDIDATE`), Entreprise (`ROLE_COMPANY`), Admin (`ROLE_ADMIN`).

### Processus
1. Parcourir / voir une offre (`HomeController`).
2. Postuler (`CandidateController::apply` → `ApplicationManager`).
3. Entreprise publie des jobs (`CompanyController`).
4. Admin consulte des totaux (`AdminController`).

### Fonctionnalités (extrait)
Profil candidat + skills, candidature unique, lettre de motivation, statuts (`SUBMITTED`…`INTERVIEW`…), compteurs côté entreprise, dashboard admin.

## 4. Architecture actuelle

```
Browser → Symfony front controller → Controllers → Services/Repositories → Doctrine → SQLite/MySQL
                ↘ Twig templates
                ↘ Security form_login (session)
```

Pas d’API Gateway, pas d’événements, pas de discovery.

## 5. Couplages — extraits commentés

### 5.1 Transaction locale synchrone
Fichier : `src/Service/ApplicationManager.php` — méthode `apply`  
Charge le job, vérifie `isPublished()`, cherche une candidature existante, `persist` + `flush` dans le même process.  
→ Tout le parcours métier est **local** et **bloquant** pour la requête HTTP.

### 5.2 Relations Doctrine cross-domaine
Fichier : `src/Entity/Application.php`  
`ManyToOne` vers `Candidate` et `Job` + contrainte d’unicité `(candidate_id, job_id)`.  
→ Le modèle d’application **connaît** physiquement les autres agrégats (jointures / cascades possibles).

### 5.3 Contrôleur candidat couplé au manager + EM
Fichier : `src/Controller/CandidateController.php`  
`apply(...)` valide CSRF, appelle `ApplicationManager`, flash session, redirect Twig.  
→ UI, sécurité session et métier dans la **même** unité de déploiement.

### 5.4 Sécurité centralisée
Fichier : `config/packages/security.yaml`  
Un firewall `main`, `form_login`, hiérarchie de rôles, `access_control` par préfixe URL.  
→ Adapté au web serveur ; **peu adapté** tel quel à un mobile token-based multi-API.

## 6. Limites

| Axe | Limite |
|---|---|
| **Maintenance** | Tout changement (offre, candidature, auth) risque de régression globale |
| **Scalabilité** | Impossible de scaler seulement la recherche d’offres |
| **Déploiement** | Release unique ; rollback monolithique |
| **Multi-terminaux** | Session cookie + Twig : mobile natif difficile sans API |
| **Auth session** | Affinité serveur / CSRF form ; pas de JWT standard out-of-the-box |

## 7. Proposition d’architecture cible

- Extraire les capacités : Candidate, Job, Application, Interview, Notification.  
- Exposer un **API Gateway** + **Keycloak** (tokens).  
- Remplacer les appels in-process par **Feign** (règles sync) + **événements** (notifications).  
- **Database per service**.  
- Front Symfony/SPA consomme le Gateway ; mobile aussi.

Voir dossiers Validation 1 (`Documentation/02-…` à `05-…`) et diagrammes associés.
