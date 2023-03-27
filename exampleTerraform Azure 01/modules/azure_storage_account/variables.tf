variable "resource_group_name" {
  type        = string
  description = "(Required) Name of the resource group where the workload will be managed"
}

variable "resource_group_location" {
  type        = string
  description = <<EOT
  (Required) Location of the resource group where the workload will be managed

  Options:
  - westeurope; west europe
  - eastus; east us
  - southeastasia; south east asia
  EOT

  validation {
    condition     = can(regex("^westeurope$|^eastus$|^southeastasia$|^west europe$|^east us$|^south east asia$", var.resource_group_location))
    error_message = "Err: location is not valid."
  }
}

variable "environment" {
  type        = string
  description = <<EOT
  (Required) Describe the environment type

  Options:
  - dev
  - test
  - prod
  EOT

  validation {
    condition     = can(regex("^dev$|^test$|^prod$", var.environment))
    error_message = "Err: Valid options are dev, test, or prod."
  }
}

variable "prefix" {
  description = "(Required) Name of the workload"
  type        = string
}

variable "st_account_tier" {
  type        = string
  description = <<EOT
  (Optional) Set the perforance tier
  
  Standard is recommened for most scenarios. But if high IOPS then premium is needed.
  
  Options:
  - Standard
  - Premium
  EOT

  default = "Standard"

  validation {
    condition     = can(regex("^Standard$|^Premium$", var.st_account_tier))
    error_message = "Err: Valid options are Standard, Premium."
  }
}

variable "st_replication_type" {
  type        = string
  description = <<EOT
  (Optional) Set the perforance tier
  
  LRS is 3x copies in a single availability zone. GRS offers 6x split between two regions. 
  
  Options:
  - LRS
  - GRS
  EOT

  default = "LRS"

  validation {
    condition     = can(regex("^LRS$|^GRS$", var.st_replication_type))
    error_message = "Err: Valid options are LRS, GRS."
  }
}

variable "st_account_kind" {
  type        = string
  description = <<EOT
  (Optional) Defines the Kind of account. 
  
  Options:
  - BlobStorage
  - BlockBlobStorage
  - FileStorage
  - StorageV2
EOT

  default = "StorageV2"

  validation {
    condition     = can(regex("^BlobStorage$|^BlockBlobStorage$|^FileStorage$|^BlobStorage$|^StorageV2$", var.st_account_kind))
    error_message = "Err: Valid options are BlobStorage, BlockBlobStorage, FileStorage, StorageV2"
  }
}