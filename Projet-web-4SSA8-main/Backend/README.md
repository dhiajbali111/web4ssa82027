# Backend — JobBoard microservices (Validation 1 skeletons)

Java 17 / Spring Boot 3.3 / Spring Cloud 2023.0. **No business logic** yet.

| Module | Port | Role |
|---|---|---|
| eureka-server | 8761 | Service discovery |
| config-server | 8888 | Centralized config (native `config-repo`) |
| api-gateway | 8080 | Spring Cloud Gateway |
| ms-candidate | 8081 | Candidates + addresses (MySQL) |
| ms-job | 8082 | Jobs + categories (MySQL) |
| ms-application | 8083 | Applications (PostgreSQL) |
| ms-interview | 8084 | Interviews (MongoDB) |
| ms-notification | 8085 | Notifications (Python FastAPI + RabbitMQ) |

## Build all Java modules

```bash
mvn -q -DskipTests package
```

## Local start without Docker DBs

Use H2 / nodb profiles:

```bash
mvn -pl eureka-server spring-boot:run
mvn -pl config-server spring-boot:run
mvn -pl ms-candidate spring-boot:run -Dspring-boot.run.profiles=h2
mvn -pl ms-job spring-boot:run -Dspring-boot.run.profiles=h2
mvn -pl ms-application spring-boot:run -Dspring-boot.run.profiles=h2
mvn -pl ms-interview spring-boot:run -Dspring-boot.run.profiles=nodb
mvn -pl api-gateway spring-boot:run
```
