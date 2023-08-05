resource random_id db_name_suffix {
  byte_length = 4
}

resource google_sql_database_instance smax_postgres {
  name             = "${var.resource_prefix}-pg-${random_id.db_name_suffix.hex}"
  database_version = var.db_version

  depends_on = [
    google_service_networking_connection.pg_vpc_peering_connection
  ]
  settings {
    tier      = var.database_machine_type
    disk_size = var.database_disk_size
    disk_type = "PD_SSD"
    ip_configuration {
      ipv4_enabled    = "false"
      private_network = var.vnet_link
    }
    database_flags {
      name  = "max_connections"
      value = 3000
    }
  }
}

resource google_sql_user postgres_user {
  name     = var.database_user_name
  instance = google_sql_database_instance.smax_postgres.name
  password = var.database_user_password
}
