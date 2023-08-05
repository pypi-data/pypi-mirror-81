resource google_compute_instance bastion_instance {
  depends_on = [
    google_compute_firewall.gcp_firewall_externalssh
  ]
  name         = "${var.resource_prefix}-bastion"
  machine_type = var.bastion_machine_type
  zone         = data.google_compute_zones.available.names[0]

  boot_disk {
    initialize_params {
      size  = 100
      type  = "pd-ssd"
      image = "centos-cloud/centos-7"
    }
  }

  network_interface {
    network    = var.vnet_link
    subnetwork = var.subnet_link
    access_config {
      // Ephemeral IP
    }
  }

  service_account {
    scopes = [
    "https://www.googleapis.com/auth/cloud-platform"]
  }
  tags = [
  "gks-bastion"]

  metadata = {
    ssh-keys = "${var.vm_user}:${var.ssh_public_key_file}"
  }
}

resource null_resource init_bastion {
  depends_on = [
    google_compute_instance.bastion_instance
  ]

  provisioner remote-exec {
    connection {
      host        = google_compute_instance.bastion_instance.network_interface[0].access_config[0].nat_ip
      user        = var.vm_user
      type        = "ssh"
      timeout     = "50s"
      private_key = var.ssh_private_key_file
      agent       = false
    }
    inline = [
      "sudo yum install -y kubectl",
      "sudo yum install -y google-cloud-sdk",
      "echo -e \"1\\n1\\nn\" | gcloud init",
      "sudo yum install -y docker",
      "sudo groupadd docker",
      "sudo usermod -a -G docker $USER",
      "sudo systemctl start docker",
      "sudo systemctl enable docker",
      "sudo yum install -y nfs-utils",
      "sudo yum install -y unzip",
      "sudo yum install -y postgresql",
      "gcloud container clusters get-credentials --region ${var.region} ${var.k8s_cluster_name}",
      "sudo gcloud container clusters get-credentials --region ${var.region} ${var.k8s_cluster_name}",
    ]
  }
}

data google_compute_zones available {
  project = var.project
  region  = var.region
}
