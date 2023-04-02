data "azurerm_client_config" "current" {}

data "azurerm_subnet" "this" {
  name                 = local.subnet_name
  virtual_network_name = local.vnet_name
  resource_group_name  = local.vnet_resource_group_name
}

data "azurerm_public_ip" "this" {
  name                = azurerm_public_ip.this.name
  resource_group_name = azurerm_resource_group.this.name
}

data "azurerm_key_vault_secret" "public_key_adminuser" {
  name         = azurerm_key_vault_secret.public_key_adminuser.name
  key_vault_id = azurerm_key_vault.this.id
}

data "azurerm_key_vault_secret" "public_key_appuser" {
  name         = azurerm_key_vault_secret.public_key_appuser.name
  key_vault_id = azurerm_key_vault.this.id
}
