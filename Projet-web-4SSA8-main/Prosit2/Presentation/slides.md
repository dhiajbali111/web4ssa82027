# Prosit n°2 — JobBoard monolithe → microservices
≤12 slides · ~10–15 min · **6 membres** · TalentConnect · AWD 2026-2027

| # | Titre | Qui | Timing |
|---|---|---|---|
| 1 | Titre | Aziz | 0:00–0:40 |
| 2 | Problématique | Aziz | 0:40–1:20 |
| 3 | Acteurs | Rayen | 1:20–2:10 |
| 4 | Diagnostic + preuves | Rayen + Samer | 2:10–3:30 |
| 5 | Domaine DDD | Maryem | 3:30–4:20 |
| 6 | Context Map | Maryem | 4:20–5:10 |
| 7 | Microservices (1 slide synthèse) | Aziz · Rayen · Maryem · Ezzedine · Dhia | 5:10–7:10 |
| 8 | Communication | Dhia + Maryem | 7:10–8:20 |
| 9 | Architecture plateforme | **Samer** | 8:20–9:30 |
| 10 | Alternatives rejetées | Rayen | 9:30–10:20 |
| 11 | Risques + roadmap | Ezzedine + Samer | 10:20–11:30 |
| 12 | Questions | Tous (6) | 11:30–15:00 |

---

## 1. Titre
**JobBoard — du backend monolithique aux microservices**  
Spring Boot 3.5.6 · `awd_db` · :8080  
**Équipe (6)** : Aziz · Rayen · Maryem · Ezzedine · Dhia · Samer

## 2. Problématique
MS scalables, polyglottes (Node/Python), sans monolithe distribué ni notif sync bloquante ?

## 3. Acteurs
Sami ×50 · Karim 1 DB · Inès async · Leïla Node+Python

## 4. Diagnostic
Preuves `awd-monolith` : 8080, `awd_db`, delete→409, Feign futur, Java-only, mail=ASSOMPTION

## 5. Domaine
Cœur Offres+Candidature(+Entretiens) · Support Identité · Générique Notif+IAM

## 6. Context Map
Customer/Supplier · Published Language · Conformist · Shared Kernel évité

## 7. Microservices + owners
| MS | Owner |
|---|---|
| ms-candidate | **Aziz** |
| ms-offer | **Rayen** |
| ms-application | **Maryem** |
| ms-interview | **Ezzedine** |
| ms-notification | **Dhia** |
| Gateway/Eureka/Config | **Samer** |

## 8. Communication
Sync Feign invariants · Async **`ApplicationStatusChanged`** · Delete sans lecture table

## 9. Architecture
Web/Mobile/Desktop → Gateway → MS · 1 DB/MS · RabbitMQ · Eureka · Config · Keycloak  
*(présentée par Samer)*

## 10. Alternatives rejetées
1 MS/table · monolithe · search-only · DB partagée · sync-only

## 11. Risques + strangler
ms-offer d’abord (Sami) · CB · éventuelle cohérence notifs

## 12. Questions
Merci — l’équipe (6) répond
