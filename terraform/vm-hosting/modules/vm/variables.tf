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

variable "vm_name" {
  type        = string
  description = "Virtual machine name."
}

variable "vm_size" {
  type        = string
  description = "Virtual machine size."
}

variable "admin_username" {
  type        = string
  description = "Linux admin username."
}

variable "ssh_public_key" {
  type        = string
  description = "SSH public key content."
}

variable "subnet_id" {
  type        = string
  description = "Subnet id for the VM NIC."
}

variable "public_ip_id" {
  type        = string
  description = "Static public IP id."
}

variable "bootstrap_script_path" {
  type        = string
  description = "Path to the VM bootstrap script."
}

variable "enable_system_assigned_identity" {
  type        = bool
  description = "Enable a system-assigned managed identity."
}

variable "tags" {
  type        = map(string)
  description = "Resource tags."
}

