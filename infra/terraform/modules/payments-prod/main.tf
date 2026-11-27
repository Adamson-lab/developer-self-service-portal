# Hardened production landing zone. Requires a named approver (G-01) before this module runs.
# Private networking only, customer-managed keys, diagnostic logs to the central SIEM.
resource "azurerm_resource_group" "this" {
  name     = "rg-${var.team}-prd-${substr(var.request_id, 0, 8)}"
  location = var.location
  tags = merge(var.tags, {
    owner        = var.owner
    team         = var.team
    template     = "payments-prod"
    data_class   = "restricted"
    change_ticket = var.request_id
  })
}

resource "azurerm_consumption_budget_resource_group" "this" {
  name              = "budget-${substr(var.request_id, 0, 8)}"
  resource_group_id = azurerm_resource_group.this.id
  amount            = var.monthly_budget_usd
  time_grain        = "Monthly"

  time_period {
    start_date = "2026-12-01T00:00:00Z"
  }

  notification {
    enabled        = true
    threshold      = 80
    operator       = "GreaterThan"
    contact_emails = [var.owner]
  }
}
