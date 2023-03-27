# terraform-azurerm-resource_group
This Terraform code creates an Azure Resource Group with a name composed of the provided prefix and environment variables, and applies the tags defined in the locals block. The azurerm_resource_group resource creates the resource group with the specified name and location, and applies the tags.

The prefix, environment, and resource_group_location variables need to be defined before using this code. The locals block defines a map of tags with keys "app" and "env", and their values taken from the corresponding variables.
<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_azurerm"></a> [azurerm](#provider\_azurerm) | 3.47.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [azurerm_resource_group.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/resource_group) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_environment"></a> [environment](#input\_environment) | (Required) Describe the environment type<br><br>  Options:<br>  - dev<br>  - test<br>  - prod | `string` | n/a | yes |
| <a name="input_prefix"></a> [prefix](#input\_prefix) | (Required) Name of the workload | `string` | n/a | yes |
| <a name="input_resource_group_location"></a> [resource\_group\_location](#input\_resource\_group\_location) | (Required) Location of the resource group where the workload will be managed<br><br>  Options:<br>  - westeurope; west europe<br>  - eastus; east us<br>  - southeastasia; south east asia | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_resource_group_location"></a> [resource\_group\_location](#output\_resource\_group\_location) | The location of the resource group |
| <a name="output_resource_group_name"></a> [resource\_group\_name](#output\_resource\_group\_name) | The name of the resource group |
<!-- END_TF_DOCS -->