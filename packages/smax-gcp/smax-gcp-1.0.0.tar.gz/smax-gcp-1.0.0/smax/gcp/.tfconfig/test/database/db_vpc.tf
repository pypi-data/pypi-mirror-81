resource google_compute_global_address database_private_ip_address {
  name          = "${var.resource_prefix}-pg-ip"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = var.vnet_link
}

resource google_service_networking_connection pg_vpc_peering_connection {
  network = var.vnet_link
  service = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [
  google_compute_global_address.database_private_ip_address.name]
}
