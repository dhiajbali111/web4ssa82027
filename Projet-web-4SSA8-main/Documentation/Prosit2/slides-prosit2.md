# Prosit n°2 — JobBoard : monolithe → microservices
≤12 slides · ESPRIT AWD · TalentConnect

---

## 1. Titre
**JobBoard — du backend monolithique aux microservices**  
TalentConnect · Spring Boot 3.5.6 · MySQL `awd_db` → architecture cible  
Équipe : Aziz · Rayen · Maryem · Ezzedine · Dhia

---

## 2. Problématique
Comment passer du monolithe REST unique (`:8080`, `awd_db`) à des microservices  
**scalables**, **polyglottes** (Node / Python) et **sans monolithe distribué** ?

---

## 3. Acteurs & douleurs
| | Douleur | Attente |
|---|---|---|
| **Sami** | ×50 recherche → 4× monolithe entier | Scaler `ms-job` seul |
| **Karim** | 1 DB ; rename `job` casse Application ; delete lit `application` | DB / ownership par service |
| **Ines** | Mail sync = plus personne ne postule | Notif **async** |
| **Leila** | Équipes Node + Python | Frontières métier argumentées |

---

## 4. Diagnostic (preuves)
- 1 process / port **8080** · Boot **3.5.6**
- `awd_db` + FK `application`→`candidate`/`job`
- `JobService` / `CandidateService` → `ApplicationRepository` → **409**
- `ApplicationService.create` = transaction cross-modules
- Stack Java-only · mail sync = scénario Ines

---

## 5. Carte de domaine
| Sous-domaine | Type |
|---|---|
| Catalogue offres | **Cœur** |
| Candidature | **Cœur** |
| Identité candidat (+ address) | Support |
| Entretiens | Support |
| Notifications | **Générique** |
| Keycloak IAM | Générique |

---

## 6. Context Map
- Candidate / Job → Application : **Customer/Supplier** (Feign)
- Application → Interview : **Customer/Supplier**
- Métiers → Notification : **Published Language** (events)
- Keycloak → tous : **Conformist**
- **Shared Kernel évité** · ACL via DTO/events

---

## 7. Microservices (pas 1/table)
| MS | Techno | DB | Owns |
|---|---|---|---|
| ms-candidate | Java | MySQL | candidate + **address** |
| ms-job | Java | MySQL | job + **category** |
| ms-application | Java | PostgreSQL | application (IDs) |
| ms-interview | **Node** | Mongo | interview |
| ms-notification | **Python** | — | consume events |

**Rejeté** : 1 service/table · DB partagée · notif sync · ms-search seul

---

## 8. Communication
| Cas | Mode |
|---|---|
| Existe candidat / job available | **Sync** Feign (+ CB) |
| Statut → mail / SMS / push | **Async** `ApplicationStatusChanged` |
| Delete job/candidate | Feign ms-application (plus de lecture table) |
| SMTP down | Postuler **reste possible** |

---

## 9. Architecture cible
Clients (web / mobile / desktop) → **API Gateway** → MS (Eureka)  
1 DB / service · RabbitMQ → notification · Config · Keycloak  
*(diagramme architecture.svg)*

---

## 10. Trade-offs
- Latence réseau → timeouts / retry / circuit breaker  
- Plus d’ACID global → sync invariants + cohérence éventuelle notifs  
- Ops + complexe → Compose + health + discovery  
- Risque monolithe distribué → frontières strictes + journal

---

## 11. Qui porte quoi / suite
| MS | Owner |
|---|---|
| ms-candidate | Aziz |
| ms-job | Rayen |
| ms-application | Maryem |
| ms-interview | Ezzedine |
| ms-notification | Dhia |

Validation suivante = squelettes + démo health — **pas** le cœur de ce Prosit.

---

## 12. Questions
Merci — questions examinateur ?
