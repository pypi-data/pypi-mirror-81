data azurerm_kubernetes_service_versions current {
  location       = var.location
  version_prefix = var.k8s_version
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


resource azurerm_kubernetes_cluster cluster {
  name                = "${random_id.prefix.hex}-cluster"
  location            = var.location
  dns_prefix          = var.resource_group_name
  resource_group_name = var.resource_group_name
  kubernetes_version  = data.azurerm_kubernetes_service_versions.current.latest_version

  linux_profile {
    admin_username = var.admin_user
    ssh_key {
      key_data = var.ssh_pub_key
    }
  }

  default_node_pool {
    name            = "default"
    node_count      = var.k8s_nodes
    os_disk_size_gb = 100
    vm_size         = "Standard_D8s_v3"
    max_pods        = 50
    type            = "AvailabilitySet"
    vnet_subnet_id  = azurerm_subnet.subnet.id
  }

  service_principal {
    client_id     = var.client_id
    client_secret = var.client_secret
  }

  addon_profile {
    oms_agent {
      enabled = false
      #log_analytics_workspace_id = "{var.resource_group_name}-lgi"
    }
  }

  network_profile {
    network_plugin = var.network_plugin
  }
}
