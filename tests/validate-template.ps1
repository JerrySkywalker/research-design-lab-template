[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$required = @(
    'AGENTS.md', 'README.md', '.gitignore',
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

$ignore = Get-Content -LiteralPath (Join-Path $root '.gitignore') -Raw
foreach ($entry in @('/generated/', '/scratch/', 'research.local.toml', '.env', '*.pem', '*.key')) {
    if ($ignore -notmatch [regex]::Escape($entry)) { $failures.Add(".gitignore missing: $entry") }
}

$repositoryFiles = @(git -C $root ls-files; git -C $root ls-files --others --exclude-standard) | Sort-Object -Unique
$large = $repositoryFiles | Where-Object { (Get-Item -LiteralPath (Join-Path $root $_)).Length -gt 1MB }
if ($large) { $failures.Add("Tracked file(s) exceed 1 MiB: $($large -join ', ')") }

$textFiles = $repositoryFiles | Where-Object { $_ -match '\.(md|ya?ml|ps1|txt)$' -or $_ -in @('README.md', 'AGENTS.md', '.gitignore') }
$contentFiles = $textFiles | Where-Object { $_ -ne 'tests/validate-template.ps1' }
$sensitive = '(?im)^\s*(?:[A-Z0-9_]*?(?:TOKEN|SECRET|PASSWORD|API_KEY)|aws_access_key_id)\s*[:=]\s*(?!<)(?!TBD)(?!none\b)(?!not-applicable\b).+'
$absolutePath = '(?im)(?:[A-Z]:\\Users\\|/home/[^/]+/|/Users/[^/]+/)'
foreach ($relative in $contentFiles) {
    $content = Get-Content -LiteralPath (Join-Path $root $relative) -Raw
    if ($content -match $sensitive) { $failures.Add("Possible credential assignment in: $relative") }
    if ($content -match $absolutePath) { $failures.Add("Private absolute path in: $relative") }
}

$genericTemplateText = ($contentFiles | ForEach-Object { Get-Content -LiteralPath (Join-Path $root $_) -Raw }) -join "`n"
foreach ($forbiddenTopic in @('ai-satellite', 'cislunar transport', 'satellite payload', 'spacecraft mass')) {
    if ($genericTemplateText -match [regex]::Escape($forbiddenTopic)) {
        $failures.Add("Generic template includes a domain-specific selected-design topic: $forbiddenTopic")
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
