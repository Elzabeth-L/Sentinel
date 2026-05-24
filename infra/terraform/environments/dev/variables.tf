variable "name_prefix" {
  type        = string
  description = "Resource naming prefix."
  default     = "aks-gov-dev"
}

variable "location" {
  type        = string
  description = "Azure region."
  default     = "eastus"
}

variable "tenant_id" {
  type        = string
  description = "Microsoft Entra tenant id."
}

variable "admin_object_id" {
  type        = string
  description = "Object id for initial Key Vault and AKS admin role assignment."
}

