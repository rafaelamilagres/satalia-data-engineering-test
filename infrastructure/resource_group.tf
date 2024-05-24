resource "azurerm_resource_group" "rg" {
  name     = azurecaf_name.rg.result
  location = var.main_region
}

resource "azurerm_role_assignment" "rg_users" {
  for_each = toset(var.team_ids)

  scope                = azurerm_resource_group.rg.id
  role_definition_name = "Reader"
  principal_id         = each.key
}

resource "azurerm_role_assignment" "rg_admins" {
  for_each = toset(var.admin_ids)

  scope                = azurerm_resource_group.rg.id
  role_definition_name = "Contributor"
  principal_id         = each.key
}