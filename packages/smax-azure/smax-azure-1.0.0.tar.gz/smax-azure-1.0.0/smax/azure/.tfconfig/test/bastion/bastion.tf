locals {
  virtual_machine_name = "${random_id.prefix.hex}-bastion"
}

resource random_id prefix {
  byte_length = 4
}

resource azurerm_subnet subnet {
  name                 = "${random_id.prefix.hex}-bastion-subnet"
  resource_group_name  = var.resource_group_name
  address_prefixes     = var.subnet_cidr
  virtual_network_name = var.vnet_name
}

resource azurerm_public_ip pub_ip {
  name                = "${random_id.prefix.hex}-bastion-ip"
  location            = var.location
  resource_group_name = var.resource_group_name
  allocation_method   = "Static"
}

resource azurerm_network_interface ni {
  name                = "${random_id.prefix.hex}-bastion-ni"
  location            = var.location
  resource_group_name = var.resource_group_name

  ip_configuration {
    name                          = "bastion_interface"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.pub_ip.id
  }
}

resource azurerm_virtual_machine bastion {
  name                = local.virtual_machine_name
  location            = var.location
  resource_group_name = var.resource_group_name
  network_interface_ids = [
  azurerm_network_interface.ni.id]
  delete_os_disk_on_termination    = true
  delete_data_disks_on_termination = true
  vm_size                          = var.size

  storage_image_reference {
    publisher = "OpenLogic"
    offer     = "CentOS"
    sku       = "7.6"
    version   = "latest"
  }

  storage_os_disk {
    name              = "${local.virtual_machine_name}-osdisk"
    managed_disk_type = "Premium_LRS"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    disk_size_gb      = 100
  }

  os_profile {
    computer_name  = local.virtual_machine_name
    admin_username = var.user
    admin_password = var.password
  }

  os_profile_linux_config {
    disable_password_authentication = true
    ssh_keys {
      path     = "/home/${var.user}/.ssh/authorized_keys"
      key_data = (var.ssh_pub_key)
    }
  }
}

resource local_file init {
  content  = file("${path.module}/scripts/init_bastion.sh")
  filename = "${var.upload_folder}/init_bastion.sh"
}

resource local_file kube_config {
  content  = var.kube_config
  filename = "${var.upload_folder}/kube-config"
}

resource null_resource upload {
  depends_on = [
    azurerm_virtual_machine.bastion,
    local_file.init,
    local_file.kube_config,
  ]

  provisioner file {
    source      = var.upload_folder
    destination = "~"

    connection {
      host        = azurerm_public_ip.pub_ip.ip_address
      type        = "ssh"
      user        = var.user
      timeout     = "10m"
      private_key = (var.ssh_private_key)
      agent       = false
    }
  }
}

resource null_resource run_init {
  depends_on = [
    null_resource.upload
  ]
  provisioner remote-exec {
    connection {
      host        = azurerm_public_ip.pub_ip.ip_address
      type        = "ssh"
      user        = var.user
      timeout     = "10m"
      private_key = (var.ssh_private_key)
      agent       = false
    }
    inline = [
      "sudo chmod 755 **",
      "./init_bastion.sh ${var.user}",
    ]
  }
}

data null_data_source bastion_info {
  depends_on = [
    null_resource.run_init
  ]
  inputs = {
    bastion_ip = azurerm_public_ip.pub_ip.ip_address,
  }
}
