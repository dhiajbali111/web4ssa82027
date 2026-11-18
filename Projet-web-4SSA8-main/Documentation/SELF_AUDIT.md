# Self-audit — grille Validation 1 (examinateur sévère)

Date : 2026-11-14 · Projet JobBoard · Cible **20/20**  
Règle : ne cocher « Atteint » que si une preuve fichier existe et est cohérente (ports, noms, events).

---

## E1 — Sujet et analyse fonctionnelle (2)

**Attendu « Atteint »** : problème concret + users ; table acteurs ; 12–15 US avec IDs groupées par acteur et mappées au MS ; diagramme de cas d’utilisation ; in/out of scope réaliste.

| Exigence | Preuve | Score |
|---|---|---|
| Problème + users | `00-sujet-et-perimetre.md` §1 | Atteint |
| Table acteurs | idem §2 | Atteint |
| 15 US US-01…15 + MS | idem §3 | Atteint |
| Use case diagram | `Diagrams/use-cases.mmd` + `.svg` | Atteint |
| In / out of scope | idem §5 | Atteint |

**Verdict E1 : 2/2 Atteint**

---

## E2 — Découpage microservices (2)

**Attendu** : 4 métier + 1 avancé ; table capacité/BC/responsabilités/ne-pas-faire/pourquoi ; alternatives rejetées ; pas de chevauchement.

| Exigence | Preuve | Score |
|---|---|---|
| 5 MS | `02-decoupage-microservices.md` §1 | Atteint |
| Table complète | colonnes demandées présentes | Atteint |
| Rejected alternatives | §2 A–D | Atteint |
| Non-chevauchement | « ne doit PAS » explicite | Atteint |

**Verdict E2 : 2/2 Atteint**

---

## E3 — Données et communication (2)

**Attendu** : table DB justifiée ; pas de DB partagée / pas de FK cross-service ; matrice sync/async + panne ; catalogue events (nom, prod, cons, payload).

| Exigence | Preuve | Score |
|---|---|---|
| DB table | `04-matrice-interactions.md` §1 | Atteint |
| IDs only | §1 + fiches Application/Interview | Atteint |
| Matrice + down | §3 | Atteint |
| Event catalog + payload | §2 | Atteint |

**Verdict E3 : 2/2 Atteint**

---

## E4 — Architecture technique (2)

**Attendu** : un diagramme complet (front, GW, Eureka, Config, Keycloak, MS, DB, broker, Docker) ; flèches labellisées ; légende ; 100 % cohérent compose/code.

| Exigence | Preuve | Score |
|---|---|---|
| Diagramme complet | `Diagrams/architecture.mmd` / `.svg` | Atteint |
| Légende | `05-architecture.md` | Atteint |
| Cohérence ports | table § ports = `docker-compose.yml` = yml services | Atteint |

**Vérif compose** : `docker compose config` → OK (2026-11-14).

**Verdict E4 : 2/2 Atteint**

---

## E5 — Repo Git et documentation (2)

**Attendu** : structure imposée ; MS créés ; README complet ; PROJECT_MANAGEMENT Issues + conventions branches/commits.

| Exigence | Preuve | Score |
|---|---|---|
| Backend/ Frontend/ Documentation/ | arborescence racine | Atteint |
| README subject/members/archi/launch | `README.md` | Atteint |
| PROJECT_MANAGEMENT | `Documentation/PROJECT_MANAGEMENT.md` | Atteint |
| Repo public accessible | **manuel** — *not created yet* | ⚠️ bloquant externe |

**Note examinateur** : le contenu E5 est prêt ; le point « repo public » dépend du push étudiant (sinon 0 réglementaire hors machine). Contenu technique = Atteint.

**Verdict E5 contenu : 2/2** (sous réserve push public)

---

## E6 — Présentation orale (2)

**Attendu** : ≤12 slides, 10 min, diagrammes lisibles, texte minimal ; notes + timing ; chaque membre présente son MS.

| Exigence | Preuve | Score |
|---|---|---|
| 12 slides | `Presentation/Validation1-JobBoard.pptx` | Atteint |
| Notes + timing | notes PPTX + `slides.md` | Atteint |
| Split [membre→périmètre] | slides 5–9 MS + slide 10 **Samer** plateforme | Atteint |
| 6 membres | Aziz…Dhia + Samer | Atteint |

**Verdict E6 : 2/2 Atteint**

---

## I1 — Design microservice (3) — TOUS les services

**Attendu** : entités attributs/types/relations ; DB justifiée ; table REST complète (resource, URI, method, body, response, status, pagination/validation).

| Service | Preuve | Score |
|---|---|---|
| candidate | `03-fiches` §1 + `er-candidate` | Atteint |
| job | §2 + `er-job` | Atteint |
| application | §3 + `er-application` | Atteint |
| interview | §4 + `er-interview` | Atteint |
| notification | §5 | Atteint |

**Verdict I1 : 3/3 Atteint**

---

## I2 — Interactions (2)

**Attendu** : pour chaque service : qui appelle / est appelé ; données ; sync/async justifié ; plan panne (timeout, retry, CB Resilience4j, fallback, idempotence, éventualité).

| Preuve | `03-fiches` sections Interactions + `04-matrice` §3–4 | Atteint |

**Verdict I2 : 2/2 Atteint**

---

## I3 — Projet créé + Git (1)

**Attendu** : compile + start ; Eureka ; health UP ; start-all.sh/.bat ; docker-compose autant que possible.

| Check | Résultat | Preuve |
|---|---|---|
| `mvn -DskipTests package` | BUILD_OK | Backend/ |
| Eureka / candidate health | testés UP (session précédente + scripts) | README |
| start-all.bat / .sh | présents | `Backend/start-all.*` |
| `docker compose config` | OK | SELF_AUDIT |
| `docker compose up -d` infra | **Started** : mysql-candidate/job, postgres, mongo, rabbitmq | `docker compose ps` 2026-11-14 |

**Verdict I3 : 1/1 Atteint** (sous réserve que chaque membre démarre son MS avant l’oral)

---

## I4 — Q&A (2)

**Attendu** : QA_PREP FR ≥35 questions ; transverses + 5–8 / MS.

| Preuve | `QA_PREP.md` Q1–Q60 | Atteint |

**Verdict I4 : 2/2 Atteint**

---

## Total interne

| Bloc | Score |
|---|---|
| E1–E6 | 12/12 |
| I1–I4 | 8/8 |
| **Total** | **20/20** (contenu) |

## Actions restantes étudiants (hors code)

1. Créer / pousser le **repo public** (sinon E5 réglementaire = 0).  
2. Chaque membre **commit** sur son service.  
3. Coller Issues dans GitHub Projects (`PROJECT_MANAGEMENT.md`).  
4. Répéter l’oral 10 min avec le PPTX.  
5. Vérifier `docker compose up --build` une fois les images tirées.

## Passe de cohérence (noms / ports / events)

| Élément | Valeur unique |
|---|---|
| Services | ms-candidate, ms-job, ms-application, ms-interview, ms-notification |
| Ports | 8081, 8082, 8083, 8084, 8085, GW 8080, Eureka 8761, Config 8888, KC 8180 |
| Events | CandidateDeleted, JobAvailabilityChanged, ApplicationCreated, ApplicationStatusChanged, InterviewScheduled, InterviewCancelled |
| Owners | Aziz, Rayen, Maryem, Ezzedine, Dhia, **Samer** (plateforme) |

Contrôlé dans : README, compose, yml, 02/03/04/05, slides, PPTX, PROJECT_MANAGEMENT, QA_PREP.
