[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$required = @(
    'AGENTS.md', 'README.md', '.gitignore',
    'docs/SPECIALIZATION.md', 'docs/UPGRADE.md', 'docs/TERMINOLOGY.md', 'tests/fixtures/v0.2-instance-lifecycle.md',
    'terminology/REGISTER.md', 'terminology/LOCAL_TERM_TEMPLATE.md',
    'project/CHARTER_TEMPLATE.md', 'project/DECISION_LOG_TEMPLATE.md',
    'hypotheses/REGISTER.md', 'hypotheses/HYPOTHESIS_TEMPLATE.md',
    'experiments/REGISTER.md', 'experiments/EXPERIMENT_TEMPLATE.md',
    'experiments/RUN_EVIDENCE_MANIFEST_TEMPLATE.yaml',
    'sources/REGISTER.md', 'sources/SOURCE_TEMPLATE.md',
    'research/RESEARCH_LOG_TEMPLATE.md', 'research/SYNTHESIS_TEMPLATE.md',
    'research/CONVERSATION_INGESTION.md', 'research/PRIOR_ART_WORKFLOW.md'
)

$failures = [System.Collections.Generic.List[string]]::new()
foreach ($relative in $required) {
    if (-not (Test-Path -LiteralPath (Join-Path $root $relative) -PathType Leaf)) {
        $failures.Add("Missing required template contract file: $relative")
    }
}

if ($failures.Count -eq 0) {
    $upgrade = Get-Content -LiteralPath (Join-Path $root 'docs/UPGRADE.md') -Raw
    $specialization = Get-Content -LiteralPath (Join-Path $root 'docs/SPECIALIZATION.md') -Raw
    $fixture = Get-Content -LiteralPath (Join-Path $root 'tests/fixtures/v0.2-instance-lifecycle.md') -Raw
    foreach ($term in @(
        'TEMPLATE_OWNED', 'INSTANCE_OWNED', 'INSTANCE_SPECIALIZED', 'BOOTSTRAP_ONLY',
        'PORT', 'ADAPT', 'SKIP', 'ALREADY_PRESENT',
        'Generated from', 'Last reviewed', 'Reconciled through'
    )) {
        if ($upgrade -notmatch [regex]::Escape($term)) { $failures.Add("Upgrade contract missing lifecycle term: $term") }
    }
    foreach ($term in @('TEMPLATE_BASELINE.md', 'TEMPLATE_UPGRADES.md', 'per-file ownership metadata')) {
        if ($specialization -notmatch [regex]::Escape($term)) { $failures.Add("Specialization contract missing lifecycle boundary: $term") }
    }
    foreach ($term in @('020fc7343e8bb7ec7182b3898c75ec7fc03ba447', 'OS-local temporary directory', 'Formal execution')) {
        if ($fixture -notmatch [regex]::Escape($term)) { $failures.Add("Synthetic scenario definition is incomplete: $term") }
    }
    if ($upgrade -notmatch 'JSON/YAML') { $failures.Add('Upgrade contract does not prohibit a machine-readable upgrade manifest.') }
    $termGuide = Get-Content -LiteralPath (Join-Path $root 'docs/TERMINOLOGY.md') -Raw
    $termForm = Get-Content -LiteralPath (Join-Path $root 'terminology/LOCAL_TERM_TEMPLATE.md') -Raw
    foreach ($term in @('project-local', 'Canonical Vault repository', 'Canonical Vault note', 'Canonical revision used', 'Promotion review')) {
        if ($term -notmatch 'project-local' -and $termForm -notmatch [regex]::Escape($term)) { $failures.Add("Local term form missing: $term") }
        if ($term -eq 'project-local' -and $termGuide -notmatch 'project-local') { $failures.Add('Terminology guide missing project-local authority.') }
    }
}

$ignore = Get-Content -LiteralPath (Join-Path $root '.gitignore') -Raw
foreach ($entry in @('/generated/', '/scratch/', 'research.local.toml', '.env', '*.pem', '*.key')) {
    if ($ignore -notmatch [regex]::Escape($entry)) { $failures.Add(".gitignore missing: $entry") }
}
foreach ($path in @('generated/validator-probe.txt', 'scratch/validator-probe.txt', 'research.local.toml', '.env', 'validator-probe.pem', 'validator-probe.key')) {
    git -C $root check-ignore --quiet -- $path
    if ($LASTEXITCODE -ne 0) { $failures.Add("Documented ignored path is not ignored: $path") }
}

$repositoryFiles = @(git -C $root ls-files) | Sort-Object -Unique
$large = $repositoryFiles | Where-Object { (Get-Item -LiteralPath (Join-Path $root $_)).Length -gt 1MB }
if ($large) { $failures.Add("Tracked file(s) exceed 1 MiB: $($large -join ', ')") }

$textFiles = $repositoryFiles | Where-Object { $_ -match '\.(md|ya?ml|ps1|txt)$' -or $_ -in @('README.md', 'AGENTS.md', '.gitignore') }
$contentFiles = $textFiles | Where-Object { $_ -ne 'tests/validate-template.ps1' }
$sensitive = '(?im)^\s*(?:[A-Z0-9_]*?(?:TOKEN|SECRET|PASSWORD|API_KEY)|aws_access_key_id)\s*[:=]\s*(?!<)(?!TBD)(?!none\b)(?!not-applicable\b).+'
$absolutePath = '(?im)(?:[A-Z]:\\Users\\|/home/[^/]+/|/Users/[^/]+/)'
$secretMarkers = @(
    '-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----',
    '\bAKIA[0-9A-Z]{16}\b',
    '\bghp_[A-Za-z0-9]{36}\b',
    '\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b'
)
foreach ($relative in $contentFiles) {
    $content = Get-Content -LiteralPath (Join-Path $root $relative) -Raw
    if ($content -match $sensitive) { $failures.Add("Possible credential assignment in: $relative") }
    if ($content -match $absolutePath) { $failures.Add("Private absolute path in: $relative") }
    foreach ($marker in $secretMarkers) {
        if ($content -match $marker) { $failures.Add("Possible secret material in: $relative") }
    }
}

$genericChecks = @(
    @{ File = 'README.md'; Pattern = 'Owner decision' },
    @{ File = 'README.md'; Pattern = 'assistant recommendation' },
    @{ File = 'research/CONVERSATION_INGESTION.md'; Pattern = 'raw chat transcript' },
    @{ File = 'research/PRIOR_ART_WORKFLOW.md'; Pattern = 'access limitations' },
    @{ File = 'experiments/RUN_EVIDENCE_MANIFEST_TEMPLATE.yaml'; Pattern = 'interpretation_boundary' }
)
foreach ($check in $genericChecks) {
    if ((Get-Content -LiteralPath (Join-Path $root $check.File) -Raw) -notmatch $check.Pattern) {
        $failures.Add("Required generic safety wording missing: $($check.File) [$($check.Pattern)]")
    }
}

if ($failures.Count) {
    $failures | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Output "PASS: $($required.Count) required contract files; ignored boundaries, public-safety scan, size scan, and generic-state checks passed."
