resource random_id prefix {
  count       = var.create_me ? 1 : 0
  byte_length = 4
}

locals {
  nfs_server_machine_name = var.create_me ? "${random_id.prefix[0].hex}-nfs" : ""
  nfs_admin_username      = var.vm_ssh_username
}

resource "azurerm_network_interface" "smax_nfs_interface" {
  count                     = var.create_me ? 1 : 0
  name                      = "${random_id.prefix[0].hex}-nfs-nic"
  location                  = var.location
  resource_group_name       = var.resource_group_name
  network_security_group_id = var.nsg_id

  ip_configuration {
    name                          = "smax_nfs_interface"
    subnet_id                     = var.subnet_id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.smax_nfs_server_ip[0].id
  }
}

resource "azurerm_public_ip" "smax_nfs_server_ip" {
  count               = var.create_me ? 1 : 0
  name                = "${random_id.prefix[0].hex}-nfs-ip"
  location            = var.location
  resource_group_name = var.resource_group_name
  allocation_method   = "Static"
}

resource "azurerm_virtual_machine" "nfs_server_vm" {
  count               = var.create_me ? 1 : 0
  name                = local.nfs_server_machine_name
  location            = var.location
  resource_group_name = var.resource_group_name
  network_interface_ids = [
  azurerm_network_interface.smax_nfs_interface[0].id]
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
    name              = "${local.nfs_server_machine_name}-osdisk"
    managed_disk_type = "Premium_LRS"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    disk_size_gb      = var.nfs_disk_size_gb
  }

  os_profile {
    computer_name  = local.nfs_server_machine_name
    admin_username = local.nfs_admin_username
    admin_password = var.vm_password
  }

  os_profile_linux_config {
    disable_password_authentication = true
    ssh_keys {
      path     = "/home/${local.nfs_admin_username}/.ssh/authorized_keys"
      key_data = file("${path.module}/../../keys/ssh_public_key")
    }
  }
}


resource "null_resource" "initialize_nfs_server" {
  count = var.create_me ? 1 : 0
  depends_on = [
    azurerm_virtual_machine.nfs_server_vm
  ]

  provisioner file {
    source      = "${path.module}/scripts/"
    destination = "~"

    connection {
      host        = azurerm_public_ip.smax_nfs_server_ip[0].ip_address
      type        = "ssh"
      user        = local.nfs_admin_username
      timeout     = "10m"
      private_key = file("${path.module}/../../keys/ssh_private_key")
      agent       = false
    }
  }

  provisioner "remote-exec" {
    connection {
      host        = azurerm_public_ip.smax_nfs_server_ip[0].ip_address
      type        = "ssh"
      user        = local.nfs_admin_username
      timeout     = "10m"
      private_key = file("${path.module}/../../keys/ssh_private_key")
      agent       = false
    }
    inline = [
      "sudo chmod 755 **",
      "sudo ./extend_disk.sh",
      "./setup_nfs_server.sh ${var.smax_version}",
    ]
  }
}

data null_data_source nfs_srv_info {
  count = var.create_me ? 1 : 0
  depends_on = [
  null_resource.initialize_nfs_server]
  inputs = {
    nfs_public_ip  = azurerm_public_ip.smax_nfs_server_ip[0].ip_address
    nfs_private_ip = azurerm_network_interface.smax_nfs_interface[0].private_ip_address
  }
}

