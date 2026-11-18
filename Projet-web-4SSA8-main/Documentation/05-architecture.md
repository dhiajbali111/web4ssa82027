# E4 — Architecture technique

## Diagramme unique

Fichier source : [`Diagrams/architecture.mmd`](Diagrams/architecture.mmd) · export [`Diagrams/architecture.svg`](Diagrams/architecture.svg).

Le diagramme inclut : Frontend, API Gateway, Eureka, Config Server, Keycloak, les 5 microservices, les 4 bases + RabbitMQ, le périmètre Docker Compose.

## Légende

| Style de flèche / lien | Signification |
|---|---|
| **REST + JWT** | Appel HTTP synchrone authentifié (client → Gateway) |
| **lb REST Eureka** | Routage Gateway → instance découverte via Eureka |
| **OpenFeign sync** | Appel synchrone service-à-service (validation métier) |
| **events async** | Publication / consommation RabbitMQ (domain events) |
| **register / config** | Enregistrement Eureka · chargement Config Server |
| **— trait plein vers DB** | Persistance exclusive (database per service) |

## Cohérence ports (code = compose = docs)

| Composant | Port | Preuve |
|---|---|---|
| api-gateway | 8080 | `api-gateway/.../application.yml`, `docker-compose.yml` |
| ms-candidate | 8081 | idem |
| ms-job | 8082 | idem |
| ms-application | 8083 | idem |
| ms-interview | 8084 | idem |
| ms-notification | 8085 | `Dockerfile`, compose |
| eureka-server | 8761 | idem |
| config-server | 8888 | idem |
| Keycloak | 8180→8080 | compose |
| RabbitMQ | 5672 / 15672 | compose |
| MySQL candidate/job | 3307 / 3308 | compose |
| PostgreSQL | 5433 | compose |
| MongoDB | 27017 | compose |

## Flux Keycloak (cible)

1. Front obtient un token (Authorization Code + PKCE) auprès de Keycloak.  
2. Front appelle Gateway avec `Authorization: Bearer`.  
3. Gateway valide JWT (JWKS Keycloak) et route.  
4. Rôles : `ROLE_CANDIDATE`, `ROLE_RECRUITER`, `ROLE_ADMIN` (config realm — itération sécurité).
