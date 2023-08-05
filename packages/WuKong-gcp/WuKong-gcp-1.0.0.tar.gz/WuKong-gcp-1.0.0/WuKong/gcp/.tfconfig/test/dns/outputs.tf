output fqdn_ip {
  value = google_compute_address.fqdn.address
}

output fqdn_name {
  value = var.fqdn
}


