
locals {
  tmp_arrs    = split(".", var.fqdn)
  tmp_length  = length(local.tmp_arrs)
  fqdn_prefix = join(".", slice(local.tmp_arrs, 0, local.tmp_length - 2))
  fqdn_domain = join(".", [local.tmp_arrs[local.tmp_length - 2], local.tmp_arrs[local.tmp_length - 1]])
}

resource azurerm_public_ip fqdn_ip {
  depends_on = [
    azurerm_resource_group.rg
  ]
  name                = "${random_id.prefix.hex}-fqdn-ip"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
}

resource azurerm_dns_zone dz {
  depends_on = [
    azurerm_resource_group.rg
  ]
  name                = local.fqdn_domain
  resource_group_name = azurerm_resource_group.rg.name
}

resource azurerm_dns_a_record dar {
  depends_on = [
    azurerm_resource_group.rg
  ]
  name                = local.fqdn_prefix
  zone_name           = azurerm_dns_zone.dz.name
  resource_group_name = azurerm_resource_group.rg.name
  ttl                 = 300
  records = [
    azurerm_public_ip.fqdn_ip.ip_address
  ]
}