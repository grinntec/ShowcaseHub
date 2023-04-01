terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }

  required_version = ">= 1.1.0"

}

provider "azurerm" {
  features {}
}

locals {
  prefix                   = "project00"
  location                 = "west europe"
  subnet_name              = "subnet01"
  vnet_name                = "vnet01"
  vnet_resource_group_name = "rg-network"
}

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

resource "azurerm_resource_group" "this" {
  name     = "rg-${local.prefix}"
  location = local.location
}

# Generate a 4 character long random string used for the unique name
# of resources
resource "random_id" "name" {
  byte_length = 2
}
# Generate a 12 character long random string for the password
resource "random_password" "this" {
  length  = 16
  special = true
}

# Create public IP address
resource "azurerm_public_ip" "this" {
  name                = "pip-${local.prefix}-${lower(random_id.name.hex)}"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  allocation_method   = "Dynamic"
}

# Create a network interface card and assign an IP from the subnet
# set from the data block
resource "azurerm_network_interface" "this" {
  name                = "nic-${local.prefix}-${lower(random_id.name.hex)}"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location

  ip_configuration {
    name                          = "internal"
    subnet_id                     = data.azurerm_subnet.this.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.this.id
  }
}

resource "azurerm_linux_virtual_machine" "this" {
  name                = "vm-${local.prefix}-${lower(random_id.name.hex)}"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  size                = "Standard_B1s"

  admin_username                  = "adminuser"
  admin_password                  = random_password.this.result
  disable_password_authentication = false

  os_disk {
    name                 = "osdisk"
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  network_interface_ids = [azurerm_network_interface.this.id]

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}

output "random_name" {
  value = random_id.name.hex
}

output "admin_password" {
  value = nonsensitive(random_password.this.result)
}

output "resource_group_name" {
  value = azurerm_resource_group.this.name
}

output "vm_public_ip" {
  value = azurerm_public_ip.this.ip_address
}