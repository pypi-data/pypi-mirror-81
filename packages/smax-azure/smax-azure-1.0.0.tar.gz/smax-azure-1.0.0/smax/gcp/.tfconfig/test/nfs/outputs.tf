output "ip_addr" {
  value = google_filestore_instance.fsi.networks[0].ip_addresses[0]
}

output "share_name" {
  value = google_filestore_instance.fsi.file_shares[0].name
}
