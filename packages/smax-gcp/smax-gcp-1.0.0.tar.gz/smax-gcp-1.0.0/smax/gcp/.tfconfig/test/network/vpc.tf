resource google_compute_network vpc_network {
  name                    = "${var.resource_prefix}-vpc"
  auto_create_subnetworks = "false"
  routing_mode            = "REGIONAL"
}

resource random_id subnet_suffix {
  byte_length = 4
}

resource google_compute_subnetwork vpc_subnetwork {
  count         = length(var.vpc_subnet_cidr_block)
  name          = "${google_compute_network.vpc_network.name}-${count.index}-${random_id.subnet_suffix.hex}"
  ip_cidr_range = var.vpc_subnet_cidr_block[count.index]
  region        = var.region
  network       = google_compute_network.vpc_network.self_link
  #secondary_ip_range {
  #  range_name = "${google_compute_network.vpc_network.name}-${count.index}-${random_id.subnet_suffix.hex}-subrn"
  #  ip_cidr_range = "10.100.0.0/20"
  #}
  private_ip_google_access = true
}

