# Recipe + registry dump for tools/quest_audit.py --full. Runs the normal smoke test once with the dump marker
# set, so pack/kubejs/server_scripts/zz_recipe_dump.js writes every recipe (after all KubeJS changes) and the
# item/entity/biome/structure/dimension registries. The marker lives in test\server only (never in pack\) and is
# removed again afterwards, so the dump script ships inactive.
#   powershell -NoProfile -ExecutionPolicy Bypass -File test\audit_dump.ps1
# Output: test\dump\recipe_dump.json, test\dump\registry_dump.json (git-ignored, like the rest of test\).
# Must run from a real terminal (or the Claude app's Terminal panel): Java can't open loopback sockets in Claude's shell.
$ErrorActionPreference = 'Stop'
$TestDir = $PSScriptRoot
$Cfg = Join-Path $TestDir 'server\kubejs\config'
$Marker = Join-Path $Cfg 'dump_recipes.json'
$DumpDir = Join-Path $TestDir 'dump'
New-Item -ItemType Directory -Force $Cfg, $DumpDir | Out-Null
foreach ($f in 'recipe_dump.json', 'registry_dump.json') { Remove-Item (Join-Path $Cfg $f) -Force -ErrorAction SilentlyContinue }
[IO.File]::WriteAllText($Marker, '{"dump": true}')
if (-not $env:KEEP_WORLD) { $env:KEEP_WORLD = '1' }   # recipes load on every start; no need for a fresh world
try {
  & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $TestDir 'smoke.ps1')
  $code = $LASTEXITCODE
} finally {
  Remove-Item $Marker -Force -ErrorAction SilentlyContinue
}
$ok = $true
foreach ($f in 'recipe_dump.json', 'registry_dump.json') {
  $src = Join-Path $Cfg $f
  if (Test-Path $src) { Move-Item $src (Join-Path $DumpDir $f) -Force; Write-Host "Dump: test\dump\$f" }
  else { Write-Host "MISSING: $f (check the kubejs server log for [recipe_dump])"; $ok = $false }
}
if (-not $ok) { exit 1 }
exit $code
