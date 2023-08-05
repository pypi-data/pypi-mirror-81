resource "google_compute_router" "router" {
  name    = "${var.resource_prefix}-router-${random_id.subnet_suffix.hex}"
  region  = var.region
  network = google_compute_network.vpc_network.self_link
  bgp {
    asn = 64514
  }
}

resource "google_compute_router_nat" "nat" {
  name                               = "${var.resource_prefix}-router-nat-${random_id.subnet_suffix.hex}"
  router                             = google_compute_router.router.name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}