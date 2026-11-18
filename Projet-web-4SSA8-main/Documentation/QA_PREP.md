# I4 — Préparation Q&A orale (35+ questions)

Réponses **courtes et solides**. Ports / noms = ceux du README.

---

## A. Concepts transverses

**Q1. Qu’est-ce qu’un bounded context ?**  
Frontière explicite d’un modèle et de son ubiquitous language. Ex. : BC Candidature ≠ BC Catalogue Offres.

**Q2. À quoi sert le DDD ici ?**  
Découper selon le métier (capacités), pas selon les tables ou les écrans.

**Q3. Database per service ?**  
Chaque MS a sa propre base. Pas de schéma partagé → autonomie de déploiement et d’évolution.

**Q4. Pourquoi pas de base partagée `awd_db` ?**  
Recrée le couplage du monolithe (FK cross-domaine, lock, schéma unique). On stocke seulement des IDs distants.

**Q5. Rôle de l’API Gateway ?**  
Point d’entrée unique (routage, cross-cutting auth). Port **8080**.

**Q6. Rôle d’Eureka ?**  
Service discovery : les instances s’enregistrent ; le Gateway résout `lb://ms-job`. Port **8761**.

**Q7. Rôle du Config Server ?**  
Configuration centralisée (ici native `config-repo`). Port **8888**.

**Q8. Différence Gateway vs Eureka vs Config ?**  
Gateway = entrée client ; Eureka = où sont les instances ; Config = quoi comme propriétés.

**Q9. Flux Keycloak / OAuth2 / JWT ?**  
User s’authentifie auprès de Keycloak → JWT → Front appelle Gateway avec Bearer → Gateway valide via JWKS.

**Q10. Sync vs async ?**  
Sync (Feign) quand la réponse est nécessaire pour décider maintenant. Async (events) pour effets de bord (mails).

**Q11. OpenFeign ?**  
Client HTTP déclaratif Spring Cloud pour appels sync inter-services via Eureka.

**Q12. Circuit breaker ?**  
Resilience4j ouvre le circuit après trop d’échecs → fail-fast + fallback 503 au lieu de saturer un service down.

**Q13. Qu’est-ce qu’un monolithe distribué ?**  
« Microservices » trop couplés (chaînes sync longues, DB partagée) → mêmes défauts qu’un monolithe, en pire.

**Q14. Cohérence éventuelle ?**  
Après un 201 Application, l’e-mail peut arriver plus tard ; le système converge sans transaction globale.

**Q15. Saga / transactional outbox ?**  
Saga = enchaînement d’étapes locales + compensations. Outbox = publier l’event dans la même TX locale que l’écriture, puis relayer vers RabbitMQ (fiabilité). Prévu V2, pas codé en V1.

**Q16. Pourquoi ce découpage et pas par table ?**  
Address n’est pas une capacité ; la coller à Candidate évite un Feign inutile. Idem Category↔Job.

**Q17. CAP en une phrase ?**  
En partition réseau, on choisit entre Consistency et Availability. Nos mails préfèrent Availability + éventualité.

**Q18. ACID vs BASE ?**  
ACID = TX locale d’une DB. BASE = Basically Available, Soft state, Eventual consistency — adapté aux events cross-MS.

**Q19. Pourquoi Docker Compose ?**  
Reproduire infra (DBs, broker, Keycloak, MS) de façon reproductible pour la démo étudiante.

**Q20. H2 dans le projet ?**  
Profil local `h2` pour démarrer sans Docker MySQL/Postgres — **pas** la DB de prod pédagogique (MySQL/Postgres/Mongo dans compose).

**Q21. Idempotence des consumers ?**  
Le payload porte `eventId` ; notification ignore un double delivery RabbitMQ.

**Q22. Pourquoi 5e service Python ?**  
Technologie avancée : polyglotte + messaging + I/O e-mail/LLM hors chemin critique Java.

**Q23. Pagination ?**  
Listes : `?page=&size=` (prévu) pour ne pas renvoyer tout le catalogue.

**Q24. Codes HTTP clés ?**  
200 lecture/MAJ, 201 création, 204 delete, 400 validation, 404 introuvable, 409 conflit métier, 503 dépendance down.

**Q25. Qui présente quoi ?**  
Aziz→candidate, Rayen→job, Maryem→application, Ezzedine→interview, Dhia→notification.

---

## B. ms-candidate (Aziz) — 6 Q

**Q26. Entités ?** Candidate, Address (1–1 même DB).  
**Q27. Pourquoi MySQL ?** Relationnel simple + continuité monolithe.  
**Q28. Email dupliqué ?** 409 Conflict.  
**Q29. Qui l’appelle ?** ms-application (Feign) avant postuler.  
**Q30. Delete avec candidatures ?** 409 ou event + cohérence éventuelle — pas de FK cross-DB.  
**Q31. Port / health ?** 8081 · `/actuator/health`.

---

## C. ms-job (Rayen) — 6 Q

**Q32. Entités ?** Job, Category.  
**Q33. Pourquoi pas Mongo ici ?** Relations/filtres relationnels clairs ; MySQL suffit.  
**Q34. PATCH availability ?** Changer `available` sans renvoyer tout le Job.  
**Q35. Event publié ?** `JobAvailabilityChanged`.  
**Q36. Qui consomme la dispo en sync ?** ms-application via Feign.  
**Q37. Port ?** 8082.

---

## D. ms-application (Maryem) — 7 Q

**Q38. Pourquoi PostgreSQL ?** Polyglot + UNIQUE robuste ; indépendance.  
**Q39. FK vers candidate ?** **Non** — seulement `candidateId` Long.  
**Q40. Pourquoi Feign sync à la création ?** Règle bloquante : candidat existe + job ouvert.  
**Q41. Si candidate down ?** Timeout → retry → CB → 503, **pas** d’insert.  
**Q42. Event principal ?** `ApplicationCreated` → notification.  
**Q43. Double candidature ?** 409.  
**Q44. Port ?** 8083.

---

## E. ms-interview (Ezzedine) — 6 Q

**Q45. Pourquoi MongoDB ?** Document flexible (URL, notes).  
**Q46. Lien métier ?** `applicationId` logique, validé via Feign.  
**Q47. Events ?** `InterviewScheduled`, `InterviewCancelled`.  
**Q48. Profil `nodb` ?** Démarrer le squelette sans Mongo local.  
**Q49. Doit-il connaître Candidate ?** Non — hors BC.  
**Q50. Port ?** 8084.

---

## F. ms-notification (Dhia) — 6 Q

**Q51. Pourquoi avancé ?** Python + RabbitMQ + e-mail/LLM optionnel.  
**Q52. Appelle-t-il Feign les autres MS ?** Non (évite monolithe distribué).  
**Q53. Si RabbitMQ down ?** Events rejouables / retry producteur ; cohérence éventuelle.  
**Q54. Si LLM down ?** Fallback template fixe.  
**Q55. Health URL ?** `http://localhost:8085/actuator/health`.  
**Q56. Comment démarrer sans PATH uvicorn ?** `python -m uvicorn app.main:app --port 8085`.

---

## G. Pièges oraux fréquents

**Q57. « Vous avez combien de bases ? »** Quatre DBs métier + pas de DB partagée notification.  
**Q58. « Address est un microservice ? »** Non — support du BC Candidate.  
**Q59. « Transaction globale ? »** Impossible cross-MS ; TX locales + events.  
**Q60. « Eureka remplace-t-il le Gateway ? »** Non.
