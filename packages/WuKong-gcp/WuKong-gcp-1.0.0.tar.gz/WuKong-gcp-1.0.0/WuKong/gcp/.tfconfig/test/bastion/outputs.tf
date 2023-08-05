output ip_addr {
  value = google_compute_instance.bastion_instance.network_interface[0].access_config[0].nat_ip
}

output vm_user {
  value = var.vm_user
}

output instance_id {
  value = google_compute_instance.bastion_instance.instance_id
}