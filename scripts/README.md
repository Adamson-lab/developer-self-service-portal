# Scripts

| Script | Platform | Purpose |
|---|---|---|
| `run-local.ps1` | Windows PowerShell | Creates a virtual environment, installs dependencies and starts the API on port 8000 |
| `demo_requests.py` | Any (standard library) | Sends a demo sequence that triggers every control, then verifies the audit chain |
| `push-to-github.ps1` | Windows PowerShell | Creates the private GitHub repository with its description and pushes the first commit |
| `catalog_lint.py` | CI | Validates templates against the schema and cost ceilings against budgets |
| `crosscheck_policy.py` | CI | Runs example cases through the Python and Rego engines and fails on disagreement |

Scripts are short on purpose. Anything an auditor should read belongs in the Python or Rego source, not hidden in a script.
