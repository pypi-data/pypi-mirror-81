resource google_compute_firewall gcp_firewall_externalssh {
  name    = "${var.resource_prefix}-bastion-ssh-firewall"
  network = var.vnet_link
  allow {
    protocol = "tcp"
    ports = [
      "22",
      "443",
      "3000",
    "5443"]
  }
  source_ranges = [
  "0.0.0.0/0"]
}

resource google_compute_firewall gcp_firewall_internal {
  name    = "${google_compute_instance.bastion_instance.name}-internal-firewall"
  network = var.vnet_link

  allow {
    protocol = "tcp"
  }
  source_ranges = [
  "10.0.0.0/8"]
}
