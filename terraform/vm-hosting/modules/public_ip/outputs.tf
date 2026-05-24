output "id" {
  description = "Public IP id."
  value       = azurerm_public_ip.this.id
}

output "ip_address" {
  description = "Static public IP address."
  value       = azurerm_public_ip.this.ip_address
}

