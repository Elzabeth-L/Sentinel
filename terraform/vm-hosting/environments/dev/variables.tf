variable "resource_group_name" {
  type        = string
  description = "Name of the resource group that will host the application runtime VM."
}

variable "location" {
  type        = string
  description = "Azure region for all resources."
  default     = "centralindia"
}

variable "name_prefix" {
  type        = string
  description = "Short naming prefix used for Azure resources."
  default     = "aks-gov"
}

variable "vm_name" {
  type        = string
  description = "Linux VM name."
  default     = "aks-gov-host-dev"
}

variable "vm_size" {
  type        = string
  description = "Azure VM size."
  default     = "Standard_B2s"
}

variable "admin_username" {
  type        = string
  description = "Linux admin username for SSH."
  default     = "azureuser"
}

variable "ssh_public_key_path" {
  type        = string
  description = "Path to the SSH public key used for VM login."
}

variable "vnet_cidr" {
  type        = string
  description = "Virtual network CIDR."
  default     = "10.70.0.0/16"
}

variable "subnet_cidr" {
  type        = string
  description = "Application subnet CIDR."
  default     = "10.70.1.0/24"
}

variable "allowed_ssh_source_cidrs" {
  type        = list(string)
  description = "CIDR ranges allowed to SSH to the VM. Restrict this for production demos."
  default     = ["0.0.0.0/0"]
}

variable "enable_system_assigned_identity" {
  type        = bool
  description = "Enable a system-assigned managed identity on the VM for Azure SDK/CLI access."
  default     = true
}

variable "tags" {
  type        = map(string)
  description = "Tags applied to all resources."
  default = {
    project     = "aks-governance-platform"
    environment = "dev"
    owner       = "platform-engineering"
    managed_by  = "terraform"
  }
}

