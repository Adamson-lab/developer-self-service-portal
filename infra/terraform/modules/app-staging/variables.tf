variable "request_id" { type = string }
variable "team" { type = string }
variable "environment" { type = string }
variable "owner" { type = string }
variable "monthly_budget_usd" { type = number }
variable "location" { type = string }
variable "tags" {
  type    = map(string)
  default = {}
}
