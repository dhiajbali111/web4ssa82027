@echo off
setlocal EnableExtensions EnableDelayedExpansion
REM JobBoard stack verification — Maven builds, Docker readiness, Eureka, health, DB isolation.

set "ROOT=%~dp0.."
pushd "%ROOT%" >nul
set "ROOT=%CD%"
popd >nul
set "BACKEND=%ROOT%\Backend"
set "FAILED=0"
if not defined READY_TIMEOUT set "READY_TIMEOUT=300"
if not defined READY_INTERVAL set "READY_INTERVAL=5"
set "TABLE_FILE=%TEMP%\jobboard_verify_table_%RANDOM%.txt"
if exist "%TABLE_FILE%" del "%TABLE_FILE%" >nul 2>&1

call :echo_header "1) Maven clean package (per project)"
for /d %%D in ("%BACKEND%\*") do (
  if exist "%%D\pom.xml" (
    set "NAME=%%~nxD"
    echo --- !NAME! ---
    pushd "%%D" >nul
    call mvn -q clean package -DskipTests
    if errorlevel 1 (
      call :fail "!NAME! (mvn clean package -DskipTests)"
      call :record "build:!NAME!" "FAIL" "%%D"
    ) else (
      call :pass "!NAME!"
      call :record "build:!NAME!" "PASS" "%%D"
    )
    popd >nul
  )
)

echo.
call :echo_header "2) Docker Compose up -d --build"
where docker >nul 2>&1
if errorlevel 1 (
  call :fail "docker not found"
  call :record "docker-compose" "FAIL" "Backend/docker-compose.yml"
) else (
  pushd "%BACKEND%" >nul
  docker compose up -d --build
  if errorlevel 1 (
    call :fail "docker compose up -d --build"
    call :record "docker-compose" "FAIL" "Backend/docker-compose.yml"
  ) else (
    call :pass "docker compose up -d --build"
    call :record "docker-compose" "PASS" "Backend/docker-compose.yml"
  )
  popd >nul
)

echo.
call :echo_header "2b) Wait for readiness"
call :wait_url "http://localhost:8761/actuator/health" "eureka-server"
call :wait_url "http://localhost:8888/actuator/health" "config-server"
call :wait_url "http://localhost:8080/actuator/health" "api-gateway"
call :wait_url "http://localhost:8081/actuator/health" "ms-candidate"
call :wait_url "http://localhost:8082/actuator/health" "ms-job"
call :wait_url "http://localhost:8083/actuator/health" "ms-application"
call :wait_url "http://localhost:8084/actuator/health" "ms-interview"
call :wait_url "http://localhost:8085/actuator/health" "ms-notification"
call :wait_url "http://localhost:8180" "keycloak"

echo.
call :echo_header "3a) Eureka — every service UP"
set "EUREKA_APPS_URL=http://localhost:8761/eureka/apps"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0verify-helpers.ps1" -Action EurekaCheck -Url "%EUREKA_APPS_URL%" -TableFile "%TABLE_FILE%"
if errorlevel 1 set "FAILED=1"

echo.
call :echo_header "3b) Actuator health — direct"
call :check_health_up "ms-candidate" "http://localhost:8081/actuator/health" "health:ms-candidate"
call :check_health_up "ms-job" "http://localhost:8082/actuator/health" "health:ms-job"
call :check_health_up "ms-application" "http://localhost:8083/actuator/health" "health:ms-application"
call :check_health_up "ms-interview" "http://localhost:8084/actuator/health" "health:ms-interview"
call :check_health_up "ms-notification" "http://localhost:8085/actuator/health" "health:ms-notification"
call :check_health_up "api-gateway" "http://localhost:8080/actuator/health" "health:api-gateway"

echo.
call :echo_header "3c) Actuator health — via API Gateway"
call :check_health_up "api-gateway" "http://localhost:8080/actuator/health" "gw-health:api-gateway"
call :check_health_up "ms-candidate" "http://localhost:8080/ms-candidate/actuator/health" "gw-health:ms-candidate"
call :check_health_up "ms-job" "http://localhost:8080/ms-job/actuator/health" "gw-health:ms-job"
call :check_health_up "ms-application" "http://localhost:8080/ms-application/actuator/health" "gw-health:ms-application"
call :check_health_up "ms-interview" "http://localhost:8080/ms-interview/actuator/health" "gw-health:ms-interview"
call :check_health_up "ms-notification" "http://localhost:8080/ms-notification/actuator/health" "gw-health:ms-notification"

echo.
call :echo_header "3d) Config Server and Keycloak"
call :check_health_up "config-server" "http://localhost:8888/actuator/health" "config-server"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0verify-helpers.ps1" -Action HttpOk -Url "http://localhost:8180" -Component "keycloak" -TableFile "%TABLE_FILE%"
if errorlevel 1 (
  call :fail "keycloak (http://localhost:8180)"
  set "FAILED=1"
) else (
  call :pass "keycloak"
)

echo.
call :echo_header "4) Datasource URL uniqueness (database-per-service)"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0verify-helpers.ps1" -Action DatasourceCheck -Backend "%BACKEND%" -TableFile "%TABLE_FILE%"
if errorlevel 1 set "FAILED=1"

echo.
call :echo_header "FINAL TABLE"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0verify-helpers.ps1" -Action PrintTable -TableFile "%TABLE_FILE%"

echo.
if "!FAILED!"=="0" (
  echo RESULT: PASS - all checks ok
  if exist "%TABLE_FILE%" del "%TABLE_FILE%" >nul 2>&1
  exit /b 0
) else (
  echo RESULT: FAIL - one or more checks failed
  if exist "%TABLE_FILE%" del "%TABLE_FILE%" >nul 2>&1
  exit /b 1
)

REM ---------- helpers ----------
:echo_header
echo === %~1 ===
exit /b 0

:pass
echo   PASS  %~1
exit /b 0

:fail
echo   FAIL  %~1
set "FAILED=1"
exit /b 0

:record
echo %~1^|%~2^|%~3>>"%TABLE_FILE%"
exit /b 0

:wait_url
set "WURL=%~1"
set "WLABEL=%~2"
echo   waiting for %WLABEL% (%WURL%)...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0verify-helpers.ps1" -Action WaitUrl -Url "%WURL%" -TimeoutSec %READY_TIMEOUT% -IntervalSec %READY_INTERVAL%
if errorlevel 1 (
  call :fail "timeout waiting for %WLABEL% (%WURL%)"
) else (
  call :pass "ready %WLABEL%"
)
exit /b 0

:check_health_up
set "HNAME=%~1"
set "HURL=%~2"
set "HCOMP=%~3"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0verify-helpers.ps1" -Action HealthUp -Url "%HURL%" -Component "%HCOMP%" -TableFile "%TABLE_FILE%"
if errorlevel 1 (
  call :fail "health %HNAME% (%HURL%)"
) else (
  call :pass "health %HNAME%"
)
exit /b 0
