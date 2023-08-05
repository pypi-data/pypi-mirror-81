resource azurerm_network_security_group nsg {
  name                = "${random_id.prefix.hex}-nsg"
  resource_group_name = var.resource_group_name
  location            = var.location
}

resource azurerm_network_security_rule ssh_sr {
  name                        = "ssh"
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.nsg.name
  priority                    = 102
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "22"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
}

/*
resource azurerm_network_interface_security_group_association nisga {
  network_interface_id      = azurerm_network_interface.ni.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}*/
