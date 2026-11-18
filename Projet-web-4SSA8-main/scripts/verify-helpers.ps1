param(
  [Parameter(Mandatory = $true)][ValidateSet('WaitUrl','HealthUp','HttpOk','EurekaCheck','DatasourceCheck','PrintTable')]
  [string]$Action,
  [string]$Url = '',
  [string]$Component = '',
  [string]$Backend = '',
  [string]$TableFile = '',
  [int]$TimeoutSec = 180,
  [int]$IntervalSec = 5
)

$ErrorActionPreference = 'Continue'

function Write-Record([string]$component, [string]$status, [string]$url) {
  if ($TableFile) {
    Add-Content -Path $TableFile -Value "$component|$status|$url"
  }
}

function Get-Http([string]$target, [int]$timeoutSec = 15, [hashtable]$Headers = $null) {
  try {
    $params = @{
      Uri = $target
      UseBasicParsing = $true
      TimeoutSec = $timeoutSec
    }
    if ($Headers) { $params.Headers = $Headers }
    $resp = Invoke-WebRequest @params
    return @{ Code = [int]$resp.StatusCode; Body = [string]$resp.Content }
  } catch {
    $code = 0
    $body = ''
    try {
      if ($_.Exception.Response) {
        $code = [int]$_.Exception.Response.StatusCode
        $stream = $_.Exception.Response.GetResponseStream()
        if ($stream) {
          $reader = New-Object System.IO.StreamReader($stream)
          $body = $reader.ReadToEnd()
          $reader.Close()
        }
      }
    } catch { }
    return @{ Code = $code; Body = $body }
  }
}

function Test-BodyUp([string]$body) {
  return $body -match '"status"\s*:\s*"UP"' -or $body -match '"status"\s*:\s*"up"'
}

switch ($Action) {
  'WaitUrl' {
    $deadline = (Get-Date).AddSeconds($TimeoutSec)
    while ((Get-Date) -lt $deadline) {
      $r = Get-Http $Url
      if ($r.Code -ge 200 -and $r.Code -lt 400) { exit 0 }
      Start-Sleep -Seconds $IntervalSec
    }
    exit 1
  }
  'HealthUp' {
    $r = Get-Http $Url -Headers @{ Accept = 'application/json' }
    if (Test-BodyUp $r.Body) {
      Write-Record $Component 'UP' $Url
      exit 0
    }
    Write-Record $Component 'FAIL' $Url
    exit 1
  }
  'HttpOk' {
    $r = Get-Http $Url
    if ($r.Code -ge 200 -and $r.Code -lt 400) {
      Write-Record $Component 'UP' $Url
      exit 0
    }
    Write-Record $Component 'FAIL' $Url
    exit 1
  }
  'EurekaCheck' {
    $expected = @('API-GATEWAY','MS-CANDIDATE','MS-JOB','MS-APPLICATION','MS-INTERVIEW')
    $failed = $false
    $xml = ''
    try {
      $resp = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 15 -Headers @{ Accept = 'application/xml' }
      $xml = [string]$resp.Content
    } catch {
      $xml = ''
    }
    foreach ($svc in $expected) {
      $ok = $false
      if ($xml) {
        $pattern = "(?is)<name>\s*$([regex]::Escape($svc))\s*</name>.*?<status>\s*UP\s*</status>"
        if ($xml -match $pattern) { $ok = $true }
      }
      if ($ok) {
        Write-Host "  PASS  Eureka $svc UP"
        Write-Record "eureka:$svc" 'UP' $Url
      } else {
        Write-Host "  FAIL  Eureka $svc not UP / not registered"
        Write-Record "eureka:$svc" 'FAIL' $Url
        $failed = $true
      }
    }
    if ($failed) { exit 1 } else { exit 0 }
  }
  'DatasourceCheck' {
    $owners = @{}
    $script:DupFound = $false

    function Add-Url([string]$owner, [string]$raw) {
      if (-not $raw) { return }
      $key = ($raw -split '\?')[0].Trim().ToLowerInvariant() -replace '\s',''
      if (-not $key) { return }
      if ($key -match 'jdbc:h2:|mem:') { return }
      if ($owners.ContainsKey($key)) {
        Write-Host "  FAIL  shared datasource: $owner and $($owners[$key]) -> $key"
        $script:DupFound = $true
      } else {
        $owners[$key] = $owner
      }
    }

    Get-ChildItem -Path (Join-Path $Backend 'ms-*') -Directory -ErrorAction SilentlyContinue | ForEach-Object {
      $svc = $_.Name
      $yml = Join-Path $_.FullName 'src\main\resources\application.yml'
      if (-not (Test-Path $yml)) { return }
      $text = Get-Content -Path $yml -Raw
      $default = ($text -split '(?m)^---\s*$')[0]
      foreach ($line in ($default -split "`n")) {
        if ($line -match '^\s*url:\s*(jdbc:\S+)') {
          Add-Url $svc $Matches[1].Trim('"').Trim("'")
        }
        if ($line -match '^\s*uri:\s*(mongodb:\S+)') {
          Add-Url $svc $Matches[1].Trim('"').Trim("'")
        }
      }
    }

    $compose = Join-Path $Backend 'docker-compose.yml'
    if (Test-Path $compose) {
      $current = ''
      foreach ($line in Get-Content $compose) {
        if ($line -match '^  ([a-z0-9-]+):\s*$') { $current = $Matches[1] }
        if ($line -match 'SPRING_DATASOURCE_URL:\s*(.+)$' -or $line -match 'SPRING_DATA_MONGODB_URI:\s*(.+)$') {
          Add-Url "compose:$current" $Matches[1].Trim().Trim('"').Trim("'")
        }
      }
    }

    if ($script:DupFound) {
      Write-Record 'datasource-isolation' 'FAIL' 'n/a'
      exit 1
    }
    Write-Host "  PASS  no shared datasource URLs ($($owners.Count) unique)"
    Write-Record 'datasource-isolation' 'PASS' 'n/a'
    exit 0
  }
  'PrintTable' {
    Write-Host ("{0,-28} | {1,-6} | {2}" -f 'component','status','URL')
    Write-Host ("{0,-28}-+-{1,-6}-+-{2}" -f ('-' * 28),('-' * 6),('-' * 32))
    if ($TableFile -and (Test-Path $TableFile)) {
      Get-Content $TableFile | ForEach-Object {
        $p = $_ -split '\|', 3
        if ($p.Count -ge 3) {
          Write-Host ("{0,-28} | {1,-6} | {2}" -f $p[0],$p[1],$p[2])
        }
      }
    }
    exit 0
  }
}
