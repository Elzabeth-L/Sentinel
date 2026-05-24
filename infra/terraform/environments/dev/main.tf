resource "azurerm_resource_group" "this" {
  name     = "${var.name_prefix}-rg"
  location = var.location
}

module "network" {
  source              = "../../modules/network"
  name_prefix         = var.name_prefix
  location            = var.location
  resource_group_name = azurerm_resource_group.this.name
}

module "acr" {
  source              = "../../modules/acr"
  name_prefix         = replace(var.name_prefix, "-", "")
  location            = var.location
  resource_group_name = azurerm_resource_group.this.name
}

module "observability" {
  source              = "../../modules/observability"
  name_prefix         = var.name_prefix
  location            = var.location
  resource_group_name = azurerm_resource_group.this.name
}

module "key_vault" {
  source              = "../../modules/key-vault"
  name_prefix         = replace(var.name_prefix, "-", "")
  location            = var.location
  resource_group_name = azurerm_resource_group.this.name
  tenant_id           = var.tenant_id
  admin_object_id     = var.admin_object_id
}

module "aks" {
  source                     = "../../modules/aks"
  name_prefix                = var.name_prefix
  location                   = var.location
  resource_group_name        = azurerm_resource_group.this.name
  subnet_id                  = module.network.aks_subnet_id
  log_analytics_workspace_id = module.observability.log_analytics_workspace_id
  acr_id                     = module.acr.id
}

module "container_apps" {
  source                     = "../../modules/container-apps"
  name_prefix                = var.name_prefix
  location                   = var.location
  resource_group_name        = azurerm_resource_group.this.name
  log_analytics_workspace_id = module.observability.log_analytics_workspace_id
}

