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
  # This uses the replace function to remove any BOM character from the beginning of the file before passing it to csvdecode.
  nsg_rules = csvdecode(replace(file((var.nsg_ruleset)), "/^\uFEFF/", ""))
}

variable "nsg_ruleset" {
  default = "nsg_rules.csv"
}

resource "azurerm_resource_group" "this" {
  name     = "rg-nsg-example"
  location = "west europe"
}

resource "azurerm_network_security_group" "this" {
  name                = "nsg-example"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
}

resource "azurerm_network_security_rule" "this" {
  for_each = { for nsg_rule in local.nsg_rules : nsg_rule.rule_ref => nsg_rule }


  resource_group_name         = azurerm_network_security_group.this.resource_group_name
  network_security_group_name = azurerm_network_security_group.this.name

  # Priority
  priority = each.value.priority

  # Direction of the traffic
  direction = each.value.direction

  # Source port range(s)
  source_port_range  = each.value.source_port_range != "" ? each.value.source_port_range : null
  source_port_ranges = length(each.value.source_port_ranges) > 0 ? split(",", each.value.source_port_ranges) : null

  # Source IP address prefix(es)
  source_address_prefix   = each.value.source_address_prefix != "" ? each.value.source_address_prefix : null
  source_address_prefixes = length(each.value.source_address_prefixes) > 0 ? split(",", each.value.source_address_prefixes) : null

  # Destination IP address prefix(es), service tag, application security group
  destination_address_prefix                 = each.value.destination_address_prefix != "" ? each.value.destination_address_prefix : null
  destination_address_prefixes               = length(each.value.destination_address_prefixes) > 0 ? split(",", each.value.destination_address_prefixes) : null
  destination_application_security_group_ids = length(each.value.destination_application_security_group_ids) > 0 ? split(",", each.value.destination_application_security_group_ids) : null

  # Destination port range(s)
  destination_port_range  = each.value.destination_port_range != "" ? each.value.destination_port_range : null
  destination_port_ranges = length(each.value.destination_port_ranges) > 0 ? split(",", each.value.destination_port_ranges) : null

  # Protocol
  protocol = each.value.protocol

  # Action
  access = each.value.access

  # Name of the rule
  name = "r${each.value.priority}-${each.value.direction}"

  # Description of the rule
  description = each.value.description
}
