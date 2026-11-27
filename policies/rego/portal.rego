# OPA/Rego mirror of core/policy.py. Used in CI to prove both engines agree on every example.
package portal.decision

import rego.v1

default allow := false

default needs_approval := false

allow if {
    count(violations) == 0
}

violations contains msg if {
    not environment_offered
    msg := sprintf("template '%s' is not offered in %s", [input.template.name, input.request.environment])
}

violations contains msg if {
    not team_entitled
    msg := sprintf("team '%s' is not entitled to this template", [input.request.team])
}

violations contains msg if {
    input.request.estimated_monthly_usd > input.template.max_monthly_usd
    msg := "estimated cost exceeds template ceiling (G-02)"
}

environment_offered if {
    input.request.environment in input.template.environments
}

team_entitled if {
    "any" in input.template.allowed_teams
}

team_entitled if {
    input.request.team in input.template.allowed_teams
}

needs_approval if {
    input.template.approval_required
}

needs_approval if {
    input.request.environment == "prod"
}

decision := {"allowed": allow, "needs_approval": needs_approval, "reasons": [v | some v in violations]}
