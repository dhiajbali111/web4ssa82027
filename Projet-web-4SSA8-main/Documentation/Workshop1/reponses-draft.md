# Workshop 1 — Brouillon de réponses (monolithe Spring `awd-monolith`)

> Dérivé **uniquement du code**. Les items marquées ⚠️ doivent être **vérifiés en lançant** MySQL + l’app + Swagger.

## A. Infos runtime (code)

| Élément | Valeur (code) | À vérifier soi-même |
|---|---|---|
| Port | **8080** (`application.properties`) | ⚠️ `http://localhost:8080` répond |
| OpenAPI JSON | `/v3/api-docs` (+ groupes `/v3/api-docs/0-all`, `1-candidat`, `2-job`, `3-candidature`) | ⚠️ ouvrir l’URL |
| Swagger UI | `/swagger-ui.html` | ⚠️ |
| DB | MySQL `awd_db` | ⚠️ importer `database/awd_db.sql` |

Groupes OpenAPI : `OpenApiConfig.java` (`0-all`, `1-candidat`, `2-job`, `3-candidature`).

## B. Ressources & opérations

### Candidates `/api/candidates`
| Op | Méthode | URI |
|---|---|---|
| Liste | GET | `/api/candidates` |
| Détail | GET | `/api/candidates/{id}` |
| Créer | POST | `/api/candidates` |
| MAJ | PUT | `/api/candidates/{id}` |
| Suppr | DELETE | `/api/candidates/{id}` |
| Associer adresse | PUT | `/api/candidates/{id}/address/{addressId}` |
| Détacher adresse | DELETE | `/api/candidates/{id}/address` |
| Sous-ressource | GET | `/api/candidates/{id}/applications` |

### Addresses `/api/addresses`
CRUD GET/POST/PUT/DELETE `/api/addresses[/{id}]`

### Jobs `/api/jobs`
| Op | Méthode | URI |
|---|---|---|
| Liste (+ filtres) | GET | `/api/jobs?available=&categoryId=` |
| Détail | GET | `/api/jobs/{id}` |
| Créer | POST | `/api/jobs` |
| MAJ | PUT | `/api/jobs/{id}` |
| Dispo | PATCH | `/api/jobs/{id}/availability?available=` |
| Suppr | DELETE | `/api/jobs/{id}` |
| Sous-ressource | GET | `/api/jobs/{id}/applications` |

### Categories `/api/categories`
CRUD + sous-ressource `GET /api/categories/{id}/jobs`

### Applications `/api/applications`
CRUD + filtres `?candidateId=&jobId=`

## C. Codes HTTP (GlobalExceptionHandler + controllers)

| Code | Cas |
|---|---|
| 200 | Lecture / update OK |
| 201 | Création (Location) |
| 204 | Delete OK |
| 400 | Validation / JSON invalide (`MethodArgumentNotValidException`, etc.) |
| 404 | `ResourceNotFoundException` |
| 409 | `ConflictException` + contraintes DB |

Format erreur : RFC 7807 `ProblemDetail`.

## D. Scénarios E1–E10 (attendus d’après les règles métier)

| ID | Scénario | Code attendu | Base code |
|---|---|---|---|
| E1 | GET candidat inexistant | **404** | `CandidateService.getCandidate` |
| E2 | POST candidat email déjà pris | **409** | `existsByEmailIgnoreCase` |
| E3 | POST candidat body invalide (email manquant) | **400** | validation Bean Validation |
| E4 | POST application job `available=false` | **409** | `ApplicationService.create` |
| E5 | POST application doublon même (candidat, job) | **409** | `existsByCandidateIdAndJobId` |
| E6 | POST application candidateId inconnu | **404** | Feign/monolithe `getCandidate` |
| E7 | DELETE candidat ayant des candidatures | **409** | `CandidateService.delete` |
| E8 | DELETE job ayant des candidatures | **409** | `JobService.delete` |
| E9 | POST catégorie nom déjà existant | **409** | CategoryService / contrainte UK |
| E10 | GET `/api/applications?candidateId=999` | **404** | `search` vérifie candidat |

⚠️ **Exécuter chaque scénario dans Swagger** et noter le body `application/problem+json`.

## E. Ce que **vous** devez faire

1. Importer `awd_db.sql` et lancer `mvn spring-boot:run` dans `awd-monolith`.
2. Vérifier les URLs OpenAPI / Swagger.
3. Rejouer E1–E10 et corriger ce brouillon si un code diffère.

## F. 3 captures d’écran obligatoires (à prendre)

1. **Swagger UI** avec le dropdown `0-all` / modules visibles.  
2. **Réponse 201** d’un `POST /api/applications` réussi (body + status).  
3. **Réponse 409** (ex. double candidature ou email dupliqué) au format ProblemDetail.
