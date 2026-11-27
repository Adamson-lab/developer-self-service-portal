terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
}

variable "template" {
  type        = string
  description = "Golden-path template name. Must match a module below."
  validation {
    condition     = contains(["sandbox-web", "app-staging", "payments-prod"], var.template)
    error_message = "template must be one of the catalogued golden paths."
  }
}

variable "request_id" { type = string }
variable "team" { type = string }
variable "environment" { type = string }
variable "owner" { type = string }
variable "monthly_budget_usd" { type = number }
variable "justification" {
  type    = string
  default = ""
}
variable "location" {
  type    = string
  default = "westeurope"
}
variable "tags" {
  type    = map(string)
  default = {}
}

module "sandbox_web" {
  count              = var.template == "sandbox-web" ? 1 : 0
  source             = "./modules/sandbox-web"
  request_id         = var.request_id
  team               = var.team
  environment        = var.environment
  owner              = var.owner
  monthly_budget_usd = var.monthly_budget_usd
  location           = var.location
  tags               = var.tags
}

module "app_staging" {
  count              = var.template == "app-staging" ? 1 : 0
  source             = "./modules/app-staging"
  request_id         = var.request_id
  team               = var.team
  environment        = var.environment
  owner              = var.owner
  monthly_budget_usd = var.monthly_budget_usd
  location           = var.location
  tags               = var.tags
}

module "payments_prod" {
  count              = var.template == "payments-prod" ? 1 : 0
  source             = "./modules/payments-prod"
  request_id         = var.request_id
  team               = var.team
  environment        = var.environment
  owner              = var.owner
  monthly_budget_usd = var.monthly_budget_usd
  location           = var.location
  tags               = var.tags
}

output "resource_group" {
  value = coalesce(
    try(module.sandbox_web[0].resource_group_name, null),
    try(module.app_staging[0].resource_group_name, null),
    try(module.payments_prod[0].resource_group_name, null),
  )
}
