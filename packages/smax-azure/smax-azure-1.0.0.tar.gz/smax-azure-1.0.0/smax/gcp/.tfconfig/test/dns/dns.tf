locals {
  tmp_arrs    = split(".", var.fqdn)
  tmp_length  = length(local.tmp_arrs)
  fqdn_prefix = local.tmp_arrs[0]
  fqdn_domain = join(".", slice(local.tmp_arrs, 1, local.tmp_length))
}

resource google_dns_record_set fqdn {
  project      = var.project
  name         = "${local.fqdn_prefix}.${local.fqdn_domain}."
  managed_zone = google_dns_managed_zone.fqdn.name
  type         = "A"
  ttl          = 300
  rrdatas = [
  google_compute_address.fqdn.address]
}

resource google_dns_managed_zone fqdn {
  project    = var.project
  name       = "${var.resource_prefix}-zone"
  dns_name   = "${local.fqdn_domain}."
  visibility = "public"
}

resource google_compute_address fqdn {
  project      = var.project
  region       = var.region
  name         = "${var.resource_prefix}-fqdn"
  address_type = "EXTERNAL"
}