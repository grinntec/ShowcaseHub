# exampleTerraform-AzureNetworkSecurityGroup
This is a Terraform configuration file written in HashiCorp Configuration Language (HCL) that uses the Azure provider to create and configure a network security group (NSG) with rules in Azure.

The code begins by declaring the Azure provider and its version requirements, followed by a definition for the provider configuration.

The configuration also defines a local variable called nsg_rules which reads a CSV file containing NSG rules specified by the nsg_ruleset variable. The CSV file is decoded using the csvdecode function, and the replace function is used to remove any byte-order mark (BOM) character that may be present at the beginning of the file.

Next, the configuration creates an Azure resource group, followed by a network security group within that resource group. The NSG is given a name of "nsg-example".

Finally, the configuration creates NSG rules based on the contents of the CSV file specified by nsg_ruleset. The for_each meta-argument is used to create one rule per row in the CSV file. Each rule is defined by the properties in the resource block, including its priority, direction, source and destination port and IP address ranges, protocol, and access. The values for these properties are obtained from the corresponding columns in the CSV file using the each.value syntax. The name of each rule is constructed from its priority and direction, and a description can also be provided.

Overall, this configuration creates a network security group with rules in Azure that can be maintained and modified by updating the CSV file.

## How to edit and create the NSG ruleset
This Terraform code relies on a CSV being imported to manage the ruleset. Terraform is very sensitive to error so it's ultra-important that the CSV file is true and correct. There is an Excel macro file that can aid in the creation of the CSV file. The file is called `nsg.editor.xlsm`. To use this file simple open it in Excel and edit the `EditRules` worksheet as described below. To generate the CSV version of the rulest use the button on the worksheet named `Export Rules` which will output your data into CSV UTF-8 format and ask you to save the file. I suggest you keep both the macro and CSV files in the working directory as the Terraform code is looking for a file in the working directory and you'll likely need to add/remove NSG rules again in the future which will need the macro file. The rules you create in the macro file stay there as a record of what you have created.

### Each value in the Excel CSV described

|Column Header                              |Description                
|---                                        |---
|rule_ref                                   |(Required) Unique key value per rule
|priority                                   |(Required) Specifies the priority of the rule. The value can be between 100 and 4096. The priority number must be unique for each rule in the collection. The lower the priority number, the higher the priority of the rule.
|direction                                  |(Required) The direction specifies if rule will be evaluated on incoming or outgoing traffic. Possible values are Inbound and Outbound.
|source_address_prefix                      |(Optional) CIDR or source IP range or * to match any IP. Tags such as ‘VirtualNetwork’, ‘AzureLoadBalancer’ and ‘Internet’ can also be used. This is required if source_address_prefixes is not specified.
|source_address_prefixes                    |(Optional) List of source address prefixes. Tags may not be used. This is required if source_address_prefix is not specified.
|source_application_security_group_ids      |(Optional) A List of source Application Security Group IDs
|source_port_range                          |(Optional) Source Port or Range. Integer or range between 0 and 65535 or * to match any. This is required if source_port_ranges is not specified.
|source_port_ranges                         |(Optional) List of source ports or port ranges. This is required if source_port_range is not specified.
|destination_address_prefix                 |(Optional) CIDR or destination IP range or * to match any IP. Tags such as ‘VirtualNetwork’, ‘AzureLoadBalancer’ and ‘Internet’ can also be used. Besides, it also supports all available Service Tags like ‘Sql.WestEurope‘, ‘Storage.EastUS‘, etc. You can list the available service tags with the CLI: shell az network list-service-tags --location westcentralus. For further information please see Azure CLI - az network list-service-tags. This is required if destination_address_prefixes is not specified.
|destination_address_prefixes               |(Optional) List of destination address prefixes. Tags may not be used. This is required if destination_address_prefix is not specified.
|destination_application_security_group_ids |(Optional) A List of destination Application Security Group IDs
|destination_port_range                     |(Optional) Destination Port or Range. Integer or range between 0 and 65535 or * to match any. This is required if destination_port_ranges is not specified.
|destination_port_ranges                    |(Optional) List of destination ports or port ranges. This is required if destination_port_range is not specified
|protocol                                   |(Required) Network protocol this rule applies to. Possible values include Tcp, Udp, Icmp, Esp, Ah or * (which matches all).
|access                                     |(Required) Specifies whether network traffic is allowed or denied. Possible values are Allow and Deny.
|description                                |(optional) Free text to describe the rule

## Examples
The following are examples of how to complete the form. Each example is a single row in the Excel file.

### Example rule 01

|Column Header                              |Value              
|---                                        |---
|rule_ref                                   |1
|priority                                   |100
|direction                                  |Inbound
|source_address_prefix                      |187.203.200.206/32
|source_address_prefixes                    |
|source_application_security_group_ids      |
|source_port_range                          |*
|source_port_ranges                         |
|destination_address_prefix                 |VirtualNetwork
|destination_address_prefixes               |
|destination_application_security_group_ids |
|destination_port_range                     |22
|destination_port_ranges                    |
|protocol                                   |Tcp
|access                                     |Allow
|description                                |Allow TCP/22 inbound to the VNet from a specific Internet IP address

### Example rule 02

|Column Header                              |Value              
|---                                        |---
|rule_ref                                   |2
|priority                                   |200
|direction                                  |Inbound
|source_address_prefix                      |
|source_address_prefixes                    |187.203.200.206/32,80.208.70.23/32
|source_application_security_group_ids      |
|source_port_range                          |*
|source_port_ranges                         |
|destination_address_prefix                 |10.0.1.10/32
|destination_address_prefixes               |
|destination_application_security_group_ids |
|destination_port_range                     |
|destination_port_ranges                    |3389,22
|protocol                                   |Tcp
|access                                     |Allow
|description                                |Allow TCP/3389 & TCP/22 inbound to a specified IP from two specific Internet IP address

### Example rule 03

|Column Header                              |Value              
|---                                        |---
|rule_ref                                   |3
|priority                                   |100
|direction                                  |Outbound
|source_address_prefix                      |VirtualNetwork
|source_address_prefixes                    |
|source_application_security_group_ids      |
|source_port_range                          |*
|source_port_ranges                         |
|destination_address_prefix                 |192.168.1.23/32
|destination_address_prefixes               |
|destination_application_security_group_ids |
|destination_port_range                     |
|destination_port_ranges                    |443,8080,589
|protocol                                   |*
|access                                     |Allow
|description                                |Allow the Vnet outbound to a specified IP


<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.1.0 |
| <a name="requirement_azurerm"></a> [azurerm](#requirement\_azurerm) | ~> 3.0.2 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_azurerm"></a> [azurerm](#provider\_azurerm) | 3.0.2 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [azurerm_network_security_group.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/network_security_group) | resource |
| [azurerm_network_security_rule.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/network_security_rule) | resource |
| [azurerm_resource_group.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/resource_group) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_nsg_ruleset"></a> [nsg\_ruleset](#input\_nsg\_ruleset) | n/a | `string` | `"nsg_rules.csv"` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->