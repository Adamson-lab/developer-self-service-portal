# Tests

| Folder | Scope | Speed |
|---|---|---|
| `unit/` | Policy rules, audit chain, catalog validation | Under one second |
| `integration/` | HTTP API through FastAPI's test client, end to end | A few seconds |

Run everything from the repository root:

```powershell
pip install -r services\api\requirements.txt
pytest -q
```

`conftest.py` sets the import path so tests use the same packages as the running service.
