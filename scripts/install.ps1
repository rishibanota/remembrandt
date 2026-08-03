# Install the remembrandt CLI and register it as a Claude Code skill (Windows).
# Usage:  powershell -ExecutionPolicy Bypass -File scripts/install.ps1
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

Write-Host ">> Installing remembrandt CLI..."
if (Get-Command pip -ErrorAction SilentlyContinue) {
    pip install -e $Root
} else {
    Write-Warning "pip not found. Install Python 3 and retry."
}

$SkillsDir = if ($env:CLAUDE_SKILLS_DIR) { $env:CLAUDE_SKILLS_DIR } else { Join-Path $HOME ".claude\skills" }
$Target = Join-Path $SkillsDir "remembrandt"
if (Test-Path (Join-Path $Root "SKILL.md")) {
    New-Item -ItemType Directory -Force -Path $Target | Out-Null
    Copy-Item (Join-Path $Root "SKILL.md") (Join-Path $Target "SKILL.md") -Force
    Write-Host ">> Claude Code skill installed at $Target"
}

Write-Host ">> Done. Try:  remembrandt remember 'hello world'; remembrandt recall"
