terraform {
  required_providers {
    azurerm = { source = "hashicorp/azurerm" }
    random  = { source = "hashicorp/random" }
  }
}

provider "azurerm" { 
    features {} 
    }
resource "random_integer" "suffix" { 
    min = 1000 
    max = 9999 
    }

resource "azurerm_resource_group" "rg" {
  name     = "CloudDevOps_Project-${random_integer.suffix.result}"
  location = "westeurope"
}

resource "azurerm_container_registry" "acr" {
  name                = "containerregistry${random_integer.suffix.result}"
  resource_group_name = azurerm_resource_group.rg.name
  location = azurerm_resource_group.rg.location
  sku                 = "Standard"
  admin_enabled       = false
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = "kubernetescluster${random_integer.suffix.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "dns${random_integer.suffix.result}"

  default_node_pool {
    name       = "agentpool"
    node_count = 1
    vm_size    = "Standard_D2_v3"
  }

  identity { type = "SystemAssigned" }

  network_profile { network_plugin = "azure" }
}

data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "kv" {
  name                        = "akeyvault${random_integer.suffix.result}"
  location                    = azurerm_resource_group.rg.location
  resource_group_name         = azurerm_resource_group.rg.name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"
}
