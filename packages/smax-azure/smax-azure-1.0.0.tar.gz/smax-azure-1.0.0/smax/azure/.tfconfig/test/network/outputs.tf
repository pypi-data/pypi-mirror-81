output resource_group_name {
  depends_on = [
  azurerm_resource_group.rg]
  value = azurerm_resource_group.rg.name
}

output location {
  depends_on = [
  azurerm_resource_group.rg]
  value = azurerm_resource_group.rg.location
}

output vnet_name {
  depends_on = [
  azurerm_virtual_network.vnet]
  value = azurerm_virtual_network.vnet.name
}

output fqdn_ip {
  value = azurerm_public_ip.fqdn_ip.ip_address
}