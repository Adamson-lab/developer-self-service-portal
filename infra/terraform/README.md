# Terraform landing-zone composition

`main.tf` selects exactly one golden-path module per request using `var.template`. Each
module is created with `count`, so a request can never create resources from another template.

## Plan and apply (landing-zone runner only)

```powershell
cd infra\terraform
terraform init -input=false
terraform plan -input=false -var-file=<request_id>.auto.tfvars.json -out=tfplan
terraform apply -input=false tfplan
```

The API renders the tfvars file. Developers never run these commands directly.

## State

Remote state in an Azure storage account with blob lease locking. One state file per
landing zone, keyed by subscription. Encryption at rest with customer-managed keys.
