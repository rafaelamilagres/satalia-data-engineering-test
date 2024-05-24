resource "azurerm_storage_account" "storage" {
  name                = azurecaf_name.storage.result
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.main_region
  account_tier        = "Standard"
  account_kind        = "StorageV2"

  account_replication_type  = "LRS"
  enable_https_traffic_only = false
  is_hns_enabled            = true
}

resource "azurerm_storage_container" "storage" {
  name                  = azurecaf_name.storage.result
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

resource "azurerm_role_assignment" "storage" {
  for_each = toset(var.team_ids)

  scope                = azurerm_storage_account.storage.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = each.key
}

resource "azurerm_key_vault" "vault" {
  name                          = azurecaf_name.vault.result
  location                      = azurerm_resource_group.rg.location
  resource_group_name           = azurerm_resource_group.rg.name
  enabled_for_disk_encryption   = true
  enable_rbac_authorization     = true
  tenant_id                     = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days    = 7
  sku_name                      = "standard"

}

resource "azurerm_role_assignment" "vault_admin" {
  scope                = azurerm_key_vault.vault.id
  role_definition_name = "Key Vault Administrator"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_key_vault_secret" "storage" {
  name         = "fsm-storage-access-key"
  value        = azurerm_storage_account.storage.primary_access_key
  key_vault_id = azurerm_key_vault.vault.id

  depends_on = [
    azurerm_role_assignment.storage
  ]
}


resource "azurerm_databricks_workspace" "databricks" {
  name                = azurecaf_name.databricks_workspace.result
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.main_region
  sku                 = "premium"

  managed_resource_group_name = azurecaf_name.rg_databricks.result
}

resource "azurerm_role_assignment" "databricks" {
  scope                = azurerm_databricks_workspace.databricks.id
  role_definition_name = "Owner"
  principal_id         = data.azurerm_client_config.current.object_id
}


resource "databricks_secret_scope" "databricks_secrets" {
  name = "fsm-secret-scope"

  keyvault_metadata {
    resource_id = azurerm_key_vault.vault.id
    dns_name    = azurerm_key_vault.vault.vault_uri
  }
}
