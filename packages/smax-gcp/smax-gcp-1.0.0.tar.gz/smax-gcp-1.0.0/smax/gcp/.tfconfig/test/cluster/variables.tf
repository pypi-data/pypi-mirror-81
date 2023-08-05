variable resource_prefix {}

variable region {}

variable vpc_cidr_block {
  description = "The IP address range of the VPC in CIDR notation."
  default     = "10.0.0.0/8"
}

variable k8s_node_pool_size {
  description = "per zone node size for kubernete cluster."
  default     = 1
}

variable k8s_node_machine_type {
  description = "kubernete cluster worker node machine type."
  default     = "n1-standard-8"
}

variable k8s_node_disk_size {
  description = "kubernete cluster worker node disk size"
  default     = 100
}

variable master_ipv4_cidr_block {
  description = "The IP range in CIDR notation (size must be /28) to use for the hosted master network. This range will be used for assigning internal IP addresses to the master or set of masters, as well as the ILB VIP. This range must not overlap with any other ranges in use within the cluster's network."
  default     = "172.16.0.0/28"
}

variable k8s_version {
  default = "latest"
}

variable vnet_link {}
variable subnet_link {}
