locals {
  app_image_name             = "streamlit_app"
  app_image_tag              = "latest"
}

resource "null_resource" "build_app_image" {
  depends_on = [
    azurerm_container_registry.this
  ]

  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = (templatefile("${path.module}/build_image.tpl", {
      source         = "${local.root_path}/src/app"
      registry_name  = lower(azurerm_container_registry.this.name)
      image_name     = local.app_image_name
      image_tag      = "latest",
      }
    ))
  }
}

resource "azurerm_service_plan" "this" {
  name                = "${var.location}-${var.project_name}-app"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "this" {
  name                = "${var.location}-${var.project_name}-app"
  location            = var.location
  resource_group_name = azurerm_resource_group.this.name
  service_plan_id     = azurerm_service_plan.this.id
  https_only          = true

  site_config {
    application_stack {
      docker_image_name = "${local.app_image_name}:${local.app_image_tag}"
      docker_registry_url =  "https://${azurerm_container_registry.this.login_server}"
      docker_registry_username = azurerm_container_registry.this.admin_username
      docker_registry_password = azurerm_container_registry.this.admin_password
    }
  }

  app_settings = {
    ENDPOINT_URL = "https://${azurerm_container_app.this.ingress[0].fqdn}"
  }
}
