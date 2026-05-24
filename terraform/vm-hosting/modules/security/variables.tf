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

variable "subnet_id" {
  type        = string
  description = "Subnet id to associate with the NSG."
}

variable "allowed_ssh_source_cidrs" {
  type        = list(string)
  description = "CIDR ranges allowed to SSH to the VM."
}

variable "tags" {
  type        = map(string)
  description = "Resource tags."
}

