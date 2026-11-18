#!/usr/bin/env python3
"""Generate Spring Boot / Python microservice skeletons for AWD JobBoard Validation 1.
No business logic — compile & start only. Identifiers in English.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "Backend"
BOOT = "3.3.5"
CLOUD = "2023.0.3"
JAVA = "17"
GROUP = "tn.esprit.awd"

SERVICES = {
    "eureka-server": {"port": 8761, "type": "eureka"},
    "config-server": {"port": 8888, "type": "config"},
    "api-gateway": {"port": 8080, "type": "gateway"},
    "ms-candidate": {"port": 8081, "type": "business", "db": "mysql", "pkg": "candidate"},
    "ms-job": {"port": 8082, "type": "business", "db": "mysql", "pkg": "job"},
    "ms-application": {"port": 8083, "type": "business", "db": "postgres", "pkg": "application"},
    "ms-interview": {"port": 8084, "type": "business", "db": "mongo", "pkg": "interview"},
}


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def parent_bom():
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>{BOOT}</version>
    <relativePath/>
  </parent>
  <groupId>{GROUP}</groupId>
  <artifactId>jobboard-parent</artifactId>
  <version>0.0.1-SNAPSHOT</version>
  <packaging>pom</packaging>
  <name>jobboard-parent</name>
  <properties>
    <java.version>{JAVA}</java.version>
    <spring-cloud.version>{CLOUD}</spring-cloud.version>
  </properties>
  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-dependencies</artifactId>
        <version>${{spring-cloud.version}}</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>
  <modules>
    <module>eureka-server</module>
    <module>config-server</module>
    <module>api-gateway</module>
    <module>ms-candidate</module>
    <module>ms-job</module>
    <module>ms-application</module>
    <module>ms-interview</module>
  </modules>
</project>
"""


def pom(name: str, deps: list[str], extra: str = "") -> str:
    dep_xml = "\n".join(deps)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>{GROUP}</groupId>
    <artifactId>jobboard-parent</artifactId>
    <version>0.0.1-SNAPSHOT</version>
  </parent>
  <artifactId>{name}</artifactId>
  <name>{name}</name>
  <dependencies>
{dep_xml}
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
      </plugin>
    </plugins>
  </build>
{extra}
</project>
"""


DEP = {
    "web": '    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>',
    "actuator": '    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-actuator</artifactId></dependency>',
    "eureka-client": '    <dependency><groupId>org.springframework.cloud</groupId><artifactId>spring-cloud-starter-netflix-eureka-client</artifactId></dependency>',
    "eureka-server": '    <dependency><groupId>org.springframework.cloud</groupId><artifactId>spring-cloud-starter-netflix-eureka-server</artifactId></dependency>',
    "config-server": '    <dependency><groupId>org.springframework.cloud</groupId><artifactId>spring-cloud-config-server</artifactId></dependency>',
    "config-client": '    <dependency><groupId>org.springframework.cloud</groupId><artifactId>spring-cloud-starter-config</artifactId></dependency>',
    "gateway": '    <dependency><groupId>org.springframework.cloud</groupId><artifactId>spring-cloud-starter-gateway</artifactId></dependency>',
    "jpa": '    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-data-jpa</artifactId></dependency>',
    "mongo": '    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-data-mongodb</artifactId></dependency>',
    "mysql": '    <dependency><groupId>com.mysql</groupId><artifactId>mysql-connector-j</artifactId><scope>runtime</scope></dependency>',
    "postgres": '    <dependency><groupId>org.postgresql</groupId><artifactId>postgresql</artifactId><scope>runtime</scope></dependency>',
    "h2": '    <dependency><groupId>com.h2database</groupId><artifactId>h2</artifactId><scope>runtime</scope></dependency>',
    "validation": '    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-validation</artifactId></dependency>',
    "amqp": '    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-amqp</artifactId></dependency>',
    "feign": '    <dependency><groupId>org.springframework.cloud</groupId><artifactId>spring-cloud-starter-openfeign</artifactId></dependency>',
    "circuit": '    <dependency><groupId>org.springframework.cloud</groupId><artifactId>spring-cloud-starter-circuitbreaker-resilience4j</artifactId></dependency>',
}


def java_app(pkg: str, class_name: str, annotations: list[str]) -> str:
    anns = "\n".join(annotations)
    return f"""package {pkg};

{chr(10).join('import ' + a.split('(')[0].replace('@','') + ';' for a in [] )}
{anns}
public class {class_name} {{

    public static void main(String[] args) {{
        org.springframework.boot.SpringApplication.run({class_name}.class, args);
    }}
}}
""".replace(
        "\n\n\n", "\n\n"
    )


def main_class(pkg: str, class_name: str, imports: list[str], annotations: list[str]) -> str:
    imp = "\n".join(f"import {i};" for i in imports)
    anns = "\n".join(annotations)
    return f"""package {pkg};

{imp}

{anns}
public class {class_name} {{

    public static void main(String[] args) {{
        org.springframework.boot.SpringApplication.run({class_name}.class, args);
    }}
}}
"""


def placeholder_layers(base: Path, root_pkg: str, entity_name: str):
    """Empty/placeholder controller/service/repository/entity/dto."""
    pkg_path = root_pkg.replace(".", "/")
    write(
        base / f"src/main/java/{pkg_path}/entity/{entity_name}.java",
        f"""package {root_pkg}.entity;

/** Placeholder entity — no business logic in Validation 1. */
public class {entity_name} {{
    private Long id;

    public Long getId() {{ return id; }}
    public void setId(Long id) {{ this.id = id; }}
}}
""",
    )
    write(
        base / f"src/main/java/{pkg_path}/dto/{entity_name}Dto.java",
        f"""package {root_pkg}.dto;

/** Placeholder DTO — no business logic in Validation 1. */
public class {entity_name}Dto {{
    private Long id;

    public Long getId() {{ return id; }}
    public void setId(Long id) {{ this.id = id; }}
}}
""",
    )
    write(
        base / f"src/main/java/{pkg_path}/repository/{entity_name}Repository.java",
        f"""package {root_pkg}.repository;

import org.springframework.stereotype.Repository;

/** Placeholder repository — no business logic in Validation 1. */
@Repository
public class {entity_name}Repository {{
}}
""",
    )
    write(
        base / f"src/main/java/{pkg_path}/service/{entity_name}Service.java",
        f"""package {root_pkg}.service;

import org.springframework.stereotype.Service;

/** Placeholder service — no business logic in Validation 1. */
@Service
public class {entity_name}Service {{
}}
""",
    )
    write(
        base / f"src/main/java/{pkg_path}/controller/{entity_name}Controller.java",
        f"""package {root_pkg}.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/** Placeholder controller — exposes a ping endpoint only. */
@RestController
@RequestMapping("/api/placeholder")
public class {entity_name}Controller {{

    @GetMapping("/ping")
    public Map<String, String> ping() {{
        return Map.of("status", "ok", "service", "{entity_name.lower()}");
    }}
}}
""",
    )


def dockerfile(jar_name: str, port: int) -> str:
    return f"""FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY target/{jar_name}-0.0.1-SNAPSHOT.jar app.jar
EXPOSE {port}
ENTRYPOINT ["java","-jar","/app/app.jar"]
"""


def bootstrap_yml(app_name: str, port: int, extra: str = "") -> str:
    return f"""spring:
  application:
    name: {app_name}
  config:
    import: optional:configserver:http://localhost:8888
server:
  port: {port}
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
    register-with-eureka: true
    fetch-registry: true
management:
  endpoints:
    web:
      exposure:
        include: health,info
  endpoint:
    health:
      show-details: always
{extra}
"""


def create_eureka():
    name = "eureka-server"
    base = ROOT / name
    write(base / "pom.xml", pom(name, [DEP["eureka-server"], DEP["actuator"]]))
    write(
        base / "src/main/java/tn/esprit/awd/eureka/EurekaServerApplication.java",
        main_class(
            "tn.esprit.awd.eureka",
            "EurekaServerApplication",
            [
                "org.springframework.boot.autoconfigure.SpringBootApplication",
                "org.springframework.cloud.netflix.eureka.server.EnableEurekaServer",
            ],
            ["@SpringBootApplication", "@EnableEurekaServer"],
        ),
    )
    write(
        base / "src/main/resources/application.yml",
        f"""spring:
  application:
    name: eureka-server
server:
  port: 8761
eureka:
  client:
    register-with-eureka: false
    fetch-registry: false
  server:
    enable-self-preservation: false
management:
  endpoints:
    web:
      exposure:
        include: health,info
""",
    )
    write(base / "Dockerfile", dockerfile(name, 8761))


def create_config():
    name = "config-server"
    base = ROOT / name
    write(base / "pom.xml", pom(name, [DEP["config-server"], DEP["actuator"]]))
    write(
        base / "src/main/java/tn/esprit/awd/config/ConfigServerApplication.java",
        main_class(
            "tn.esprit.awd.config",
            "ConfigServerApplication",
            [
                "org.springframework.boot.autoconfigure.SpringBootApplication",
                "org.springframework.cloud.config.server.EnableConfigServer",
            ],
            ["@SpringBootApplication", "@EnableConfigServer"],
        ),
    )
    # native file-based config repo
    write(
        base / "src/main/resources/application.yml",
        """spring:
  application:
    name: config-server
  profiles:
    active: native
  cloud:
    config:
      server:
        native:
          search-locations: classpath:/config-repo,file:./config-repo,file:../config-repo
server:
  port: 8888
management:
  endpoints:
    web:
      exposure:
        include: health,info
""",
    )
    # shared config files
    for svc, port in [
        ("ms-candidate", 8081),
        ("ms-job", 8082),
        ("ms-application", 8083),
        ("ms-interview", 8084),
        ("api-gateway", 8080),
        ("application", None),  # shared defaults
    ]:
        if svc == "application":
            write(
                base / "src/main/resources/config-repo/application.yml",
                """eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
management:
  endpoints:
    web:
      exposure:
        include: health,info
""",
            )
            write(
                ROOT / "config-repo/application.yml",
                """eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
management:
  endpoints:
    web:
      exposure:
        include: health,info
""",
            )
        else:
            content = f"""server:
  port: {port}
spring:
  application:
    name: {svc}
"""
            write(base / f"src/main/resources/config-repo/{svc}.yml", content)
            write(ROOT / f"config-repo/{svc}.yml", content)
    write(base / "Dockerfile", dockerfile(name, 8888))


def create_gateway():
    name = "api-gateway"
    base = ROOT / name
    write(
        base / "pom.xml",
        pom(name, [DEP["gateway"], DEP["eureka-client"], DEP["config-client"], DEP["actuator"]]),
    )
    write(
        base / "src/main/java/tn/esprit/awd/gateway/ApiGatewayApplication.java",
        main_class(
            "tn.esprit.awd.gateway",
            "ApiGatewayApplication",
            [
                "org.springframework.boot.autoconfigure.SpringBootApplication",
                "org.springframework.cloud.client.discovery.EnableDiscoveryClient",
            ],
            ["@SpringBootApplication", "@EnableDiscoveryClient"],
        ),
    )
    write(
        base / "src/main/resources/application.yml",
        """spring:
  application:
    name: api-gateway
  config:
    import: optional:configserver:http://localhost:8888
  cloud:
    gateway:
      discovery:
        locator:
          enabled: true
          lower-case-service-id: true
      routes:
        - id: ms-candidate
          uri: lb://ms-candidate
          predicates:
            - Path=/api/candidates/**,/api/addresses/**
        - id: ms-job
          uri: lb://ms-job
          predicates:
            - Path=/api/jobs/**,/api/categories/**
        - id: ms-application
          uri: lb://ms-application
          predicates:
            - Path=/api/applications/**
        - id: ms-interview
          uri: lb://ms-interview
          predicates:
            - Path=/api/interviews/**
        - id: ms-notification
          uri: http://localhost:8085
          predicates:
            - Path=/api/notifications/**
server:
  port: 8080
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
management:
  endpoints:
    web:
      exposure:
        include: health,info,gateway
""",
    )
    write(base / "Dockerfile", dockerfile(name, 8080))


def db_yml(db: str, service: str) -> str:
    if db == "mysql":
        db_name = service.replace("ms-", "").replace("-", "_") + "_db"
        host_port = 3307 if "candidate" in service else 3308
        return f"""
spring:
  datasource:
    url: jdbc:mysql://localhost:{host_port}/{db_name}?createDatabaseIfNotExist=true&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC
    username: root
    password: root
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    hibernate:
      ddl-auto: update
    open-in-view: false
    show-sql: false
  # Fallback H2 profile for local compile/start without MySQL:
  # spring.profiles.active=h2
---
spring:
  config:
    activate:
      on-profile: h2
  datasource:
    url: jdbc:h2:mem:{db_name};MODE=MySQL;DB_CLOSE_DELAY=-1
    username: sa
    password:
    driver-class-name: org.h2.Driver
  h2:
    console:
      enabled: true
  jpa:
    hibernate:
      ddl-auto: update
    database-platform: org.hibernate.dialect.H2Dialect
"""
    if db == "postgres":
        return """
spring:
  datasource:
    url: jdbc:postgresql://localhost:5433/application_db
    username: app
    password: app
    driver-class-name: org.postgresql.Driver
  jpa:
    hibernate:
      ddl-auto: update
    open-in-view: false
---
spring:
  config:
    activate:
      on-profile: h2
  datasource:
    url: jdbc:h2:mem:application_db;MODE=PostgreSQL;DB_CLOSE_DELAY=-1
    username: sa
    password:
    driver-class-name: org.h2.Driver
  jpa:
    hibernate:
      ddl-auto: update
    database-platform: org.hibernate.dialect.H2Dialect
"""
    if db == "mongo":
        return """
spring:
  data:
    mongodb:
      uri: mongodb://localhost:27017/interview_db
---
spring:
  config:
    activate:
      on-profile: h2
  # No real Mongo required for skeleton start: embedded not used;
  # autoconfig excluded below when profile=h2 via main class optional.
  data:
    mongodb:
      uri: mongodb://localhost:27017/interview_db
"""
    return ""


def create_business(name: str, port: int, db: str, pkg: str, entity: str):
    base = ROOT / name
    root_pkg = f"tn.esprit.awd.{pkg}"
    deps = [
        DEP["web"],
        DEP["actuator"],
        DEP["eureka-client"],
        DEP["config-client"],
        DEP["validation"],
        DEP["feign"],
        DEP["circuit"],
        DEP["amqp"],
        DEP["h2"],
    ]
    if db == "mysql":
        deps += [DEP["jpa"], DEP["mysql"]]
    elif db == "postgres":
        deps += [DEP["jpa"], DEP["postgres"]]
    elif db == "mongo":
        deps += [DEP["mongo"]]

    write(base / "pom.xml", pom(name, deps))

    annotations = [
        "@SpringBootApplication",
        "@EnableDiscoveryClient",
        "@EnableFeignClients",
    ]
    imports = [
        "org.springframework.boot.autoconfigure.SpringBootApplication",
        "org.springframework.cloud.client.discovery.EnableDiscoveryClient",
        "org.springframework.cloud.openfeign.EnableFeignClients",
    ]
    # For interview mongo skeleton: exclude mongo autoconfig on h2 profile is complex;
    # use optional auto-config and allow fail-fast false
    class_name = f"{entity}ServiceApplication"
    write(
        base / f"src/main/java/{root_pkg.replace('.', '/')}/{class_name}.java",
        main_class(root_pkg, class_name, imports, annotations),
    )
    yml_extra = db_yml(db, name)
    if db == "mongo":
        yml_extra += """
---
spring:
  config:
    activate:
      on-profile: nodb
  autoconfigure:
    exclude:
      - org.springframework.boot.autoconfigure.mongo.MongoAutoConfiguration
      - org.springframework.boot.autoconfigure.data.mongo.MongoDataAutoConfiguration
"""
    write(
        base / "src/main/resources/application.yml",
        bootstrap_yml(name, port, yml_extra),
    )

    placeholder_layers(base, root_pkg, entity)
    # Feign client placeholder
    write(
        base / f"src/main/java/{root_pkg.replace('.', '/')}/client/RemotePingClient.java",
        f"""package {root_pkg}.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.Map;

/** Placeholder Feign client — wired later for sync calls. */
@FeignClient(name = "ms-candidate", path = "/api/placeholder")
public interface RemotePingClient {{

    @GetMapping("/ping")
    Map<String, String> ping();
}}
""",
    )
    write(base / "Dockerfile", dockerfile(name, port))


def create_notification():
    base = ROOT / "ms-notification"
    write(
        base / "requirements.txt",
        """fastapi==0.115.0
uvicorn[standard]==0.30.6
pika==1.3.2
pydantic==2.9.2
httpx==0.27.2
""",
    )
    write(
        base / "app/main.py",
        '''"""Notification microservice (advanced): Python FastAPI + RabbitMQ consumer.
Validation 1 skeleton — no real e-mail / LLM business logic yet.
"""
from fastapi import FastAPI

app = FastAPI(title="ms-notification", version="0.0.1")


@app.get("/actuator/health")
def health():
    return {"status": "UP", "service": "ms-notification"}


@app.get("/api/notifications/ping")
def ping():
    return {"status": "ok", "service": "notification"}


# Placeholder: RabbitMQ consumer will be wired in a later iteration.
# Expected queues: application.created, interview.scheduled, application.status.changed
''',
    )
    write(
        base / "app/__init__.py",
        '"""ms-notification package."""\n',
    )
    write(
        base / "Dockerfile",
        """FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
EXPOSE 8085
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8085"]
""",
    )
    write(
        base / "README.md",
        """# ms-notification (advanced technology)

Python **FastAPI** service that will consume domain events from **RabbitMQ**
and send notifications (e-mail). Optional LLM-assisted message drafting is planned.

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --port 8085 --reload
```

Health: http://localhost:8085/actuator/health
""",
    )


def create_docker_compose():
    write(
        ROOT / "docker-compose.yml",
        """services:
  mysql-candidate:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: candidate_db
    ports: ["3307:3306"]
    volumes: [mysql_candidate_data:/var/lib/mysql]
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 10

  mysql-job:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: job_db
    ports: ["3308:3306"]
    volumes: [mysql_job_data:/var/lib/mysql]
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 10

  postgres-application:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: application_db
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
    ports: ["5433:5432"]
    volumes: [postgres_application_data:/var/lib/postgresql/data]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d application_db"]
      interval: 10s
      timeout: 5s
      retries: 10

  mongo-interview:
    image: mongo:7
    ports: ["27017:27017"]
    volumes: [mongo_interview_data:/data/db]

  rabbitmq:
    image: rabbitmq:3.13-management-alpine
    ports: ["5672:5672", "15672:15672"]
    environment:
      RABBITMQ_DEFAULT_USER: guest
      RABBITMQ_DEFAULT_PASS: guest

  keycloak:
    image: quay.io/keycloak/keycloak:25.0.0
    command: ["start-dev"]
    environment:
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin
    ports: ["8180:8080"]

  eureka-server:
    build: ./eureka-server
    ports: ["8761:8761"]
    depends_on: [rabbitmq]

  config-server:
    build: ./config-server
    ports: ["8888:8888"]
    depends_on: [eureka-server]

  api-gateway:
    build: ./api-gateway
    ports: ["8080:8080"]
    environment:
      EUREKA_CLIENT_SERVICEURL_DEFAULTZONE: http://eureka-server:8761/eureka/
      SPRING_CONFIG_IMPORT: optional:configserver:http://config-server:8888
    depends_on: [eureka-server, config-server]

  ms-candidate:
    build: ./ms-candidate
    ports: ["8081:8081"]
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://mysql-candidate:3306/candidate_db?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC
      SPRING_DATASOURCE_USERNAME: root
      SPRING_DATASOURCE_PASSWORD: root
      EUREKA_CLIENT_SERVICEURL_DEFAULTZONE: http://eureka-server:8761/eureka/
      SPRING_CONFIG_IMPORT: optional:configserver:http://config-server:8888
      SPRING_RABBITMQ_HOST: rabbitmq
    depends_on: [mysql-candidate, eureka-server, config-server, rabbitmq]

  ms-job:
    build: ./ms-job
    ports: ["8082:8082"]
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://mysql-job:3306/job_db?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC
      SPRING_DATASOURCE_USERNAME: root
      SPRING_DATASOURCE_PASSWORD: root
      EUREKA_CLIENT_SERVICEURL_DEFAULTZONE: http://eureka-server:8761/eureka/
      SPRING_CONFIG_IMPORT: optional:configserver:http://config-server:8888
      SPRING_RABBITMQ_HOST: rabbitmq
    depends_on: [mysql-job, eureka-server, config-server, rabbitmq]

  ms-application:
    build: ./ms-application
    ports: ["8083:8083"]
    environment:
      SPRING_DATASOURCE_URL: jdbc:postgresql://postgres-application:5432/application_db
      SPRING_DATASOURCE_USERNAME: app
      SPRING_DATASOURCE_PASSWORD: app
      EUREKA_CLIENT_SERVICEURL_DEFAULTZONE: http://eureka-server:8761/eureka/
      SPRING_CONFIG_IMPORT: optional:configserver:http://config-server:8888
      SPRING_RABBITMQ_HOST: rabbitmq
    depends_on: [postgres-application, eureka-server, config-server, rabbitmq]

  ms-interview:
    build: ./ms-interview
    ports: ["8084:8084"]
    environment:
      SPRING_DATA_MONGODB_URI: mongodb://mongo-interview:27017/interview_db
      EUREKA_CLIENT_SERVICEURL_DEFAULTZONE: http://eureka-server:8761/eureka/
      SPRING_CONFIG_IMPORT: optional:configserver:http://config-server:8888
      SPRING_RABBITMQ_HOST: rabbitmq
    depends_on: [mongo-interview, eureka-server, config-server, rabbitmq]

  ms-notification:
    build: ./ms-notification
    ports: ["8085:8085"]
    environment:
      RABBITMQ_HOST: rabbitmq
    depends_on: [rabbitmq]

volumes:
  mysql_candidate_data:
  mysql_job_data:
  postgres_application_data:
  mongo_interview_data:
""",
    )


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    write(ROOT / "pom.xml", parent_bom())
    create_eureka()
    create_config()
    create_gateway()
    create_business("ms-candidate", 8081, "mysql", "candidate", "Candidate")
    create_business("ms-job", 8082, "mysql", "job", "Job")
    create_business("ms-application", 8083, "postgres", "candidature", "Application")
    create_business("ms-interview", 8084, "mongo", "interview", "Interview")
    create_notification()
    create_docker_compose()
    write(
        ROOT / "README.md",
        """# Backend — JobBoard microservices (Validation 1 skeletons)

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
""",
    )
    print(f"Scaffolded under {ROOT}")


if __name__ == "__main__":
    main()
