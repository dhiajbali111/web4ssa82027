# E5 — Pilotage projet (GitHub Projects)

À coller dans GitHub : Issues + Project Board (Backlog / In progress / Review / Done).

## Convention de branches

| Préfixe | Usage | Exemple |
|---|---|---|
| `main` | Branche stable Validation 1 | — |
| `feat/<service>-<desc>` | Nouvelle fonctionnalité | `feat/candidate-crud` |
| `fix/<service>-<desc>` | Correction | `fix/gateway-route-jobs` |
| `docs/<topic>` | Documentation | `docs/e1-user-stories` |
| `chore/<topic>` | Build, scripts, compose | `chore/start-all-scripts` |

## Conventional Commits (anglais)

```
feat(candidate): add address assign endpoint skeleton
fix(application): correct Feign client name
docs(architecture): align ports with docker-compose
chore(scripts): add start-all.bat
```

Types : `feat`, `fix`, `docs`, `chore`, `test`, `refactor`.  
Scope = nom court du service (`candidate`, `job`, `application`, `interview`, `notification`, `gateway`, `eureka`).

**Règle E5** : chaque membre pousse ≥ 1 commit visible sur le repo public.

## Labels suggérés

`type:feat` `type:docs` `type:infra` `service:candidate` `service:job` `service:application` `service:interview` `service:notification` `priority:P0` `priority:P1` `milestone:V1` `milestone:V2`

## Milestones

| Milestone | Objectif |
|---|---|
| **V1-Design** | Conception + squelettes + docs (Validation 1) |
| **V2-Business** | CRUD métier + Feign réel + events |
| **V3-Security-UI** | Keycloak JWT + Frontend |

## Backlog Issues (prêtes à coller)

### INFRA

**Issue #1 — Bootstrap Eureka + Config + Gateway**  
- Owner: Mohamed Aziz Mehrez  
- Labels: `type:infra`, `priority:P0`, `milestone:V1`  
- Acceptance: `mvn package` OK ; Eureka UI :8761 ; Gateway :8080 `/actuator/health` UP  

**Issue #2 — docker-compose stack complète**  
- Owner: Dhia Jbali  
- Labels: `type:infra`, `priority:P0`, `milestone:V1`  
- Acceptance: `docker compose config` valide ; services listés = docs ; DBs séparées  

**Issue #3 — Scripts start-all.bat / start-all.sh**  
- Owner: Mohamed Rayen Sboui  
- Labels: `type:infra`, `chore`, `milestone:V1`  
- Acceptance: scripts documentés dans README ; démarrage local profils h2/nodb  

### MS Candidate (Aziz)

**Issue #10 — Skeleton ms-candidate**  
- Owner: Mohamed Aziz Mehrez · Labels: `service:candidate`, `milestone:V1`  
- AC: compile, start profil `h2`, register Eureka, `/actuator/health` UP, packages controller/service/repository/entity/dto  

**Issue #11 — Design API Candidate/Address**  
- Owner: Mohamed Aziz Mehrez · Labels: `service:candidate`, `type:docs`, `milestone:V1`  
- AC: table REST + ER dans `03-fiches-microservices.md`  

**Issue #12 — CRUD métier Candidate (V2)**  
- Owner: Mohamed Aziz Mehrez · Labels: `service:candidate`, `milestone:V2`  
- AC: endpoints réels, validation, 409 email dupliqué  

### MS Job (Rayen)

**Issue #20 — Skeleton ms-job**  
- Owner: Mohamed Rayen Sboui · Labels: `service:job`, `milestone:V1`  
- AC: idem skeleton (port 8082, MySQL/H2)  

**Issue #21 — Design API Job/Category**  
- Owner: Mohamed Rayen Sboui · Labels: `service:job`, `type:docs`, `milestone:V1`  
- AC: REST + events `JobAvailabilityChanged` documentés  

**Issue #22 — CRUD métier Job (V2)**  
- Owner: Mohamed Rayen Sboui · Labels: `service:job`, `milestone:V2`  
- AC: filtres available/categoryId, PATCH availability  

### MS Application (Maryem)

**Issue #30 — Skeleton ms-application**  
- Owner: Maryem Slatni · Labels: `service:application`, `milestone:V1`  
- AC: port 8083, PostgreSQL/H2, health UP  

**Issue #31 — Design Feign + events Application**  
- Owner: Maryem Slatni · Labels: `service:application`, `type:docs`, `milestone:V1`  
- AC: matrice sync/async + failure plan Resilience4j  

**Issue #32 — Apply flow métier (V2)**  
- Owner: Maryem Slatni · Labels: `service:application`, `milestone:V2`  
- AC: Feign candidate+job, 409 double apply, publish `ApplicationCreated`  

### MS Interview (Ezzedine)

**Issue #40 — Skeleton ms-interview**  
- Owner: Mohamed Ezzedine Zouiten · Labels: `service:interview`, `milestone:V1`  
- AC: port 8084, Mongo/nodb, health UP  

**Issue #41 — Design Interview API + events**  
- Owner: Mohamed Ezzedine Zouiten · Labels: `service:interview`, `type:docs`, `milestone:V1`  
- AC: ER Mongo + `InterviewScheduled` payload  

**Issue #42 — Schedule interview métier (V2)**  
- Owner: Mohamed Ezzedine Zouiten · Labels: `service:interview`, `milestone:V2`  
- AC: Feign application, CRUD interviews  

### MS Notification (Dhia)

**Issue #50 — Skeleton ms-notification Python**  
- Owner: Dhia Jbali · Labels: `service:notification`, `milestone:V1`  
- AC: FastAPI :8085 health + ping  

**Issue #51 — Design event consumers**  
- Owner: Dhia Jbali · Labels: `service:notification`, `type:docs`, `milestone:V1`  
- AC: catalogue events + idempotence `eventId`  

**Issue #52 — Consumer RabbitMQ + mail (V2)**  
- Owner: Dhia Jbali · Labels: `service:notification`, `milestone:V2`  
- AC: consume `ApplicationCreated`, envoi mail stub  

### DOCS / ORAL

**Issue #60 — Dossier E1–E4 + diagrammes**  
- Owner: Tous · Labels: `type:docs`, `milestone:V1`  
- AC: US-01..15, use-cases, architecture SVG  

**Issue #61 — Présentation 12 slides + notes**  
- Owner: Tous (1 slide MS chacun) · Labels: `type:docs`, `milestone:V1`  
- AC: PPTX ≤12 slides, timing 10 min, speaker notes  

**Issue #62 — QA_PREP + SELF_AUDIT**  
- Owner: Mohamed Aziz Mehrez · Labels: `type:docs`, `milestone:V1`  
- AC: ≥35 Q/R ; audit grille 20/20  

**Issue #63 — Repo public + Blackboard**  
- Owner: Chef d’équipe · Labels: `priority:P0`, `milestone:V1`  
- AC: URL publique accessible ; tous ont commité  

## Board GitHub Projects — colonnes

`Backlog` → `In progress` → `Review` → `Done`
