# E1 — Sujet et analyse fonctionnelle (JobBoard)

**Équipe (6)** : Mohamed Aziz Mehrez, Mohamed Rayen Sboui, Maryem Slatni, Mohamed Ezzedine Zouiten, Dhia Jbali, **Samer**  
**Module** : AWD ESPRIT 2026-2027 · Validation 1 (conception + squelettes)  
**Références monolithes** : `JobBoard_Symfony_6_4` (Twig) + `BackEndRestFul_SpringBoot/awd-monolith` (REST + `awd_db`)

## 1. Problème réel et utilisateurs cibles

Les entreprises tunisiennes / startups tech publient des offres ; les candidats postulent en ligne ; les recruteurs trient et planifient des entretiens. Aujourd’hui, deux monolithes pédagogiques (Symfony Twig + Spring REST + MySQL unique) forcent un déploiement unique, une base partagée et un couplage fort — impossibles à scaler ou à exposer proprement à un mobile.

**Utilisateurs cibles** : candidats (étudiants / jeunes diplômés), recruteurs d’entreprise, administrateurs de plateforme.

## 2. Table des acteurs

| Acteur | Description | Objectifs principaux |
|---|---|---|
| **Candidat** | Personne cherchant un emploi | Profil, candidatures, notifications, entretiens |
| **Recruteur** | Représentant d’une entreprise | Publier/fermer offres, voir candidatures, planifier entretiens |
| **Administrateur** | Opérateur plateforme | Catégories, supervision, IAM (Keycloak) |
| **Système de notification** | Service technique | Envoyer e-mails suite aux domain events |

## 3. User stories (15) — par acteur, avec MS propriétaire

### Candidat

| ID | User story | MS |
|---|---|---|
| **US-01** | En tant que candidat, je veux créer mon profil (nom, prénom, email) afin d’être identifiable. | `ms-candidate` |
| **US-02** | En tant que candidat, je veux renseigner / modifier mon adresse afin de localiser mon profil. | `ms-candidate` |
| **US-03** | En tant que candidat, je veux consulter les offres ouvertes filtrées par catégorie afin de trouver un poste. | `ms-job` |
| **US-04** | En tant que candidat, je veux postuler une seule fois à une offre ouverte avec une motivation. | `ms-application` |
| **US-05** | En tant que candidat, je veux lister / retirer mes candidatures afin de suivre mon parcours. | `ms-application` |
| **US-06** | En tant que candidat, je veux recevoir un e-mail quand ma candidature est créée ou change de statut. | `ms-notification` |
| **US-07** | En tant que candidat, je veux être notifié lorsqu’un entretien est planifié. | `ms-notification` |

### Recruteur

| ID | User story | MS |
|---|---|---|
| **US-08** | En tant que recruteur, je veux créer / modifier une offre rattachée à une catégorie. | `ms-job` |
| **US-09** | En tant que recruteur, je veux ouvrir ou fermer une offre (`available`) sans republier tout l’objet. | `ms-job` |
| **US-10** | En tant que recruteur, je veux lister les candidatures reçues pour une offre. | `ms-application` |
| **US-11** | En tant que recruteur, je veux changer le statut d’une candidature (ex. UNDER_REVIEW → INTERVIEW). | `ms-application` |
| **US-12** | En tant que recruteur, je veux planifier / annuler un entretien lié à une candidature. | `ms-interview` |

### Administrateur

| ID | User story | MS |
|---|---|---|
| **US-13** | En tant qu’admin, je veux gérer les catégories d’offres (CRUD, nom unique). | `ms-job` |
| **US-14** | En tant qu’admin, je veux que l’accès API soit protégé par Keycloak (rôles). | Gateway + Keycloak (**Samer**) |
| **US-15** | En tant qu’admin / ops, je veux un healthcheck par service pour superviser la plateforme. | tous (`/actuator/health`) + Eureka (**Samer**) |

## 4. Diagramme de cas d’utilisation

Source : `Diagrams/use-cases.mmd` (export SVG associé).

## 5. Périmètre — In scope / Out of scope

### In scope (réaliste équipe étudiante — Validation 1 + itérations proches)

- Conception DDD + découpage 5 MS + infra Spring Cloud  
- Squelettes compilables / démarrables, Eureka, Config, Gateway, Keycloak, RabbitMQ, Docker Compose  
- APIs planifiées + events documentés (CRUD métier en itération suivante)  
- Notifications async (Python)  
- Documentation, présentation 10 min, suivi Issues  

### Out of scope (volontairement exclu)

- Matching IA obligatoire / scoring CV  
- Paiement / abonnements recruteurs  
- Chat temps réel candidat–recruteur  
- Kubernetes production, multi-région, DR  
- Upload CV sécurisé + antivirus + object storage cloud  
- Application mobile native complète  
- Saga distribuée complète avec compensation automatique (documentée, pas codée en V1)  
- Logique métier complète déjà livrée en Validation 1  

**Justification réalisme** : **6** étudiants, un module semestriel ; V1 valide l’architecture avant le code métier.
