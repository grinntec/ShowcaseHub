module "storage_account" {
  source  = "../../modules/azure_storage_account/"
  # insert required variables here
  prefix                  = local.prefix
  resource_group_name     = module.resource_group.resource_group_name
  resource_group_location = module.resource_group.resource_group_location
  environment             = local.environment
  st_account_tier         = "Standard"
  st_replication_type     = "LRS"
  st_account_kind         = "StorageV2"
}

output "storage_account_name" {
  description = "The name of the storage account"
  value       = module.storage_account.storage_account_name
}

output "primary_blob_endpoint" {
  description = "THe URI endpoint for the primaryu blob"
  value       = module.storage_account.primary_blob_endpoint
}
