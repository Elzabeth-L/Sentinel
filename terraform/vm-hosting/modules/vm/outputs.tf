output "id" {
  description = "VM id."
  value       = azurerm_linux_virtual_machine.this.id
}

output "name" {
  description = "VM name."
  value       = azurerm_linux_virtual_machine.this.name
}

output "principal_id" {
  description = "System-assigned managed identity principal id."
  value       = try(azurerm_linux_virtual_machine.this.identity[0].principal_id, null)
}

