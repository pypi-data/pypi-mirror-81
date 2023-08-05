locals {
  database_server_machine_name = "${random_id.prefix.hex}-db"
  database_admin_username      = var.vm_ssh_username
  database_admin_pwd           = var.vm_password
}

resource random_id prefix {
  byte_length = 4
}

resource azurerm_subnet subnet {
  name                 = "${random_id.prefix.hex}-db-subnet"
  resource_group_name  = var.resource_group_name
  address_prefixes     = var.subnet_cidr
  virtual_network_name = var.vnet_name
}

resource azurerm_network_interface ni {
  name                = "${random_id.prefix.hex}-db-nic"
  location            = var.location
  resource_group_name = var.resource_group_name

  ip_configuration {
    name                          = "smax_database_interface"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.pub_ip.id
  }
}

resource azurerm_public_ip pub_ip {
  name                = "${random_id.prefix.hex}-db-ip"
  location            = var.location
  resource_group_name = var.resource_group_name
  allocation_method   = "Static"
}

resource azurerm_virtual_machine database_server_vm {
  name                             = local.database_server_machine_name
  location                         = var.location
  resource_group_name              = var.resource_group_name
  network_interface_ids            = [azurerm_network_interface.ni.id]
  delete_os_disk_on_termination    = true
  delete_data_disks_on_termination = true
  vm_size                          = var.vm_size

  storage_image_reference {
    publisher = "OpenLogic"
    offer     = "CentOS"
    sku       = "7.6"
    version   = "latest"
  }

  storage_os_disk {
    name              = "${local.database_server_machine_name}-osdisk"
    managed_disk_type = "Premium_LRS"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    disk_size_gb      = var.database_disk_size_gb
  }

  os_profile {
    computer_name  = local.database_server_machine_name
    admin_username = local.database_admin_username
    admin_password = local.database_admin_pwd
  }

  os_profile_linux_config {
    disable_password_authentication = true
    ssh_keys {
      path     = "/home/${local.database_admin_username}/.ssh/authorized_keys"
      key_data = var.ssh_pub_key
    }
  }
}

resource null_resource initialize_pg {
  depends_on = [
    azurerm_virtual_machine.database_server_vm,
    local_file.setup_pg_script
  ]

  provisioner file {
    source      = var.upload_folder
    destination = "~"

    connection {
      host        = azurerm_public_ip.pub_ip.ip_address
      type        = "ssh"
      user        = local.database_admin_username
      timeout     = "10m"
      private_key = var.ssh_private_key
      agent       = false
    }
  }

  provisioner remote-exec {
    connection {
      host        = azurerm_public_ip.pub_ip.ip_address
      type        = "ssh"
      user        = local.database_admin_username
      timeout     = "10m"
      private_key = var.ssh_private_key
      agent       = false
    }
    inline = [
      "sudo chmod 755 **",
      "sudo ./extend_disk.sh",
      "./setup_pg.sh",
    ]
    //on_failure = "continue"
  }
}

data null_data_source db_srv_info {
  depends_on = [
  null_resource.initialize_pg]
  inputs = {
    db_private_ip = azurerm_network_interface.ni.private_ip_address
    db_public_ip  = azurerm_public_ip.pub_ip.ip_address
  }
}

