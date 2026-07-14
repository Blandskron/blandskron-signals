$ErrorActionPreference = 'Stop'
$python = 'C:\Users\BlandskronNotebook\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $python -m compileall -q apps
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
git diff --check
Write-Output 'Python compilation and diff checks passed.'
