locals {
  prefix                   = "project00"
  location                 = "west europe"
  subnet_name              = "subnet01"
  vnet_name                = "vnet01"
  vnet_resource_group_name = "rg-network"
  vm_name                  = "vm-${local.prefix}-${lower(random_id.name.hex)}"
  appuser_object_id        = "sdgashsgæasdsfjijasdfijsadf"
}