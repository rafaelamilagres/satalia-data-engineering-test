provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }

  subscription_id = "12efb9ee-a929-4476-be80-21f4777e7216"
}

provider "azurecaf" {}

provider "databricks" {
  host = azurerm_databricks_workspace.databricks.workspace_url
}