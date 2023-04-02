resource "azurerm_resource_group" "this" {
  name     = "rg-${local.prefix}"
  location = local.location
}