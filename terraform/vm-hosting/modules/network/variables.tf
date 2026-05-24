variable "name_prefix" {
  type        = string
  description = "Resource naming prefix."
}

variable "location" {
  type        = string
  description = "Azure region."
}

variable "resource_group_name" {
  type        = string
  description = "Resource group name."
}

variable "vnet_cidr" {
  type        = string
  description = "Virtual network CIDR."
}

variable "subnet_cidr" {
  type        = string
  description = "Subnet CIDR."
}

variable "tags" {
  type        = map(string)
  description = "Resource tags."
}

