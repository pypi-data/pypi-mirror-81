output project {
  value = var.project
}

output vnet_name {
  value = module.network.name
}

output bastion_ip {
  value = module.bastion.ip_addr
}

output bastion_user {
  value = var.vm_user
}

output bastion_id {
  value = module.bastion.instance_id
}


output database_ip {
  value = module.database.private_ip
}

output default_database_user {
  value = module.database.default_db_user
}

output default_database_user_password {
  value = module.database.db_password
}

output nfs_ip {
  value = module.nfs.ip_addr
}

output nfs_share_name {
  value = module.nfs.share_name
}

output fqdn_name {
  value = module.dns.fqdn_name
}

output fqdn_ip {
  value = module.dns.fqdn_ip
}

output ssh_private_key {
  value = file(local.ssh_private_key)
}

output ssh_public_key {
  value = file(local.ssh_public_key)
}