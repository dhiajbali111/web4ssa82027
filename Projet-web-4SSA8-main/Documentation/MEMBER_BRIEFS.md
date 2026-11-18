# Briefs individuels — qui fait quoi / que savoir

**Règle orale** : chaque membre présente **son** microservice (sinon risque 0 sur I1–I3).  
Lire aussi : `03-fiches-microservices.md`, `QA_PREP.md` (section de ton MS), slide dédiée dans le PPTX.

Ports / noms / events = même chose partout (README, docker-compose, docs).

---

## 1. Mohamed Aziz Mehrez → `ms-candidate` (port **8081**)

### Son rôle dans l’équipe
- Owner du **profil candidat** (identité).
- Ouvre souvent la présentation (intro / démo Eureka / health) **et** présente obligatoirement la slide **ms-candidate**.

### Ce qu’il POSSEDE (son service)
| Élément | Détail |
|---|---|
| Bounded context | BC Identité Candidat |
| Entités | `Candidate` (id, firstname, lastname, email unique), `Address` (street, houseNumber, zipCode) |
| Relation | Candidate 0..1 — Address (FK **dans la même DB**, OK) |
| Base | **MySQL** `candidate_db` · hôte Docker port **3307** |
| Techno | Spring Boot, JPA, Eureka client, Config client, Feign, Actuator |
| API racine | `/api/candidates`, `/api/addresses` |
| Event publié | `CandidateDeleted` |
| Dossier code | `Backend/ms-candidate/` |

### Ce qu’il ne doit PAS faire
- Gérer les jobs, candidatures, entretiens, e-mails.
- Mettre Address dans un microservice séparé.

### User stories qu’il porte
US-01, US-02 (profil / adresse). US-15 santé (comme tous).

### Qui l’appelle / qu’il appelle
- **Appelé par** `ms-application` (Feign) : « ce candidat existe-t-il ? »
- Peut appeler `ms-application` avant un DELETE (optionnel) pour éviter d’effacer un candidat qui a des candidatures.
- Si son service est **down** → Application répond **503** (pas de candidature créée).

### Ce qu’il doit savoir expliquer à l’oral (30–60 s)
1. Pourquoi MySQL (relationnel 1–1, continuité monolithe).  
2. Pourquoi Address n’est pas un MS (pas une capacité métier).  
3. API REST plurielle + codes 201/404/409 (email dupliqué).  
4. Database per service : sa DB ≠ `job_db`.  
5. Health : `http://localhost:8081/actuator/health`.

### Comment le démarrer
```bat
cd Backend
mvn -pl ms-candidate spring-boot:run -Dspring-boot.run.profiles=h2
```

### Q&A à réviser
QA_PREP Q26–Q31 + Q1–Q8.

---

## 2. Mohamed Rayen Sboui → `ms-job` (port **8082**)

### Son rôle
- Owner du **catalogue d’offres**.
- Présente souvent le **découpage E2** (slide alternatives rejetées) **et** sa slide **ms-job**.

### Ce qu’il POSSEDE
| Élément | Détail |
|---|---|
| Bounded context | BC Catalogue Offres |
| Entités | `Job` (name, description, available, date, categoryId), `Category` (name unique, description) |
| Relation | Category 1 — * Job (FK **locale**) |
| Base | **MySQL** `job_db` · port hôte **3308** |
| API | `/api/jobs`, `/api/categories`, `PATCH /api/jobs/{id}/availability` |
| Event | `JobAvailabilityChanged` `{jobId, available, …}` |
| Code | `Backend/ms-job/` |

### Ce qu’il ne doit PAS faire
- Gérer candidats, candidatures, entretiens, mails.
- Partager sa MySQL avec candidate (même techno ≠ même base).

### User stories
US-03 (consultation), US-08, US-09, US-13 (catégories admin).

### Interactions
- **Appelé sync** par `ms-application` (job existe + `available=true`).
- Publie event async quand dispo change → Application (éventuel) + Notification.

### À expliquer à l’oral
1. Pourquoi Category reste dans job (pas 1 service/table).  
2. PATCH availability = ouvrir/fermer sans republier tout.  
3. Event async vs Feign sync.  
4. Port 8082, health UP.  
5. Si job down → postuler impossible (503).

### Démarrage
```bat
mvn -pl ms-job spring-boot:run -Dspring-boot.run.profiles=h2
```

### Q&A
QA_PREP Q32–Q37.

---

## 3. Maryem Slatni → `ms-application` (port **8083**) — cœur métier

### Son rôle
- Owner des **candidatures** (core domain).
- Présente souvent **DDD / context map** + sa slide + une partie **sync vs async / CB**.

### Ce qu’elle POSSEDE
| Élément | Détail |
|---|---|
| Bounded context | BC Candidature |
| Entité | `Application` : id, applicationDate, motivation, status, **candidateId**, **jobId** |
| Important | **Pas de FK** vers MySQL candidate/job — seulement des IDs Long |
| Base | **PostgreSQL** `application_db` · port **5433** |
| API | `/api/applications` (GET/POST/PUT/PATCH/DELETE) |
| Events publiés | `ApplicationCreated`, `ApplicationStatusChanged` |
| Event consommé | `JobAvailabilityChanged` (cohérence éventuelle) |
| Code | `Backend/ms-application/` |

### Ce qu’elle ne doit PAS faire
- Stocker le profil candidat ou l’offre complète.
- Envoyer l’e-mail en synchrone dans le POST (→ notification async).
- Chaîne Feign trop longue (sinon monolithe distribué).

### User stories
US-04, US-05, US-10, US-11.

### Interactions (à maîtriser parfaitement)
```
POST /applications
  → Feign ms-candidate (existe ?)
  → Feign ms-job (available ?)
  → save Application
  → publish ApplicationCreated → RabbitMQ → ms-notification
```
**Si candidate ou job down** : timeout 2s → retry ×3 → circuit breaker Resilience4j → **503**, **aucune** écriture.

### À expliquer à l’oral
1. Pourquoi PostgreSQL (polyglot + UNIQUE).  
2. Pourquoi sync pour valider, async pour mail.  
3. Plan de panne Resilience4j.  
4. Cohérence éventuelle des notifications.  
5. 409 = double candidature ou job fermé.

### Démarrage
```bat
mvn -pl ms-application spring-boot:run -Dspring-boot.run.profiles=h2
```

### Q&A
QA_PREP Q38–Q44 + Q10–Q15 (saga/outbox/éventualité).

---

## 4. Mohamed Ezzedine Zouiten → `ms-interview` (port **8084**)

### Son rôle
- Owner de la **planification d’entretiens**.
- Présente sa slide MS ; peut aider sur Mongo / documents.

### Ce qu’il POSSEDE
| Élément | Détail |
|---|---|
| Bounded context | BC Entretien |
| Document | `Interview` : id, applicationId, slot, status, meetingUrl, notes |
| Base | **MongoDB** `interview_db` · port **27017** |
| API | `/api/interviews` + `PATCH .../status` |
| Events | `InterviewScheduled`, `InterviewCancelled` |
| Code | `Backend/ms-interview/` |
| Profil local sans Mongo | `nodb` |

### Ce qu’il ne doit PAS faire
- Recréer Candidate / Job / Application.
- Joindre cross-DB (seulement `applicationId` logique).

### User stories
US-12 (planifier/annuler entretien).

### Interactions
- **Feign sync** → `ms-application` (la candidature existe).
- **Async** → RabbitMQ → notification (mail entretien).

### À expliquer à l’oral
1. Pourquoi Mongo (champs optionnels flexibles).  
2. Pourquoi après candidature (BC séparé).  
3. Feign vers application puis event.  
4. Port 8084 / profil `nodb` pour squelette.  
5. Si application down → 503, pas d’interview orpheline.

### Démarrage
```bat
mvn -pl ms-interview spring-boot:run -Dspring-boot.run.profiles=nodb
```

### Q&A
QA_PREP Q45–Q50.

---

## 5. Dhia Jbali → `ms-notification` (port **8085**) — service avancé

### Son rôle
- Owner du **5e MS avancé** (Python + messaging).
- Présente sa slide ; peut co-présenter events / RabbitMQ ; owner Issues docker souvent.

### Ce qu’il POSSEDE
| Élément | Détail |
|---|---|
| Bounded context | BC Notification (generic) |
| Techno | **Python FastAPI** + **RabbitMQ** (+ LLM optionnel plus tard) |
| DB métier | **Aucune** partagée (pas de vérité métier) |
| API | `/actuator/health`, `/api/notifications/ping` |
| Consomme | ApplicationCreated, ApplicationStatusChanged, InterviewScheduled, InterviewCancelled, (opt.) JobAvailabilityChanged |
| Code | `Backend/ms-notification/` |

### Ce qu’il ne doit PAS faire
- Décider si une candidature est valide.
- Appeler Feign les MS métier (créérait un monolithe distribué).
- Bloquer le POST candidature en attendant SMTP.

### User stories
US-06, US-07 (mails).

### Interactions
- **Uniquement async** : RabbitMQ → consumer.
- Idempotence via `eventId` (ignorer doublons).
- Si service down → messages restent en queue, rattrapage ensuite.
- Si LLM down → template texte fixe.

### À expliquer à l’oral (très important — « avancé »)
1. Pourquoi Python (polyglotte / équipe différente).  
2. Pourquoi async (I/O lente).  
3. Pourquoi pas de DB partagée.  
4. Idempotence + cohérence éventuelle.  
5. Comment démarrer : `python -m uvicorn app.main:app --port 8085` (uvicorn pas toujours dans le PATH).

### Démarrage
```bat
cd Backend\ms-notification
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8085
```

### Q&A
QA_PREP Q51–Q56 + Q19–Q22.

---

---

## 6. Samer → plateforme (Gateway / Eureka / Config / Keycloak)

### Son rôle
- Owner de la **plateforme** (pas un MS métier).
- Présente souvent l’architecture cible, les ports infra et le démarrage Compose / Gateway.

### Ce qu’il POSSEDE
| Élément | Détail |
|---|---|
| Composants | API Gateway `:8080`, Eureka `:8761`, Config Server `:8888`, Keycloak `:8180`, Docker Compose |
| Rôle | Point d’entrée unique, discovery, config centralisée, IAM JWT |
| Code | `Backend/api-gateway/`, `eureka-server/`, `config-server/`, `docker-compose.yml` |

### Ce qu’il ne doit PAS faire
- Implémenter les règles métier candidature / offres / entretiens.
- Posséder une base métier (pas de `awd_db` partagée).

### À expliquer à l’oral
1. Pourquoi un Gateway (3 clients).  
2. Pourquoi Eureka (pas d’IP figées).  
3. Pourquoi Config Server.  
4. Keycloak = Conformist JWT.  
5. Health / restart d’un MS sans tout couper (contrairement au monolithe `:8080`).

### Q&A
QA_PREP Q sur Gateway / Eureka / Config / Keycloak.

---

## Tableau récap (à imprimer)

| Membre | MS / rôle | Port | DB | Parle de |
|---|---|---|---|---|
| Aziz Mehrez | candidate | 8081 | MySQL :3307 | Profil, Address, Feign inbound |
| Rayen Sboui | job / offer | 8082 | MySQL :3308 | Offres, Category, availability |
| Maryem Slatni | application | 8083 | PostgreSQL :5433 | Core, Feign, CB, events |
| Ezzedine Zouiten | interview | 8084 | Mongo :27017 | Documents, créneaux |
| Dhia Jbali | notification | 8085 | — (Python) | RabbitMQ, avancé, mails |
| Samer | plateforme | 8080 / 8761 / 8888 / 8180 | — | Gateway, Eureka, Config, Keycloak |

## Ce que TOUT LE MONDE doit savoir (même hors de son MS)

1. Architecture : Front → Gateway:8080 → MS via Eureka:8761 + Config:8888 + Keycloak:8180 + RabbitMQ.  
2. **1 base / service**, jamais de FK cross-service.  
3. Sync = règle bloquante ; Async = effet de bord.  
4. Validation 1 = **squelettes** (compile/start/health), pas encore tout le métier.  
5. Repo **public** + chacun committe + Issues (`PROJECT_MANAGEMENT.md`).  
6. Lire `QA_PREP.md` entier au moins une fois.
