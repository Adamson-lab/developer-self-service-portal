"""Loads golden-path templates from catalog/templates.yaml and validates their shape.

A template that fails validation stops the API from starting. Shadow IT is blocked
at the source: if a template is not in the reviewed catalog, it cannot be requested.
"""
from pathlib import Path

import yaml

# services/api/core/catalog.py -> repository root is parents[3]
CATALOG_PATH = Path(__file__).resolve().parents[3] / "catalog" / "templates.yaml"

REQUIRED_KEYS = {
    "title", "description", "environments", "allowed_teams",
    "max_monthly_usd", "approval_required", "iac_module",
}
ALLOWED_ENVIRONMENTS = {"dev", "staging", "prod"}


class CatalogError(ValueError):
    pass


def validate(name: str, tpl: dict) -> None:
    missing = REQUIRED_KEYS - tpl.keys()
    if missing:
        raise CatalogError(f"template '{name}' is missing keys: {sorted(missing)}")
    bad_env = set(tpl["environments"]) - ALLOWED_ENVIRONMENTS
    if bad_env:
        raise CatalogError(f"template '{name}' has unknown environments: {sorted(bad_env)}")
    if tpl["max_monthly_usd"] <= 0:
        raise CatalogError(f"template '{name}' must have a positive cost ceiling")


def load_catalog(path: Path = CATALOG_PATH) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    templates = data["templates"]
    for name, tpl in templates.items():
        validate(name, tpl)
    return templates
