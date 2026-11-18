# E3 — Données et communication

## 1. Bases de données (une par service — jamais partagée)

| Service | Base | Techno | Justification |
|---|---|---|---|
| ms-candidate | `candidate_db` :3307 | **MySQL** | Modèle relationnel 1–1 Candidate–Address ; continuité pédagogique avec le monolithe |
| ms-job | `job_db` :3308 | **MySQL** | Catégories + jobs relationnels, filtres/index `available` |
| ms-application | `application_db` :5433 | **PostgreSQL** | Polyglot persistence ; contrainte UNIQUE forte `(candidate_id, job_id)` ; indépendance d’équipe |
| ms-interview | `interview_db` :27017 | **MongoDB** | Documents souples (meetingUrl, notes) ; pas de jointures critiques |
| ms-notification | aucune DB métier partagée | fichiers/logs locaux (optionnel plus tard) | Traitement événementiel ; pas de vérité métier |

**Règle** : aucun foreign key cross-service. On stocke uniquement l’**ID** distant (`candidateId`, `jobId`, `applicationId`).

Profils locaux de démarrage sans Docker : H2 (`h2`) pour candidate/job/application ; `nodb` pour interview (exclut Mongo autoconfig).

## 2. Catalogue d’événements (RabbitMQ)

| Event | Producer | Consumers | Payload (JSON) |
|---|---|---|---|
| `CandidateDeleted` | ms-candidate | ms-application (optionnel V2), ms-notification | `{ "eventId", "candidateId", "occurredAt" }` |
| `JobAvailabilityChanged` | ms-job | ms-application, ms-notification | `{ "eventId", "jobId", "available", "occurredAt" }` |
| `ApplicationCreated` | ms-application | ms-notification | `{ "eventId", "applicationId", "candidateId", "jobId", "email", "occurredAt" }` |
| `ApplicationStatusChanged` | ms-application | ms-notification | `{ "eventId", "applicationId", "fromStatus", "toStatus", "occurredAt" }` |
| `InterviewScheduled` | ms-interview | ms-notification | `{ "eventId", "interviewId", "applicationId", "slot", "meetingUrl", "occurredAt" }` |
| `InterviewCancelled` | ms-interview | ms-notification | `{ "eventId", "interviewId", "applicationId", "reason", "occurredAt" }` |

`eventId` (UUID) → **idempotence** côté consommateur (ignorer un double delivery).

## 3. Matrice d’interactions

| Caller | Callee | Mode | Justification | Si callee down |
|---|---|---|---|---|
| Frontend | api-gateway | REST sync | Point d’entrée unique | Erreur client ; retry UX |
| api-gateway | ms-* | REST (lb:// Eureka) | Routage | 503 Gateway ; Eureka retire instance unhealthy |
| ms-application | ms-candidate | **OpenFeign sync** | Candidat doit exister avant postuler | Timeout 2s → retry 3× backoff → Resilience4j CB open → **503**, **aucune** écriture Application |
| ms-application | ms-job | **OpenFeign sync** | Job doit être `available=true` | Idem fail-fast 503 |
| ms-interview | ms-application | **OpenFeign sync** | Entretien lié à une candidature réelle | Timeout/CB → 503 ; pas d’interview orpheline |
| ms-candidate | ms-application | Feign sync *(optionnel delete)* | Éviter delete si candidatures | Si down : refuser delete (fail-safe) **ou** publier event + cohérence éventuelle |
| ms-application | RabbitMQ | **async** `ApplicationCreated` | Mail non bloquant | Publish retry ; API OK → **cohérence éventuelle** notif |
| ms-job | RabbitMQ | **async** `JobAvailabilityChanged` | Découpler consommateurs | Idem |
| ms-interview | RabbitMQ | **async** `InterviewScheduled` | Découpler | Idem |
| RabbitMQ | ms-notification | **async consume** | I/O e-mail / LLM | Messages restent en queue ; rattrapage au redémarrage ; consumer idempotent |
| * → Eureka / Config | discovery / config | sync bootstrap | Infra | Démarrage dégradé ; `optional:configserver` |

## 4. Résilience transversale (Resilience4j)

| Mécanisme | Réglage pédagogique |
|---|---|
| Timeout Feign | 2000 ms |
| Retry | max 3, backoff exponentiel, seulement erreurs transitoires (timeout/502/503) |
| Circuit breaker | sliding window 10 ; open si ≥50 % échecs ; wait 5–10 s ; fallback → ProblemDetail 503 |
| Fallback | ne jamais inventer un candidat/job « fantôme » |
| Idempotence events | dédoublonnage par `eventId` |
| Cohérence éventuelle | mails / projections dérivées peuvent arriver après le 201 |
