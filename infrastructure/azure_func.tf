provider "azurerm" {
  skip_provider_registration = true

  features {}
}

data "azurerm_resource_group" "example" {
  name = "amani-sandbox"
}

resource "azurerm_storage_account" "example" {
  name                     = "functionsappbasecamp"
  resource_group_name      = data.azurerm_resource_group.example.name
  location                 = "West Europe"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "example" {
  name                = "Basecamp-app-service-plan"
  resource_group_name = data.azurerm_resource_group.example.name
  location            = data.azurerm_resource_group.example.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "example" {
  name                = "Basecamp-Email-Forwarding-automation"
  resource_group_name = data.azurerm_resource_group.example.name
  location            = "west Europe"
  service_plan_id            = azurerm_service_plan.example.id
  storage_account_name       = azurerm_storage_account.example.name
  storage_account_access_key = azurerm_storage_account.example.primary_access_key
  
  site_config {
    application_stack{
    python_version = 3.11
  }
  }
}

