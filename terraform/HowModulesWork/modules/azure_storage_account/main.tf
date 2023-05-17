locals {
  tags = {
    app = var.prefix
    env = var.environment
  }
}

# Generate random text for a unique name for the resources
resource "random_id" "this" {
  byte_length = 4
}

resource "azurerm_storage_account" "this" {
  name                      = "st${var.prefix}${var.environment}${lower(random_id.this.hex)}"
  resource_group_name       = var.resource_group_name
  location                  = var.resource_group_location
  tags                      = local.tags
  account_tier              = var.st_account_tier
  account_replication_type  = var.st_replication_type
  account_kind              = var.st_account_kind
  min_tls_version           = "TLS1_2"
  enable_https_traffic_only = true

  # The system-assigned managed identity for an Azure resource is used
  # to authenticate the resource when it needs to access other Azure 
  # services that support Azure Active Directory authentication.
  identity {
    type = "SystemAssigned"
  }
}