locals {
  api_name = "langchain-service"
  api_image_name             = "langchain_api"
  api_image_tag              = "latest"
}

resource "azurerm_log_analytics_workspace" "this" {
  name                = local.api_name
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "this" {
  name                       = local.api_name
  location                   = azurerm_resource_group.this.location
  resource_group_name        = azurerm_resource_group.this.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.this.id
}

resource "null_resource" "build_image" {
  depends_on = [
    azurerm_container_registry.this
  ]

  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = (templatefile("${path.module}/build_image.tpl", {
      source         = "${local.root_path}/src/api/"
      registry_name  = lower(azurerm_container_registry.this.name)
      image_name     = local.api_image_name
      image_tag      = local.api_image_tag
      }
    ))
  }
}

resource "azurerm_container_app" "this" {
  name                         = local.api_name
  container_app_environment_id = azurerm_container_app_environment.this.id
  resource_group_name          = azurerm_resource_group.this.name
  revision_mode                = "Single"

  secret {
    name  = "registry-credentials"
    value = azurerm_container_registry.this.admin_password
  }

  registry {
    server               = azurerm_container_registry.this.login_server
    username             = azurerm_container_registry.this.admin_username
    password_secret_name = "registry-credentials"
    
  }

  ingress {
    external_enabled = true
    target_port  = 8080

    traffic_weight {
      latest_revision = true
      percentage = 100
    }
  }

  template {
    container {
      name   = local.api_name
      image  = "${azurerm_container_registry.this.login_server}/${local.api_image_name}:${local.api_image_tag}"
      cpu    = 2.0
      memory = "4.0Gi"

      env {
        name = "OPENAI_API_KEY"
        value = var.openai_api_key
      }

      env {
        name = "HUGGINGFACE_TOKEN"
        value = var.huggingface_token
      }

      env {
        name = "COHERE_API_KEY"
        value = var.cohere_api_key
      }

      env {
        name = "TORCH_DEVICE"
        value = var.torch_device
      }

      env {
        name = "AZURE_SEARCH_ENDPOINT"
        value = var.azure_search_endpoint
      }

      env {
        name = "AZURE_SEARCH_KEY"
        value = var.azure_search_key
      }

      env {
        name = "AZURE_SEARCH_INDEX_NAME"
        value = var.azure_search_index_name
      }
    }
  }
}
