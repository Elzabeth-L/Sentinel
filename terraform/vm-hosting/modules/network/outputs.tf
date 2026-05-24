output "vnet_id" {
  description = "Virtual network id."
  value       = azurerm_virtual_network.this.id
}

output "subnet_id" {
  description = "Application subnet id."
  value       = azurerm_subnet.app.id
}

