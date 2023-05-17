output "random_name" {
  value = random_id.name.hex
}

output "resource_group_name" {
  value = azurerm_resource_group.this.name
}

output "vm_public_ip" {
  value = azurerm_public_ip.this.ip_address
}