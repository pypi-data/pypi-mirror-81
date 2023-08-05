variable context_folder {
  default = "."
}

variable resource_prefix {
  description = "A prefix used for all resources in this example"
  default     = "sdeploy"
}

locals {
  ssh_private_key     = "./keys/id_rsa"
  ssh_public_key      = "./keys/id_rsa.pub"
  vnet_cidr           = ["10.88.0.0/16"]
  subnet_bastion_cidr = ["10.88.1.0/24"]
  subnet_k8s_cidr     = ["10.88.2.0/24"]
  subnet_db_cidr      = ["10.88.3.0/24"]
}

module network {
  source              = "./network"
  resource_group_name = var.resource_prefix
  location            = var.location
  vnet_cidr           = local.vnet_cidr
  fqdn                = var.fqdn
}

module db {
  source                 = "./database"
  upload_folder          = "${var.context_folder}/upload.db/"
  resource_group_name    = module.network.resource_group_name
  location               = module.network.location
  database_user_password = var.default_database_user_password
  database_disk_size_gb  = var.database_disk_size_gb
  vm_password            = var.vm_pwd
  vm_size                = var.database_server_vm_size
  vm_ssh_username        = var.vm_user
  ssh_private_key        = file(local.ssh_private_key)
  ssh_pub_key            = file(local.ssh_public_key)
  subnet_cidr            = local.subnet_db_cidr
  vnet_name              = module.network.vnet_name
}


module k8s {
  source              = "./k8s"
  resource_group_name = module.network.resource_group_name
  location            = module.network.location
  vnet_name           = module.network.vnet_name
  subnet_cidr         = local.subnet_k8s_cidr
  k8s_version         = var.k8s_version
  k8s_nodes           = var.k8s_nodes
  network_plugin      = var.network_plugin
  client_id           = var.client_id
  client_secret       = var.client_secret
  admin_user          = var.vm_user
  ssh_pub_key         = file(local.ssh_public_key)
}

module bastion {
  source              = "./bastion"
  vnet_name           = module.network.vnet_name
  upload_folder       = "${var.context_folder}/upload.bastion/"
  resource_group_name = module.network.resource_group_name
  location            = module.network.location
  password            = var.vm_pwd
  size                = var.bastion_server_vm_size
  user                = var.vm_user
  kube_config         = module.k8s.kube_config
  ssh_private_key     = file(local.ssh_private_key)
  ssh_pub_key         = file(local.ssh_public_key)
  subnet_cidr         = local.subnet_bastion_cidr
}

module azfile {
  source              = "./azfile"
  file_store_size     = 200
  location            = module.network.location
  resource_group_name = module.network.resource_group_name
}
