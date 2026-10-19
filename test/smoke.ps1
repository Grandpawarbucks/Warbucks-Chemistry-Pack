# Smoke test (Windows port of smoke.sh): sync the pack, start the server on a fixed seed, wait for "Done"
# (5-minute timeout), stop it, collect logs, and print a pass/fail summary. The first run also downloads
# packwiz-installer-bootstrap and installs the NeoForge server into test\server.
#   powershell -ExecutionPolicy Bypass -File test\smoke.ps1                       fresh world each run
#   $env:KEEP_WORLD=1; powershell -ExecutionPolicy Bypass -File test\smoke.ps1    reuse the existing world
. "$PSScriptRoot\lib.ps1"

Write-Host '== Preparing test server =='
Initialize-TestServer

Write-Host '== Syncing pack =='
Sync-Pack
Initialize-ServerConfig
if ($env:KEEP_WORLD -ne '1') { Remove-Item (Join-Path $Server 'world') -Recurse -Force -ErrorAction SilentlyContinue }
Remove-Item (Join-Path $Server 'crash-reports'), (Join-Path $Server 'logs') -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "== Starting server (seed $Seed) =="
$t0 = [Diagnostics.Stopwatch]::StartNew()
$started = 0
try {
  Start-Server
  if (Wait-For 'Done \([0-9.]+s\)!' 300) { $started = 1 }
  $elapsed = [int]$t0.Elapsed.TotalSeconds
  if ($started) { Start-Sleep -Seconds $(if ($env:POST_DONE_WAIT) { [int]$env:POST_DONE_WAIT } else { 5 }) }
} finally {
  Stop-Server   # also on Ctrl+C or an error, so no server is left running
}

$out = Save-Logs 'smoke'
Write-Host "== Logs: $out =="
$env:PYTHONUTF8 = '1'   # logs are UTF-8; Windows Python would default to cp1252
& $Python (Join-Path $TestDir 'parse_logs.py') $out --started $started --elapsed $elapsed
exit $LASTEXITCODE
