resource azurerm_resource_group rg {
  name     = var.resource_group_name
  location = var.location
}

resource random_id prefix {
  byte_length = 4
}

resource azurerm_virtual_network vnet {
  name                = "${random_id.prefix.hex}-network"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = var.vnet_cidr
}

