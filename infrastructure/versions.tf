terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.94.0"
    }
    azurecaf = {
      source  = "aztfmod/azurecaf"
      version = "1.2.23"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "1.35.0"
    }
  }

  required_version = ">= 1.3.3"
}
