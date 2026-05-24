variable "name_prefix" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }

resource "azurerm_log_analytics_workspace" "this" {
  name                = "${var.name_prefix}-law"
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_monitor_workspace" "this" {
  name                = "${var.name_prefix}-amw"
  resource_group_name = var.resource_group_name
  location            = var.location
}

resource "azurerm_dashboard_grafana" "this" {
  name                              = "${var.name_prefix}-grafana"
  resource_group_name               = var.resource_group_name
  location                          = var.location
  api_key_enabled                   = false
  deterministic_outbound_ip_enabled = true
  public_network_access_enabled     = true
  identity {
    type = "SystemAssigned"
  }
}

output "log_analytics_workspace_id" {
  value = azurerm_log_analytics_workspace.this.id
}

output "monitor_workspace_id" {
  value = azurerm_monitor_workspace.this.id
}

