resource google_container_node_pool worker_nodes_pool {
  name       = "${google_container_cluster.k8s_cluster.name}-node-pool"
  location   = var.region
  cluster    = google_container_cluster.k8s_cluster.name
  node_count = var.k8s_node_pool_size
  version    = data.google_container_engine_versions.gce_versions.latest_node_version

  node_config {
    preemptible  = false
    machine_type = var.k8s_node_machine_type
    disk_size_gb = var.k8s_node_disk_size
    disk_type    = "pd-ssd"

    metadata = {
      disable-legacy-endpoints = "true"
    }

    labels = {
      "cdfapiserver" = "true"
      "worker"       = "label"
      "node.type"    = "worker"
      "role"         = "loadbalancer"
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }
}
