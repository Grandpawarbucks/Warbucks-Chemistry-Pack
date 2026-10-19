# Shared helpers for the PowerShell test scripts (Windows port of lib.sh). Dot-source this file; don't run it.
# Works in Windows PowerShell 5.1 and PowerShell 7.
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$TestDir = $PSScriptRoot
$Root = Split-Path $TestDir
$Server = Join-Path $TestDir 'server'
$Pack = Join-Path $Root 'pack'
$Port = if ($env:PACKWIZ_PORT) { [int]$env:PACKWIZ_PORT } else { 8099 }
$Seed = if ($env:SEED) { $env:SEED } else { '20261018' }
$Bootstrap = Join-Path $TestDir 'packwiz-installer-bootstrap.jar'
$BootstrapUrl = 'https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar'

# Java 21: $JAVA_HOME (process, then machine), then any Temurin 21. Never the `java` on PATH,
# which can be an old Oracle Java 8 shim on Windows.
function Find-Java {
  $cands = @($env:JAVA_HOME, [Environment]::GetEnvironmentVariable('JAVA_HOME', 'Machine')) +
           @(Get-ChildItem 'C:\Program Files\Eclipse Adoptium\jdk-21*' -Directory -ErrorAction SilentlyContinue | ForEach-Object FullName)
  foreach ($c in $cands) {
    if ($c -and (Test-Path (Join-Path $c 'bin\java.exe'))) { return (Join-Path $c 'bin\java.exe') }
  }
  throw 'Java 21 not found (set JAVA_HOME or install EclipseAdoptium.Temurin.21.JDK)'
}
$Java = Find-Java

$Packwiz = if ($env:PACKWIZ) { $env:PACKWIZ }
           elseif (Get-Command packwiz -ErrorAction SilentlyContinue) { (Get-Command packwiz).Source }
           else { Join-Path $env:USERPROFILE 'go\bin\packwiz.exe' }
$Python = if (Test-Path (Join-Path $Root '.venv\Scripts\python.exe')) { Join-Path $Root '.venv\Scripts\python.exe' } else { 'python' }
$NeoForge = ((Get-Content (Join-Path $Pack 'pack.toml')) -match '^neoforge = ' -replace '^neoforge = "([^"]+)".*', '$1') | Select-Object -First 1

# Quote arguments for ProcessStartInfo (paths here contain spaces, e.g. "Chem Modpack Dev").
function Join-Args([string[]]$ArgList) {
  ($ArgList | ForEach-Object { if ($_ -match '[\s"]') { '"' + ($_ -replace '"', '\"') + '"' } else { $_ } }) -join ' '
}

# Run a program and wait. Output goes to the console, or to $Log if given. Returns the exit code.
function Invoke-Tool([string]$Exe, [string[]]$ArgList, [string]$Dir, [string]$Log) {
  $psi = New-Object Diagnostics.ProcessStartInfo $Exe, (Join-Args $ArgList)
  $psi.WorkingDirectory = $Dir
  $psi.UseShellExecute = $false
  if ($Log) { $psi.RedirectStandardOutput = $true; $psi.RedirectStandardError = $true }
  $p = [Diagnostics.Process]::Start($psi)
  if ($Log) { $o = $p.StandardOutput.ReadToEndAsync(); $e = $p.StandardError.ReadToEndAsync() }
  $p.WaitForExit()
  if ($Log) { [IO.File]::WriteAllText($Log, $o.Result + $e.Result) }
  $p.ExitCode
}

# Start "cmd /c <command line>" in the background (so it can redirect to files). Returns the Process.
function Start-Cmd([string]$CommandLine, [string]$Dir, [switch]$Stdin) {
  $psi = New-Object Diagnostics.ProcessStartInfo 'cmd.exe', ('/d /s /c "' + $CommandLine + '"')
  $psi.WorkingDirectory = $Dir
  $psi.UseShellExecute = $false
  $psi.RedirectStandardInput = [bool]$Stdin
  [Diagnostics.Process]::Start($psi)
}

function Stop-Tree($Proc) {
  if ($Proc -and -not $Proc.HasExited) { & taskkill.exe /T /F /PID $Proc.Id 2>&1 | Out-Null }
}

function Read-Shared([string]$Path) {
  try {
    $fs = [IO.File]::Open($Path, 'Open', 'Read', 'ReadWrite')
    try { (New-Object IO.StreamReader $fs).ReadToEnd() } finally { $fs.Dispose() }
  } catch { '' }
}

# First run only: download packwiz-installer-bootstrap and install the NeoForge server the pack wants
# (same sources as server/install.sh and server/start.sh).
function Initialize-TestServer {
  New-Item -ItemType Directory -Force $Server | Out-Null
  if (-not (Test-Path $Bootstrap)) {
    Write-Host "Downloading packwiz-installer-bootstrap v0.0.3"
    Invoke-WebRequest -UseBasicParsing $BootstrapUrl -OutFile $Bootstrap
  }
  if (-not (Test-Path (Join-Path $Server "libraries\net\neoforged\neoforge\$NeoForge\win_args.txt"))) {
    Write-Host "Installing NeoForge $NeoForge server (log: test\server\neoforge-install.log)"
    $jar = Join-Path $Server 'neoforge-installer.jar'
    Invoke-WebRequest -UseBasicParsing "https://maven.neoforged.net/releases/net/neoforged/neoforge/$NeoForge/neoforge-$NeoForge-installer.jar" -OutFile $jar
    $code = Invoke-Tool $Java @('-jar', $jar, '--installServer') $Server (Join-Path $Server 'neoforge-install.log')
    Remove-Item $jar -Force
    if ($code -ne 0) { throw "NeoForge install failed (exit $code), see test\server\neoforge-install.log" }
  }
}

# Serve the packwiz pack over HTTP and install it into the test server.
function Sync-Pack {
  # packwiz cf/mr add can pull in a dependency that is already in the pack from the
  # other site. Two entries for one jar confuse packwiz-installer, so fail early.
  $dupes = Select-String -Path (Join-Path $Pack 'mods\*.pw.toml') -Pattern '^filename' |
           ForEach-Object Line | Group-Object | Where-Object Count -gt 1 | ForEach-Object Name
  if ($dupes) { throw "Duplicate mod files in pack: $($dupes -join ', ')" }
  $code = Invoke-Tool $Packwiz @('refresh') $Pack (Join-Path $Server 'packwiz-refresh.log')
  if ($code -ne 0) { throw "packwiz refresh failed (exit $code), see test\server\packwiz-refresh.log" }
  $serve = Start-Cmd ((Join-Args @($Packwiz, 'serve', '--port', "$Port")) + ' >nul 2>&1') $Pack
  try {
    for ($i = 0; $i -lt 20; $i++) {
      try { Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 "http://localhost:$Port/pack.toml" | Out-Null; break } catch { Start-Sleep -Milliseconds 500 }
    }
    $code = Invoke-Tool $Java @('-jar', $Bootstrap, '-g', '-s', 'server', "http://localhost:$Port/pack.toml") $Server
    if ($code -ne 0) { throw "packwiz-installer failed (exit $code)" }
  } finally { Stop-Tree $serve }
}

# Write server settings: EULA (test folder only), fixed seed, offline local server.
function Initialize-ServerConfig {
  $utf8 = New-Object Text.UTF8Encoding $false
  [IO.File]::WriteAllText((Join-Path $Server 'eula.txt'), "eula=true`n", $utf8)
  $props = Join-Path $Server 'server.properties'
  $lines = New-Object Collections.Generic.List[string]
  if (Test-Path $props) { $lines.AddRange([string[]](Get-Content $props)) }
  $set = [ordered]@{
    'level-seed' = $Seed; 'level-name' = 'world'; 'online-mode' = 'false'; 'server-ip' = '127.0.0.1'
    'spawn-protection' = '0'; 'view-distance' = '6'
    'allow-flight' = 'true'  # as on the real server (server/server.properties)
  }
  foreach ($k in $set.Keys) {
    $i = $lines.FindIndex({ param($l) $l.StartsWith("$k=") })
    if ($i -ge 0) { $lines[$i] = "$k=$($set[$k])" } else { $lines.Add("$k=$($set[$k])") }
  }
  [IO.File]::WriteAllLines($props, $lines, $utf8)
  # Use the pack's JVM args (from docs/README.md) for the test server too.
  Copy-Item (Join-Path $TestDir 'jvm_args.txt') (Join-Path $Server 'user_jvm_args.txt') -Force
}

# Start the server with stdin on a pipe and output in test\server\console.out. Write to it with Send.
function Start-Server {
  $argFile = "libraries/net/neoforged/neoforge/$NeoForge/win_args.txt"
  $script:ServerProc = Start-Cmd ((Join-Args @($Java, '@user_jvm_args.txt', "@$argFile", 'nogui')) + ' > console.out 2>&1') $Server -Stdin
  $script:ServerProc.StandardInput.AutoFlush = $true
}
function Send([string]$Line) {
  try { $script:ServerProc.StandardInput.WriteLine($Line) } catch { }
}

# Wait until a regex shows up in console output. Returns $false on timeout or server exit.
function Wait-For([string]$Pattern, [int]$Timeout) {
  $sw = [Diagnostics.Stopwatch]::StartNew()
  $log = Join-Path $Server 'console.out'
  while ($sw.Elapsed.TotalSeconds -lt $Timeout) {
    if ((Read-Shared $log) -match $Pattern) { return $true }
    if ($script:ServerProc.HasExited) { return $false }
    Start-Sleep -Seconds 2
  }
  $false
}

function Stop-Server {
  if (-not $script:ServerProc) { return }
  Send 'stop'
  for ($i = 0; $i -lt 60 -and -not $script:ServerProc.HasExited; $i++) { Start-Sleep -Seconds 1 }
  Stop-Tree $script:ServerProc
  try { $script:ServerProc.StandardInput.Close() } catch { }
  $script:ServerProc = $null
}

# Copy logs and crash reports into test\results\<label>-<timestamp>. Returns the folder.
function Save-Logs([string]$Label) {
  $out = Join-Path $TestDir "results\$Label-$(Get-Date -Format yyyyMMdd-HHmmss)"
  New-Item -ItemType Directory -Force $out | Out-Null
  foreach ($f in 'console.out', 'logs\latest.log', 'logs\debug.log') {
    $p = Join-Path $Server $f
    if (Test-Path $p) { Copy-Item $p $out }
  }
  foreach ($d in 'logs\kubejs', 'crash-reports') {
    $p = Join-Path $Server $d
    if (Test-Path $p) { Copy-Item $p $out -Recurse }
  }
  $out
}
