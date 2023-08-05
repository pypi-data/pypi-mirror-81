output private_ip {
  value = google_sql_database_instance.smax_postgres.first_ip_address
}

output ins_name {
  value = google_sql_database_instance.smax_postgres.name
}

output default_db_user {
  value = var.database_user_name
}

output db_password {
  value = var.database_user_password
}