# Creates the GitHub repository and pushes the first commit. Requires GitHub CLI (gh) and git.
# Run from the repository root in Windows PowerShell.
$ErrorActionPreference = "Stop"
$Owner       = "Adamson-lab"
$Repo        = "developer-self-service-portal"
$Description = "Policy-gated developer self-service environment portal: golden-path templates, approvals, segregation of duties and a tamper-evident audit trail for regulated enterprises"

git init -b main
git add .
git commit -m "feat: developer self-service environment portal, first complete build"
gh repo create "$Owner/$Repo" --private --description "$Description" --source . --remote origin --push
Write-Host "Pushed to https://github.com/$Owner/$Repo"
