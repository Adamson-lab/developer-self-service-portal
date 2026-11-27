"""CI check: every template validates against the JSON Schema, and cost ceilings match cost/budgets.json.

Exit code 1 on any failure so the pipeline blocks the merge.
"""
import json
import sys
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    templates = yaml.safe_load((ROOT / "catalog" / "templates.yaml").read_text())["templates"]
    schema = json.loads((ROOT / "catalog" / "schemas" / "template.schema.json").read_text())
    budgets = json.loads((ROOT / "cost" / "budgets.json").read_text())["ceilings"]
    errors: list[str] = []

    for name, tpl in templates.items():
        try:
            jsonschema.validate(tpl, schema)
        except jsonschema.ValidationError as exc:
            errors.append(f"{name}: schema violation: {exc.message}")
        for env in tpl["environments"]:
            ceiling = budgets.get(name, {}).get(env)
            if ceiling != tpl["max_monthly_usd"]:
                errors.append(f"{name}/{env}: cost ceiling {tpl['max_monthly_usd']} differs from budgets.json ({ceiling})")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"catalog ok: {len(templates)} templates validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
