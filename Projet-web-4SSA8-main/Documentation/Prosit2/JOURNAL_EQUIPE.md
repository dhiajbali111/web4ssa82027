# Journal d’équipe — Prosit n°2 JobBoard

> Les décisions sont **collectives**. Chaque entrée note qui a analysé quoi, les options discutées, les rejets et la décision finale.

---

## Séance 1 — Lecture du monolithe Spring (`awd-monolith`)

| Membre | Analyse |
|---|---|
| **Aziz** | Package `candidat` : `CandidateService`, `Address`, FK locale ; delete + `ApplicationRepository` |
| **Rayen** | Package `job` : `JobService`, `CategoryService`, index `available`, delete → 409 |
| **Maryem** | Package `candidature` : `ApplicationService.create` transactionnelle cross-modules |
| **Ezzedine** | `pom.xml` / `application.properties` : Boot 3.5.6, port 8080, `awd_db` |
| **Dhia** | Absence de mail dans le code ; scénario Ines (SMTP sync) comme limite à traiter |

**Décision** : fonder le diagnostic sur des **preuves fichier** (pas sur des intuitions).  
**Rejeté** : inventer un envoi mail « déjà présent » dans Spring — marqué ASSOMPTION / scénario.

---

## Séance 2 — Scénario acteurs (Sami, Karim, Ines, Leila)

| Discussion | Issue |
|---|---|
| Scalabilité recherche ×50 (Sami) | `ms-job` doit être scalable **seul** |
| Rename colonne `job` a cassé Application (Karim) | **Database per service** obligatoire |
| Proposition Karim : 1 MS / table | **Rejetée** (Sami + équipe) — voir alternatives A |
| Notif sync dans save (Ines) | Events async → `ms-notification` |
| Équipes Node / Python (Leila) | `ms-interview` Node ; `ms-notification` Python |

**Décision finale** : 5 microservices par **capacité métier** (Candidate, Job, Application, Interview, Notification) + Gateway / Eureka / Config / RabbitMQ / Keycloak.

---

## Séance 3 — Frontières Address & Category

| Option | Votes / arguments | Verdict |
|---|---|---|
| Address = MS séparé | − latence ; − panne ; pas de capacité autonome | **Rejeté** |
| Address dans ms-candidate | + même BC identité ; FK locale OK | **Retenu** |
| Category = MS séparé | Même objection Sami | **Rejeté** |
| Category dans ms-job | Classifie les offres | **Retenu** |

---

## Séance 4 — Sync vs async

| Cas | Décision | Pourquoi |
|---|---|---|
| Existe candidat / job available avant postuler | **Sync Feign** | Invariant métier ; fail-fast 503 |
| Statut candidature → e-mail / SMS / push | **Async event** | SMTP down ≠ postuler impossible |
| Delete job/candidate (ex-lecture table application) | Feign vers ms-application **ou** event + politique fail-safe | Plus de `ApplicationRepository` cross-module |
| Extraire seulement un ms-search | — | **Rejeté** : ne règle pas ownership / polyglotte / couplage delete |

---

## Séance 5 — Polyglot persistence

| Service | Techno DB | Qui a porté l’argument |
|---|---|---|
| ms-candidate / ms-job | MySQL | Aziz / Rayen — continuité monolithe + relationnel |
| ms-application | PostgreSQL | Maryem — UNIQUE fort + indépendance d’équipe |
| ms-interview | MongoDB | Ezzedine — documents souples (slot, meetingUrl) |
| ms-notification | pas de DB métier | Dhia — pure consommation d’events |

---

## Séance 6 — Cohérence livrables

| Action | Owner |
|---|---|
| Aligner noms MS / events / ports dossier ↔ diagrammes ↔ slides | Tous |
| Context Map + architecture Mermaid/SVG | Maryem + Aziz |
| Journal + alternatives rejetées | Rayen + Dhia |
| Slides Prosit 2 (≤12) | Équipe (1 slide MS / speaker) |

**Décision** : un **seul** vocabulaire canonique (voir annexe du dossier). Shared Kernel et base partagée = **hors jeu**.

---

## Synthèse des alternatives définitivement rejetées

1. Un microservice par table  
2. Base MySQL partagée type `awd_db`  
3. Notification synchrone dans `ApplicationService.create`  
4. Extraire uniquement la recherche sans découper le reste  
5. Forcer Node/Python dans le monolithe Java  

---

*Dernière mise à jour collective : 2026-11-14*
