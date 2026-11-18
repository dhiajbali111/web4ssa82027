# Prosit n°2 — JobBoard (TalentConnect)

## Fichiers

| Fichier | Rôle |
|---|---|
| [Dossier_Conception.md](Dossier_Conception.md) | Dossier FR complet (§1–11) |
| [JOURNAL_EQUIPE.md](JOURNAL_EQUIPE.md) | Décisions collectives |
| [Presentation/slides.md](Presentation/slides.md) | Plan des 12 slides + timing |
| [Presentation/Prosit2-JobBoard.pptx](Presentation/Prosit2-JobBoard.pptx) | Support oral |
| [Diagrams/architecture.mmd](Diagrams/architecture.mmd) (+ `.svg`) | Architecture cible |
| [Diagrams/context-map.mmd](Diagrams/context-map.mmd) (+ `.svg`) | Context Map |
| [TODO.md](TODO.md) | Checklist |

Base monolithe enseignant : `BackEndRestFul_SpringBoot/awd-monolith/database/awd_db.sql` → MySQL **`awd_db`**.

---

## (a) Résumé des fichiers créés

Tout le livrable est sous `/Prosit2/` (dossier, journal, diagrammes Mermaid+SVG, slides MD+PPTX, TODO).

## (b) Hypothèses

1. **E-mail synchrone** : absent du code Spring → ASSOMPTION scénario Inès.  
2. **E9/E10** du brief Prosit (delete → 409) = dans le code `JobService`/`CandidateService` ; dans `Workshop1/reponses-draft.md` ces cas sont numérotés **E7/E8** (E9/E10 Workshop = autre chose).  
3. Service offres nommé **`ms-offer`** (capacité) alors que le package monolithe s’appelle `job`.  
4. **6 membres** : Aziz, Rayen, Maryem, Ezzedine, Dhia, **Samer** (plateforme).  
5. RabbitMQ plutôt que Kafka (périmètre étudiant).

## (c) 5 questions difficiles + réponses courtes

1. **Pourquoi pas 1 MS Address / Category ?** → Pas des capacités ; monolithe distribué (Sami a raison).  
2. **SMTP down : peut-on postuler ?** → Oui ; `ApplicationStatusChanged` est async.  
3. **Comment remplacer `existsByJobId` ?** → Feign vers `ms-application` ; sinon bloquer le delete.  
4. **Pourquoi PostgreSQL pour Application ?** → Isolation d’équipe + UNIQUE ; DB **séparée**.  
5. **Ce n’est pas un monolithe découpé ?** → Non si 1 DB/service, sync limité, notifs async, Node/Python autonomes, scale de `ms-offer` seul.

## (d) À personnaliser / vérifier manuellement

1. Rouvrir le PPTX (Samer déjà intégré).  
2. Relancer Swagger sur `awd-monolith` + scénarios 409 delete.  
3. Si le prof exige le nom `ms-job` au lieu de `ms-offer`, renommer partout.  
4. Exporter PDF Blackboard si demandé.  
5. Ajouter le nom de famille de Samer si l’état civil complet est requis.
