output resource_group {
  value = module.network.resource_group_name
}

output database_ip {
  value = module.db.db_public_ip
}

output database_private_ip {
  value = module.db.db_private_ip
}

output default_database_user_password {
  value = var.default_database_user_password
}

output default_database_user {
  value = var.default_database_user
}


output bastion_ip {
  value = module.bastion.bastion_ip
}

output bastion_user {
  value = var.vm_user
}

output vnet_name {
  value = module.network.vnet_name
}

output ssh_private_key {
  value = file(local.ssh_private_key)
}

output ssh_public_key {
  value = file(local.ssh_public_key)
}

output fqdn_ip {
  value = module.network.fqdn_ip
}

output fqdn_name {
  value = var.fqdn
}

output k8s_nodes {
  value = var.k8s_nodes
}

output k8s_version {
  value = module.k8s.version
}

output kube_config {
  value = module.k8s.kube_config
}

output kube_config_admin {
  value = module.k8s.kube_config_admin
}


output ssa_name {
  value = module.azfile.ssa_name
}

output ssb_name {
  value = module.azfile.ssb_name
}

output azfile_account_name {
  value = module.azfile.account_name
}

output azfile_primary_key {
  value = module.azfile.primary_key
}
