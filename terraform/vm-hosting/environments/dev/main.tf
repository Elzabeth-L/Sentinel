resource "azurerm_resource_group" "this" {
  name     = var.resource_group_name
  location = var.location
  tags     = var.tags
}

module "network" {
  source              = "../../modules/network"
  name_prefix         = var.name_prefix
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  vnet_cidr           = var.vnet_cidr
  subnet_cidr         = var.subnet_cidr
  tags                = var.tags
}

module "public_ip" {
  source              = "../../modules/public_ip"
  name_prefix         = var.name_prefix
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  tags                = var.tags
}

module "security" {
  source                   = "../../modules/security"
  name_prefix              = var.name_prefix
  location                 = azurerm_resource_group.this.location
  resource_group_name      = azurerm_resource_group.this.name
  subnet_id                = module.network.subnet_id
  allowed_ssh_source_cidrs = var.allowed_ssh_source_cidrs
  tags                     = var.tags
}

module "vm" {
  source                          = "../../modules/vm"
  name_prefix                     = var.name_prefix
  location                        = azurerm_resource_group.this.location
  resource_group_name             = azurerm_resource_group.this.name
  vm_name                         = var.vm_name
  vm_size                         = var.vm_size
  admin_username                  = var.admin_username
  ssh_public_key                  = file(var.ssh_public_key_path)
  subnet_id                       = module.network.subnet_id
  public_ip_id                    = module.public_ip.id
  bootstrap_script_path           = "${path.module}/../../scripts/bootstrap.sh"
  enable_system_assigned_identity = var.enable_system_assigned_identity
  tags                            = var.tags

  depends_on = [module.security]
}

