output "storage_account_name" {
  description = "The name of the storage account"
  value       = azurerm_storage_account.this.name
}

output "primary_blob_endpoint" {
  description = "THe URI endpoint for the primaryu blob"
  value       = azurerm_storage_account.this.primary_blob_endpoint
}