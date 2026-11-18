# PROSIT2_AUDIT — JobBoard (TalentConnect)

Date : **2026-11-14**  
Sources lues : `BackEndRestFul_SpringBoot/awd-monolith` (Java, SQL, tests, pom, properties), `Documentation/Prosit2/*`, `Documentation/01`–`05`, `Diagrams/*`, `Presentation/*`.  
Règle : statut **PASS** seulement si preuve fichier + contenu conforme après correction.

---

## Table d’audit (exigences 1–11)

| # | Exigence | Avant | Après | Evidence | Ce qui a été corrigé |
|---|---|---|---|---|---|
| 1 | Définitions mots-clés (tous, liés JobBoard) | **PARTIAL** — glossaire court, termes manquants (OpenAPI, couplage/cohésion, déploiement indépendant…) | **PASS** | `dossier-prosit2.md` §1 | Glossaire complet (18 termes) en français, ancré JobBoard / `awd-monolith` |
| 2 | Problématique claire | **PARTIAL** — question trop générique | **PASS** | `dossier-prosit2.md` §2 | Problématique reformulée (scale, polyglotte, anti monolithe distribué, notif non bloquante) |
| 3 | Acteurs Leila/Karim/Ines/Sami (attente \| contrainte \| décision) | **PARTIAL** — acteurs génériques Validation 1, colonnes incomplètes | **PASS** | `dossier-prosit2.md` §3 | Table scénario TalentConnect + colonne « décision de design » |
| 4 | Diagnostic + preuves code/DB/scénario | **PARTIAL** — bonnes preuves mais acteurs Sami/Karim/Ines peu reliés ; E9/E10 partiels | **PASS** | `dossier-prosit2.md` §4 | Preuves pom 3.5.6, port 8080, `awd_db.sql` FK, `ApplicationRepository` dans Job/Candidate, test 409, OpenAPI ; mail = ASSOMPTION explicite |
| 5 | Carte de domaine (types + justif.) | **PASS** (déjà dans `01-…`) | **PASS** | `dossier-prosit2.md` §5 + `01-analyse-domaine-ddd.md` | Alignement cœur/support/générique ; Address/Category non autonomes |
| 6 | Liste MS (capacité, DB, REST, events, techno Node/Python, ownership tables) | **PARTIAL** — table courte ; Node pas explicite ; ownership tables flou | **PASS** | `dossier-prosit2.md` §6 + `03-fiches-…` | Tableau complet ; `ms-interview` **Node** ; `ms-notification` **Python** ; redistribution 5 tables ; alternatives A–E |
| 7 | Architecture cible (clients ×3, GW, MS, DB, broker, Eureka/Config/Keycloak) | **PARTIAL** — diagramme Validation 1 ok mais dossier Prosit2 minimal | **PASS** | `dossier-prosit2.md` §7 + `Diagrams/architecture.svg` | Mermaid Prosit2 avec web/mobile/desktop + légende sync/async |
| 8 | Context Map (relations DDD) | **PARTIAL** — manquait Shared Kernel / ACL | **PASS** | `dossier-prosit2.md` §8 + `context-map.mmd` / `.svg` + `01-…` | Customer/Supplier, Published Language, Conformist, Shared Kernel évité, ACL |
| 9 | Communication sync/async + panne + notif async + delete sans lecture table | **PARTIAL** — matrice E3 ok ; Prosit2 ne la reprenait pas assez | **PASS** | `dossier-prosit2.md` §9 + `04-matrice-interactions.md` | Cas Ines async forcé ; delete → Feign/fail-safe ; CB/timeout/idempotence |
| 10 | Journal d’équipe collectif | **MISSING** | **PASS** | `Prosit2/JOURNAL_EQUIPE.md` | Créé : analyses par membre, débats, rejets, décisions |
| 11 | Présentation ≤12 slides | **MISSING** (seul Validation1 PPTX) | **PASS** | `slides-prosit2.md` + `Prosit2-JobBoard.pptx` | 12 slides Prosit2 (problème → trade-offs) |

### Contrôles qualité transverses

| Contrôle | Avant | Après | Fix |
|---|---|---|---|
| Alternatives rejetées (table, merge, sync-only, shared DB, search-only) | PARTIAL (A–D) | **PASS** | Alt. **E** ajoutée dans `02-…` et dossier §6.2 |
| Trade-offs / risques + mitigations | PARTIAL | **PASS** | §6.3 dossier |
| Cohérence noms MS/DB/events/ports | PARTIAL (Prosit2 vs Validation1) | **PASS** | Annexe dossier + alignement docs |
| Exactitude faits monolithe | PASS (version/port/DB déjà corrects) | **PASS** | Revérifié pom / properties / SQL / services / test |
| Pas d’implémentation requise | PASS | **PASS** | Dossier design only |
| Scope 4–6 MS | PASS (5) | **PASS** | — |

---

## Incohérences trouvées puis corrigées

| Incohérence | Correction |
|---|---|
| Acteurs Prosit2 ≠ scénario Sami/Karim/Ines/Leila | Réécrit §3 |
| `ms-interview` pas marqué Node dans le dossier Prosit2 | Explicitement Node.js |
| Journal d’équipe absent | `JOURNAL_EQUIPE.md` |
| Slides Prosit2 absents (seul Validation 1) | MD + PPTX dédiés |
| Alt. « extract search only » absente | Alt. E |
| Context Map sans Shared Kernel / ACL | Mis à jour |
| Proposition Karim 1 service/table peu visible | §3 + §6.2 + journal + slides |

---

## (a) Liste des changements effectués

1. Réécriture complète de `Documentation/Prosit2/dossier-prosit2.md` (exigences 1–11).  
2. Création de `Documentation/Prosit2/JOURNAL_EQUIPE.md`.  
3. Création de `Documentation/Prosit2/slides-prosit2.md` + `Prosit2-JobBoard.pptx` (`scripts/build_prosit2_presentation.py`).  
4. Mise à jour `Diagrams/context-map.mmd` (+ SVG régénéré).  
5. Alt. E + ACL/Shared Kernel dans `01-…` et `02-…`.  
6. Liens Prosit2 dans `Documentation/README.md`.  
7. Ce fichier `PROSIT2_AUDIT.md`.

---

## (b) Hypothèses (assumptions)

1. **Mail synchrone** : **0** occurrence mail/SMS/`JavaMailSender` dans `awd-monolith` → exigence tirée du **scénario Ines** (ASSOMPTION pédagogique).  
2. **Libellés E9/E10** : le sujet Prosit peut parler de « delete offre / delete catégorie → 409 » ; la grille Workshop1 du repo est différente (**E7/E8** = delete candidat/job 409 ; **E9** = catégorie dupliquée ; **E10** = GET apps candidat inconnu → 404). DELETE catégorie → 409 = code + SQL, **pas** d’IT dédié.  
3. **Équipe Node/Python** : `ms-interview` = Node, `ms-notification` = Python (aligné Leila + Validation 1).  
4. Les docs Validation 1 (`03`, `04`, `05`) = détail API/ports ; le dossier Prosit2 = livrable argumentatif.  
5. Keycloak / Gateway / Eureka = architecture cible pédagogique (compose Backend).

---

## (c) 5 questions difficiles (examinateur) + réponses courtes

**Q1. Pourquoi ne pas faire un microservice Address et Category ?**  
Parce que ce ne sont pas des capacités métier : Address vit avec le profil candidat ; Category classifie les jobs. Les séparer = Feign inutile + panne en cascade = **monolithe distribué** (objection de Sami à la proposition de Karim).

**Q2. Si RabbitMQ est down, peut-on encore postuler ?**  
Oui pour l’écriture Application (après validations Feign). L’event partira au rétablissement (cohérence éventuelle). L’inverse (SMTP sync dans `create`) rendrait le dépôt impossible — c’est exactement ce qu’on refuse.

**Q3. Comment remplacer `applicationRepository.existsByJobId` sans DB partagée ?**  
`ms-job` appelle `ms-application` en Feign (« y a-t-il des candidatures ? ») ou publie une intention et applique une politique fail-safe. **Plus jamais** de lecture directe de la table d’un autre service.

**Q4. Pourquoi PostgreSQL pour Application et MySQL pour Job/Candidate ?**  
Polyglot : indépendance d’équipe + contrainte UNIQUE forte ; MySQL pour continuité pédagogique relationnelle Candidate–Address / Job–Category. Bases **séparées** même si techno parfois proche.

**Q5. N’avez-vous pas juste un monolithe découpé en jars ?**  
Non si : 1 DB/service, pas de FK cross-service, sync limité aux invariants, notifs async, technos Node/Python autonomes, scale de `ms-job` seul. Sinon on retomberait dans le monolithe distribué — d’où les alternatives rejetées.

---

## (d) À vérifier manuellement

1. Ouvrir `Prosit2-JobBoard.pptx` sous PowerPoint/LibreOffice (rendu polices).  
2. Relire à voix haute la problématique §2 et le §6.2 (notés).  
3. À l’oral : utiliser les **chemins/méthodes** plutôt que « E9/E10 » seuls, ou préciser si l’on suit le sujet Prosit vs la grille Workshop1.  
4. Si Blackboard exige un PDF unique : exporter `dossier-prosit2.md` + journal + slides.  
5. Ne pas pousser ce dossier Prosit2 dans le repo **Symfony-only** (`Projet-web-4SSA8`) sauf demande.

---

## Verdict final

| Score exigences 1–11 | **11 / 11 PASS** (après corrections) |
|---|---|
| Bloquant restant | Vérifs manuelles (d) uniquement |
