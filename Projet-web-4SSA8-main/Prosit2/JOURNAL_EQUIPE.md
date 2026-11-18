# Journal d’équipe — Prosit n°2 JobBoard (TalentConnect)

> Décisions **collectives** · **6 membres**.  

## Équipe (ownership)

| # | Membre | Responsabilité Prosit 2 |
|---|---|---|
| 1 | **Mohamed Aziz Mehrez** | `ms-candidate` · intro orale |
| 2 | **Mohamed Rayen Sboui** | `ms-offer` · alternatives rejetées |
| 3 | **Maryem Slatni** | `ms-application` · DDD / Context Map / comm. |
| 4 | **Mohamed Ezzedine Zouiten** | `ms-interview` (Node) |
| 5 | **Dhia Jbali** | `ms-notification` (Python) · events async |
| 6 | **Samer** | Plateforme : API Gateway, Eureka, Config Server, Keycloak, Compose · architecture cible |

---

## 2026-11-10 — Lecture du monolithe `awd-monolith`

| Qui | Analyse |
|---|---|
| Aziz | Package `candidat` : `CandidateService`, Address, delete + `ApplicationRepository` L71–74 |
| Rayen | Package `job` : `JobService` / `CategoryService`, charge recherche |
| Maryem | Package `candidature` : `ApplicationService.create` L69–85 |
| Ezzedine | Extension entretien (hors monolithe actuel) · Node/Mongo |
| Dhia | Absence mail dans le code · scénario Inès (SMTP sync) |
| Samer | `pom.xml` 3.5.6, port 8080, `awd_db.sql` FK, `OpenApiConfig`, déploiement unique |

**Rejeté** : inventer un envoi mail déjà présent.  
**Décision** : preuves fichier + notif sync = ASSOMPTION scénario.

---

## 2026-11-11 — Acteurs Sami / Karim / Inès / Leïla

| Sujet | Décision | Porté par |
|---|---|---|
| Scale ×50 | **ms-offer** scalable seul | Rayen + Samer |
| 1 MS / table | **Refus** (Address∈candidate, Category∈offer) | Aziz + Rayen |
| Notif statut | **`ApplicationStatusChanged` async** | Dhia + Maryem |
| Polyglotte | Interview **Node**, Notification **Python** | Ezzedine + Dhia + Leïla (produit) |

---

## 2026-11-12 — Frontières Address & Category

| Option | Verdict |
|---|---|
| Address / Category = MS séparés | **Rejeté** |
| Address∈ms-candidate · Category∈ms-offer | **Retenu** (plénière 6/6) |

---

## 2026-11-13 — Sync / async & delete

| Cas | Décision |
|---|---|
| Existe candidat / job available | Sync Feign (Maryem) |
| Statut → mail/SMS/push | Async (Dhia) |
| Delete job/candidate | Feign ms-application ; sinon bloquer (Maryem + Rayen + Aziz) |
| Gateway / discovery | Eureka + Gateway (Samer) |

---

## 2026-11-14 — Polyglot DB & roadmap strangler

| Service | DB | Owner |
|---|---|---|
| ms-candidate | MySQL `candidate_db` | Aziz |
| ms-offer | MySQL `offer_db` | Rayen |
| ms-application | PostgreSQL `application_db` | Maryem |
| ms-interview | MongoDB `interview_db` | Ezzedine |
| ms-notification | pas de DB métier | Dhia |
| Gateway / Eureka / Config / Keycloak | — | Samer |

**Roadmap** : ms-offer → candidate → application → notification → interview (+ plateforme en parallèle).

**Rejets** : 1 MS/table · garder monolithe · search-only · DB partagée · sync-only.

---

*Dernière mise à jour : 2026-11-14 · 6 personnes*
