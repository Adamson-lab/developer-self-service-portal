# Staging mirrors production topology at reduced scale: separate RG, budget, and a
# lifecycle tag so the reaper can expire it (see lifecycle/).
resource "azurerm_resource_group" "this" {
  name     = "rg-${var.team}-stg-${substr(var.request_id, 0, 8)}"
  location = var.location
  tags = merge(var.tags, {
    owner     = var.owner
    team      = var.team
    template  = "app-staging"
    expires   = "30d"
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
