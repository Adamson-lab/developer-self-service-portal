import pytest

from core.catalog import load_catalog
from core.models import EnvRequest
from core.policy import can_approve, evaluate

CATALOG = load_catalog()


def req(**kw):
    base = dict(template="sandbox-web", team="web", requester="a@bank.example",
                environment="dev", estimated_monthly_usd=50)
    base.update(kw)
    return EnvRequest(**base)


def test_sandbox_auto_approved():  # G-01 not triggered, G-02/G-03 pass
    d = evaluate(req(), CATALOG["sandbox-web"])
    assert d.allowed and not d.needs_approval


def test_prod_always_needs_approval():  # G-01
    d = evaluate(req(template="payments-prod", team="payments", environment="prod",
                     estimated_monthly_usd=1000), CATALOG["payments-prod"])
    assert d.allowed and d.needs_approval


def test_cost_ceiling_rejects():  # G-02
    d = evaluate(req(estimated_monthly_usd=999), CATALOG["sandbox-web"])
    assert not d.allowed
    assert any("exceeds ceiling" in r for r in d.reasons)


def test_unentitled_team_rejected():  # G-03
    d = evaluate(req(template="payments-prod", team="marketing", environment="prod",
                     estimated_monthly_usd=100), CATALOG["payments-prod"])
    assert not d.allowed
    assert any("not entitled" in r for r in d.reasons)


def test_wrong_environment_rejected():  # catalog scoping
    d = evaluate(req(environment="prod"), CATALOG["sandbox-web"])
    assert not d.allowed


def test_staging_template_flags_no_approval_outside_prod():
    d = evaluate(req(template="app-staging", environment="staging", estimated_monthly_usd=800),
                 CATALOG["app-staging"])
    assert d.allowed and not d.needs_approval


@pytest.mark.parametrize("approver,requester,ok", [
    ("a@bank.example", "a@bank.example", False),   # G-06 self approval
    ("A@Bank.example ", "a@bank.example", False),  # normalisation
    ("cto@bank.example", "a@bank.example", True),
])
def test_segregation_of_duties(approver, requester, ok):  # G-06
    allowed, _ = can_approve(approver, requester)
    assert allowed is ok
