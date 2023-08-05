data google_container_engine_versions gce_versions {
  provider       = google-beta
  location       = var.region
  version_prefix = var.k8s_version
}

locals {
  use_latest_ver          = var.k8s_version == "latest"
  ver_prefix              = data.google_container_engine_versions.gce_versions.version_prefix
  static_latest_ver       = data.google_container_engine_versions.gce_versions.latest_master_version
  channel_versions        = data.google_container_engine_versions.gce_versions.release_channel_default_version
  stable_channel_version  = substr(local.channel_versions["STABLE"], 0, length(local.ver_prefix))
  regular_channel_version = substr(local.channel_versions["REGULAR"], 0, length(local.ver_prefix))
  rapid_channel_version   = substr(local.channel_versions["RAPID"], 0, length(local.ver_prefix))
  channel_default         = "UNSPECIFIED"
  channel_value_rapid     = local.rapid_channel_version == local.ver_prefix ? "RAPID" : null
  channel_value_regular   = local.regular_channel_version == local.ver_prefix ? "REGULAR" : null
  channel_value_stable    = local.stable_channel_version == local.ver_prefix ? "STABLE" : null
  release_channel         = local.use_latest_ver ? "RAPID" : (local.static_latest_ver == null ? (local.channel_value_stable == null ? (local.channel_value_regular == null ? (local.channel_value_rapid == null ? local.channel_default : local.channel_value_rapid) : local.channel_value_regular) : local.channel_value_stable) : local.channel_default)
}

resource google_container_cluster k8s_cluster {
  provider                  = google-beta
  name                      = "${var.resource_prefix}-cluster"
  location                  = var.region
  remove_default_node_pool  = true
  initial_node_count        = 1
  network                   = var.vnet_link
  subnetwork                = var.subnet_link
  default_max_pods_per_node = 60
  min_master_version        = local.ver_prefix == null ? null : data.google_container_engine_versions.gce_versions.latest_master_version
  node_version              = local.ver_prefix == null ? null : data.google_container_engine_versions.gce_versions.latest_master_version
  logging_service           = "none"
  monitoring_service        = "none"
  release_channel {
    channel = local.release_channel
  }

  ip_allocation_policy {
    cluster_ipv4_cidr_block  = ""
    services_ipv4_cidr_block = ""
  }
  networking_mode = "VPC_NATIVE"

  private_cluster_config {
    enable_private_endpoint = true
    enable_private_nodes    = true
    master_ipv4_cidr_block  = var.master_ipv4_cidr_block
  }

  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = var.vpc_cidr_block
      display_name = "world"
    }
  }

  master_auth {
    username = ""
    password = ""
    client_certificate_config {
      issue_client_certificate = false
    }
  }
}

