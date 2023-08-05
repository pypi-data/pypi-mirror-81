resource random_id prefix {
  byte_length = 4
}

resource azurerm_storage_account storage_account {
  name                     = "${random_id.prefix.hex}asa"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Premium"
  account_kind             = "FileStorage"
  account_replication_type = "LRS"
}

resource azurerm_storage_share storage_share_a {
  name                 = "${random_id.prefix.hex}ssa"
  storage_account_name = azurerm_storage_account.storage_account.name
  quota                = var.file_store_size
}

resource azurerm_storage_share storage_share_b {
  name                 = "${random_id.prefix.hex}ssb"
  storage_account_name = azurerm_storage_account.storage_account.name
  quota                = var.file_store_size
}

