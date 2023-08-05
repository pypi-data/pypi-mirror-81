variable location {
  default = "West US 2"
}

variable vm_user {
  description = "The user for ssh login azure instance"
  default     = "centos"
}

variable vm_pwd {
  description = "The user for ssh login azure instance"
  default     = "centos"
}


variable database_server_vm_size {
  description = "database server instance size"
  default     = "Standard_D4s_v3"
}

variable bastion_server_vm_size {
  description = "database server instance size"
  default     = "Standard_D2s_v3"
}

variable database_disk_size_gb {
  description = "database server instance size"
  default     = "100"
}

variable fqdn {
  description = "The FQDN for access suite"
  default     = "sdeploy.testonly.com"
}

variable default_database_user {
  default = "postgres"
}

variable default_database_user_password {
  default = "Admin_1234"
}

variable default_database_db {
  default = "postgres"
}

variable cdf_admin_password {
  default = "Admin_1234"
}

variable k8s_version {
  default = "1.16"
}

variable k8s_nodes {
  default = 2
}

variable network_plugin {
  default = "azure"
}

