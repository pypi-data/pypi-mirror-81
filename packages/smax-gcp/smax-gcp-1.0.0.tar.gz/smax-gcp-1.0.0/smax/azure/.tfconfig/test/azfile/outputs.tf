output account_name {
  depends_on = [
    azurerm_storage_share.storage_share_a,
    azurerm_storage_share.storage_share_b,
  ]
  value = azurerm_storage_account.storage_account.name
}

output ssa_name {
  depends_on = [
    azurerm_storage_share.storage_share_a
  ]
  value = azurerm_storage_share.storage_share_a.name
}

output ssb_name {
  depends_on = [
    azurerm_storage_share.storage_share_b
  ]
  value = azurerm_storage_share.storage_share_b.name
}

output primary_key {
  depends_on = [
    azurerm_storage_share.storage_share_a,
    azurerm_storage_share.storage_share_b,
  ]
  value = azurerm_storage_account.storage_account.primary_access_key
}