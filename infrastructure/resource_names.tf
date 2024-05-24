resource "azurecaf_name" "rg" {
  name          = "satalia-data-engineering-test"
  resource_type = "azurerm_resource_group"
}

resource "azurecaf_name" "rg_databricks" {
  name          = "satalia-data-engineering-test-databricks"
  resource_type = "azurerm_resource_group"
}

resource "azurecaf_name" "storage" {
  name          = "fsmdata"
  resource_type = "azurerm_storage_account"
}

resource "azurecaf_name" "storage_container" {
  name          = "data"
  resource_type = "azurerm_storage_container"
  separator     = "-"
}

resource "azurecaf_name" "databricks_workspace" {
  name          = "fsm-workspace"
  resource_type = "azurerm_databricks_workspace"
  separator     = "-"
}

resource "azurecaf_name" "vault" {
  name          = "fsm"
  resource_type = "azurerm_key_vault"
}

resource "azurecaf_name" "databricks_cluster" {
  name          = "fsm-processing"
  resource_type = "databricks_cluster"
}