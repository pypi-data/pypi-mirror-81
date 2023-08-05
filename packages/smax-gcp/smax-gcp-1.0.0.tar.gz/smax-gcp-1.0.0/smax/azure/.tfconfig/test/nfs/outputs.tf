output nfs__public_ip {
  value = var.create_me ? data.null_data_source.nfs_srv_info[0].outputs["nfs_public_ip"] : ""
}

output nfs_private_ip {
  value = var.create_me ? data.null_data_source.nfs_srv_info[0].outputs["nfs_private_ip"] : ""
}
