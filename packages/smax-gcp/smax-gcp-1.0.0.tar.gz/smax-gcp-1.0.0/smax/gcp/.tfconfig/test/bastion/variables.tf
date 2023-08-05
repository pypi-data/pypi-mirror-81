variable resource_prefix {}
variable project {}
variable region {}

variable bastion_machine_type {
  description = "GCP bastion machine type"
  default     = "n1-standard-2"
}
variable ssh_public_key_file {}
variable ssh_private_key_file {}
variable vnet_link {}
variable subnet_link {}
variable vm_user {}
variable k8s_cluster_name {}
