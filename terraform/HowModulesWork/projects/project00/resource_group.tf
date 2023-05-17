module "resource_group" {
  source = "../../modules/azure_resource_group/"
  # insert required variables here
  prefix                  = local.prefix
  resource_group_location = local.location
  environment             = local.environment
}

output "resource_group_name" {
  description = "The name of the resource group"
  value       = module.resource_group.resource_group_name
}

output "resource_group_location" {
  description = "The location of the resource group"
  value       = module.resource_group.resource_group_location
}