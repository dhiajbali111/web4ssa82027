#!/usr/bin/env bash
# JobBoard stack verification — Maven builds, Docker readiness, Eureka, health, DB isolation.
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND="$ROOT/Backend"
FAILED=0
READY_TIMEOUT="${READY_TIMEOUT:-300}"
READY_INTERVAL="${READY_INTERVAL:-5}"

# component|status|url rows for final table
declare -a TABLE_ROWS=()

pass() { echo "  PASS  $*"; }
fail() { echo "  FAIL  $*"; FAILED=1; }

record() {
  local component="$1" status="$2" url="${3:-}"
  TABLE_ROWS+=("${component}|${status}|${url}")
}

http_code() {
  local url="$1"
  curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 --max-time 15 "$url" 2>/dev/null || echo "000"
}

http_body() {
  local url="$1"
  curl -s --connect-timeout 5 --max-time 15 -H "Accept: application/json" "$url" 2>/dev/null || true
}

body_is_up() {
  local body="$1"
  echo "$body" | grep -Eqi '"status"[[:space:]]*:[[:space:]]*"UP"' \
    || echo "$body" | grep -Eqi '"status"[[:space:]]*:[[:space:]]*"up"'
}

wait_url() {
  local url="$1" label="$2" deadline=$((SECONDS + READY_TIMEOUT))
  echo "  waiting for $label ($url)..."
  while (( SECONDS < deadline )); do
    local code
    code="$(http_code "$url")"
    if [[ "$code" =~ ^2 ]]; then
      return 0
    fi
    sleep "$READY_INTERVAL"
  done
  return 1
}

# ---------------------------------------------------------------------------
echo "=== 1) Maven clean package (per project) ==="
MAVEN_PROJECTS=()
while IFS= read -r -d '' pom; do
  MAVEN_PROJECTS+=("$(dirname "$pom")")
done < <(find "$BACKEND" -mindepth 2 -maxdepth 2 -name pom.xml -print0 | sort -z)

if [[ ${#MAVEN_PROJECTS[@]} -eq 0 ]]; then
  fail "No Maven projects found under Backend/"
  record "maven" "FAIL" "Backend/*"
fi

for proj in "${MAVEN_PROJECTS[@]}"; do
  name="$(basename "$proj")"
  echo "--- $name ---"
  if (cd "$proj" && mvn -q clean package -DskipTests); then
    pass "$name"
    record "build:$name" "PASS" "$proj"
  else
    fail "$name (mvn clean package -DskipTests)"
    record "build:$name" "FAIL" "$proj"
  fi
done

# ---------------------------------------------------------------------------
echo ""
echo "=== 2) Docker Compose up -d --build ==="
if ! command -v docker >/dev/null 2>&1; then
  fail "docker not found"
  record "docker-compose" "FAIL" "Backend/docker-compose.yml"
else
  if (cd "$BACKEND" && docker compose up -d --build); then
    pass "docker compose up -d --build"
    record "docker-compose" "PASS" "Backend/docker-compose.yml"
  else
    fail "docker compose up -d --build"
    record "docker-compose" "FAIL" "Backend/docker-compose.yml"
  fi
fi

echo ""
echo "=== 2b) Wait for readiness ==="
READY_CHECKS=(
  "http://localhost:8761/actuator/health|eureka-server"
  "http://localhost:8888/actuator/health|config-server"
  "http://localhost:8080/actuator/health|api-gateway"
  "http://localhost:8081/actuator/health|ms-candidate"
  "http://localhost:8082/actuator/health|ms-job"
  "http://localhost:8083/actuator/health|ms-application"
  "http://localhost:8084/actuator/health|ms-interview"
  "http://localhost:8085/actuator/health|ms-notification"
  "http://localhost:8180|keycloak"
)
for entry in "${READY_CHECKS[@]}"; do
  url="${entry%%|*}"
  label="${entry##*|}"
  if wait_url "$url" "$label"; then
    pass "ready $label"
  else
    fail "timeout waiting for $label ($url)"
  fi
done

# ---------------------------------------------------------------------------
echo ""
echo "=== 3a) Eureka — every service UP ==="
EUREKA_APPS_URL="http://localhost:8761/eureka/apps"
EXPECTED_EUREKA=(API-GATEWAY MS-CANDIDATE MS-JOB MS-APPLICATION MS-INTERVIEW)
EUREKA_XML="$(curl -s --connect-timeout 5 --max-time 15 -H "Accept: application/xml" "$EUREKA_APPS_URL" 2>/dev/null || true)"
EUREKA_JSON="$(http_body "$EUREKA_APPS_URL")"

for svc in "${EXPECTED_EUREKA[@]}"; do
  # Match app name and UP status in XML or JSON
  if echo "$EUREKA_XML" | grep -qi "<name>${svc}</name>" && echo "$EUREKA_XML" | grep -A80 -i "<name>${svc}</name>" | grep -qi "<status>UP</status>"; then
    pass "Eureka $svc UP"
    record "eureka:$svc" "UP" "$EUREKA_APPS_URL"
  elif echo "$EUREKA_JSON" | grep -qi "\"name\"[[:space:]]*:[[:space:]]*\"${svc}\"" \
    && echo "$EUREKA_JSON" | grep -qi "\"status\"[[:space:]]*:[[:space:]]*\"UP\""; then
    # JSON may list multiple apps; require the app block roughly contains UP
    if echo "$EUREKA_JSON" | tr '\n' ' ' | grep -Eiq "\"name\"[[:space:]]*:[[:space:]]*\"${svc}\"[^]]*\"status\"[[:space:]]*:[[:space:]]*\"UP\"" \
      || echo "$EUREKA_JSON" | tr '\n' ' ' | grep -Eiq "\"name\"[[:space:]]*:[[:space:]]*\"${svc}\".{0,400}\"status\"[[:space:]]*:[[:space:]]*\"UP\""; then
      pass "Eureka $svc UP"
      record "eureka:$svc" "UP" "$EUREKA_APPS_URL"
    else
      fail "Eureka $svc not UP"
      record "eureka:$svc" "FAIL" "$EUREKA_APPS_URL"
    fi
  else
    fail "Eureka $svc not UP / not registered"
    record "eureka:$svc" "FAIL" "$EUREKA_APPS_URL"
  fi
done

# ---------------------------------------------------------------------------
echo ""
echo "=== 3b) Actuator health — direct ==="
DIRECT_SERVICES=(
  "api-gateway|http://localhost:8080/actuator/health"
  "ms-candidate|http://localhost:8081/actuator/health"
  "ms-job|http://localhost:8082/actuator/health"
  "ms-application|http://localhost:8083/actuator/health"
  "ms-interview|http://localhost:8084/actuator/health"
  "ms-notification|http://localhost:8085/actuator/health"
)
for entry in "${DIRECT_SERVICES[@]}"; do
  name="${entry%%|*}"
  url="${entry##*|}"
  body="$(http_body "$url")"
  if body_is_up "$body"; then
    pass "direct health $name"
    record "health:$name" "UP" "$url"
  else
    fail "direct health $name ($url) body=${body:0:120}"
    record "health:$name" "FAIL" "$url"
  fi
done

echo ""
echo "=== 3c) Actuator health — via API Gateway ==="
# Discovery locator: /{serviceId}/actuator/health ; notification via explicit /ms-notification/**
GW_SERVICES=(
  "api-gateway|http://localhost:8080/actuator/health"
  "ms-candidate|http://localhost:8080/ms-candidate/actuator/health"
  "ms-job|http://localhost:8080/ms-job/actuator/health"
  "ms-application|http://localhost:8080/ms-application/actuator/health"
  "ms-interview|http://localhost:8080/ms-interview/actuator/health"
  "ms-notification|http://localhost:8080/ms-notification/actuator/health"
)
for entry in "${GW_SERVICES[@]}"; do
  name="${entry%%|*}"
  url="${entry##*|}"
  body="$(http_body "$url")"
  if body_is_up "$body"; then
    pass "gateway health $name"
    record "gw-health:$name" "UP" "$url"
  else
    fail "gateway health $name ($url) body=${body:0:120}"
    record "gw-health:$name" "FAIL" "$url"
  fi
done

echo ""
echo "=== 3d) Config Server & Keycloak ==="
CS_URL="http://localhost:8888/actuator/health"
CS_BODY="$(http_body "$CS_URL")"
if body_is_up "$CS_BODY"; then
  pass "config-server"
  record "config-server" "UP" "$CS_URL"
else
  fail "config-server ($CS_URL)"
  record "config-server" "FAIL" "$CS_URL"
fi

KC_URL="http://localhost:8180"
KC_CODE="$(http_code "$KC_URL")"
if [[ "$KC_CODE" =~ ^2 ]] || [[ "$KC_CODE" =~ ^3 ]]; then
  pass "keycloak HTTP $KC_CODE"
  record "keycloak" "UP" "$KC_URL"
else
  fail "keycloak ($KC_URL) HTTP $KC_CODE"
  record "keycloak" "FAIL" "$KC_URL"
fi

# ---------------------------------------------------------------------------
echo ""
echo "=== 4) Datasource URL uniqueness (database-per-service) ==="
# Collect JDBC / Mongo URLs from default (non-profile) application.yml and compose env
declare -A URL_OWNERS=()
DUP_FOUND=0

add_url() {
  local owner="$1" raw="$2"
  # Strip query string for comparison identity of the same database
  local key="${raw%%\?*}"
  key="$(echo "$key" | tr '[:upper:]' '[:lower:]' | sed 's/[[:space:]]//g')"
  [[ -z "$key" ]] && return
  # Ignore H2 / in-memory
  if echo "$key" | grep -Eqi 'jdbc:h2:|mem:'; then
    return
  fi
  if [[ -n "${URL_OWNERS[$key]+x}" ]]; then
    fail "shared datasource: $owner and ${URL_OWNERS[$key]} -> $key"
    DUP_FOUND=1
  else
    URL_OWNERS[$key]="$owner"
  fi
}

for yml in "$BACKEND"/ms-*/src/main/resources/application.yml; do
  [[ -f "$yml" ]] || continue
  svc="$(basename "$(dirname "$(dirname "$(dirname "$yml")")")")"
  # Extract default-profile datasource url / mongodb uri (before first ---)
  default_block="$(awk 'BEGIN{p=1} /^---/{p=0} p' "$yml")"
  while IFS= read -r line; do
    if echo "$line" | grep -Eq '^[[:space:]]*url:[[:space:]]*jdbc:'; then
      url="$(echo "$line" | sed -E 's/^[[:space:]]*url:[[:space:]]*//;s/[[:space:]]*$//;s/^["'\'']//;s/["'\'']$//')"
      add_url "$svc" "$url"
    fi
    if echo "$line" | grep -Eq '^[[:space:]]*uri:[[:space:]]*mongodb:'; then
      url="$(echo "$line" | sed -E 's/^[[:space:]]*uri:[[:space:]]*//;s/[[:space:]]*$//;s/^["'\'']//;s/["'\'']$//')"
      add_url "$svc" "$url"
    fi
  done <<< "$default_block"
done

# Compose env overrides
if [[ -f "$BACKEND/docker-compose.yml" ]]; then
  current_svc=""
  while IFS= read -r line; do
    if echo "$line" | grep -Eq '^  [a-z0-9-]+:[[:space:]]*$'; then
      current_svc="$(echo "$line" | sed -E 's/^  ([^:]+):.*/\1/')"
    fi
    if echo "$line" | grep -Eq 'SPRING_DATASOURCE_URL:|SPRING_DATA_MONGODB_URI:'; then
      url="$(echo "$line" | sed -E 's/.*:[[:space:]]*//;s/[[:space:]]*$//;s/^["'\'']//;s/["'\'']$//')"
      add_url "compose:$current_svc" "$url"
    fi
  done < "$BACKEND/docker-compose.yml"
fi

if [[ $DUP_FOUND -eq 0 ]]; then
  pass "no shared datasource URLs (${#URL_OWNERS[@]} unique)"
  record "datasource-isolation" "PASS" "n/a"
else
  record "datasource-isolation" "FAIL" "n/a"
fi

# ---------------------------------------------------------------------------
echo ""
echo "=== FINAL TABLE ==="
printf "%-28s | %-6s | %s\n" "component" "status" "URL"
printf "%-28s-+-%-6s-+-%s\n" "----------------------------" "------" "--------------------------------"
for row in "${TABLE_ROWS[@]}"; do
  IFS='|' read -r c s u <<< "$row"
  printf "%-28s | %-6s | %s\n" "$c" "$s" "$u"
done

echo ""
if [[ $FAILED -ne 0 ]]; then
  echo "RESULT: FAIL - one or more checks failed"
  exit 1
fi
echo "RESULT: PASS - all checks ok"
exit 0
