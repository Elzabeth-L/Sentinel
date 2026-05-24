variable "name_prefix" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "subnet_id" { type = string }
variable "log_analytics_workspace_id" { type = string }
variable "acr_id" { type = string }

resource "azurerm_kubernetes_cluster" "this" {
  name                      = "${var.name_prefix}-aks"
  location                  = var.location
  resource_group_name       = var.resource_group_name
  dns_prefix                = "${var.name_prefix}-aks"
  kubernetes_version        = null
  oidc_issuer_enabled       = true
  workload_identity_enabled = true
  azure_policy_enabled      = true

  default_node_pool {
    name           = "system"
    node_count     = 2
    vm_size        = "Standard_D2s_v5"
    vnet_subnet_id = var.subnet_id
  }

  identity {
    type = "SystemAssigned"
  }

  oms_agent {
    log_analytics_workspace_id = var.log_analytics_workspace_id
  }

  monitor_metrics {}

  network_profile {
    network_plugin = "azure"
    network_policy = "azure"
  }
}

resource "azurerm_role_assignment" "acr_pull" {
  scope                = var.acr_id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.this.kubelet_identity[0].object_id
}

output "name" {
  value = azurerm_kubernetes_cluster.this.name
}

output "id" {
  value = azurerm_kubernetes_cluster.this.id
}

