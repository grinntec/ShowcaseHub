locals {
  tags = {
    app = var.prefix
    env = var.environment
  }
}

resource "azurerm_resource_group" "this" {
  name     = "rg-${var.prefix}-${var.environment}"
  location = var.resource_group_location
  tags     = local.tags
}