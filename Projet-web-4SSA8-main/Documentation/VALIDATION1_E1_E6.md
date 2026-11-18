# Grille Validation 1 — E1 à E6 (JobBoard)

Date : 2026-11-14 · Équipe **6** (Aziz, Rayen, Maryem, Ezzedine, Dhia, **Samer**)  
Monolithes de référence : `JobBoard_Symfony_6_4` + `awd-monolith` / **`awd_db`**.  
*Note : E1–E6 = livrable **microservices** (racine `Backend/` + `Documentation/`), pas le code Symfony seul.*

| Critère | Attendu « Atteint » | Preuve | Statut |
|---|---|---|---|
| **E1** Sujet / analyse | Problème réel, acteurs, US/cas d’usage, périmètre réaliste | `00-sujet-et-perimetre.md` · `Diagrams/use-cases.svg` | **Atteint** |
| **E2** Découpage MS | Capacité/BC, pas par table, 4+1 avancé, sans recouvrement | `02-decoupage-microservices.md` | **Atteint** |
| **E3** Données & comm | 1 DB/MS justifiée, sync/async justifié | `04-matrice-interactions.md` · `03-fiches-…` | **Atteint** |
| **E4** Architecture | Front, GW, Eureka, Config, Keycloak, MS, DB, Docker | `Diagrams/architecture.svg` · `05-architecture.md` · `Backend/docker-compose.yml` | **Atteint** |
| **E5** Git & docs | Backend/ Frontend/ Documentation/… README, MS créés, PM, commits tous | `README.md` · `PROJECT_MANAGEMENT.md` · structure racine | **Contenu OK** — repo **public** + commits des **6** à finaliser |
| **E6** Oral | Clair, diagrammes, temps, parole partagée (6) | `Presentation/Validation1-JobBoard.pptx` · `slides.md` | **Atteint** (répéter à 6) |

## Qui parle de quoi (E6)

| Membre | E / slide |
|---|---|
| Aziz | E1 intro + ms-candidate |
| Rayen | E2 découpage + ms-job |
| Maryem | DDD + ms-application + E3 |
| Ezzedine | ms-interview |
| Dhia | ms-notification (avancé) + E3 events |
| **Samer** | **E4 plateforme** (Gateway, Eureka, Config, Keycloak, Compose) |

## Actions restantes (étudiants)

1. ~~Pousser le dépôt public~~ → https://github.com/AzizMehrez/JobBoard-AWD-4SSA8  
2. ~~6 auteurs dans `git log`~~ → Samer, Aziz, Rayen, Maryem, Ezzedine, Dhia  
3. Issues → GitHub Projects (`PROJECT_MANAGEMENT.md`).  
4. Inviter les 5 coéquipiers comme **collaborators** GitHub (pour de vrais pushes personnels).  
5. Répétition orale 10 min avec Samer sur la slide 10.
