resource google_filestore_instance fsi {
  name = "${var.resource_prefix}-fs"
  zone = data.google_compute_zones.available.names[1]
  tier = var.gcp_filestore_tier

  file_shares {
    capacity_gb = var.filestore_gb
    name        = var.filestore_share_name
  }

  networks {
    network           = var.vnet_name
    reserved_ip_range = "10.190.3.0/29"
    modes = [
    "MODE_IPV4"]
  }

  timeouts {
    create = "60m"
  }
}

data google_compute_zones available {
  project = var.project
  region  = var.region
}
