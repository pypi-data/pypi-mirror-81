output name {
  value = google_compute_network.vpc_network.name
}

output link {
  value = google_compute_network.vpc_network.self_link
}

output subnet_link_0 {
  value = length(google_compute_subnetwork.vpc_subnetwork) > 0 ? google_compute_subnetwork.vpc_subnetwork[0].self_link : null
}
