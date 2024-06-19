locals {
  root_path       = abspath("${path.root}/../")
  project_name    = "${var.location}-${var.project_name}"
  slug_name       = "transcriptiondemo"
}

data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "this" {
  name     = local.project_name
  location = var.location
}

resource "azurerm_container_registry" "this" {
  name                = "RagApplication"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  sku                 = "Standard"
  admin_enabled       = true
}

# resource "azurerm_search_service" "this" {
#   name                = var.project_name
#   resource_group_name = azurerm_resource_group.this.name
#   location            = azurerm_resource_group.this.location
#   sku                 = "basic"
# }
