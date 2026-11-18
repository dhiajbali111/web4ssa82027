#!/usr/bin/env bash
# JobBoard Validation 1 - local start (Linux/macOS)
set -euo pipefail
cd "$(dirname "$0")"

echo "[1/3] Building Java modules..."
mvn -DskipTests package

echo "[2/3] Starting infra + business services..."
mvn -pl eureka-server spring-boot:run &
sleep 15
mvn -pl config-server spring-boot:run &
sleep 10
mvn -pl api-gateway spring-boot:run &
mvn -pl ms-candidate spring-boot:run -Dspring-boot.run.profiles=h2 &
mvn -pl ms-job spring-boot:run -Dspring-boot.run.profiles=h2 &
mvn -pl ms-application spring-boot:run -Dspring-boot.run.profiles=h2 &
mvn -pl ms-interview spring-boot:run -Dspring-boot.run.profiles=nodb &

echo "[3/3] Starting ms-notification..."
( cd ms-notification && python -m uvicorn app.main:app --port 8085 ) &

echo "Eureka:        http://localhost:8761"
echo "Gateway:       http://localhost:8080/actuator/health"
echo "Candidate:     http://localhost:8081/actuator/health"
echo "Notification:  http://localhost:8085/actuator/health"
echo "Stop with: pkill -f 'spring-boot:run' ; pkill -f 'uvicorn app.main'"
