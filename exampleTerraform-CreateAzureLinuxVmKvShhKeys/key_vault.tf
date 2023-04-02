resource "azurerm_key_vault" "this" {
  name                     = "kv-${local.prefix}-${lower(random_id.name.hex)}"
  location                 = azurerm_resource_group.this.location
  resource_group_name      = azurerm_resource_group.this.name
  tenant_id                = data.azurerm_client_config.current.tenant_id
  sku_name                 = "standard"
  purge_protection_enabled = false
}

resource "azurerm_key_vault_access_policy" "terraformspn" {
  key_vault_id = azurerm_key_vault.this.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id

  secret_permissions      = ["Get", "Set", "List", "Delete"]
  key_permissions         = []
  certificate_permissions = []

  depends_on = [
    azurerm_key_vault.this
  ]
}

resource "azurerm_key_vault_access_policy" "appuser" {
  key_vault_id = azurerm_key_vault.this.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = local.appuser_object_id

  secret_permissions      = ["Get", "Set", "List", "Delete"]
  key_permissions         = []
  certificate_permissions = []

  depends_on = [
    azurerm_key_vault.this
  ]
}

resource "tls_private_key" "adminuser" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "tls_private_key" "appuser" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

# When using SSH key pairs, the public key should be in OpenSSH format, and the private key 
# should be in PEM format.

resource "azurerm_key_vault_secret" "private_key_adminuser" {
  name         = "${local.vm_name}-adminuser-private-key"
  value        = tls_private_key.adminuser.private_key_pem
  key_vault_id = azurerm_key_vault.this.id

  depends_on = [
    azurerm_key_vault_access_policy.terraformspn
  ]
}

resource "azurerm_key_vault_secret" "public_key_adminuser" {
  name         = "${local.vm_name}-adminuser-public-key"
  value        = tls_private_key.adminuser.public_key_openssh
  key_vault_id = azurerm_key_vault.this.id

  depends_on = [
    azurerm_key_vault_access_policy.terraformspn
  ]
}

resource "azurerm_key_vault_secret" "private_key_appuser" {
  name         = "${local.vm_name}-appuser-private-key"
  value        = tls_private_key.appuser.private_key_pem
  key_vault_id = azurerm_key_vault.this.id

  depends_on = [
    azurerm_key_vault_access_policy.terraformspn
  ]
}

resource "azurerm_key_vault_secret" "public_key_appuser" {
  name         = "${local.vm_name}-appuser-public-key"
  value        = tls_private_key.appuser.public_key_openssh
  key_vault_id = azurerm_key_vault.this.id

  depends_on = [
    azurerm_key_vault_access_policy.terraformspn
  ]
}

