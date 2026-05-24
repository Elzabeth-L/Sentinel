output "resource_group_name" {
  description = "Resource group name."
  value       = azurerm_resource_group.this.name
}

output "vm_name" {
  description = "Virtual machine name."
  value       = module.vm.name
}

output "vm_public_ip" {
  description = "Static public IP address for DNS A records."
  value       = module.public_ip.ip_address
}

output "ssh_command" {
  description = "SSH command for VM access."
  value       = "ssh ${var.admin_username}@${module.public_ip.ip_address}"
}

output "frontend_dns_record" {
  description = "Recommended frontend DNS A record."
  value       = "governance.vaultrix.in -> ${module.public_ip.ip_address}"
}

output "api_dns_record" {
  description = "Recommended backend API DNS A record."
  value       = "api.governance.vaultrix.in -> ${module.public_ip.ip_address}"
}

output "vm_principal_id" {
  description = "System-assigned managed identity principal id. Use this for Azure RBAC assignments."
  value       = module.vm.principal_id
}

